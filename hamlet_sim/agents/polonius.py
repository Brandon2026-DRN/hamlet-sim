"""Polonius agent implementation."""

import random
from typing import List, Tuple, Optional
from .base_agent import BaseAgent, ActionType
from ..world.world_state import WorldState


class Polonius(BaseAgent):
    """Polonius - spies often."""
    
    def __init__(self):
        super().__init__(
            name="Polonius",
            aggression=0.3,
            loyalty=0.5,
            paranoia=0.6,
            goals=["spy", "serve_claudius", "protect_family", "survive"]
        )
        self.state.mood = 0.5
        self.state.suspicion_level = 0.5
    
    def _make_decision(
        self,
        world_state: WorldState,
        other_agents: List[BaseAgent]
    ) -> Tuple[ActionType, Optional[BaseAgent]]:
        """Polonius's decision-making: spies frequently."""
        hamlet = next((a for a in other_agents if a.name == "Hamlet"), None)
        claudius = next((a for a in other_agents if a.name == "Claudius"), None)
        ophelia = next((a for a in other_agents if a.name == "Ophelia"), None)
        
        # Spies on Hamlet frequently (serves Claudius)
        if hamlet and hamlet.state.is_alive:
            if random.random() < 0.5:
                return (ActionType.SPY_ON, hamlet)
        
        # Reports to Claudius
        if claudius and claudius.state.is_alive:
            if random.random() < 0.3:
                return (ActionType.TALK_TO, claudius)
        
        # Protective of Ophelia
        if ophelia and ophelia.state.is_alive:
            if random.random() < 0.2:
                return (ActionType.TALK_TO, ophelia)
        
        # Sometimes spies on others
        if other_agents and random.random() < 0.3:
            target = random.choice(other_agents)
            return (ActionType.SPY_ON, target)
        
        # Default: talk to random agent
        if other_agents:
            return (ActionType.TALK_TO, random.choice(other_agents))
        
        return (ActionType.HIDE, None)

