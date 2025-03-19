from pydantic import Field
from pydantic_settings import BaseSettings


class PMMAPIConfig(BaseSettings):
    PMM_HOST: str = Field(...)
    PMM_PORT: str = Field(...)


