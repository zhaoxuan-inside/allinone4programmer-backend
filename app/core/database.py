from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import settings

engine = create_async_engine(settings.database_url, echo=settings.debug)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    # 每个请求开始时：AsyncSessionLocal() 创建一个新的 AsyncSession 对象。
    # 底层会从连接池中 借出一个数据库连接（不会新建 TCP 连接，除非池子空了且未达到上限）。
    # 请求结束时：退出 async with，session.close() 将连接 归还给连接池（不是真正关闭）。
    async with AsyncSessionLocal() as session:
        # yield 是 Python 中用于定义 生成器（generator） 的关键字。
        # 当一个函数中包含 yield 时，这个函数就不再是普通函数，而是一个生成器函数；调用它不会立刻执行函数体，而是返回一个生成器对象。
        yield session
