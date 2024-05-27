from typing import Any
from pydantic import validator, BaseSettings
import orjson
from fastapi.responses import JSONResponse



class Settings(BaseSettings):
    middleware_host: str
    api_main_path: str = '/subfeddit-api'
    api_version: str = '/api/v1'

    @validator('api_main_path')
    def validate_api_main_path(cls, v):
        """
        api_main_path has to begin with / and finish without /
        
        Example:
            /feddit-api-main
        """
        if v[0] != '/':
            v = '/' + v
        if v[-1] == '/':
            v = v[:-1]
        return v
    
    class Config:
        env_prefix = "API_SUBFEDDIT_"
        case_sensitive = False
        env_file = ".env_api"



def _parse_dict_key_to_str(d: dict):
    result = {}
    if isinstance(d, dict):
        for k, v in d.items():
            if isinstance(v, dict):
                result[str(k)] = _parse_dict_key_to_str(v)
            elif isinstance(v, list):
                result[str(k)] = [_parse_dict_key_to_str(e) for e in v]
            else:
                result[str(k)] = v
    else:
        return d
    return result



class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return orjson.dumps(_parse_dict_key_to_str(content))


