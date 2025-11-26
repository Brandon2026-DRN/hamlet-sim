"""Decision engine for processing agent actions and their consequences."""

from typing import Tuple
from ..agents.base_agent import BaseAgent, ActionType
from ..world.world_state import WorldState
from ..events.event import Event
import random


class DecisionEngine:
    """Processes agent decisions and updates world state accordingly."""
    
    def __init__(self, world_state: WorldState):
        """
        Initialize decision engine.
        
        Args:
            world_state: The world state to modify
        """
        self.world_state = world_state
    
    def process_action(
        self,
        agent: BaseAgent,
        action: ActionType,
        target: BaseAgent = None
    ) -> Event:
        """
        Process an agent's action and update world state.
        
        Args:
            agent: The agent performing the action
            action: The type of action
            target: Optional target agent
            
        Returns:
            Event object representing the action
        """
        description = self._generate_description(agent, action, target)
        
        # Update relationships based on action
        if target:
            self._update_relationships(agent, action, target)
        
        # Handle special action consequences
        self._handle_action_consequences(agent, action, target)
        
        # Create event
        event = Event(
            turn=self.world_state.turn_number,
            agent=agent,
            action=action,
            target=target,
            description=description
        )
        
        return event
    
    def _generate_description(
        self,
        agent: BaseAgent,
        action: ActionType,
        target: BaseAgent = None
    ) -> str:
        """Generate a description for an action."""
        target_name = target.name if target else "themselves"
        
        descriptions = {
            ActionType.TALK_TO: f"{agent.name} speaks with {target_name}",
            ActionType.SPY_ON: f"{agent.name} spies on {target_name}",
            ActionType.BETRAY: f"{agent.name} betrays {target_name}",
            ActionType.ACCUSE: f"{agent.name} accuses {target_name}",
            ActionType.DEFEND: f"{agent.name} defends {target_name}",
            ActionType.ATTACK: f"{agent.name} attacks {target_name}",
            ActionType.HIDE: f"{agent.name} hides from view",
            ActionType.SCHEME: f"{agent.name} schemes against {target_name}" if target else f"{agent.name} schemes",
        }
        
        return descriptions.get(action, f"{agent.name} acts")
    
    def _update_relationships(
        self,
        agent: BaseAgent,
        action: ActionType,
        target: BaseAgent
    ):
        """Update relationships based on action type."""
        matrix = self.world_state.relationship_matrix
        
        if action == ActionType.TALK_TO:
            # Talking increases trust slightly
            matrix.modify_relationship(agent, target, trust_delta=0.1, love_delta=0.05)
            matrix.modify_relationship(target, agent, trust_delta=0.05)
        
        elif action == ActionType.SPY_ON:
            # Spying increases suspicion if discovered
            if random.random() < 0.3:  # 30% chance of discovery
                matrix.modify_relationship(target, agent, suspicion_delta=0.2, trust_delta=-0.1)
            matrix.modify_relationship(agent, target, suspicion_delta=0.1)
        
        elif action == ActionType.BETRAY:
            # Betrayal severely damages relationships
            matrix.modify_relationship(agent, target, trust_delta=-0.3, love_delta=-0.2)
            matrix.modify_relationship(target, agent, trust_delta=-0.4, suspicion_delta=0.3, fear_delta=0.2)
        
        elif action == ActionType.ACCUSE:
            # Accusation increases suspicion and fear
            matrix.modify_relationship(agent, target, suspicion_delta=0.2)
            matrix.modify_relationship(target, agent, suspicion_delta=0.15, fear_delta=0.1, trust_delta=-0.1)
        
        elif action == ActionType.DEFEND:
            # Defense increases trust and love
            matrix.modify_relationship(agent, target, trust_delta=0.15, love_delta=0.1)
            matrix.modify_relationship(target, agent, trust_delta=0.2, love_delta=0.15)
        
        elif action == ActionType.ATTACK:
            # Attack severely damages relationships and may cause harm
            matrix.modify_relationship(agent, target, suspicion_delta=0.3, fear_delta=0.1)
            matrix.modify_relationship(target, agent, suspicion_delta=0.3, fear_delta=0.3, trust_delta=-0.3)
            # Attack may cause health damage
            if random.random() < 0.3:  # 30% chance of injury
                target.state.health = max(0.0, target.state.health - 0.2)
                if target.state.health <= 0:
                    target.state.is_alive = False
        
        elif action == ActionType.SCHEME:
            # Scheming increases suspicion
            if target:
                matrix.modify_relationship(agent, target, suspicion_delta=0.15)
                if random.random() < 0.2:  # 20% chance of discovery
                    matrix.modify_relationship(target, agent, suspicion_delta=0.1, trust_delta=-0.1)
    
    def _handle_action_consequences(
        self,
        agent: BaseAgent,
        action: ActionType,
        target: BaseAgent = None
    ):
        """Handle special consequences of actions."""
        # TODO: Add more complex consequences
        # - Death mechanics
        # - Mood changes
        # - Hidden state changes
        pass

