import logging
import json
import bson
import os
import time
import datetime
from datetime import date
from pymongo import MongoClient

# Logger settings - CloudWatch
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Set client
client = MongoClient('mongodb://{}:27017/'.format(os.environ['DB_HOST'] ))

# Set database
db = client.vote_app_database
##### For testing
# event={"VotedFor":"Jeff Bezos"}

def lambda_handler(event, context):
    start_time = int(round(time.time() * 1000))
    logger.info("Received event: " + json.dumps(event, indent=2))
    
    logger.info("initializing the votes collection")
    votes = db.votes
    
    created_vote_id = cast_vote(event, start_time, votes)
    
    # Current time in date time format
    first_call_time = datetime.datetime.now()
    current_hour = first_call_time.strftime("%H:%M:%S")
    print(current_hour)
    first_call_time_seconds = int(start_time)
    #int(first_call_time.hour*60) + int(first_call_time.minute*60) + int(first_call_time.second)

    pipeline = [
            { "$match": { "initial_time": first_call_time_seconds }},
            ]
    
    logger.info("Check if collection for initial time exists or not")
    if event['agg_db_collection'] not in db.list_collection_names():
        print('Creating aggregator collection')
        agg_db_collection = db.agg_db_collection
        init_time = {"initial_time": first_call_time_seconds,}
        initial_time_id = agg_db_collection.insert_one(init_time).inserted_id
        saved_initial_time = list(agg_db_collection.aggregate(pipeline))[0]
    else:
        agg_db_collection = db.agg_db_collection
        #saved_initial_time = list(agg_db_collection.aggregate(pipeline))[0]
        saved_initial_time = list(agg_db_collection.find())[0]

    logger.info("Get the base initial time stored in db")
    for k,v in saved_initial_time.items():
        if k=='initial_time':
            initial_time = v


    print('Initial Time is : - ' + str(initial_time))

    if (first_call_time_seconds >= (initial_time + 9666)):
        
        logger.info("Reset the base initial time after 10 seconds")
        agg_db_collection.update_one( {"initial_time" : initial_time}, {"$set": { "initial_time" : first_call_time_seconds}});
        logger.info("Updated base execution time ...")
        votes_aggregated = get_votes()
        
        # Separate Collection  to store the results after every 10 seconds
        agg_db_collection_counter = db.agg_db_collection_counter
        

        print('votes_aggregated ==>' + str(votes_aggregated))
        total_exec_time_10sec_counter = votes_aggregated["total_time"]
        total_votes_10sec_counter = votes_aggregated["total_votes"]
        vote_counter = {
            "_id": str(first_call_time_seconds),
            "total_exec_time_10sec_counter": int(total_exec_time_10sec_counter),
            "total_votes_10sec_counter": total_votes_10sec_counter,
         }
        #print('total time taken ==>' + str(total_time_consumed))
        vote_id = agg_db_collection_counter.insert_one(vote_counter).inserted_id

    # Get created document from the database using ID.
        vote = votes.find_one({ "_id": vote_id })
    votes_aggregated = get_votes()
    return votes_aggregated
    
def cast_vote(event, start_time, votes):

    logger.info("creating the vote...")

    end_time = int(round(time.time() * 1000))
    time_taken = end_time - start_time
    vote = {
        "VotedFor": event["VotedFor"],
	    "executionTime": time_taken,
    }
    vote_id = votes.insert_one(vote).inserted_id

    # Get created document from the database using ID.
    vote = votes.find_one({ "_id": vote_id })
    print('\n-------------')
    print(vote)
    print('\n-------------')
    return json.loads(json.dumps(vote, default=json_unknown_type_handler))

def json_unknown_type_handler(x):
    """
    JSON cannot serialize decimal, datetime and ObjectId. So we provide this handler.
    """
    if isinstance(x, bson.ObjectId):
        return str(x)
    raise TypeError("Unknown datetime type")
    
def get_votes():

    logger.info("initializing the votes collection")
    votes = db.votes
    data_votes = {}
    data_total_time = {}

    for participant in ['Jeff Bezos', 'Sundar Pichai', 'Satya Nadella']:
        pipeline = [
            { "$match": { "VotedFor": participant }},
            { "$group": { "_id": participant,
                    "total_time": {
                    "$sum": "$executionTime"
                            }
                    }
            }
        ]

        if (votes.find( { "VotedFor": { "$eq": participant } } ).count() > 0):
            vote = list(votes.aggregate(pipeline))[0]
            print('\n-------------')
            print(vote)
            print('\n-------------')
            for k,v in vote.items():
              if k=='total_time':
                  total_time=v
    
            total_votes=votes.find( { "VotedFor": { "$eq": participant } } ).count()
            print('Total votes :' + str(total_votes))
            average_time=total_time/total_votes
            print('Average Time is :' + str(average_time))
    
            data_votes['votes_' + participant]=total_votes
            data_total_time['total_time_' + participant]=total_time
        else:
            print('No votes for this participant' + participant)
    print(data_votes)
    total_votes_all = sum(data_votes.values())
    print('Total votes to all the participants - ' + str(total_votes_all))
    print(data_total_time)
    total_time_all = sum(data_total_time.values())
    print('Total time for all the participants - ' + str(total_time_all))
    average_time_all = total_time_all/total_votes_all
    print('Average time for all the participants' + str(average_time_all))

    return_data = {}
    return_data['total_time']=total_time_all
    return_data['total_votes']=total_votes_all

    return return_data

