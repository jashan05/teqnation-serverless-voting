import json
import bson
import os
import time
import datetime
from datetime import date
from pymongo import MongoClient

client = MongoClient('mongodb://{}:27017/'.format(os.environ['DB_HOST'] ))
# Set database
db = client.vote_app_database_GoogleCloud

# initializing the votes collection
votes = db.votes

def delete_votes(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    print('Collections in the current db - {}'.format(db.list_collection_names()))

    ## votes
    print('\nCleaning Collection - {} from table'.format('votes'))
    print('Collection - {} has {} documents before cleaning'.format('votes', db.votes.count_documents({})))
    
    db.votes.delete_many({})
    if (db.votes.count_documents({})==0):
       print('All the Votes deleted\n')
    
    ## agg_db_collection
    print('\nCleaning Collection - {} from table'.format('agg_db_collection'))
    print('Collection - {} has {} documents before cleaning'.format('agg_db_collection', db.agg_db_collection.count_documents({})))
    
    db.agg_db_collection.delete_many({})
    if (db.agg_db_collection.count_documents({})==0):
       print('Documents in agg_db_collection deleted\n')
    return 'All the documents cleaned in DB'
