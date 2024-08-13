"""pycqs a package of CQS (Command Query Separation) utilities"""

from .command_bus import Command, CommandBus, CommandHandler
from .query_bus import Query, QueryBus, QueryHandler, QueryResult

__version__ = '1.0.0'
__all__ = [
    'Command',
    'CommandBus',
    'CommandHandler',
    'Query',
    'QueryBus',
    'QueryHandler',
    'QueryResult',
]
