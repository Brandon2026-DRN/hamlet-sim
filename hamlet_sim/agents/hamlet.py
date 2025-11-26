"""Hamlet agent implementation."""

import random
from typing import List, Tuple, Optional
from .base_agent import BaseAgent, ActionType
from ..world.world_state import WorldState


class Hamlet(BaseAgent):
    """Hamlet - seeks truth, low trust, high introspection."""
    
    def __init__(self):
        super().__init__(
            name="Hamlet",
            aggression=0.4,
            loyalty=0.6,
            paranoia=0.7,
            goals=["seek_truth", "avenge_father", "survive"]
        )
        self.state.mood = 0.3  # Starts melancholic
        self.state.suspicion_level = 0.6
    
    def _make_decision(
        self,
        world_state: WorldState,
        other_agents: List[BaseAgent]
    ) -> Tuple[ActionType, Optional[BaseAgent]]:
        """Hamlet's decision-making: seeks truth, suspicious of Claudius."""
        # Find Claudius
        claudius = next((a for a in other_agents if a.name == "Claudius"), None)
        horatio = next((a for a in other_agents if a.name == "Horatio"), None)
        
        # High suspicion of Claudius - likely to spy or accuse
        if claudius and claudius.state.is_alive:
            suspicion = world_state.relationship_matrix.get_suspicion_level(
                self, claudius
            )
            if suspicion > 0.5 or random.random() < 0.4:
                if random.random() < 0.6:
                    return (ActionType.SPY_ON, claudius)
                else:
                    return (ActionType.ACCUSE, claudius)
        
        # Trust Horatio - talk to him
        if horatio and horatio.state.is_alive:
            trust = world_state.relationship_matrix.get_trust_level(self, horatio)
            if trust > 0.5 or random.random() < 0.5:
                return (ActionType.TALK_TO, horatio)
        
        # Sometimes schemes or hides
        if random.random() < 0.3:
            return (ActionType.SCHEME, None)
        elif random.random() < 0.2:
            return (ActionType.HIDE, None)
        
        # Default: talk to random agent
        if other_agents:
            return (ActionType.TALK_TO, random.choice(other_agents))
        
        return (ActionType.HIDE, None)

