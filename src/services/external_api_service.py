import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel
from services.core_http_service import BaseHTTPService
from config import PMMAPIConfig, MLAPIConfig


class PMMAPIService(BaseHTTPService):
    URLS = {
        'fmm': 'v1/fmm/calc_fmm_task',
        'adapt': 'v1/fmm/calc_adapt_task',
        'validate': 'v1/fmm/calc_validate_task',
    }

    def __init__(self, config: PMMAPIConfig):
        self.url = f'http://{config.PMM_HOST}:{config.PMM_PORT}'




class MLAPIService(BaseHTTPService):
    URLS = {
        'ml_predict': 'predict'
    }

    def __init__(self, config: MLAPIConfig):
        self.url = f'http://{config.ML_PREDICT_HOST}:{config.ML_PORT}'



class VRAPICore(BaseHTTPService):
    URLS = {
        'ml_predict': 'predict',
        'adapt': 'adapt',
        'validate': 'validate',
        'fmm': 'fmm'
    }

    def __init__(self, config):
        self.url = f'http://{config.TSDB_HOST}:{config.TSDB_PORT}/'

    async def get_data(
            self,
            obj_name: str,
            point: str,
            time_left: str,
            time_right: Optional[str] = None
    ) -> Dict[str, Any]:
        """Получает данные из TSDB для указанного объекта и временного периода"""
        if point not in self.URLS:
            raise ValueError(f"Unknown point: {point}")

        params = {'obj': obj_name}
        if time_right:
            params.update({
                'time_left': time_left,
                'time_right': time_right
            })
        else:
            params['time'] = time_left

        response = await self.execute_request(
            url=f'{self.url}/{self.URLS[point]}',
            method='GET',
            body=params
        )
        return response