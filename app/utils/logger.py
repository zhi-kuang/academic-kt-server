import logging
from logging.handlers import TimedRotatingFileHandler


def create_logger(app):
    # 配置log
    logging.basicConfig(level=logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s] - %(message)s')
    handler = logging.handlers.TimedRotatingFileHandler(
        'logs/academic_llm.log',
        when='D',
        interval=1,
        backupCount=15,
        encoding="UTF-8",
        delay=False,
        utc=True
    )
    handler.suffix = '%Y-%m-%d.log'
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
