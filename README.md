# teqnation-serverless-voting
Lambda functions in python for voting app


## Download the dependencies for these lambda functions while using them.


### Commands for MongoDB

#### Install MongoDB
- vi /etc/yum.repos.d/mongodb-org-3.0.repo
- Add the following in the file
 `
  [mongodb-org-3.0]
  name=MongoDB Repository
  baseurl=https://repo.mongodb.org/yum/amazon/2013.03/mongodb-org/3.0/x86_64/
  gpgcheck=0
  enabled=1
`
- Install MongoDB
`
sudo yum install -y mongodb-org
`
- Start MongoDB
`
sudo service mongod start
`
- Optionally - To ensure mongoDB starts automatically in case of reboot
`
sudo chkconfig mongod on
`

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
