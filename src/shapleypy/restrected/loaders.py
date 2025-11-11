from __future__ import annotations
import ast
import json
from pathlib import Path
from shapleypy.game import Game

def load_restricted_game(file: str | Path):
    """
    Loads a restricted game from JSON file.
    """
    p = Path(file)
    data = json.loads(p.read_text(encoding="utf-8"))
    
    if "n" not in data:
        raise ValueError("Missing 'n' in JSON.")
    n = int(data["n"])
    
    # Load game values
    values_pairs = []
    vals = data.get("values", {})
    for k, v in vals.items():
        players = ast.literal_eval(k)  # Parse coalition strings like "[0,1]"
        values_pairs.append((players, float(v)))
    
    game = Game(n)
    game.set_values(values_pairs)
    
    # TODO: Add feasible family support
    return game