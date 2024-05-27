from typing import List, Dict
import datetime
import pandas as pd
import requests
from fastapi import FastAPI, APIRouter

from app.api.configuration import ORJSONResponse, Settings
from app.api.sentiment_analysis.polarity_score import get_polarity, classify_polarity

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
   

@prefix_router.get('/subfeddit_comments')
async def get_subfeddit_comments(
        subfeddit: str,
        time_range: int = None,
        sorted_results: bool = False,
        comments_limit: int = 25) -> List[Dict]:
    """
    Returns a list of comments from the specified subfeddit.
    For each comment, the following data is provided: 
        - Uniquie identifier of the comment
        - The text of the comment
        - The polarity score and the classification of the comment (positive/negative) based on that score
    The following variables are optional based on the request:
        - Limit number of comments
        - Time range filter if the time_range is provided (in minutes, will be filtered from the limit number of comments)
        - Sorted by polarity if specified
    """

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
