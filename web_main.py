"""Web server entry point for Hamlet simulation game."""

import sys
from hamlet_sim.main import main

if __name__ == "__main__":
    port = 8001
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port: {sys.argv[1]}. Using default port 8001.")
    
    main(web_mode=True, port=port)

