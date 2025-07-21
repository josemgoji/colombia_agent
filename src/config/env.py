from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    HF_TOKEN: str
    CHROMA_DB_PATH: str 
    WIKIPEDIA_URL: str
    EMBEDDING_MODEL: str
    ENVIRONMENT: str = "dev"
    HF_REPO_ID: str
    HF_PROVIDER: str
    HF_TEMPERATURE: float
    HF_MAX_TOKENS: int
    

    model_config = ConfigDict(env_file=".env")

settings = Settings()