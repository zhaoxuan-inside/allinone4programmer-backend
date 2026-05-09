import logging

def setup_logger():
    from app.config import settings
    logging.basicConfig(
        level=logging.DEBUG if settings.debug else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    return logging.getLogger("fastapi-app")

logger = setup_logger()