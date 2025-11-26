"""Claudius agent implementation."""

import random
from typing import List, Tuple, Optional
from .base_agent import BaseAgent, ActionType
from ..world.world_state import WorldState


class Claudius(BaseAgent):
    """Claudius - seeks power, high paranoia."""
    
    def __init__(self):
        super().__init__(
            name="Claudius",
            aggression=0.7,
            loyalty=0.2,
            paranoia=0.9,
            goals=["gain_power", "maintain_power", "survive"]
        )
        self.state.mood = 0.6  # Confident but paranoid
        self.state.suspicion_level = 0.8
    
    def _make_decision(
        self,
        world_state: WorldState,
        other_agents: List[BaseAgent]
    ) -> Tuple[ActionType, Optional[BaseAgent]]:
        """Claudius's decision-making: paranoid, seeks to maintain power."""
        # Find Hamlet (threat to power)
        hamlet = next((a for a in other_agents if a.name == "Hamlet"), None)
        polonius = next((a for a in other_agents if a.name == "Polonius"), None)
        gertrude = next((a for a in other_agents if a.name == "Gertrude"), None)
        
        # Very suspicious of Hamlet - likely to spy or scheme against him
        if hamlet and hamlet.state.is_alive:
            suspicion = world_state.relationship_matrix.get_suspicion_level(
                self, hamlet
            )
            if suspicion > 0.4 or random.random() < 0.5:
                if random.random() < 0.4:
                    return (ActionType.SPY_ON, hamlet)
                elif random.random() < 0.3:
                    return (ActionType.SCHEME, hamlet)
                else:
                    return (ActionType.ATTACK, hamlet)
        
        # Use Polonius as spy
        if polonius and polonius.state.is_alive:
            if random.random() < 0.3:
                return (ActionType.TALK_TO, polonius)
        
        # Maintain relationship with Gertrude
        if gertrude and gertrude.state.is_alive:
            if random.random() < 0.3:
                return (ActionType.TALK_TO, gertrude)
        
        # Often schemes
        if random.random() < 0.4:
            return (ActionType.SCHEME, None)
        
        # Default: talk to random agent
        if other_agents:
            return (ActionType.TALK_TO, random.choice(other_agents))
        
        return (ActionType.HIDE, None)

