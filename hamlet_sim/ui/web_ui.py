"""Web-based UI for the Hamlet simulation using Flask."""

from flask import Flask, render_template, jsonify, request
from typing import List, Optional
from ..agents.base_agent import BaseAgent
from ..world.world_state import WorldState
from ..events.event_log import EventLog
from ..simulation.simulation_loop import SimulationLoop
import threading
import time


class WebUI:
    """Web-based user interface for the simulation."""
    
    def __init__(self, simulation: SimulationLoop, port: int = 8001):
        """
        Initialize web UI.
        
        Args:
            simulation: The simulation loop to control
            port: Port to run the web server on
        """
        self.simulation = simulation
        self.event_log = simulation.event_log
        self.world_state = simulation.world_state
        self.port = port
        self.app = Flask(__name__, 
                        template_folder='templates',
                        static_folder='static')
        self._setup_routes()
        self._auto_run_thread = None
        self._auto_running = False
    
    def _setup_routes(self):
        """Set up Flask routes."""
        
        @self.app.route('/')
        def index():
            """Main page."""
            return render_template('index.html')
        
        @self.app.route('/api/state')
        def get_state():
            """Get current simulation state."""
            return jsonify(self._get_state_dict())
        
        @self.app.route('/api/agents')
        def get_agents():
            """Get all agents and their states."""
            agents_data = []
            for agent in self.world_state.agents:
                state = agent.get_state()
                traits = agent.get_personality_traits()
                agents_data.append({
                    'name': agent.name,
                    'alive': state['is_alive'],
                    'mood': state['mood'],
                    'health': state['health'],
                    'suspicion_level': state['suspicion_level'],
                    'aggression': traits['aggression'],
                    'loyalty': traits['loyalty'],
                    'paranoia': traits['paranoia'],
                    'goals': agent.goals
                })
            return jsonify(agents_data)
        
        @self.app.route('/api/relationships')
        def get_relationships():
            """Get relationship matrix."""
            relationships = {}
            living = self.world_state.get_living_agents()
            for agent in living:
                rels = self.world_state.relationship_matrix.get_all_relationships(agent)
                relationships[agent.name] = {
                    other_name: rel
                    for other_name, rel in rels.items()
                    if other_name in [a.name for a in living]
                }
            return jsonify(relationships)
        
        @self.app.route('/api/alliances')
        def get_alliances():
            """Get current alliances."""
            alliances = self.world_state.get_alliances()
            return jsonify([
                {
                    'agent1': a1.name,
                    'agent2': a2.name,
                    'trust': self.world_state.relationship_matrix.get_relationship(a1, a2)['trust'],
                    'love': self.world_state.relationship_matrix.get_relationship(a1, a2)['love']
                }
                for a1, a2 in alliances
            ])
        
        @self.app.route('/api/conflicts')
        def get_conflicts():
            """Get current conflicts."""
            conflicts = self.world_state.get_conflicts()
            return jsonify([
                {
                    'agent1': a1.name,
                    'agent2': a2.name,
                    'suspicion': self.world_state.relationship_matrix.get_relationship(a1, a2)['suspicion'],
                    'fear': self.world_state.relationship_matrix.get_relationship(a1, a2)['fear']
                }
                for a1, a2 in conflicts
            ])
        
        @self.app.route('/api/events')
        def get_events():
            """Get recent events."""
            count = request.args.get('count', 20, type=int)
            events = self.event_log.get_recent_events(count)
            return jsonify([
                {
                    'turn': e.turn,
                    'agent': e.agent.name,
                    'action': e.action.value,
                    'target': e.target.name if e.target else None,
                    'description': e.description
                }
                for e in events
            ])
        
        @self.app.route('/api/step', methods=['POST'])
        def step():
            """Execute one turn."""
            events = self.simulation.step()
            return jsonify({
                'success': True,
                'events': [
                    {
                        'turn': e.turn,
                        'agent': e.agent.name,
                        'action': e.action.value,
                        'target': e.target.name if e.target else None,
                        'description': e.description
                    }
                    for e in events
                ],
                'turn': self.world_state.turn_number
            })
        
        @self.app.route('/api/run', methods=['POST'])
        def run():
            """Start auto-running simulation."""
            data = request.json or {}
            max_turns = data.get('max_turns', 10)
            turn_delay = data.get('turn_delay', 0.5)
            
            if not self._auto_running:
                self._auto_running = True
                self.simulation.auto_mode = True
                self.simulation.turn_delay = turn_delay
                self._auto_run_thread = threading.Thread(
                    target=self._auto_run,
                    args=(max_turns,),
                    daemon=True
                )
                self._auto_run_thread.start()
            
            return jsonify({'success': True, 'message': 'Simulation started'})
        
        @self.app.route('/api/stop', methods=['POST'])
        def stop():
            """Stop auto-running simulation."""
            self._auto_running = False
            self.simulation.stop()
            return jsonify({'success': True, 'message': 'Simulation stopped'})
        
        @self.app.route('/api/reset', methods=['POST'])
        def reset():
            """Reset simulation (reload page to fully reset)."""
            # Note: Full reset would require recreating simulation
            # For now, just stop auto-run
            self._auto_running = False
            self.simulation.stop()
            return jsonify({'success': True, 'message': 'Simulation stopped'})
    
    def _auto_run(self, max_turns: int):
        """Auto-run simulation in background thread."""
        turns_run = 0
        while self._auto_running and turns_run < max_turns:
            if len(self.world_state.get_living_agents()) < 2:
                self._auto_running = False
                break
            self.simulation.step()
            turns_run += 1
            time.sleep(self.simulation.turn_delay)
        self._auto_running = False
    
    def _get_state_dict(self):
        """Get complete state as dictionary."""
        living = self.world_state.get_living_agents()
        return {
            'turn': self.world_state.turn_number,
            'living_count': len(living),
            'living_agents': [a.name for a in living],
            'auto_running': self._auto_running
        }
    
    def run(self, debug: bool = False):
        """Run the web server."""
        print(f"\n{'='*60}")
        print(f"  HAMLET SIMULATION - WEB INTERFACE")
        print(f"{'='*60}")
        print(f"\nStarting web server on http://localhost:{self.port}")
        print(f"Open your browser and navigate to the URL above")
        print(f"\nPress Ctrl+C to stop the server\n")
        
        self.app.run(host='0.0.0.0', port=self.port, debug=debug, use_reloader=False)

