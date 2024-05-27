import calendar
from typing import List, Literal
import datetime

import pandas as pd
from pydantic import BaseModel, BaseSettings, validator, root_validator, Field

class DefaultInitialDate(BaseSettings):
    """ 
        Parameter: default number of days before the current date or the end date provided
    
        env var:
            API_SUBFEDDIT_DEFAULT_START_RANGE

        example:
            API_SUBFEDDIT_DEFAULT_START_RANGE=7 | If the current date or the end_date provided is 2024-05-27, the default initial date would be 2024-05-20
    """
    default_initial_date_range: datetime.date 
    class Config:
        env_prefix = "API_SUBFEDDIT_"
        case_sensitive = False
        env_file = ".env_api"

class ParamSubfeddit(BaseModel):
    """
    Parameters:
       - id: int, subfeddit to get the comments from

    Cases:
        - id is int:
            - id is returned
        - id is Empty or None
            - id is returned None
    """
    id: int

    @root_validator(pre=True)
    def check_all(cls, values):
        if ('id' not in values) or (values['LISTA_SKUS'] is None):
            values['id'] = None
        if not isinstance(values, int):
            values['id'] = None

        return values
    

class DateRange(BaseModel):
    """ 
    Period Parameters (Start Date and End Date) for API Methods

    Parameters:
        start_date: datetime.date | None
        end_date: datetime.date | None

    Class Instantiation Cases:

        DateRange(start_date=None, end_date=None):
            Instantiated values:
                start_date = Value of environment variable API_SUBFEDDIT_DEFAULT_START_RANGE
                end_date = Current date

        DateRange(start_date=None, end_date=date):
            Instantiated values:
                start_date = Value of environment variable API_SUBFEDDIT_DEFAULT_START_RANGE
                end_date = date

        DateRange(start_date=date, end_date=None):
            Instantiated values:
                start_date = date
                end_date = Current date

        DateRange(start_date=date1, end_date=date2):
            Instantiated values:
                start_date = date1
                end_date = date2  
    """
    start_date: datetime.date | None 
    end_date: datetime.date | None 
    format: str | None = '%Y-%m-%d' 
     
    @root_validator(pre=True)
    def check_all(cls, values):
        """
        Update the start_date and end_date values to their default values if they are not present in the values dictionary or if they have None values
        """
        # If the format is not defined, then we set the default format
        if 'format' not in values or values['format'] is None:
            values['format'] = '%Y-%m-%d'


        if ('end_date' not in values) or (values['end_date'] is None):
            values['end_date'] = datetime.datetime.now().date()
        # If the date is a str, check that the date matches the correct date format
        if isinstance(values['end_date'], str):
            try:
                values['end_date'] = datetime.datetime.strptime(values['end_date'], values['format'])
            except ValueError:
                raise ValueError("The format of the end_date is not correct")

        if ('start_date' not in values) or (values['start_date'] is None):
            values['start_date'] = values['end_date'] - DefaultInitialDate().default_initial_date_range
        # If the date is a str, check that the date matches the correct date format
        if isinstance(values['start_date'], str):
            try:
                values['start_date'] = datetime.datetime.strptime(values['start_date'], values['format'])
            except ValueError:
                raise ValueError("The format of the start_date is not correct")
        
        return values

    class Config:
        # extra fields not allowed
        extra = 'forbid'
