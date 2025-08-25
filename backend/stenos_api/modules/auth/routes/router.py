from . import auth_router
from . import register

auth_router.include_router(register.auth_router)

