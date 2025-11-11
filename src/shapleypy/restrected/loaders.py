from __future__ import annotations
import ast
import json
from pathlib import Path

from shapleypy.coalition import Coalition, EMPTY_COALITION
from shapleypy.game import Game
from shapleypy.restrected.feasible_family import FeasibleFamily

def _feasible_from_permission_data(n: int, permission: dict) -> FeasibleFamily:
    """
    Creates feasible family from permission structure using DFS.

    """
    preds = {int(k): set(map(int, v)) for k, v in permission.items()}
    for i in range(n):
        preds.setdefault(i, set())

    res = set()
    order = list(range(n))

    def dfs(idx: int, taken: set[int]):
        if idx == len(order):
            res.add(Coalition.from_players(taken))
            return
        i = order[idx]
        # Option 1: skip player i
        dfs(idx + 1, taken)
        # Option 2: include player i only if predecessors are included
        if preds[i].issubset(taken):
            taken.add(i)
            dfs(idx + 1, taken)
            taken.remove(i)

    dfs(0, set())
    res.add(EMPTY_COALITION)
    return FeasibleFamily(n, res)

def _feasible_from_list_data(n: int, feasible_list: list[list[int]]) -> FeasibleFamily:
    """Creates feasible family from explicit list of coalitions."""
    cols = [EMPTY_COALITION] + [Coalition.from_players(lst) for lst in feasible_list]
    return FeasibleFamily(n, cols)

def load_restricted_game(file: str | Path):
    """
    Loads a restricted game from JSON file.
    
    Now supports permission structures:
    {
      "n": 3,
      "values": {...},
      "permission": {"1": [0], "2": [0]}
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
    
    # Load feasible family
    if "permission" in data:
        feasible = _feasible_from_permission_data(n, data["permission"])
    elif "feasible" in data:
        feasible = _feasible_from_list_data(n, data["feasible"])
    else:
        # Default to all coalitions
        all_cols = list(Coalition.all_coalitions(n))
        feasible = FeasibleFamily(n, all_cols)
    
    return game, feasible