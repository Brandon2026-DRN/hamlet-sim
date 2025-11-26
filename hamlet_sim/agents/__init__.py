"""Agent module for Hamlet simulation game."""

from .base_agent import BaseAgent
from .hamlet import Hamlet
from .claudius import Claudius
from .gertrude import Gertrude
from .ophelia import Ophelia
from .horatio import Horatio
from .laertes import Laertes
from .polonius import Polonius

__all__ = [
    'BaseAgent',
    'Hamlet',
    'Claudius',
    'Gertrude',
    'Ophelia',
    'Horatio',
    'Laertes',
    'Polonius',
]

