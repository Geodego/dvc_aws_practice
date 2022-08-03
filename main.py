import pandas as pd
import os
import logging
from fastapi import FastAPI
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

pull_err = None

if "DYNO" in os.environ and os.path.isdir(".dvc"):
    # This code is necessary for Heroku to use dvc
    os.system("dvc config core.no_scm true")
    # os.system("dvc remote add -d s3remote s3://censusbucketgg")

    pull_err = os.system("dvc pull")
    if pull_err != 0:
        exit(f"dvc pull failed, error {pull_err}")
    else:
        logger.warning("DVC Pull worked.")
    logger.warning('removing dvc files')
    os.system("rm -r .dvc .apt/usr/lib/dvc")


class Item(BaseModel):
    a: int
    b: int

    class Config:
        schema_extra = {
            "example": {
                'a': 2,
                'b': 5
            }
        }


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
    logger.warning("entering GET request")
    logger.warning(f'error status of dvc pull: {pull_err}')
    df = pd.read_csv('data.csv')
    return {"columns of data.csv": str(list(df.columns))}


def post_tool(predict_body: Item) -> Item:
    """
    Basic transformation of the input of the post request.
    """
    df = pd.read_csv('data.csv')[['a', 'b']].iloc[0]
    output = predict_body.copy()
    output.a += df['a']
    output.b += df['b']
    return output


@app.post("/predict")
async def predict(predict_body: Item):
    """
    In this basic example we read data.csv and return a dictionary with the values of its first row added
    to predict_body.
    This requires dvc pull to be executed on the Heroku VM.
    """
    logger.warning("entering POST request")
    logger.warning(f'error status of dvc pull: {pull_err}')
    output = post_tool(predict_body)

    return output


if __name__ == '__main__':
    item = Item(**{'a': 1, 'b': 2})
    item1 = post_tool(item)
    print(item1)
    #create_data()
