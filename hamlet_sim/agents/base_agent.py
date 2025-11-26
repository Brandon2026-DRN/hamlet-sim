"""Base agent class for all characters in the simulation."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
from enum import Enum


class ActionType(Enum):
    """Types of actions an agent can take."""
    TALK_TO = "talk_to"
    SPY_ON = "spy_on"
    BETRAY = "betray"
    ACCUSE = "accuse"
    DEFEND = "defend"
    ATTACK = "attack"
    HIDE = "hide"
    SCHEME = "scheme"


class AgentState:
    """Represents the current state of an agent."""
    
    def __init__(self):
        self.mood: float = 0.5  # 0.0 = very negative, 1.0 = very positive
        self.health: float = 1.0  # 0.0 = dead, 1.0 = full health
        self.suspicion_level: float = 0.0  # How suspicious this agent is of others
        self.is_alive: bool = True
        self.is_hidden: bool = False


class BaseAgent(ABC):
    """Base class for all agents in the Hamlet simulation."""
    
    def __init__(
        self,
        name: str,
        aggression: float = 0.5,
        loyalty: float = 0.5,
        paranoia: float = 0.5,
        goals: Optional[List[str]] = None
    ):
        """
        Initialize a base agent.
        
        Args:
            name: Agent's name
            aggression: Aggression level (0.0 to 1.0)
            loyalty: Loyalty level (0.0 to 1.0)
            paranoia: Paranoia level (0.0 to 1.0)
            goals: List of goal strings (e.g., ["survive", "gain_power"])
        """
        self.name = name
        self.aggression = max(0.0, min(1.0, aggression))
        self.loyalty = max(0.0, min(1.0, loyalty))
        self.paranoia = max(0.0, min(1.0, paranoia))
        self.goals = goals or ["survive"]
        self.state = AgentState()
        
    def decide_action(
        self,
        world_state: 'WorldState',
        other_agents: List['BaseAgent']
    ) -> Tuple[ActionType, Optional['BaseAgent']]:
        """
        Decide what action to take this turn.
        
        Args:
            world_state: Current state of the world
            other_agents: List of other agents in the simulation
            
        Returns:
            Tuple of (action_type, target_agent) where target_agent can be None
        """
        # Filter out dead agents
        living_agents = [a for a in other_agents if a.state.is_alive]
        
        if not living_agents:
            return (ActionType.HIDE, None)
        
        # Use personality-driven decision making
        return self._make_decision(world_state, living_agents)
    
    @abstractmethod
    def _make_decision(
        self,
        world_state: 'WorldState',
        other_agents: List['BaseAgent']
    ) -> Tuple[ActionType, Optional['BaseAgent']]:
        """
        Agent-specific decision making logic.
        
        Args:
            world_state: Current state of the world
            other_agents: List of other living agents
            
        Returns:
            Tuple of (action_type, target_agent)
        """
        pass
    
    def get_personality_traits(self) -> Dict[str, float]:
        """Return a dictionary of personality traits."""
        return {
            "aggression": self.aggression,
            "loyalty": self.loyalty,
            "paranoia": self.paranoia,
        }
    
    def get_state(self) -> Dict:
        """Return current state information."""
        return {
            "mood": self.state.mood,
            "health": self.state.health,
            "suspicion_level": self.state.suspicion_level,
            "is_alive": self.state.is_alive,
            "is_hidden": self.state.is_hidden,
        }
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"

