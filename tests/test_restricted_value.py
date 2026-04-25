import pytest

from shapleypy.coalition import Coalition
from shapleypy.game import Game
from shapleypy.restricted.classes_checkers import check_accessible_union_stable
from shapleypy.restricted.classes_checkers import check_antimatroid
from shapleypy.restricted.feasible_family import FeasibleFamily
from shapleypy.restricted.game import RestrictedGame
from shapleypy.restricted.value import shapley_accessible_union_stable
from shapleypy.restricted.value import shapley_antimatroid


@pytest.fixture
def accessible_union_stable_game() -> RestrictedGame:
    n = 2
    game = Game(n)

    values = [
        ([], 0.0),
        ([0], 1.0),
        ([1], 2.0),
        ([0, 1], 100.0),
    ]

    game.set_values([(Coalition.from_players(players), value) for players, value in values])

    feasible_coalitions = [
        Coalition.from_players([]),
        Coalition.from_players([0]),
        Coalition.from_players([1]),
    ]

    feasible_family = FeasibleFamily(n, feasible_coalitions)

    return RestrictedGame(game, feasible_family)


@pytest.fixture
def antimatroid_game() -> RestrictedGame:
    n = 2
    game = Game(n)

    values = [
        ([], 0.0),
        ([0], 2.0),
        ([1], 50.0),
        ([0, 1], 10.0),
    ]

    game.set_values([(Coalition.from_players(players), value) for players, value in values])

    feasible_coalitions = [
        Coalition.from_players([]),
        Coalition.from_players([0]),
        Coalition.from_players([0, 1]),
    ]

    feasible_family = FeasibleFamily(n, feasible_coalitions)

    return RestrictedGame(game, feasible_family)


@pytest.fixture
def full_family_game() -> RestrictedGame:
    n = 2
    game = Game(n)

    values = [
        ([], 0.0),
        ([0], 1.0),
        ([1], 3.0),
        ([0, 1], 10.0),
    ]

    game.set_values([(Coalition.from_players(players), value) for players, value in values])

    feasible_coalitions = [
        Coalition.from_players([]),
        Coalition.from_players([0]),
        Coalition.from_players([1]),
        Coalition.from_players([0, 1]),
    ]

    feasible_family = FeasibleFamily(n, feasible_coalitions)

    return RestrictedGame(game, feasible_family)


def test_check_accessible_union_stable(accessible_union_stable_game: RestrictedGame) -> None:
    result = check_accessible_union_stable(accessible_union_stable_game)

    assert result is True


def test_accessible_union_stable_is_not_antimatroid(
    accessible_union_stable_game: RestrictedGame,
) -> None:
    result = check_antimatroid(accessible_union_stable_game)

    assert result is False


def test_shapley_accessible_union_stable(
    accessible_union_stable_game: RestrictedGame,
) -> None:
    result = shapley_accessible_union_stable(accessible_union_stable_game)

    assert len(result) == 2
    assert result[0] == pytest.approx(1.0)
    assert result[1] == pytest.approx(2.0)
    assert sum(result) == pytest.approx(3.0)


def test_shapley_antimatroid_raises_for_non_antimatroid(
    accessible_union_stable_game: RestrictedGame,
) -> None:
    with pytest.raises(ValueError):
        shapley_antimatroid(accessible_union_stable_game)


def test_check_antimatroid(antimatroid_game: RestrictedGame) -> None:
    result = check_antimatroid(antimatroid_game)

    assert result is True


def test_antimatroid_is_accessible_union_stable(
    antimatroid_game: RestrictedGame,
) -> None:
    result = check_accessible_union_stable(antimatroid_game)

    assert result is True


def test_shapley_antimatroid(antimatroid_game: RestrictedGame) -> None:
    result = shapley_antimatroid(antimatroid_game)

    assert len(result) == 2
    assert result[0] == pytest.approx(6.0)
    assert result[1] == pytest.approx(4.0)
    assert sum(result) == pytest.approx(10.0)


def test_full_family_antimatroid(full_family_game: RestrictedGame) -> None:
    result = shapley_antimatroid(full_family_game)

    assert len(result) == 2
    assert result[0] == pytest.approx(4.0)
    assert result[1] == pytest.approx(6.0)
    assert sum(result) == pytest.approx(10.0)


def test_full_family_accessible_union_stable(full_family_game: RestrictedGame) -> None:
    result = shapley_accessible_union_stable(full_family_game)

    assert len(result) == 2
    assert result[0] == pytest.approx(4.0)
    assert result[1] == pytest.approx(6.0)
    assert sum(result) == pytest.approx(10.0)