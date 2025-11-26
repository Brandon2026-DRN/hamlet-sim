"""World state management for the simulation."""

from typing import List, Optional, Tuple
from .relationship_matrix import RelationshipMatrix
from ..agents.base_agent import BaseAgent


class WorldState:
    """Manages the overall state of the simulation world."""
    
    def __init__(self, agents: List[BaseAgent]):
        """
        Initialize world state with agents.
        
        Args:
            agents: List of all agents in the simulation
        """
        self.agents = agents
        self.relationship_matrix = RelationshipMatrix()
        self.turn_number = 0
        
        # Initialize relationships for all agents
        for agent in agents:
            self.relationship_matrix.initialize_agent(agent)
            # Initialize relationships between all pairs
            for other_agent in agents:
                if agent != other_agent:
                    self.relationship_matrix._ensure_exists(agent, other_agent)
    
    def get_living_agents(self) -> List[BaseAgent]:
        """Get all agents that are currently alive."""
        return [agent for agent in self.agents if agent.state.is_alive]
    
    def get_agent_by_name(self, name: str) -> Optional[BaseAgent]:
        """Get an agent by name."""
        for agent in self.agents:
            if agent.name == name:
                return agent
        return None
    
    def advance_turn(self):
        """Advance to the next turn."""
        self.turn_number += 1
    
    def get_alliances(self) -> List[Tuple[BaseAgent, BaseAgent]]:
        """
        Detect alliances based on trust and love levels.
        
        Returns:
            List of tuples representing agent pairs with strong positive relationships
        """
        alliances = []
        living = self.get_living_agents()
        
        for i, agent1 in enumerate(living):
            for agent2 in living[i+1:]:
                rel = self.relationship_matrix.get_relationship(agent1, agent2)
                # Consider it an alliance if trust + love > 1.2
                if rel["trust"] + rel["love"] > 1.2:
                    alliances.append((agent1, agent2))
        
        return alliances
    
    def get_conflicts(self) -> List[Tuple[BaseAgent, BaseAgent]]:
        """
        Detect conflicts based on suspicion and fear levels.
        
        Returns:
            List of tuples representing agent pairs with strong negative relationships
        """
        conflicts = []
        living = self.get_living_agents()
        
        for i, agent1 in enumerate(living):
            for agent2 in living[i+1:]:
                rel = self.relationship_matrix.get_relationship(agent1, agent2)
                # Consider it a conflict if suspicion + fear > 1.2
                if rel["suspicion"] + rel["fear"] > 1.2:
                    conflicts.append((agent1, agent2))
        
        return conflicts

