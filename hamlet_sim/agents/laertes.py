"""Laertes agent implementation."""

import random
from typing import List, Tuple, Optional
from .base_agent import BaseAgent, ActionType
from ..world.world_state import WorldState


class Laertes(BaseAgent):
    """Laertes - revenge-seeking, protective of Ophelia."""
    
    def __init__(self):
        super().__init__(
            name="Laertes",
            aggression=0.8,
            loyalty=0.6,
            paranoia=0.5,
            goals=["avenge_father", "protect_ophelia", "survive"]
        )
        self.state.mood = 0.4
        self.state.suspicion_level = 0.6
    
    def _make_decision(
        self,
        world_state: WorldState,
        other_agents: List[BaseAgent]
    ) -> Tuple[ActionType, Optional[BaseAgent]]:
        """Laertes's decision-making: revenge-seeking, protective."""
        hamlet = next((a for a in other_agents if a.name == "Hamlet"), None)
        ophelia = next((a for a in other_agents if a.name == "Ophelia"), None)
        claudius = next((a for a in other_agents if a.name == "Claudius"), None)
        
        # Protective of Ophelia
        if ophelia and ophelia.state.is_alive:
            if random.random() < 0.4:
                return (ActionType.DEFEND, ophelia)
            elif random.random() < 0.3:
                return (ActionType.TALK_TO, ophelia)
        
        # Revenge against Hamlet (if suspicion is high)
        if hamlet and hamlet.state.is_alive:
            suspicion = world_state.relationship_matrix.get_suspicion_level(
                self, hamlet
            )
            if suspicion > 0.5 or random.random() < 0.3:
                if random.random() < 0.5:
                    return (ActionType.ATTACK, hamlet)
                else:
                    return (ActionType.ACCUSE, hamlet)
        
        # Sometimes works with Claudius
        if claudius and claudius.state.is_alive:
            if random.random() < 0.2:
                return (ActionType.TALK_TO, claudius)
        
        # Default: talk to random agent
        if other_agents:
            return (ActionType.TALK_TO, random.choice(other_agents))
        
        return (ActionType.HIDE, None)

