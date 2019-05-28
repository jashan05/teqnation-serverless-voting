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

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

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
    return_data = {}       
    return_data['message'] = 'All the documents cleaned in DB'
    return_data = json.dumps(return_data, default=json_util.default)
    return func.HttpResponse(
            body=return_data,
            status_code=200
    )
