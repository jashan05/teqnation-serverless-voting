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

# Setting the DB connection outside lambda_handler helps to keep state in case of
# `warm ` containers

# Set client
client = MongoClient('mongodb://{}:27017/'.format(os.environ['DB_HOST'] ))

# Set database
db = client.vote_app_database_test

# initializing the votes collection
votes = db.votes

##### For testing
# event={"VotedFor":"Jeff Bezos"}

def lambda_handler(event, context):
    start_time = int(round(time.time() * 1000))
    logger.info("Received event: " + json.dumps(event, indent=2))
    
    created_vote_id = cast_vote(event, start_time, votes)
    
def cast_vote(event, start_time, votes):
    """
    cast_vote function is for casting the votes at evry 10 second intervals
    which is required to show on the graph
    """

    logger.info("creating the vote...")

    ## We need to check the execution time of lambda for each vote casted
    ## so we have to calculate the time and store in db for further processing
    end_time = int(round(time.time() * 1000))
    time_taken = end_time - start_time
    vote = {
        "VotedFor": event["VotedFor"],
	    "executionTime": time_taken,
	    "start_time": start_time,
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
