import json
import bson
import os
import time
import datetime
from flask import jsonify
from bson import json_util
from bson import BSON
from datetime import date
from pymongo import MongoClient

client = MongoClient('mongodb://{}:27017/'.format(os.environ['DB_HOST'] ))
# Set database
db = client.vote_app_database_GoogleCloud

# initializing the votes collection
votes = db.votes

def cast_votes(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    
    """
    Following is required for enabling CORS configuration
    """
    # Set CORS headers for preflight requests
    if request.method == 'OPTIONS':
        headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Headers': 'Content-Type'
        }
        return ('', 204, headers)
    # Set CORS headers for main requests
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    milli_secs = 1000
    micro_secs = milli_secs * milli_secs
    start_time = int(round(time.time() * micro_secs))
    request_json = request.get_json(silent=True)
    request_args = request.args
    if request_json and 'VotedFor' in request_json:
        VotedFor = request_json['VotedFor']
    elif request_args and 'VotedFor' in request_args:
        VotedFor = request_args['VotedFor']
    print("creating the vote...")

    ## We need to check the execution time of lambda for each vote casted
    ## so we have to calculate the time and store in db for further processing
    end_time = int(round(time.time() * micro_secs))
    time_taken = end_time - start_time
    vote = {
        "VotedFor": VotedFor,
	    "executionTime": time_taken,
	    "start_time": start_time,
    }
    vote_id = votes.insert_one(vote).inserted_id

    # Get created document from the database using ID.
    vote = votes.find_one({ "_id": vote_id })
    print('\n-------------')
    print(vote)
    print('\n-------------')

    return jsonify(str(vote))
