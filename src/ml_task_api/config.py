from pydantic import Field
from pydantic_settings import BaseSettings


class MLAPIConfig(BaseSettings):
    ML_HOST: str = Field(...)
    ML_PORT: str = Field(...)


