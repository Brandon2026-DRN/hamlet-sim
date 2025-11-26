"""Event class for tracking actions in the simulation."""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from ..agents.base_agent import BaseAgent, ActionType


@dataclass
class Event:
    """Represents a single event/action in the simulation."""
    
    turn: int
    agent: BaseAgent
    action: ActionType
    target: Optional[BaseAgent]
    description: str
    timestamp: datetime = None
    
    def __post_init__(self):
        """Initialize timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_string(self) -> str:
        """Convert event to a readable string."""
        target_str = f" -> {self.target.name}" if self.target else ""
        return (
            f"Turn {self.turn}: {self.agent.name} "
            f"{self.action.value}{target_str} - {self.description}"
        )
    
    def to_dict(self) -> dict:
        """Convert event to dictionary for logging."""
        return {
            "turn": self.turn,
            "agent": self.agent.name,
            "action": self.action.value,
            "target": self.target.name if self.target else None,
            "description": self.description,
            "timestamp": self.timestamp.isoformat(),
        }

