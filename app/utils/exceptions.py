from fastapi import Request, status
from fastapi.responses import JSONResponse
from .logger import logger


# 定义一个新异常类，继承自内置基类 Exception
class BusinessError(Exception):
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code


async def business_error_handler(request: Request, exc: BusinessError):
    logger.warning(f"Business error: {exc.message}", exc_info=exc)
    return JSONResponse(
        status_code=exc.code,
        content={"detail": exc.message},
    )


def register_exception_handlers(app):
    # app.add_exception_handler：FastAPI 应用实例的方法，用于注册异常处理器
    # 异常类型 BusinessError
    # 处理器函数 business_error_handler
    app.add_exception_handler(BusinessError, business_error_handler)
