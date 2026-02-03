"""
Logging configuration for the document extraction system.

Provides a centralized logging setup for consistent log formatting
across all modules.

Usage in any module:
    from .logging_config import get_logger
    logger = get_logger(__name__)

Log levels to use:
- DEBUG: Detailed internal state (block counts, parsing steps)
- INFO: High-level operations (starting extraction, file loaded)
- WARNING: Non-fatal issues (empty page, missing metadata field)
- ERROR: Failures captured in the errors list
"""

# TODO: Uncomment when implementing
# import logging
# import sys

# Default format: timestamp, level, module, message
# DEFAULT_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
# DEFAULT_LEVEL = logging.INFO


def get_logger(name: str, level: int = 20) -> object:
    """Get a configured logger for the given module name.

    Args:
        name: Module name, typically __name__
        level: Logging level (default: INFO = 20)

    Returns:
        Configured logger instance

    Implementation notes:
    - Use logging.getLogger(name)
    - Check if handlers already exist to avoid duplicates
    - Add StreamHandler to sys.stderr
    - Set formatter with DEFAULT_FORMAT
    - Set level on logger
    """
    # TODO: Implement logging configuration
    pass
