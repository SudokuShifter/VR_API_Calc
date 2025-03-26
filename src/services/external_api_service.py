import datetime
from typing import Optional, Dict, Any

from dependency_injector.wiring import Provide
from pydantic import BaseModel
from services.core_http_service import BaseHTTPService
from config import PMMAPIConfig, MLAPIConfig

from src.config import TSDBAPIConfig, PMMAPIConfig, MLAPIConfig



class PMMAPIService(BaseHTTPService):
    URLS = {
        'fmm': 'v1/fmm/calc_fmm_task',
        'adapt': 'v1/adapt/calc_adapt_task',
        'validate': 'v1/validate/calc_validate_task',
    }

    def __init__(self):
        self.url_addr = 'http://172.18.77.141:8080'


    async def execute_validate_task(self, data):
        return await self.execute_request(url=f'{self.url_addr}/{self.URLS["validate"]}', body=data, method='POST')

    async def execute_adapt_task(self, data):
        return await self.execute_request(url=f'{self.url_addr}/{self.URLS["adapt"]}', body=data, method='POST')

    async def execute_fmm_task(self, data):
        return await self.execute_request(url=f'{self.url_addr}/{self.URLS["fmm"]}', body=data, method='POST')


class MLAPIService(BaseHTTPService):
    URLS = {
        'ml_predict': 'predict'
    }

    def __init__(self):
        self.url_addr = f'http://127.0.0.1:8005'



class VRAPICore(BaseHTTPService):
    URLS = {
        'ml_predict': 'api/predict',
        'adapt': 'api/get_data_for_adapt_by_range',
        'validate': 'api/get_data_for_validate_by_range',
        'fmm': 'api/fmm'
    }

    def __init__(self):
        self.url_addr = f'http://127.0.0.1:8003'


    async def get_data_for_validate_by_range(
            self,
            time_left: datetime.datetime,
            time_right: datetime.datetime,
            well_id: str
    ):
        params = {'date_start': time_left, 'date_end': time_right, 'well_id': well_id}
        return await self.execute_request(url=f'{self.url_addr}/{self.URLS["validate"]}', url_params=params, method='GET')


    async def get_data_for_adapt_by_range(
            self,
            time_left: datetime.datetime,
            time_right: datetime.datetime,
            well_id: str
    ):
        params = {'date_start': time_left, 'date_end': time_right, 'well_id': well_id}
        return await self.execute_request(url=f'{self.url_addr}/{self.URLS["adapt"]}', url_params=params, method='GET')