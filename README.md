# teqnation-serverless-voting
Lambda functions in python for voting app


## Download the dependencies for these lambda functions while using them.


### Commands for MongoDB
---
#### To login to MongoDB
- mongo 

#### list all the dbs in MongoDB
- show dbs

#### Select the db which we are using
- use vote_app_database

#### show all the collections(tables)
- show collections
#### to get all the data in each collection
- db.COLLECTION_NAME.find()
##### e.g
- db.agg_db_collection.find()

#### to drop the collection(table), to clean up before testing
- db.COLLECTION_NAME.drop()
##### e.g
- db.agg_db_collection.drop()
