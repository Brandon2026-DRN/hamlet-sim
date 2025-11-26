"""Gertrude agent implementation."""

import random
from typing import List, Tuple, Optional
from .base_agent import BaseAgent, ActionType
from ..world.world_state import WorldState


class Gertrude(BaseAgent):
    """Gertrude - seeks stability, mediates others."""
    
    def __init__(self):
        super().__init__(
            name="Gertrude",
            aggression=0.2,
            loyalty=0.7,
            paranoia=0.4,
            goals=["maintain_stability", "protect_hamlet", "survive"]
        )
        self.state.mood = 0.5
        self.state.suspicion_level = 0.3
    
    def _make_decision(
        self,
        world_state: WorldState,
        other_agents: List[BaseAgent]
    ) -> Tuple[ActionType, Optional[BaseAgent]]:
        """Gertrude's decision-making: mediates, seeks stability."""
        hamlet = next((a for a in other_agents if a.name == "Hamlet"), None)
        claudius = next((a for a in other_agents if a.name == "Claudius"), None)
        
        # Try to mediate between Hamlet and Claudius
        if hamlet and claudius and hamlet.state.is_alive and claudius.state.is_alive:
            conflict = world_state.relationship_matrix.get_relationship(hamlet, claudius)
            if conflict["suspicion"] > 0.5:
                # Try to talk to both to mediate
                if random.random() < 0.5:
                    return (ActionType.TALK_TO, hamlet)
                else:
                    return (ActionType.TALK_TO, claudius)
        
        # Protect Hamlet
        if hamlet and hamlet.state.is_alive:
            if random.random() < 0.4:
                return (ActionType.DEFEND, hamlet)
            elif random.random() < 0.3:
                return (ActionType.TALK_TO, hamlet)
        
        # Maintain relationship with Claudius
        if claudius and claudius.state.is_alive:
            if random.random() < 0.3:
                return (ActionType.TALK_TO, claudius)
        
        # Default: talk to random agent
        if other_agents:
            return (ActionType.TALK_TO, random.choice(other_agents))
        
        return (ActionType.HIDE, None)

