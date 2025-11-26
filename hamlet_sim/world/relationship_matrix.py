"""Relationship matrix to track relationships between agents."""

from typing import Dict, Optional
from ..agents.base_agent import BaseAgent


class RelationshipMatrix:
    """Tracks relationships between all agents."""
    
    def __init__(self):
        """Initialize an empty relationship matrix."""
        # Nested dict: {agent1_name: {agent2_name: relationship_data}}
        self._matrix: Dict[str, Dict[str, Dict[str, float]]] = {}
    
    def initialize_agent(self, agent: BaseAgent):
        """Initialize relationship entries for a new agent."""
        if agent.name not in self._matrix:
            self._matrix[agent.name] = {}
    
    def get_relationship(
        self,
        agent1: BaseAgent,
        agent2: BaseAgent
    ) -> Dict[str, float]:
        """
        Get relationship data between two agents.
        
        Returns:
            Dict with keys: trust, fear, suspicion, love, influence
        """
        self._ensure_exists(agent1, agent2)
        return self._matrix[agent1.name][agent2.name].copy()
    
    def set_relationship_value(
        self,
        agent1: BaseAgent,
        agent2: BaseAgent,
        key: str,
        value: float
    ):
        """Set a specific relationship value."""
        self._ensure_exists(agent1, agent2)
        self._matrix[agent1.name][agent2.name][key] = max(0.0, min(1.0, value))
    
    def modify_relationship(
        self,
        agent1: BaseAgent,
        agent2: BaseAgent,
        trust_delta: float = 0.0,
        fear_delta: float = 0.0,
        suspicion_delta: float = 0.0,
        love_delta: float = 0.0,
        influence_delta: float = 0.0
    ):
        """
        Modify relationship values between two agents.
        
        Args:
            agent1: First agent
            agent2: Second agent
            trust_delta: Change in trust level
            fear_delta: Change in fear level
            suspicion_delta: Change in suspicion level
            love_delta: Change in love/loyalty level
            influence_delta: Change in influence score
        """
        self._ensure_exists(agent1, agent2)
        rel = self._matrix[agent1.name][agent2.name]
        
        rel["trust"] = max(0.0, min(1.0, rel["trust"] + trust_delta))
        rel["fear"] = max(0.0, min(1.0, rel["fear"] + fear_delta))
        rel["suspicion"] = max(0.0, min(1.0, rel["suspicion"] + suspicion_delta))
        rel["love"] = max(0.0, min(1.0, rel["love"] + love_delta))
        rel["influence"] = max(0.0, min(1.0, rel["influence"] + influence_delta))
    
    def _ensure_exists(self, agent1: BaseAgent, agent2: BaseAgent):
        """Ensure relationship entries exist for both agents."""
        for agent in [agent1, agent2]:
            if agent.name not in self._matrix:
                self._matrix[agent.name] = {}
        
        # Initialize relationship if it doesn't exist
        if agent2.name not in self._matrix[agent1.name]:
            self._matrix[agent1.name][agent2.name] = {
                "trust": 0.5,
                "fear": 0.0,
                "suspicion": 0.0,
                "love": 0.0,
                "influence": 0.0,
            }
        
        if agent1.name not in self._matrix[agent2.name]:
            self._matrix[agent2.name][agent1.name] = {
                "trust": 0.5,
                "fear": 0.0,
                "suspicion": 0.0,
                "love": 0.0,
                "influence": 0.0,
            }
    
    def get_all_relationships(self, agent: BaseAgent) -> Dict[str, Dict[str, float]]:
        """Get all relationships for a given agent."""
        if agent.name not in self._matrix:
            return {}
        return {
            other_name: rel.copy()
            for other_name, rel in self._matrix[agent.name].items()
        }
    
    def get_trust_level(self, agent1: BaseAgent, agent2: BaseAgent) -> float:
        """Get trust level between two agents."""
        self._ensure_exists(agent1, agent2)
        return self._matrix[agent1.name][agent2.name]["trust"]
    
    def get_suspicion_level(self, agent1: BaseAgent, agent2: BaseAgent) -> float:
        """Get suspicion level between two agents."""
        self._ensure_exists(agent1, agent2)
        return self._matrix[agent1.name][agent2.name]["suspicion"]

