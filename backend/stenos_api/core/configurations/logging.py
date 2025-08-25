from logging import DEBUG, basicConfig

from structlog import configure, get_logger
from structlog.processors import JSONRenderer, add_log_level, TimeStamper
from structlog.stdlib import LoggerFactory


def _setup_logger():
    basicConfig(
        format="%(message)s",
        level=DEBUG
    )

    configure(
        processors=[
            TimeStamper(fmt="iso"),
            add_log_level,
            JSONRenderer()
        ],
        logger_factory=LoggerFactory(),
        cache_logger_on_first_use=True
    )
    
    return get_logger()


logger = _setup_logger()