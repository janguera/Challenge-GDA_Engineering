from typing import List, Dict
import datetime
import pandas as pd
import requests
from fastapi import FastAPI, APIRouter, HTTPException

from app.configuration import ORJSONResponse, Settings
from app.sentiment_analysis.polarity_score import get_polarity, classify_polarity

ROOT_PATH=Settings().api_main_path
prefix_router = APIRouter(prefix=ROOT_PATH)

host = Settings().middleware_host
host = host if host[-1] != "/" else host[:-1]
host = host + Settings().api_version

print('Initialising comment classification API')

app = FastAPI(
                openapi_url=f'{ROOT_PATH}/openapi.json',
                docs_url = f'{ROOT_PATH}/docs',
                redoc_url = f'{ROOT_PATH}/redoc',
                default_response_class=ORJSONResponse
              ) 
   
@prefix_router.get('/number_of_subfeddits')
async def get_number_of_subfeddits() -> int:
    """
    Returns the number of subfeddits in the system.
    """

    res = requests.get(url = host + "/subfeddits")

    data = res.json()

    return len(data['subfeddits'])

@prefix_router.get('/subfeddit_comments')
async def get_subfeddit_comments(
        subfeddit: int,
        time_range: int = None,
        sorted_results: bool = False,
        comments_limit: int = 25) -> List[Dict]:
    """
    Returns a list of comments from the specified subfeddit.

    Parameters:
    - **subfeddit** (int): The ID of the subfeddit to fetch comments from.
    - **time_range** (int, optional): The time range filter in minutes. If provided, comments will be filtered based on this range before applying the limit.
    - **sorted_results** (bool, optional): If true, comments will be sorted by their polarity score.
    - **comments_limit** (int, optional): The maximum number of comments to return. Default is 25.

    Returns:
    - **List[Dict]**: A list of comments with the following data for each comment:
        - **Unique identifier**: A unique identifier of the comment.
        - **Text**: The text of the comment.
        - **Polarity score and classification**: The polarity score of the comment and its classification (positive/negative) based on that score.
    """

    # If subfeddit > number of subfeddits, raise an error 
    number_of_subfeddits = await get_number_of_subfeddits()
    if subfeddit > number_of_subfeddits or subfeddit < 0:
        raise HTTPException(status_code=400, detail='Subfeddit does not exist')
    
    if time_range is None or time_range < 0:
        raise HTTPException(status_code=400, detail='Time range must be greater than 0')
    
    if comments_limit < 0:
        raise HTTPException(status_code=400, detail='Comments limit must be greater than 0')

    payload = {'subfeddit_id': subfeddit, 
               'skip': 0,
               'limit': comments_limit
               }
    
    res = requests.get(url = host + "/comments", params = payload)

    data = res.json()

    df = pd.DataFrame.from_dict( data['comments'])

    # Filter by time range
    if time_range:
        df['datetime'] = pd.to_datetime(df['created_at'], unit='s')
        df = df[df['datetime'] > datetime.datetime.now() - datetime.timedelta(minutes=time_range)]

    # Get a polarity score for every text in the comments
    df['polarity_score'] = df['text'].apply(get_polarity)
    # Classify the comments based on the polarity score
    df['classification'] = df['polarity_score'].apply(classify_polarity)

    if sorted_results:
        df = df.sort_values(by='polarity_score', ascending=False)

    return df[['id', 'text', 'polarity_score', 'classification']].to_dict(orient='records')

app.include_router(prefix_router)
