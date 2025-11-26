"""Event logging system for the simulation."""

from typing import List
from .event import Event
import os


class EventLog:
    """Manages event logging to file and memory."""
    
    def __init__(self, log_file: str = "history.log"):
        """
        Initialize event log.
        
        Args:
            log_file: Path to the log file
        """
        self.log_file = log_file
        self.events: List[Event] = []
        
        # Clear or create log file
        with open(self.log_file, 'w') as f:
            f.write("=== HAMLET SIMULATION LOG ===\n\n")
    
    def add_event(self, event: Event):
        """
        Add an event to the log.
        
        Args:
            event: Event to add
        """
        self.events.append(event)
        
        # Append to file
        with open(self.log_file, 'a') as f:
            f.write(event.to_string() + "\n")
    
    def get_events_for_turn(self, turn: int) -> List[Event]:
        """Get all events for a specific turn."""
        return [e for e in self.events if e.turn == turn]
    
    def get_recent_events(self, count: int = 10) -> List[Event]:
        """Get the most recent N events."""
        return self.events[-count:] if len(self.events) > count else self.events
    
    def get_summary_for_turn(self, turn: int) -> str:
        """Generate a summary string for a turn."""
        turn_events = self.get_events_for_turn(turn)
        if not turn_events:
            return f"Turn {turn}: No events"
        
        summary_lines = [f"\n=== Turn {turn} Summary ==="]
        for event in turn_events:
            summary_lines.append(f"  {event.to_string()}")
        
        return "\n".join(summary_lines)

