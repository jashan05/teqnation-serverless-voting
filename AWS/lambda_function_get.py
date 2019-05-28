import logging
import json
import bson
import os
import time
import sys
from pymongo import MongoClient

# Logger settings - CloudWatch
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Set client
client = MongoClient('mongodb://{}:27017/'.format(os.environ['DB_HOST'] ))

# Set database
db = client.vote_app_database_test

##### For testing
#event={"participant":"Jeff Bezos"}

def lambda_handler(event, context):
    
    start_time = int(round(time.time() * 1000))
    logger.info("initializing the collection")
    votes = db.votes

    pipeline_time = [ { "$group": { "_id": "null", "last_vote_time": { "$max": "$start_time" }, "first_vote_time": { "$min": "$start_time" } }}]

    logger.info("Getting the time for first and last vote")
    if list(votes.aggregate(pipeline_time)):
        list_vote_time = list(votes.aggregate(pipeline_time))[0]
        
        first_vote_time = int(list_vote_time['first_vote_time'])
        last_vote_time = int(list_vote_time['last_vote_time'])
        
        logger.info(str(first_vote_time) + '-=-=--=-=---=----' + str(last_vote_time)) 
    
    else:
        print('No votes in DB , exiting ...')
        return None
    
    data_votes = {}
    data_total_time = {}
    chart = {}
    return_data = {}
    ten_sec_timer = first_vote_time + 10000

    for timer in range(6):
        string_timer = str(timer)
        for participant in ['Sundar Pichai', 'Jeff Bezos', 'Satya Nadella']:
            pipeline = [
                    { "$match": { "$and": [ { "start_time": { "$gte": first_vote_time, "$lte": ten_sec_timer } }, { "VotedFor": participant } ] } },
                    { "$group":  { "_id": participant, "total_time": { "$sum": "$executionTime" }, "votes_casted": { "$sum": 1 } } }
                    ]
            
            # Check if the participant has any votes casted in the 10 second timer
            
            if list(votes.aggregate(pipeline)):
                vote = list(votes.aggregate(pipeline))[0]
                print('\n-------------')
                print(vote)
                print('\n-------------')
                for k,v in vote.items():
                  if k=='total_time':
                      total_time=v
                      
                  if k=='votes_casted':
                      total_votes=v
        
                data_votes['votes_' + participant + '_' + string_timer]=total_votes
                data_total_time['time_' + participant + '_' + string_timer]=total_time

            else:
                print('No votes for this participant ==> ' + participant)
    
            
        first_vote_time = ten_sec_timer
        ten_sec_timer = ten_sec_timer + 10000

   
        print(data_votes)
        total_votes_string_timer = sum(data_votes.values())
        print('Total votes to all the participants for timer -' + string_timer + ' is ' + str(total_votes_string_timer))
        print(data_total_time)
        total_time_string_timer = sum(data_total_time.values())
        print('Total time for all the participants for timer -' + string_timer + ' is ' + str(total_time_string_timer))
        chart['votes_' + string_timer] = total_votes_string_timer
        chart['lambda_exec_time_' + string_timer] = total_time_string_timer

    # Calculate the total votes for all the participants and total time taken
    total_time_all = total_time_string_timer
    total_votes_all = total_votes_string_timer

    return_data['total_time']=total_time_all
    return_data['total_votes']=total_votes_all
    
    ## Calculate lambda charges
    logger.info("Calculate lambda charges")
    return_data['total_cost'] = total_votes_all * (total_time_all/1000) * (128/1024) * 0.00001667
    
    return_data['chart'] = chart
    
    return json.loads(json.dumps(return_data, default=json_unknown_type_handler))

def json_unknown_type_handler(x):
    """
    JSON cannot serialize decimal, datetime and ObjectId. So we provide this handler.
    """
    if isinstance(x, bson.ObjectId):
        return str(x)
    raise TypeError("Unknown datetime type")

