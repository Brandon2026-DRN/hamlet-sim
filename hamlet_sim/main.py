"""Main entry point for the Hamlet simulation game."""

from .agents import (
    Hamlet, Claudius, Gertrude, Ophelia, Horatio, Laertes, Polonius
)
from .simulation import SimulationLoop
from .ui import CLIUI, WebUI


def create_agents():
    """Create and return all agents for the simulation."""
    return [
        Hamlet(),
        Claudius(),
        Gertrude(),
        Ophelia(),
        Horatio(),
        Laertes(),
        Polonius(),
    ]


def initialize_relationships(world_state):
    """Initialize starting relationships between characters."""
    matrix = world_state.relationship_matrix
    
    # Get agents by name
    hamlet = world_state.get_agent_by_name("Hamlet")
    claudius = world_state.get_agent_by_name("Claudius")
    gertrude = world_state.get_agent_by_name("Gertrude")
    ophelia = world_state.get_agent_by_name("Ophelia")
    horatio = world_state.get_agent_by_name("Horatio")
    laertes = world_state.get_agent_by_name("Laertes")
    polonius = world_state.get_agent_by_name("Polonius")
    
    # Hamlet - Horatio: High trust and love (close friends)
    if hamlet and horatio:
        matrix.set_relationship_value(hamlet, horatio, "trust", 0.9)
        matrix.set_relationship_value(hamlet, horatio, "love", 0.8)
        matrix.set_relationship_value(horatio, hamlet, "trust", 0.9)
        matrix.set_relationship_value(horatio, hamlet, "love", 0.85)
    
    # Hamlet - Claudius: High suspicion (Hamlet suspects Claudius)
    if hamlet and claudius:
        matrix.set_relationship_value(hamlet, claudius, "suspicion", 0.7)
        matrix.set_relationship_value(hamlet, claudius, "trust", 0.2)
        matrix.set_relationship_value(claudius, hamlet, "suspicion", 0.6)
        matrix.set_relationship_value(claudius, hamlet, "fear", 0.4)
    
    # Claudius - Gertrude: Moderate trust (married)
    if claudius and gertrude:
        matrix.set_relationship_value(claudius, gertrude, "trust", 0.6)
        matrix.set_relationship_value(claudius, gertrude, "love", 0.5)
        matrix.set_relationship_value(gertrude, claudius, "trust", 0.6)
        matrix.set_relationship_value(gertrude, claudius, "love", 0.5)
    
    # Hamlet - Gertrude: Moderate trust (mother-son, but strained)
    if hamlet and gertrude:
        matrix.set_relationship_value(hamlet, gertrude, "trust", 0.4)
        matrix.set_relationship_value(hamlet, gertrude, "love", 0.5)
        matrix.set_relationship_value(gertrude, hamlet, "trust", 0.5)
        matrix.set_relationship_value(gertrude, hamlet, "love", 0.7)
    
    # Ophelia - Laertes: High love (siblings)
    if ophelia and laertes:
        matrix.set_relationship_value(ophelia, laertes, "love", 0.9)
        matrix.set_relationship_value(ophelia, laertes, "trust", 0.8)
        matrix.set_relationship_value(laertes, ophelia, "love", 0.9)
        matrix.set_relationship_value(laertes, ophelia, "trust", 0.8)
    
    # Ophelia - Polonius: High love (father-daughter)
    if ophelia and polonius:
        matrix.set_relationship_value(ophelia, polonius, "love", 0.8)
        matrix.set_relationship_value(ophelia, polonius, "trust", 0.7)
        matrix.set_relationship_value(polonius, ophelia, "love", 0.8)
        matrix.set_relationship_value(polonius, ophelia, "trust", 0.7)
    
    # Polonius - Claudius: Moderate trust (serves Claudius)
    if polonius and claudius:
        matrix.set_relationship_value(polonius, claudius, "trust", 0.6)
        matrix.set_relationship_value(polonius, claudius, "influence", 0.5)
        matrix.set_relationship_value(claudius, polonius, "trust", 0.5)
    
    # Hamlet - Ophelia: Complex relationship
    if hamlet and ophelia:
        matrix.set_relationship_value(hamlet, ophelia, "love", 0.4)
        matrix.set_relationship_value(hamlet, ophelia, "trust", 0.3)
        matrix.set_relationship_value(ophelia, hamlet, "love", 0.5)
        matrix.set_relationship_value(ophelia, hamlet, "trust", 0.4)


def main(web_mode: bool = False, port: int = 8001):
    """
    Main entry point.
    
    Args:
        web_mode: If True, run web interface; if False, run CLI
        port: Port for web server (only used in web mode)
    """
    print("Initializing Hamlet Simulation...")
    
    # Create agents
    agents = create_agents()
    print(f"Created {len(agents)} agents: {', '.join([a.name for a in agents])}")
    
    # Create simulation
    simulation = SimulationLoop(agents, auto_mode=False)
    
    # Initialize relationships
    initialize_relationships(simulation.world_state)
    print("Initialized relationships between characters.")
    
    # Create UI and run
    if web_mode:
        ui = WebUI(simulation, port=port)
        ui.run()
    else:
        ui = CLIUI(simulation)
        ui.run_interactive()


if __name__ == "__main__":
    main()

