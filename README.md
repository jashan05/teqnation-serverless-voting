# teqnation-serverless-voting
Voting Application in following 3 platforms:

- AWS
- AZURE
- GOOGLE

Overall Architecture for all the platforms is as per below:

![Alt text](images/All_Platforms.jpeg?raw=true "Title")


## 1. AWS 
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

## API Gateway 
- Create API gateway to handle all 3 lambda functions mentioned above.

## 2. Microsoft Azure

## Azure Functions

- **delete_votes.py** - This is a function which cleans are the documents in a MongoDB collection
- **get_votes.py** - This is the lambda function which is used for Getting results after votes are casted.
- **cast_votes.py** - This is the function which is used to cast votes. 

## API Management 
- Create API Management gateway to handle all 3 Azure functions mentioned above.

## 3. Google Cloud

TBD

## 4. MongoDB

Here we are using MongoDB for storing an retrieving the *votes*. We have created MongoDB VM in each platform.

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

- Change the configuration file for MongoDB so as to accept traffic from anywhere over the Internet
```
vi /etc/mongod.conf
```
and change the IP from **127.0.0.1** to **0.0.0.0** as shown below:
```
# network interfaces
net:
  port: 27017
  bindIp: 0.0.0.0  # Listen to local interface only, comment to listen on all interfaces.

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
