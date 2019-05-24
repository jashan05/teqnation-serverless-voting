# teqnation-serverless-voting
Lambda functions in python for voting app

## Architectural diagram of the application
![Alt text](images/Capture.PNG?raw=true "Title")

## Lambda Functions
- **lambda_function_clean_db** - This is a function which cleans are the documents in a MongoDB collection
- **lambda_function_get** - This is the lambda function which is used for Getting results after votes are casted.
- **lambda_function** - This is the function which is used to cast votes. 

## Download the dependencies for these lambda functions while using them.
- Refer the **requiremnts.txt** file for all the dependencies which you need to download to run these functions.
- use `pip install -r requirements.txt`


## MongoDB

Here we are using MongoDB for storing an retrieving the *votes*.

### 1. Installation of MongDB
- For MongoDB 3.0, create the below file using VI or any other editor:
```
vi /etc/yum.repos.d/mongodb-org-3.0.repo
```
- Add the following in the file
 ```
  [mongodb-org-3.0]
  name=MongoDB Repository
  baseurl=https://repo.mongodb.org/yum/amazon/2013.03/mongodb-org/3.0/x86_64/
  gpgcheck=0
  enabled=1
```
- Install MongoDB
```
sudo yum install -y mongodb-org
```
- Start MongoDB
```
sudo service mongod start
```
- Optionally - To ensure mongoDB starts automatically in case of reboot
```
sudo chkconfig mongod on
```

### 2. Some useful Commands for MongoDB
- To login to MongoDB
```
 mongo 
```
- list all the dbs in MongoDB
``` 
show dbs 
```
- Select the db which we are using
``` 
use vote_app_database
 ```

- show all the collections(tables)
```
 show collections
 ```
- to get all the data in each collection
```
 db.<COLLECTION_NAME>.find()
 e.g
 db.votes.find()
 ```

- to drop the collection(table), to clean up before testing
```
 db.<COLLECTION_NAME>.drop()
 e.g
 db.votes.drop()
 ```

 - to clean the documents *(items)* in a collection in MongoDB
 ```
db.<COLLECTION_NAME>.delete_many({})
e.g
db.votes.delete_many({})
 ```
