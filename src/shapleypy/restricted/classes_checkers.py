# ruff: noqa: N806
from __future__ import annotations

from shapleypy.coalition import Coalition
from shapleypy.restricted.rc_game import RestrictedGame


def check_monotonicity_restricted(restricted_game: RestrictedGame) -> bool:
    """
    Check if the restricted game is monotone on the feasible family F.

    For all S, T in F with T ⊂ S we require v(S) ≥ v(T).

    Args:
        restricted_game (RestrictedGame): The restricted game to check.

    Returns:
        bool: True if the restricted game is monotone, False otherwise.
    """
    base_game = restricted_game.base_game
    for coalition in restricted_game.coalitions():
        value_S = base_game.get_value(coalition)
        for subcoalition in coalition.all_subcoalitions():
            if subcoalition != coalition and restricted_game.is_feasible(subcoalition):
                if value_S < base_game.get_value(subcoalition):
                    return False
    return True