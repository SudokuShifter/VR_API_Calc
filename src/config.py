import os
from dataclasses import dataclass

from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


@dataclass
class PSQLConfig:
    PSQL_HOST: str
    PSQL_PORT: str
    PSQL_USER: str
    PSQL_PASS: str
    PSQL_DB: str


def load_psql_config() -> PSQLConfig:
    return PSQLConfig(
        PSQL_HOST=os.getenv('PSQL_HOST'),
        PSQL_PORT=os.getenv('PSQL_PORT'),
        PSQL_USER=os.getenv('PSQL_USER'),
        PSQL_PASS=os.getenv('PSQL_PASS'),
        PSQL_DB=os.getenv('PSQL_DB')
    )


class MLAPIConfig(BaseSettings):
    ML_HOST: str = Field(...)
    ML_PORT: str = Field(...)


class PMMAPIConfig(BaseSettings):
    PMM_HOST: str = Field(...)
    PMM_PORT: str = Field(...)


class TSDBAPIConfig(BaseSettings):
    """
    Наш ZIIOT
    """
    TSDB_HOST: str = Field(...)
    TSDB_PORT: str = Field(...)

