from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    HF_TOKEN: str
    CHROMA_DB_PATH: str = "data/chroma"
    ENVIRONMENT: str = "dev"

    model_config = ConfigDict(env_file=".env")

settings = Settings()