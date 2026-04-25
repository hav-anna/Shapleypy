from __future__ import annotations 
import itertools 
import math
from typing import Iterable
from shapleypy.restricted.game import RestrictedGame
from shapleypy.coalition import Coalition
from shapleypy.coalition import EMPTY_COALITION
from shapleypy.restricted.classes_checkers import check_antimatroid
from shapleypy.restricted.classes_checkers import check_accessible_union_stable
from shapleypy.game import Game
from shapleypy.solution_concept.shapley_value import shapley


def _all_coalitions(number_of_players: int) -> list[Coalition]:
    """
    Generate all coalitions for the given number of players.

    Args:
        number_of_players: Number of players in the game.

    Returns:
        List of all coalitions.
    """
    coalitions = []
    number_of_coalitions = 2 ** number_of_players

    for coalition_id in range(number_of_coalitions):
        coalition = Coalition(coalition_id)
        coalitions.append(coalition)

    return coalitions

def _restricted_game_from_value_function(
    rg: RestrictedGame,
    value_function,
) -> Game:
    """
    Create a game from a restricted value function.

    Args:
        rg: The restricted game.
        value_function: Function assigning a value to each coalition.

    Returns:
        Game with values of the restricted game.
    """
    game = Game(rg.number_of_players)
    all_coalitions = _all_coalitions(rg.number_of_players)

    for coalition in all_coalitions:
        value = float(value_function(coalition))
        game.set_value(coalition, value)

    return game


def _shapley_from_restricted_value(
    rg: RestrictedGame,
    value_function,
) -> list[float]:
    """
    Compute the Shapley value of a restricted game.

    Args:
        rg: The restricted game.
        value_function: Function assigning a value to each coalition.

    Returns:
        List of Shapley values for all players.
    """
    restricted_game = _restricted_game_from_value_function(rg, value_function)
    values = shapley(restricted_game)

    return list(values)


def _interior_antimatroid(
    rg: RestrictedGame,
    coalition: Coalition,
) -> Coalition:
    """
    Find the interior of a coalition in an antimatroid.

    Args:
        rg: The restricted game.
        coalition: Coalition whose interior is needed.

    Returns:
        The largest feasible subset of the coalition.
    """
    interior = EMPTY_COALITION

    for feasible_coalition in rg.feasible:
        if feasible_coalition in coalition:
            interior = interior + feasible_coalition

    return interior


def shapley_antimatroid(rg: RestrictedGame) -> list[float]:
    """
    Compute the restricted Shapley value for an antimatroid.

    Args:
        rg: The restricted game.

    Returns:
        List of Shapley values for all players.
    """
    if check_antimatroid(rg) is False:
        raise ValueError("The feasible family is not an antimatroid.")

    def restricted_value(coalition: Coalition) -> float:
        interior = _interior_antimatroid(rg, coalition)
        value = rg.base_game.get_value(interior)

        return float(value)

    return _shapley_from_restricted_value(rg, restricted_value)


def _components_accessible_union_stable(
    rg: RestrictedGame,
    coalition: Coalition,
) -> list[Coalition]:
    """
    Find the components of a coalition.

    Args:
        rg: The restricted game.
        coalition: Coalition whose components are needed.

    Returns:
        Maximal non-empty feasible subsets of the coalition.
    """
    feasible_subcoalitions = []

    for feasible_coalition in rg.feasible:
        if feasible_coalition != EMPTY_COALITION:
            if feasible_coalition in coalition:
                feasible_subcoalitions.append(feasible_coalition)

    components = []

    for candidate in feasible_subcoalitions:
        is_maximal = True

        for other_coalition in feasible_subcoalitions:
            if candidate != other_coalition:
                if candidate in other_coalition:
                    is_maximal = False
                    break

        if is_maximal is True:
            components.append(candidate)

    return components


def shapley_accessible_union_stable(rg: RestrictedGame) -> list[float]:
    """
    Compute the restricted Shapley value for an accessible union stable family.

    Args:
        rg: The restricted game.

    Returns:
        List of Shapley values for all players.
    """
    if check_accessible_union_stable(rg) is False:
        raise ValueError("The feasible family is not accessible union stable.")

    def restricted_value(coalition: Coalition) -> float:
        components = _components_accessible_union_stable(rg, coalition)
        value = 0.0

        for component in components:
            value += float(rg.base_game.get_value(component))

        return value

    return _shapley_from_restricted_value(rg, restricted_value)