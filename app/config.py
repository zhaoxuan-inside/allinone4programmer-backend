# BaseSettings：一个基类，用于创建配置类，自动从环境变量读取值
# 一个类型字典，用于配置 BaseSettings 的行为
from pydantic_settings import BaseSettings, SettingsConfigDict


# (BaseSettings)：括号表示继承自 BaseSettings
class Settings(BaseSettings):
    app_name: str = "AllInOne Backend"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    database_url: str
    redis_url: str
    redis_max_connections: int = 50

    # 当创建 Settings 实例时（settings = Settings()），BaseSettings 的底层机制会读取这个 model_config，
    # 并根据其中的 env_file=".env" 去加载该文件中的环境变量，然后用于填充类的属性
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
