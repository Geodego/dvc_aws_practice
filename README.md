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

### CD with Heroku
 We use Heroku to run our python application that consists in a basic API.
- Procfile:
  - The ```Procfile``` specifies that we use a web dyno which runs the command ```uvicorn```. This instruction allows 
  our API to be launched using ```uvicorn```.
  - We use the IP ```0.0.0.0``` to tell the server to listen on every open network interface. 
  - Heroku dynamically assigns the port to the ```PORT``` variable: we set the port CLI option to PORT with default 
  value 5000. Doing so we tell uvicorn which port to use.
- Pulling files from DVC with Heroku: 
  - We need to give Heroku the ability to pull in data from DVC upon app start up. We will install 
    a [buildpack](https://elements.heroku.com/buildpacks/heroku/heroku-buildpack-apt) that allows the installation of 
    apt-files and then define the Aptfile that contains a path to DVC:
  - in the CLI we run:
    ```bash
    > heroku buildpacks:add --index 1 heroku-community/apt
    ```
  - Then in the root project folder we create a file called `Aptfile` that specifies the release of DVC we want 
  installed, e.g. https://github.com/iterative/dvc/releases/download/1.10.1/dvc_1.10.1_amd64.deb
  - Finally, we need to add the following code block to main.py:
  ```
  import os
  
  if "DYNO" in os.environ and os.path.isdir(".dvc"):
      os.system("dvc config core.no_scm true")
      if os.system("dvc pull") != 0:
          exit("dvc pull failed")
      os.system("rm -r .dvc .apt/usr/lib/dvc")
  ```
- Set up access to AWS on Heroku:
  ```bash
  > heroku config:set AWS_ACCESS_KEY_ID=xxx AWS_SECRET_ACCESS_KEY=yyy
  ```
- Heroku app creation:
  - We create a new app:
  ```bash
  > heroku create dvc-aws-app --buildpack heroku/python
  ```
  - add a remote to our local repository:
  ```bash
  > heroku git:remote -a dvc-aws-app
  ```
  - To be sure Heroku deploys with the proper python version we need to add a `runtime.txt` file at the root 
  of the directory
  - then we can deploy from our GitHub repository:
  ```bash
  > git push heroku main
  ```
