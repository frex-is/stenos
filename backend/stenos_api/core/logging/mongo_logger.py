from structlog import get_logger
from pymongo.errors import (
    OperationFailure,
    ConnectionFailure,
    ServerSelectionTimeoutError,
    ConfigurationError,
    NetworkTimeout,
    InvalidName
)

_logger = get_logger()

_ERROR_MESSAGES = {
    OperationFailure: "⚠️ MongoDB operation failure. Check permissions or the query.",
    ConnectionFailure: "🔌 Connection failure to MongoDB. Please check network or server status.",
    ServerSelectionTimeoutError: "⏳ MongoDB server selection timeout. Server may be unreachable.",
    ConfigurationError: "🛠️ MongoDB client configuration error. Verify client settings.",
    NetworkTimeout: "⌛ Network timeout during MongoDB communication.",
    InvalidName: "🚫 Invalid MongoDB database name. Verify database name."
}


def log_mongo_error(error: Exception):
    for exception_type, message in _ERROR_MESSAGES.items():
        if isinstance(error, exception_type):
            _logger.error(message, error=str(error), error_type=type(error).__name__)
            break
    else:
        _logger.error("❓ Unknown MongoDB error occurred.", error=str(error), error_type=type(error).__name__)