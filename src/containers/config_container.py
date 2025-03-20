import os

from dotenv import load_dotenv
from dependency_injector import (
    providers,
    containers
)

from pmm_task_api.config import PMMAPIConfig
from ml_task_api.config import MLAPIConfig
from config import (
    PSQLConfig,
    TSDBAPIConfig
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
    psql_config = providers.Factory(
        PSQLConfig,
        PSQL_HOST=os.getenv('PSQL_HOST'),
        PSQL_PORT=os.getenv('PSQL_PORT'),
        PSQL_USER=os.getenv('PSQL_USER'),
        PSQL_PASS=os.getenv('PSQL_PASS'),
        PSQL_DB=os.getenv('PSQL_DB'),
        PSQL_SCHEMA=os.getenv('PSQL_SCHEMA')
    )
    tsdb_config = providers.Factory(
        TSDBAPIConfig,
        TSDB_HOST=os.getenv('TSDB_HOST'),
        TSDB_PORT=os.getenv('TSDB_PORT')
    )
