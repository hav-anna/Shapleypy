import pytest

from shapleypy.coalition import Coalition
from shapleypy.game import Game
from shapleypy.restricted.feasible_family import FeasibleFamily
from shapleypy.restricted.game import RestrictedGame
from shapleypy.restricted.value import shapley_feasible

@pytest.fixture
def dummy_restricted_game() -> RestrictedGame:
    n = 3
    game = Game(n)
    values = [
        ([], 0.0), ([0], 1.0), ([1], 1.0), ([2], 1.0),
        ([0, 1], 2.0), ([0, 2], 2.0), ([1, 2], 2.0),
        ([0, 1, 2], 3.0)
    ]
    game.set_values([(Coalition.from_players(p), v) for p, v in values])
    all_coalitions = [Coalition.from_players(p) for p, _ in values]
    ff = FeasibleFamily(n, all_coalitions)
    return RestrictedGame(game, ff)


def test_shapley_feasible_exact(dummy_restricted_game: RestrictedGame) -> None:
    result = shapley_feasible(dummy_restricted_game, monte_carlo=None)

    assert len(result) == 3
    assert result[0] == pytest.approx(1.0)
    assert result[1] == pytest.approx(1.0)
    assert result[2] == pytest.approx(1.0)
    assert sum(result) == pytest.approx(3.0)


def test_shapley_feasible_monte_carlo(dummy_restricted_game: RestrictedGame) -> None:
    result = shapley_feasible(dummy_restricted_game, monte_carlo=10)
    
    assert len(result) == 3
    assert sum(result) == pytest.approx(3.0)