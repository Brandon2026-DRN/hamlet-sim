# Hamlet Simulation Game

A multi-agent simulation game based on Shakespeare's Hamlet, where characters act autonomously based on their personalities.

## Setup

### Install Dependencies

```bash
# Option 1: Install with --user flag (recommended)
pip3 install --user Flask

# Option 2: Use a virtual environment (best practice)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install Flask
```

## Running the Web Interface

To run the web-based interface on port 8001:

```bash
python3 web_main.py
```

Or specify a different port:

```bash
python3 web_main.py 8080
```

Then open your browser and navigate to:
- **http://localhost:8001** (or your specified port)

## Running the CLI Interface

To run the command-line interface:

```bash
python3 main.py
```
## Or use the Render application!

https://hamlet-sim.onrender.com/

## Features

- **Real-time simulation**: Watch characters interact based on their personalities
- **Interactive controls**: Step through turns manually or run automatically
- **Visual dashboard**: See agents, relationships, alliances, and conflicts
- **Event log**: Track all actions in real-time
- **Relationship tracking**: Monitor trust, suspicion, love, and fear between characters

## Characters

- **Hamlet**: Seeks truth, low trust, high introspection
- **Claudius**: Seeks power, high paranoia
- **Gertrude**: Seeks stability, mediates others
- **Ophelia**: Avoids conflict, loyalty weighted
- **Laertes**: Revenge-seeking, protective of Ophelia
- **Polonius**: Spies often
- **Horatio**: High loyalty, rarely betrays

Enjoy watching the drama unfold!

