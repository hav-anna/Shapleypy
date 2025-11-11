
from __future__ import annotations
import ast
import json
from pathlib import Path
from typing import Set
from shapleypy.coalition import Coalition, EMPTY_COALITION
from shapleypy.game import Game
from shapleypy.restrected.rc_game import RestrictedGame
from shapleypy.restrected.feasible_family import FeasibleFamily


def _feasible_from_permission_data(n: int, permission: dict) -> FeasibleFamily:
    """
    Creates a feasible family (set of allowed coalitions) from a permission structure.

    Args:
        n (int): Number of players.
        permission (dict): Permission mapping of the form
            { "child": [pred1, pred2, ...], ... } (0-based indices).

    Returns:
        FeasibleFamily: The feasible family generated from the given permission structure.
    """
    preds = {int(k): set(map(int, v)) for k, v in permission.items()}
    for i in range(n):
        preds.setdefault(i, set())

    res: Set[Coalition] = set()
    order = list(range(n))  # topological order is trivial if permission is acyclic

    def dfs(idx: int, taken: set[int]):
        if idx == len(order):
            res.add(Coalition.from_players(taken))
            return
        i = order[idx]
        # Option 1: skip player i
        dfs(idx + 1, taken)
        # Option 2: include player i (only if all predecessors are already included)
        if preds[i].issubset(taken):
            taken.add(i)
            dfs(idx + 1, taken)
            taken.remove(i)

    dfs(0, set())
    res.add(EMPTY_COALITION)
    return FeasibleFamily(n, res)


def _feasible_from_list_data(n: int, feasible_list: list[list[int]]) -> FeasibleFamily:
    """
    Creates a feasible family directly from an explicit list of feasible coalitions.

    Args:
        n (int): Number of players.
        feasible_list (list[list[int]]): List of feasible coalitions, each as a list of player indices.

    Returns:
        FeasibleFamily: The feasible family created from the list.
    """
    cols = [EMPTY_COALITION] + [Coalition.from_players(lst) for lst in feasible_list]
    return FeasibleFamily(n, cols)


def load_restricted_game(file: str | Path) -> RestrictedGame:
    """
    Loads a restricted game (Game + FeasibleFamily) from a JSON file.

    The JSON must contain the base game and either a permission structure or a list
    of feasible coalitions. Example structure:

    {
      "n": 3,
      "values": {
        "[]": 0.0,
        "[0]": 1.0,
        "[1]": 1.0,
        "[2]": 0.5,
        "[0,1]": 3.0,
        "[0,2]": 1.2,
        "[1,2]": 1.1,
        "[0,1,2]": 4.0
      },
      "permission": {
        "1": [0],
        "2": [0]
      }
      // or alternatively:
      // "feasible": [ [], [0], [0,1], [0,2], [0,1,2] ]
    }

    If both "permission" and "feasible" are present, the permission structure is preferred.

    Args:
        file (str | Path): Path to the JSON file.

    Returns:
        RestrictedGame: The loaded restricted game.
    """
    p = Path(file)
    data = json.loads(p.read_text(encoding="utf-8"))

    if "n" not in data:
        raise ValueError("Missing 'n' in JSON.")
    n = int(data["n"])

    values_pairs: list[tuple[list[int], float]] = []
    vals = data.get("values", {})
    for k, v in vals.items():
        players = ast.literal_eval(k)  
        values_pairs.append((players, float(v)))

    game = Game(n)
    game.set_values(values_pairs)

    if "permission" in data:
        feasible = _feasible_from_permission_data(n, data["permission"])
    elif "feasible" in data:
        feasible = _feasible_from_list_data(n, data["feasible"])
    else:
        all_cols = list(Coalition.all_coalitions(n))
        feasible = FeasibleFamily(n, all_cols)

    if feasible.n != game.number_of_players:
        raise ValueError("Mismatch between 'n' and feasible family size.")

    return RestrictedGame(game, feasible)
