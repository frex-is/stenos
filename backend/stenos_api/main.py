from stenos_api.configurations.logging import logger

from fastapi import FastAPI

from stenos_api.core.lifecycle.application import application_lifecycle

stenos_application = FastAPI(lifespan=application_lifecycle)

@stenos_application.get("/")
async def root():
    return {"message": "Hello from FastAPI + MongoDB !"}