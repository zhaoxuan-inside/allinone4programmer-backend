from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.router import router as v1_router
from app.middleware.cors import add_cors_middleware
from app.utils.exceptions import register_exception_handlers
from app.config import settings
from app.core.database import engine
from app.core.redis_client import init_redis, close_redis

# 导入模型以便建表
from app.models.item import Base
from app.utils.logger import logger


# 用来将异步生成器函数包装成一个异步上下文管理器，这里用于 FastAPI 的 lifespan
# @asynccontextmanager 将 lifespan 变成一个异步上下文管理器，函数在 yield 之前的部分在应用启动时执行，yield 之后的部分在应用关闭时执行
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时：初始化 Redis
    await init_redis()
    logger.info("Redis connected")

    # 启动时：创建数据库表（仅开发用，生产应使用 Alembic 迁移）
    if settings.debug:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created (development mode)")

    yield

    # 关闭时：清理资源
    await close_redis()
    await engine.dispose()
    logger.info("Resources cleaned up")


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

add_cors_middleware(app)
register_exception_handlers(app)
app.include_router(v1_router)


@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.app_name}"}
