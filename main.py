import pandas as pd
import os
import logging
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

pull_err = None

if "DYNO" in os.environ and os.path.isdir(".dvc"):
    # This code is necessary for Heroku to use dvc
    os.system("dvc config core.no_scm true")
    # os.system("dvc remote add -d s3remote s3://censusbucketgg")

    pull_err = os.system("dvc pull")
    if pull_err != 0:
        logger.warning(f" New dvc pull failed, error: {pull_err}")
        exit(f"dvc pull failed, error {pull_err}")
    else:
        logger.warning("DVC Pull worked.")
    logger.warning('removing dvc files')
    os.system("rm -r .dvc .apt/usr/lib/dvc")


def create_data():
    df = pd.DataFrame([[1, 2], [3, 4]], columns=['a', 'b'])
    df.to_csv('data.csv', index=False)


# Instantiate the app.
app = FastAPI()


# Define a GET on the root.
@app.get("/")
async def api_columns():
    """
    In this basic example we read data.csv and return the columns of the data frame. This requires dvc pull to be
    executed on the Heroku VM.
    """
    logger.warning(f'error status of dvc pull: {pull_err}')
    df = pd.read_csv('data.csv')
    return {"columns of data.csv": str(list(df.columns))}


if __name__ == '__main__':
    create_data()
