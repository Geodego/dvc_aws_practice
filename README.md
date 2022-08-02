# DVC with Amazon S3 remote for Heroku


## Project description
Basic usage of DVC with Amazon S3 storage used for deploying an app on Heroku for training purpose.

## AWS set-up
- create a bucket on S3 named censussimul
- create an IAM user with access to the bucket
- configure your AWS CLI to use the Access key ID and Secret Access key (linked to IAM user) 

```bash
$ aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: 
Default output format [None]: 

```