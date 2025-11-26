"""Main simulation loop for the Hamlet game."""

from typing import List, Optional
from ..agents.base_agent import BaseAgent
from ..world.world_state import WorldState
from ..events.event_log import EventLog
from ..events.event import Event
from .decision_engine import DecisionEngine
import time


class SimulationLoop:
    """Main simulation loop that runs the game."""
    
    def __init__(
        self,
        agents: List[BaseAgent],
        event_log: Optional[EventLog] = None,
        auto_mode: bool = False,
        turn_delay: float = 1.0
    ):
        """
        Initialize simulation loop.
        
        Args:
            agents: List of agents in the simulation
            event_log: Optional event log (creates one if None)
            auto_mode: If True, runs automatically without pauses
            turn_delay: Delay between turns in seconds (for auto mode)
        """
        self.world_state = WorldState(agents)
        self.event_log = event_log or EventLog()
        self.auto_mode = auto_mode
        self.turn_delay = turn_delay
        self.decision_engine = DecisionEngine(self.world_state)
        self.is_running = False
        self.max_turns = 50  # TODO: Make configurable
    
    def run(self, max_turns: Optional[int] = None):
        """
        Run the simulation.
        
        Args:
            max_turns: Maximum number of turns (uses default if None)
        """
        if max_turns:
            self.max_turns = max_turns
        
        self.is_running = True
        
        while self.is_running and self.world_state.turn_number < self.max_turns:
            self._run_turn()
            
            # Check if enough agents are alive
            living = self.world_state.get_living_agents()
            if len(living) < 2:
                print(f"\nSimulation ended: Only {len(living)} agent(s) remaining.")
                break
            
            if not self.auto_mode:
                # Wait for user input in step mode
                input("\nPress Enter to continue to next turn...")
            else:
                time.sleep(self.turn_delay)
        
        if self.world_state.turn_number >= self.max_turns:
            print(f"\nSimulation ended: Reached maximum turns ({self.max_turns}).")
    
    def _run_turn(self):
        """Execute one turn of the simulation."""
        self.world_state.advance_turn()
        
        # Get all living agents
        living_agents = self.world_state.get_living_agents()
        
        # Shuffle for random order
        import random
        random.shuffle(living_agents)
        
        # Each agent decides and acts
        turn_events = []
        for agent in living_agents:
            if not agent.state.is_alive:
                continue
            
            # Get other agents (excluding self)
            other_agents = [a for a in living_agents if a != agent]
            
            # Agent decides action
            action, target = agent.decide_action(self.world_state, other_agents)
            
            # Process action
            event = self.decision_engine.process_action(agent, action, target)
            turn_events.append(event)
            self.event_log.add_event(event)
            
            # Print action
            print(event.to_string())
        
        return turn_events
    
    def step(self) -> List[Event]:
        """
        Execute one turn and return events.
        
        Returns:
            List of events from this turn
        """
        return self._run_turn()
    
    def stop(self):
        """Stop the simulation."""
        self.is_running = False
    
    def get_summary(self) -> str:
        """Get a summary of the current state."""
        living = self.world_state.get_living_agents()
        alliances = self.world_state.get_alliances()
        conflicts = self.world_state.get_conflicts()
        
        summary = [
            f"\n=== Turn {self.world_state.turn_number} Summary ===",
            f"Living agents: {len(living)}",
            f"  {', '.join([a.name for a in living])}",
            f"\nAlliances: {len(alliances)}",
        ]
        
        for agent1, agent2 in alliances:
            summary.append(f"  {agent1.name} <-> {agent2.name}")
        
        summary.append(f"\nConflicts: {len(conflicts)}")
        for agent1, agent2 in conflicts:
            summary.append(f"  {agent1.name} <-> {agent2.name}")
        
        return "\n".join(summary)

