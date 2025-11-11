from __future__ import annotations
import itertools
import math
import random
from typing import Iterable
from shapleypy.restricted.rc_game import RestrictedGame
from shapleypy.coalition import Coalition

def shapley_feasible(rg: RestrictedGame, *, monte_carlo: int | None = None) -> list[float]:
    """
    Compute Shapley value for restricted games considering only feasible coalitions.
    
    The algorithm follows the standard Shapley value computation but only considers
    marginal contributions when the resulting coalition is feasible.
    
    Examples:
        >>> game = load_restricted_game("game.json")
        >>> # Exact computation for small games
        >>> values = shapley_feasible(game)
        >>> # Monte Carlo approximation for large games
        >>> values_approx = shapley_feasible(game, monte_carlo=10000)
    """
    n = rg.number_of_players
    players = list(range(n))
    phi = [0.0] * n

    def process_single_permutation(order: Iterable[int]) -> None:
        """
        Process a single permutation and accumulate marginal contributions.
        
        Args:
            order: Order of players to process
        """
        prefix = Coalition.from_players([])
        for player in order:
            new_coalition = prefix + player
            # Only add marginal contribution if the new coalition is feasible
            if rg.is_feasible(new_coalition):
                marginal_contrib = (rg.base_game.get_value(new_coalition) - 
                                  rg.base_game.get_value(prefix))
                phi[player] += float(marginal_contrib)
            prefix = new_coalition

    if monte_carlo is None:
        # Exact computation using all permutations
        for permutation in itertools.permutations(players):
            process_single_permutation(permutation)
        denom = math.factorial(n)
    else:
        # Monte Carlo approximation using random permutations
        for _ in range(monte_carlo):
            random_order = players[:]
            random.shuffle(random_order)
            process_single_permutation(random_order)
        denom = float(monte_carlo)

    return [value / denom for value in phi]