"""Horatio agent implementation."""

import random
from typing import List, Tuple, Optional
from .base_agent import BaseAgent, ActionType
from ..world.world_state import WorldState


class Horatio(BaseAgent):
    """Horatio - high loyalty, rarely betrays."""
    
    def __init__(self):
        super().__init__(
            name="Horatio",
            aggression=0.3,
            loyalty=0.95,
            paranoia=0.2,
            goals=["protect_hamlet", "seek_truth", "survive"]
        )
        self.state.mood = 0.6
        self.state.suspicion_level = 0.3
    
    def _make_decision(
        self,
        world_state: WorldState,
        other_agents: List[BaseAgent]
    ) -> Tuple[ActionType, Optional[BaseAgent]]:
        """Horatio's decision-making: extremely loyal to Hamlet."""
        hamlet = next((a for a in other_agents if a.name == "Hamlet"), None)
        
        # Very loyal to Hamlet - often talks to or defends him
        if hamlet and hamlet.state.is_alive:
            if random.random() < 0.6:
                return (ActionType.TALK_TO, hamlet)
            elif random.random() < 0.3:
                return (ActionType.DEFEND, hamlet)
        
        # Sometimes spies on threats to Hamlet
        claudius = next((a for a in other_agents if a.name == "Claudius"), None)
        if claudius and claudius.state.is_alive:
            if random.random() < 0.2:
                return (ActionType.SPY_ON, claudius)
        
        # Default: talk to random agent
        if other_agents:
            return (ActionType.TALK_TO, random.choice(other_agents))
        
        return (ActionType.HIDE, None)

