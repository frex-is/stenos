from fastapi import FastAPI
from contextlib import asynccontextmanager

from stenos_api.core.lifecycle.mongo import init_mongo, close_mongo

@asynccontextmanager
async def application_lifecycle(stenos_application: FastAPI):
    await init_mongo(stenos_application)

    yield

    await close_mongo(stenos_application)