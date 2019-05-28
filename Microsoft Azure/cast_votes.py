import logging
import json
import bson
import os
import time
import datetime
from bson import json_util
from bson import BSON
from datetime import date
from pymongo import MongoClient
import azure.functions as func

client = MongoClient('mongodb://{}:27017/'.format(os.environ['DB_HOST'] ))
# Set database
db = client.vote_app_database_test_Azure

# initializing the votes collection
votes = db.votes

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    start_time = int(round(time.time() * 1000))
    #logging.info("Received req: " + json.dumps(req, indent=2))

    voted_for_name = req.params.get('VotedFor')
    if not voted_for_name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            voted_for_name = req_body.get('VotedFor')


    logging.info("creating the vote...")

    ## We need to check the execution time of lambda for each vote casted
    ## so we have to calculate the time and store in db for further processing
    end_time = int(round(time.time() * 1000))
    time_taken = end_time - start_time
    vote = {
        "VotedFor": voted_for_name,
	    "executionTime": time_taken,
	    "start_time": start_time,
    }
    vote_id = votes.insert_one(vote).inserted_id

    # Get created document from the database using ID.
    vote = votes.find_one({ "_id": vote_id })
    print('\n-------------')
    print(vote)
    print('\n-------------')
    vote = json.dumps(vote,  default=json_util.default)
    return func.HttpResponse(body=vote ,status_code=200)
