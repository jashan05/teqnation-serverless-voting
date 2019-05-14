import logging
import json
import bson
import os
import time
from pymongo import MongoClient

# Logger settings - CloudWatch
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Set client
client = MongoClient('mongodb://{}:27017/'.format(os.environ['DB_HOST'] ))

# Set database
db = client.vote_app_database

##### For testing
#event={"participant":"Jeff Bezos"}

def lambda_handler(event, context):
    start_time = int(round(time.time() * 1000))
    #logger.info("Received event: " + json.dumps(event, indent=2))

    #participant = event["participant"]
    print('\n----------------')
    #print(participant)

    logger.info("initializing the collection")
    votes = db.votes


    # Get created document from the database using ID.
    data_votes = {}
    data_total_time = {}
    for participant in ['Jeff Bezos', 'Satya Nadella', 'Sundar Pichai']:
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
            print('No votes for this participant ==> ' + participant)
            
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
    return_data['total_votes']=total_votes_all

    ## Calculate lambda charges
    logger.info("Calculate lambda charges")
    return_data['total_cost'] = total_votes_all * (total_time_all/1000) * (128/1024) * 0.00001667
    
    # Intitialize the collection to get the counter data for chart
    agg_db_collection_counter = db.agg_db_collection_counter
    
    return_data['chart'] =  list(agg_db_collection_counter.find({}))
    
    for k,v in return_data.items():
        print(str(k) + ':' + str(v))

    return json.loads(json.dumps(return_data, default=json_unknown_type_handler))

def json_unknown_type_handler(x):
    """
    JSON cannot serialize decimal, datetime and ObjectId. So we provide this handler.
    """
    if isinstance(x, bson.ObjectId):
        return str(x)
    raise TypeError("Unknown datetime type")

