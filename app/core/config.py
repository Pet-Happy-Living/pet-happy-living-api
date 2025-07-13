import os

class Settings:
    PROJECT_NAME: str = "Pet Happy Service"
    POSTGRES_URL: str = os.getenv("POSTGRES_URL", "localhost")
    REDIS_URL: str = os.getenv("REDIS_URL", "localhost")

settings = Settings()
