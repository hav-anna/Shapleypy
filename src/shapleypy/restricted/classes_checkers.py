# ruff: noqa: N806
from __future__ import annotations

from shapleypy.coalition import Coalition
from shapleypy.restricted.game import RestrictedGame
from shapleypy.coalition import EMPTY_COALITION


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
    for coalition in restricted_game.feasible:
        value_S = base_game.get_value(coalition)
        for subcoalition in coalition.all_subcoalitions():
            if subcoalition != coalition and restricted_game.is_feasible(subcoalition):
                if value_S < base_game.get_value(subcoalition):
                    return False
    return True

def check_superadditivity_restricted(restricted_game: RestrictedGame) -> bool:
    """
    Check if the restricted game is superadditive on the feasible family F.

    For all disjoint S, T in F such that S union T in F, 
    we require v(S union T) >= v(S) + v(T).

    Args:
        restricted_game (RestrictedGame): The restricted game to check.

    Returns:
        bool: True if the restricted game is superadditive, False otherwise.
    """
    base_game = restricted_game.base_game
    feasible_coalitions = list(restricted_game.feasible)

    for i, S in enumerate(feasible_coalitions):
        for T in feasible_coalitions[i+1:]:
            players_S = set(S.get_players)
            players_T = set(T.get_players)
            
            if not players_S.intersection(players_T):
                union_ST = S + T
                if restricted_game.is_feasible(union_ST):
                    val_S = base_game.get_value(S)
                    val_T = base_game.get_value(T)
                    val_union = base_game.get_value(union_ST)
                    
                    if val_union < (val_S + val_T):
                        return False
    return True


def check_convexity_restricted(restricted_game: RestrictedGame) -> bool:
    """
    Check if the restricted game is convex on the feasible family F.

    For all S, T in F such that S ∪ T in F and S ∩ T in F,
    we require v(S union T) + v(S intersect T) >= v(S) + v(T).

    Args:
        restricted_game (RestrictedGame): The restricted game to check.

    Returns:
        bool: True if the restricted game is convex, False otherwise.
    """
    base_game = restricted_game.base_game
    feasible_coalitions = list(restricted_game.feasible)

    for i, S in enumerate(feasible_coalitions):
        for T in feasible_coalitions[i+1:]:
            union_ST = S + T
            intersection_players = set(S.get_players).intersection(set(T.get_players))
            if intersection_players:
                intersection_ST = Coalition.from_players(list(intersection_players))
            else:
                intersection_ST = EMPTY_COALITION
            if restricted_game.is_feasible(union_ST) and restricted_game.is_feasible(intersection_ST):
                val_S = base_game.get_value(S)
                val_T = base_game.get_value(T)
                val_union = base_game.get_value(union_ST)
                val_intersection = base_game.get_value(intersection_ST)
                
                if (val_union + val_intersection) < (val_S + val_T):
                    return False
    return True


def check_antimatroid(restricted_game: RestrictedGame) -> bool:
     """
    Check if the feasible family is an antimatroid.

    The feasible family must contain the empty coalition, satisfy accessibility
    and be closed under union.

    Args:
        restricted_game: The restricted game to check.

    Returns:
        True if the feasible family is an antimatroid, False otherwise.
    """
    feasible_coalitions = list(restricted_game.feasible)

    if EMPTY_COALITION not in feasible_coalitions:
        return False

    for coalition in feasible_coalitions:
        if coalition != EMPTY_COALITION:
            has_extreme_player = False

            for player in coalition.get_players:
                smaller_coalition = coalition - player

                if smaller_coalition in feasible_coalitions:
                    has_extreme_player = True
                    break

            if has_extreme_player is False:
                return False

    for S in feasible_coalitions:
        for T in feasible_coalitions:
            union_ST = S + T

            if union_ST not in feasible_coalitions:
                return False

    return True


def check_accessible_union_stable(restricted_game: RestrictedGame) -> bool:
    """
    Check if the feasible family is accessible union stable.

    The feasible family must contain the empty coalition, satisfy accessibility
    and satisfy union stability for coalitions with non-empty intersection.

    Args:
        restricted_game: The restricted game to check.

    Returns:
        True if the feasible family is accessible union stable, False otherwise.
    """
    feasible_coalitions = list(restricted_game.feasible)

    if EMPTY_COALITION not in feasible_coalitions:
        return False

    for coalition in feasible_coalitions:
        if coalition != EMPTY_COALITION:
            has_extreme_player = False

            for player in coalition.get_players:
                smaller_coalition = coalition - player

                if smaller_coalition in feasible_coalitions:
                    has_extreme_player = True
                    break

            if has_extreme_player is False:
                return False

    for S in feasible_coalitions:
        for T in feasible_coalitions:
            intersection_ST = S * T

            if intersection_ST != EMPTY_COALITION:
                union_ST = S + T

                if union_ST not in feasible_coalitions:
                    return False

    return True
