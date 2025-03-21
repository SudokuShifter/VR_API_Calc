class PMMAPIService:
    URLS = {
        'fmm': '/v1/fmm/calc_fmm_task',
        'adapt': 'v1/fmm/calc_adapt_task',
        'validate': 'v1/fmm/calc_validate_task',
    }
    def __init__(self, config):
        self.url = f'http://{config.PMM_HOST}:{config.PMM_PORT}/'


class MLAPIService:
    URLS = {
        'ml_predict': '/predict'
    }
    def __init__(self, config):
        self.url = f'http://{config.ML_PREDICT_HOST}:{config.ML_PORT}/'


class VRAPICore:
    URLS = {

    }
    def __init__(self, config):
        self.url = f'http://{config.TSDB_HOST}:{config.TSDB_PORT}/'
