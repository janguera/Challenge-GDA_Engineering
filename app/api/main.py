from typing import List, Dict, Literal, Any #, Union
import datetime
import pandas as pd
import requests
from fastapi import FastAPI, APIRouter

from src.utils import api_parameters
from src.api.configuration import ORJSONResponse, Settings


ROOT_PATH=Settings().api_main_path
prefix_router = APIRouter(prefix=ROOT_PATH)
print('API path: ', ROOT_PATH)


host = Settings().middleware_host
host = host if host[-1] != "/" else host[:-1]
host = host + Settings().api_main_path + Settings().api_version


app = FastAPI(
                openapi_url=f'{ROOT_PATH}/openapi.json',
                docs_url = f'{ROOT_PATH}/docs',
                redoc_url = f'{ROOT_PATH}/redoc',
                default_response_class=ORJSONResponse
              ) 
   

@prefix_router.get('/subfeddit_comments')
async def get_subfeddit_comments(
        subfeddit: str,
        start_date: datetime.date = None,
        end_date: datetime.date = None,
        sorted_results: bool = False,
        comments_limit: int = 25) -> List[Dict]:
    """
    Returns a list of comments from the specified subfeddit.
    For each comment, the following data is provided: 
        - Uniquie identifier of the comment
        - The text of the comment
        - The polarity score and the classification of the comment (positive/negative) based on that score
    The following variables are optional based on the request:
        - Date filter if the start and end dates are provided
        - Sorted by polarity if specified
        - Limit number of comments
    """

    subfeddit_obj   = api_parameters.ParamSubfeddit(id=subfeddit)

    assert subfeddit_obj is not None

    dateRange_obj   = api_parameters.DateRange(start_date=start_date, end_date=end_date)

    payload = {'subfeddit_id': subfeddit_obj.id, 
               'skip': 0,
               'limit': comments_limit
               }
    
    res = requests.get(url = host + "/comments", params = payload)

    data = res.json()


app.include_router(prefix_router)
