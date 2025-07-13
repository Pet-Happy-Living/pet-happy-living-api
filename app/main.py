from fastapi import FastAPI
from app.api import endpoints

app = FastAPI(title="Pet Happy Recommendation API")

app.include_router(endpoints.router)
