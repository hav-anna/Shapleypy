from __future__ import annotations
import itertools
import math
import random
from shapleypy.restricted.game import RestrictedGame
from shapleypy.coalition import Coalition

def shapley_feasible(rg: RestrictedGame, *, monte_carlo: int | None = None) -> list[float]:
    """
    Compute Shapley value for restricted games.
    
    Args:
        rg: Restricted game instance
        monte_carlo: If provided, use Monte Carlo approximation with given number of samples
                    If None, compute exact value (only feasible for small n)
                    
    Returns:
        List of Shapley values for each player
    """
    n = rg.number_of_players
    players = list(range(n))
    phi = [0.0] * n
    
    if monte_carlo is None:
        # Exact computation - all permutations
        for order in itertools.permutations(players):
            prefix = Coalition.from_players([])
            for i in order:
                new_coalition = prefix + i
                if rg.is_feasible(new_coalition):
                    marginal_contrib = rg.base_game.get_value(new_coalition) - rg.base_game.get_value(prefix)
                    phi[i] += float(marginal_contrib)
                prefix = new_coalition
        denom = math.factorial(n)
    else:
        # Monte Carlo approximation - random permutations
        for _ in range(monte_carlo):
            order = players[:]  # Copy list
            random.shuffle(order)  # Random permutation
            
            prefix = Coalition.from_players([])
            for i in order:
                new_coalition = prefix + i
                if rg.is_feasible(new_coalition):
                    marginal_contrib = rg.base_game.get_value(new_coalition) - rg.base_game.get_value(prefix)
                    phi[i] += float(marginal_contrib)
                prefix = new_coalition
        denom = float(monte_carlo)
    
    return [x / denom for x in phi]