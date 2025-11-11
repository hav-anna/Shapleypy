from __future__ import annotations
import itertools
import math
from typing import Iterable
from shapleypy.restricted.rc_game import RestrictedGame
from shapleypy.coalition import Coalition

def shapley_feasible(rg: RestrictedGame, *, monte_carlo: int | None = None) -> list[float]:
    """
    Compute Shapley value for restricted games considering only feasible coalitions.

    Args:
        rg: The restricted game.
        monte_carlo: If provided, use Monte Carlo approximation with this many samples.
                     If None, compute exactly (only feasible for small n).

    Returns:
        List of Shapley values for each player.
    """
    n = rg.number_of_players
    players = list(range(n))
    phi = [0.0] * n

    def contribution_for_order(order: Iterable[int]):
        """Calculate contributions for a single player order."""
        prefix = Coalition.from_players([])
        for i in order:
            Si = prefix + i
            if rg.is_feasible(Si):
                phi[i] += float(rg.base_game.get_value(Si) - rg.base_game.get_value(prefix))
            prefix = Si

    if monte_carlo is None:
        # Exact computation: all n! permutations (only for small n)
        for order in itertools.permutations(players):
            contribution_for_order(order)
        denom = math.factorial(n)
    else:
        # Monte Carlo approximation: random sampling of permutations
        import random
        for _ in range(monte_carlo):
            order = players[:]
            random.shuffle(order)
            contribution_for_order(order)
        denom = float(monte_carlo)

    return [x / denom for x in phi]