import logging

def setup_logger():
    from app.config import settings
    logging.basicConfig(
        # 三目表达式，判断 setting.debug 是否为 True
        # 等价于 settings.debug ? logging.DEBUG : logging.INFO
        level=logging.DEBUG if settings.debug else logging.INFO,

        # %(asctime)s：格式化占位符，输出时间
        # %(levelname)s：格式化占位符，输出日志级别
        # %(name)s：格式化占位符，记录器名称
        # %(message)s：格式化占位符，输出日志消息
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    return logging.getLogger("allinone")

logger = setup_logger()