from pydantic import Field
from pydantic_settings import BaseSettings


class PSQLConfig(BaseSettings):
    PSQL_HOST: str = Field(...)
    PSQL_PORT: str = Field(...)
    PSQL_USER: str = Field(...)
    PSQL_PASS: str = Field(...)
    PSQL_DB: str = Field(...)
    PSQL_SCHEMA: str = Field(...)


class TSDBAPIConfig(BaseSettings):
    """
    Наш ZIIOT
    """
    TSDB_HOST: str = Field(...)
    TSDB_PORT: str = Field(...)
