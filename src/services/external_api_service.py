import datetime
from typing import Optional, Dict, Any

from dependency_injector.wiring import Provide
from pydantic import BaseModel
from services.core_http_service import BaseHTTPService
from config import PMMAPIConfig, MLAPIConfig

from src.config import TSDBAPIConfig, PMMAPIConfig, MLAPIConfig
from src.containers.config_container import ConfigContainer


class PMMAPIService(BaseHTTPService):
    URLS = {
        'fmm': 'v1/fmm/calc_fmm_task',
        'adapt': 'v1/fmm/calc_adapt_task',
        'validate': 'v1/fmm/calc_validate_task',
    }

    def __init__(self):
        self.url = 'http://172.18.77.141:8888'


    async def execute_validate_task(self, data):
        return await self.execute_request(url=f'{self.url}/{self.URLS["validate"]}', body=data, method='POST')



class MLAPIService(BaseHTTPService):
    URLS = {
        'ml_predict': 'predict'
    }

    def __init__(self, config: MLAPIConfig = Provide[ConfigContainer.ml_config]):
        self.url = f'http://{config.ML_PREDICT_HOST}:{config.ML_PORT}'



class VRAPICore(BaseHTTPService):
    URLS = {
        'ml_predict': 'api/predict',
        'adapt': 'api/adapt',
        'validate': 'api/get_data_for_validate_by_range',
        'fmm': 'api/fmm'
    }

    def __init__(self, config: TSDBAPIConfig = Provide[ConfigContainer.tsdb_config]):
        self.url = f'http://127.0.0.1:8003'


    async def get_data_for_validate_by_range(
            self,
            date_start: datetime.datetime,
            date_end: datetime.datetime,
            well_id: str
    ):
        params = {'date_start': date_start, 'date_end': date_end, 'well_id': well_id}
        return await self.execute_request(url=f'{self.url}/{self.URLS["validate"]}', url_params=params, method='GET')

