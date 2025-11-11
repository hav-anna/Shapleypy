from __future__ import annotations
import itertools
import math
from shapleypy.restricted.rc_game import RestrictedGame

def shapley_feasible(rg: RestrictedGame) -> list[float]:
    """
    Compute Shapley value for restricted games considering only feasible coalitions.
    
    Args:
        rg: Restricted game instance
        
    Returns:
        List of Shapley values for each player
    """
    n = rg.number_of_players
    players = list(range(n))
    phi = [0.0] * n
    
    # TODO: Implement permutation processing
    # TODO: Handle feasible coalitions
    
    return phi