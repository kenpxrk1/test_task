from pydantic_settings import BaseSettings, SettingsConfigDict
import os 
from dotenv import load_dotenv


from pathlib import Path

 
dotenv_path = Path(__file__).parent.parent.joinpath('.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Settings(BaseSettings):
    ENV_MODE: str 
    DB_HOST: str 
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str 
    

    @property
    def DATABASE_URL(self) -> str:
        """
        Returns a string for bd connection
        """
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # ".env" when making migration and "../.env" when starting app 
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()