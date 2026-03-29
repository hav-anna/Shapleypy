import pytest

from shapleypy.coalition import Coalition
from shapleypy.game import Game
from shapleypy.restricted.feasible_family import FeasibleFamily
from shapleypy.restricted.game
import RestrictedGame


def test_feasible_family_basic() -> None:
    n = 3
    allowed = [Coalition.from_players([]), Coalition.from_players([0])]
    ff = FeasibleFamily(n, allowed)
    assert ff.n == 3


def test_restricted_game_initialization() -> None:
    n = 3
    game = Game(n)
    game.set_values([
        (Coalition.from_players([]), 0.0),
        (Coalition.from_players([0]), 5.0)
    ])
    
    ff = FeasibleFamily(n, [Coalition.from_players([]), Coalition.from_players([0])])
    rg = RestrictedGame(game, ff)
    assert rg.number_of_players == n
    assert rg.base_game == game
    assert rg.base_game.get_value(Coalition.from_players([0])) == 5.0


def test_restricted_game_is_feasible() -> None:
    n = 3
    game = Game(n)
    allowed_lists = [[], [1], [1, 2]]
    allowed_coalitions = [Coalition.from_players(p) for p in allowed_lists]
    
    ff = FeasibleFamily(n, allowed_coalitions)
    rg = RestrictedGame(game, ff)
    assert rg.is_feasible(Coalition.from_players([])) is True
    assert rg.is_feasible(Coalition.from_players([1])) is True
    assert rg.is_feasible(Coalition.from_players([1, 2])) is True
    assert rg.is_feasible(Coalition.from_players([0])) is False
    assert rg.is_feasible(Coalition.from_players([0, 1, 2])) is False


def test_grand_coalition() -> None:
    n = 4
    game = Game(n)
    ff = FeasibleFamily(n, [])
    rg = RestrictedGame(game, ff)
    
    gc = rg.grand_coalition()
    assert set(gc.get_players) == {0, 1, 2, 3}