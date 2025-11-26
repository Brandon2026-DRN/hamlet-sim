"""Ophelia agent implementation."""

import random
from typing import List, Tuple, Optional
from .base_agent import BaseAgent, ActionType
from ..world.world_state import WorldState


class Ophelia(BaseAgent):
    """Ophelia - avoids conflict, loyalty weighted."""
    
    def __init__(self):
        super().__init__(
            name="Ophelia",
            aggression=0.1,
            loyalty=0.8,
            paranoia=0.3,
            goals=["avoid_conflict", "protect_family", "survive"]
        )
        self.state.mood = 0.4
        self.state.suspicion_level = 0.2
    
    def _make_decision(
        self,
        world_state: WorldState,
        other_agents: List[BaseAgent]
    ) -> Tuple[ActionType, Optional[BaseAgent]]:
        """Ophelia's decision-making: avoids conflict, loyal to family."""
        hamlet = next((a for a in other_agents if a.name == "Hamlet"), None)
        laertes = next((a for a in other_agents if a.name == "Laertes"), None)
        polonius = next((a for a in other_agents if a.name == "Polonius"), None)
        
        # Loyal to family - talk to Laertes and Polonius
        if laertes and laertes.state.is_alive:
            if random.random() < 0.4:
                return (ActionType.TALK_TO, laertes)
        
        if polonius and polonius.state.is_alive:
            if random.random() < 0.3:
                return (ActionType.TALK_TO, polonius)
        
        # Sometimes talks to Hamlet (complex relationship)
        if hamlet and hamlet.state.is_alive:
            if random.random() < 0.3:
                return (ActionType.TALK_TO, hamlet)
        
        # Avoids conflict - often hides
        if random.random() < 0.4:
            return (ActionType.HIDE, None)
        
        # Default: talk to random agent
        if other_agents:
            return (ActionType.TALK_TO, random.choice(other_agents))
        
        return (ActionType.HIDE, None)

