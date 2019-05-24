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
db = client.vote_app_database_test

def lambda_handler(event, context):
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

    return {
        'statusCode': 200,
        'body': json.dumps('DB Cleaned!')
    }
   
