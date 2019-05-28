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
    logging.info('Getting the results.')

    return_data = {}

    start_time = int(round(time.time() * 1000))
    logging.info("initializing the collection")
    votes = db.votes

    pipeline_time = [ { "$group": { "_id": "null", "last_vote_time": { "$max": "$start_time" }, "first_vote_time": { "$min": "$start_time" } }}]

    logging.info("Getting the time for first and last vote")
    if list(votes.aggregate(pipeline_time)):
        list_vote_time = list(votes.aggregate(pipeline_time))[0]
        
        first_vote_time = int(list_vote_time['first_vote_time'])
        last_vote_time = int(list_vote_time['last_vote_time'])
        
        logging.info(str(first_vote_time) + '-=-=--=-=---=----' + str(last_vote_time)) 
    
    else:
        logging.info('No votes in DB , exiting ...')
        return_data['message'] = 'No records in DB'
        return_data = json.dumps(return_data, default=json_util.default)
        return func.HttpResponse(body=return_data ,status_code=200)

    data_votes = {}
    data_total_time = {}
    chart = {}    
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
    logging.info("Calculate lambda charges")
    return_data['total_cost'] = total_votes_all * (total_time_all/1000) * (128/1024) * 0.00001667
    
    return_data['chart'] = chart
    
    return_data = json.dumps(return_data, default=json_util.default)
    return func.HttpResponse(body=return_data ,status_code=200)
