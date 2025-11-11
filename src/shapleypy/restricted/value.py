from __future__ import annotations
import itertools
import math
from shapleypy.restricted.rc_game import RestrictedGame
from shapleypy.coalition import Coalition

def shapley_feasible(rg: RestrictedGame) -> list[float]:
    """
    Compute Shapley value for restricted games considering only feasible coalitions.
    """
    n = rg.number_of_players
    players = list(range(n))
    phi = [0.0] * n
    
    # Process all permutations for exact computation
    for order in itertools.permutations(players):
        prefix = Coalition.from_players([])
        for i in order:
            # Create new coalition by adding current player
            new_coalition = prefix + i
            
            # Only consider marginal contribution if new coalition is feasible
            if rg.is_feasible(new_coalition):
                marginal_contrib = rg.base_game.get_value(new_coalition) - rg.base_game.get_value(prefix)
                phi[i] += float(marginal_contrib)
            
            prefix = new_coalition
    
    # Normalize by number of permutations
    denom = math.factorial(n)
    return [x / denom for x in phi]