# DVC with Amazon S3 remote for Heroku


## Project description
Basic usage of DVC with Amazon S3 storage used for deploying an app on Heroku for training purpose.

## AWS set-up
- create a bucket on S3 named censussimul
- create an IAM user with access to the bucket
- create Access key ID and Secret Access key for IAM user
- configure your AWS CLI to use the Access key ID and Secret Access key (linked to IAM user) 

```bash
$ aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: 
Default output format [None]: 

```

## Data tracked with DVC
- use create_data() in main.py to create file data.csv
- in command line:
```bash
$ git init
$ dvc init
$ dvc remote add s3remote s3://censussimul
$ dvc remote default s3remote   
$ dvc add data.csv
$ git add data.csv.dvc .gitignore
$ git commit -m "initial commit of tracked data.csv"
# make sure AWS CLI is configured with Access key ID and Secret Access key
# before pushing to dvc
$ dvc push 
```

## API Creation

- We create a RESTful API using FastAPI, using type hinting and a Pydantic model to ingest the body from POST. 
This implement:
  - GET on the root returning the columns of data.csv.

