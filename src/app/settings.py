from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()
