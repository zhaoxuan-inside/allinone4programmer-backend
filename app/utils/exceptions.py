from fastapi import Request, status
from fastapi.responses import JSONResponse
from .logger import logger

class BusinessError(Exception):
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code

async def business_error_handler(request: Request, exc: BusinessError):
    logger.warning(f"Business error: {exc.message}")
    return JSONResponse(
        status_code=exc.code,
        content={"detail": exc.message},
    )

def register_exception_handlers(app):
    app.add_exception_handler(BusinessError, business_error_handler)