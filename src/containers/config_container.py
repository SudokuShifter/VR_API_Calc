import os

from dotenv import load_dotenv
from dependency_injector import (
    providers,
    containers
)

from config import (
    TSDBAPIConfig,
    MLAPIConfig,
    PMMAPIConfig
)


load_dotenv()


class ConfigContainer(containers.DeclarativeContainer):
    pmm_config = providers.Factory(
        PMMAPIConfig,
        PMM_HOST=os.getenv('PMM_HOST'),
        PMM_PORT=os.getenv('PMM_PORT')
    )
    ml_config = providers.Factory(
        MLAPIConfig,
        ML_HOST=os.getenv('ML_HOST'),
        ML_PORT=os.getenv('ML_PORT')
    )
    tsdb_config = providers.Factory(
        TSDBAPIConfig,
        TSDB_HOST=os.getenv('TSDB_HOST'),
        TSDB_PORT=os.getenv('TSDB_PORT')
    )