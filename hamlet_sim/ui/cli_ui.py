"""Command-line interface for the Hamlet simulation."""

from typing import List, Optional
from ..agents.base_agent import BaseAgent
from ..world.world_state import WorldState
from ..events.event_log import EventLog
from ..simulation.simulation_loop import SimulationLoop


class CLIUI:
    """Command-line user interface for the simulation."""
    
    def __init__(self, simulation: SimulationLoop):
        """
        Initialize CLI UI.
        
        Args:
            simulation: The simulation loop to control
        """
        self.simulation = simulation
        self.event_log = simulation.event_log
        self.world_state = simulation.world_state
    
    def display_welcome(self):
        """Display welcome message."""
        print("=" * 60)
        print("  HAMLET SIMULATION GAME")
        print("=" * 60)
        print("\nA multi-agent simulation based on Shakespeare's Hamlet.")
        print("Watch as characters act autonomously based on their personalities.")
        print()
    
    def display_agents(self):
        """Display all agents and their states."""
        print("\n=== AGENTS ===")
        for agent in self.world_state.agents:
            state = agent.get_state()
            traits = agent.get_personality_traits()
            status = "ALIVE" if state["is_alive"] else "DEAD"
            print(f"\n{agent.name} ({status})")
            print(f"  Mood: {state['mood']:.2f} | Health: {state['health']:.2f}")
            print(f"  Aggression: {traits['aggression']:.2f} | "
                  f"Loyalty: {traits['loyalty']:.2f} | "
                  f"Paranoia: {traits['paranoia']:.2f}")
            print(f"  Goals: {', '.join(agent.goals)}")
    
    def display_relationships(self, agent: Optional[BaseAgent] = None):
        """Display relationship matrix."""
        if agent:
            print(f"\n=== RELATIONSHIPS: {agent.name} ===")
            relationships = self.world_state.relationship_matrix.get_all_relationships(agent)
            for other_name, rel in relationships.items():
                print(f"\n  {other_name}:")
                print(f"    Trust: {rel['trust']:.2f} | Fear: {rel['fear']:.2f}")
                print(f"    Suspicion: {rel['suspicion']:.2f} | Love: {rel['love']:.2f}")
                print(f"    Influence: {rel['influence']:.2f}")
        else:
            print("\n=== RELATIONSHIP MATRIX ===")
            living = self.world_state.get_living_agents()
            for agent in living:
                print(f"\n{agent.name}:")
                relationships = self.world_state.relationship_matrix.get_all_relationships(agent)
                for other_name, rel in relationships.items():
                    if other_name in [a.name for a in living]:
                        print(f"  {other_name}: "
                              f"T:{rel['trust']:.2f} S:{rel['suspicion']:.2f} "
                              f"L:{rel['love']:.2f}")
    
    def display_alliances(self):
        """Display current alliances."""
        alliances = self.world_state.get_alliances()
        print(f"\n=== ALLIANCES ({len(alliances)}) ===")
        if alliances:
            for agent1, agent2 in alliances:
                rel = self.world_state.relationship_matrix.get_relationship(agent1, agent2)
                print(f"  {agent1.name} <-> {agent2.name} "
                      f"(Trust: {rel['trust']:.2f}, Love: {rel['love']:.2f})")
        else:
            print("  No alliances detected.")
    
    def display_conflicts(self):
        """Display current conflicts."""
        conflicts = self.world_state.get_conflicts()
        print(f"\n=== CONFLICTS ({len(conflicts)}) ===")
        if conflicts:
            for agent1, agent2 in conflicts:
                rel = self.world_state.relationship_matrix.get_relationship(agent1, agent2)
                print(f"  {agent1.name} <-> {agent2.name} "
                      f"(Suspicion: {rel['suspicion']:.2f}, Fear: {rel['fear']:.2f})")
        else:
            print("  No conflicts detected.")
    
    def display_recent_events(self, count: int = 10):
        """Display recent events."""
        events = self.event_log.get_recent_events(count)
        print(f"\n=== RECENT EVENTS (Last {len(events)}) ===")
        for event in events:
            print(f"  {event.to_string()}")
    
    def display_turn_summary(self):
        """Display summary of current turn."""
        print(self.simulation.get_summary())
    
    def display_menu(self):
        """Display main menu."""
        print("\n" + "=" * 60)
        print("  MAIN MENU")
        print("=" * 60)
        print("1. Run simulation (auto mode)")
        print("2. Step through turns (manual)")
        print("3. Display agents")
        print("4. Display relationships")
        print("5. Display alliances")
        print("6. Display conflicts")
        print("7. Display recent events")
        print("8. Display turn summary")
        print("9. Quit")
        print()
    
    def run_interactive(self):
        """Run interactive CLI mode."""
        self.display_welcome()
        
        while True:
            self.display_menu()
            choice = input("Enter choice (1-9): ").strip()
            
            if choice == "1":
                turns = input("Enter number of turns (default 10): ").strip()
                max_turns = int(turns) if turns.isdigit() else 10
                self.simulation.auto_mode = True
                self.simulation.turn_delay = 0.5
                print("\nRunning simulation in auto mode...\n")
                self.simulation.run(max_turns=max_turns)
            
            elif choice == "2":
                turns = input("Enter number of turns to step through (default 1): ").strip()
                num_turns = int(turns) if turns.isdigit() else 1
                self.simulation.auto_mode = False
                print("\nStepping through turns...\n")
                for _ in range(num_turns):
                    events = self.simulation.step()
                    if events:
                        print(f"\n{len(events)} action(s) this turn.")
                    self.display_turn_summary()
            
            elif choice == "3":
                self.display_agents()
            
            elif choice == "4":
                agent_name = input("Enter agent name (or press Enter for all): ").strip()
                if agent_name:
                    agent = self.world_state.get_agent_by_name(agent_name)
                    if agent:
                        self.display_relationships(agent)
                    else:
                        print(f"Agent '{agent_name}' not found.")
                else:
                    self.display_relationships()
            
            elif choice == "5":
                self.display_alliances()
            
            elif choice == "6":
                self.display_conflicts()
            
            elif choice == "7":
                count = input("Number of events to show (default 10): ").strip()
                count = int(count) if count.isdigit() else 10
                self.display_recent_events(count)
            
            elif choice == "8":
                self.display_turn_summary()
            
            elif choice == "9":
                print("\nExiting simulation. Goodbye!")
                break
            
            else:
                print("Invalid choice. Please enter 1-9.")

