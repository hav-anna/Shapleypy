from __future__ import annotations
import ast
import json
from pathlib import Path
from shapleypy.coalition import Coalition, EMPTY_COALITION
from shapleypy.game import Game
from shapleypy.restrected.feasible_family import FeasibleFamily

def _feasible_from_list_data(n: int, feasible_list: list[list[int]]) -> FeasibleFamily:
    """
    Creates a feasible family from explicit list of coalitions.
    
    Args:
        n: Number of players
        feasible_list: List of feasible coalitions as player indices
        
    Returns:
        FeasibleFamily: The created feasible family
    """
    cols = [EMPTY_COALITION] + [Coalition.from_players(lst) for lst in feasible_list]
    return FeasibleFamily(n, cols)

def load_restricted_game(file: str | Path):
    """
    Loads a restricted game from JSON file.
    
    Now supports:
    {
      "n": 3,
      "values": {...},
      "feasible": [[], [0], [0,1], [0,2], [0,1,2]]
    }
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
        players = ast.literal_eval(k)
        values_pairs.append((players, float(v)))
    
    game = Game(n)
    game.set_values(values_pairs)
    
    # Load feasible family if provided
    if "feasible" in data:
        feasible = _feasible_from_list_data(n, data["feasible"])
        # TODO: Return RestrictedGame once we implement permission structure
        return game, feasible
    
    return game