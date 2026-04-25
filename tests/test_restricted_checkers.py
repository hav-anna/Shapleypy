import pytest

from shapleypy.coalition import Coalition
from shapleypy.game import Game
from shapleypy.restricted.classes_checkers import (
    check_accessible_union_stable,
    check_antimatroid,
    check_convexity_restricted,
    check_monotonicity_restricted,
    check_superadditivity_restricted,
)
from shapleypy.restricted.feasible_family import FeasibleFamily
from shapleypy.restricted.game import RestrictedGame


def make_restricted_game(
    n: int,
    values: list[tuple[list[int], float]],
    feasible_players: list[list[int]],
) -> RestrictedGame:
    game = Game(n)

    coalition_values = []
    for players, value in values:
        coalition = Coalition.from_players(players)
        coalition_values.append((coalition, value))

    game.set_values(coalition_values)

    feasible_coalitions = []
    for players in feasible_players:
        coalition = Coalition.from_players(players)
        feasible_coalitions.append(coalition)

    feasible_family = FeasibleFamily(n, feasible_coalitions)

    return RestrictedGame(game, feasible_family)


@pytest.fixture
def perfect_restricted_game() -> RestrictedGame:
    n = 3

    values = [
        ([], 0.0),
        ([0], 1.0),
        ([1], 1.0),
        ([2], 1.0),
        ([0, 1], 3.0),
        ([0, 2], 3.0),
        ([1, 2], 3.0),
        ([0, 1, 2], 6.0),
    ]

    feasible_players = [
        [],
        [0],
        [1],
        [2],
        [0, 1],
        [0, 2],
        [1, 2],
        [0, 1, 2],
    ]

    return make_restricted_game(n, values, feasible_players)


@pytest.fixture
def antimatroid_restricted_game() -> RestrictedGame:
    n = 2

    values = [
        ([], 0.0),
        ([0], 2.0),
        ([1], 5.0),
        ([0, 1], 10.0),
    ]

    feasible_players = [
        [],
        [0],
        [0, 1],
    ]

    return make_restricted_game(n, values, feasible_players)


@pytest.fixture
def accessible_union_stable_restricted_game() -> RestrictedGame:
    n = 2

    values = [
        ([], 0.0),
        ([0], 1.0),
        ([1], 2.0),
        ([0, 1], 10.0),
    ]

    feasible_players = [
        [],
        [0],
        [1],
    ]

    return make_restricted_game(n, values, feasible_players)


@pytest.fixture
def not_accessible_restricted_game() -> RestrictedGame:
    n = 2

    values = [
        ([], 0.0),
        ([0], 1.0),
        ([1], 2.0),
        ([0, 1], 10.0),
    ]

    feasible_players = [
        [],
        [0, 1],
    ]

    return make_restricted_game(n, values, feasible_players)


@pytest.fixture
def not_union_stable_restricted_game() -> RestrictedGame:
    n = 3

    values = [
        ([], 0.0),
        ([0], 1.0),
        ([1], 1.0),
        ([2], 1.0),
        ([0, 1], 2.0),
        ([0, 2], 2.0),
        ([1, 2], 2.0),
        ([0, 1, 2], 3.0),
    ]

    feasible_players = [
        [],
        [0],
        [1],
        [0, 1],
        [1, 2],
    ]

    return make_restricted_game(n, values, feasible_players)


def test_check_monotonicity_restricted(
    perfect_restricted_game: RestrictedGame,
) -> None:
    rg = perfect_restricted_game

    assert check_monotonicity_restricted(rg) is True

    rg.base_game.set_value(Coalition.from_players([0, 1]), 0.5)

    assert check_monotonicity_restricted(rg) is False


def test_check_superadditivity_restricted(
    perfect_restricted_game: RestrictedGame,
) -> None:
    rg = perfect_restricted_game

    assert check_superadditivity_restricted(rg) is True

    rg.base_game.set_value(Coalition.from_players([0, 1]), 1.5)

    assert check_superadditivity_restricted(rg) is False


def test_check_convexity_restricted(
    perfect_restricted_game: RestrictedGame,
) -> None:
    rg = perfect_restricted_game

    assert check_convexity_restricted(rg) is True

    rg.base_game.set_value(Coalition.from_players([0, 1, 2]), 4.0)

    assert check_convexity_restricted(rg) is False


def test_check_antimatroid_returns_true(
    antimatroid_restricted_game: RestrictedGame,
) -> None:
    rg = antimatroid_restricted_game

    assert check_antimatroid(rg) is True


def test_antimatroid_is_accessible_union_stable(
    antimatroid_restricted_game: RestrictedGame,
) -> None:
    rg = antimatroid_restricted_game

    assert check_accessible_union_stable(rg) is True


def test_check_accessible_union_stable_returns_true(
    accessible_union_stable_restricted_game: RestrictedGame,
) -> None:
    rg = accessible_union_stable_restricted_game

    assert check_accessible_union_stable(rg) is True


def test_accessible_union_stable_does_not_have_to_be_antimatroid(
    accessible_union_stable_restricted_game: RestrictedGame,
) -> None:
    rg = accessible_union_stable_restricted_game

    assert check_antimatroid(rg) is False


def test_not_accessible_is_not_antimatroid(
    not_accessible_restricted_game: RestrictedGame,
) -> None:
    rg = not_accessible_restricted_game

    assert check_antimatroid(rg) is False


def test_not_accessible_is_not_accessible_union_stable(
    not_accessible_restricted_game: RestrictedGame,
) -> None:
    rg = not_accessible_restricted_game

    assert check_accessible_union_stable(rg) is False


def test_not_union_stable_is_not_accessible_union_stable(
    not_union_stable_restricted_game: RestrictedGame,
) -> None:
    rg = not_union_stable_restricted_game

    assert check_accessible_union_stable(rg) is False