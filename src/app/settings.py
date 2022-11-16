from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False

    TINKOFF_BUSINESS_DEMO_MODE: bool = False
    TINKOFF_BUSINESS_TOKEN: str

    DIADOC_CLIENT_ID: str
    DIADOC_LOGIN: str
    DIADOC_PASSWORD: str

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()
