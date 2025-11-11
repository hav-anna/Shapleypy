from __future__ import annotations
import json
from pathlib import Path
from shapleypy.game import Game

def load_restricted_game(file: str | Path):
    """
    Loads a restricted game from JSON file.
    
    Basic structure:
    {
      "n": 3,
      "values": {
        "[]": 0.0, "[0]": 1.0, "[1]": 1.0, "[2]": 0.5,
        "[0,1]": 3.0, "[0,2]": 1.2, "[1,2]": 1.1, "[0,1,2]": 4.0
      }
    }
    """
    p = Path(file)
    data = json.loads(p.read_text(encoding="utf-8"))
    
    if "n" not in data:
        raise ValueError("Missing 'n' in JSON.")
    n = int(data["n"])
    
    # TODO: Load game values
    game = Game(n)
    
    # TODO: Add feasible family support
    return game