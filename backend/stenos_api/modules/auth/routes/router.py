from fastapi import APIRouter
from stenos_api.modules.auth.routes.register import register_router
from stenos_api.modules.auth.routes.login import login_router

auth_router = APIRouter(tags=["auth"])

auth_router.include_router(register_router)
auth_router.include_router(login_router)

