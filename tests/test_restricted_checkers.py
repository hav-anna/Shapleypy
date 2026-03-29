import pytest

from shapleypy.coalition import Coalition
from shapleypy.game import Game
from shapleypy.restricted.feasible_family import FeasibleFamily
from shapleypy.restricted.rc_game import RestrictedGame
from shapleypy.restricted.classes_checkers import (
    check_monotonicity_restricted,
    check_superadditivity_restricted,
    check_convexity_restricted,
)

@pytest.fixture
def perfect_restricted_game() -> RestrictedGame:
    n = 3
    game = Game(n)
    values = [
        ([], 0.0), 
        ([0], 1.0), ([1], 1.0), ([2], 1.0),
        ([0, 1], 3.0), ([0, 2], 3.0), ([1, 2], 3.0),
        ([0, 1, 2], 6.0)
    ]
    coalition_values = [(Coalition.from_players(p), v) for p, v in values]
    game.set_values(coalition_values)
    
    ff = FeasibleFamily(n, [c for c, _ in coalition_values])
    return RestrictedGame(game, ff)


def test_check_monotonicity_restricted(perfect_restricted_game: RestrictedGame) -> None:
    rg = perfect_restricted_game
    assert check_monotonicity_restricted(rg) is True
    rg.base_game.set_value(Coalition.from_players([0, 1]), 0.5)
    assert check_monotonicity_restricted(rg) is False


def test_check_superadditivity_restricted(perfect_restricted_game: RestrictedGame) -> None:
    rg = perfect_restricted_game
    assert check_superadditivity_restricted(rg) is True
    rg.base_game.set_value(Coalition.from_players([0, 1]), 1.5)
    assert check_superadditivity_restricted(rg) is False


def test_check_convexity_restricted(perfect_restricted_game: RestrictedGame) -> None:
    rg = perfect_restricted_game
    assert check_convexity_restricted(rg) is True
    
    rg.base_game.set_value(Coalition.from_players([0, 1, 2]), 4.0)
    assert check_convexity_restricted(rg) is False