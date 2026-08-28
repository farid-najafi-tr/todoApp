from pydantic_settings import BaseSettings,SettingsConfigDict


from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

ENV_PATH = BASE_DIR / '.env'

load_dotenv(dotenv_path=ENV_PATH)

SQLALCHEMY_POSTGRES_DATABASE_URL = os.getenv('SQLALCHEMY_POSTGRES_DATABASE_URL')

class Setting(BaseSettings):
    
    SQLALCHEMY_POSTGRES_DATABASE_URL : str
    
    model_config = SettingsConfigDict(env_file=".env")