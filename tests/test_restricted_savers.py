import csv
import json
import pytest
from shapleypy.coalition import Coalition
from shapleypy.game import Game
from shapleypy.restricted.feasible_family import FeasibleFamily
from shapleypy.restricted.game import RestrictedGame
from shapleypy.restricted.savers import (
    save_restricted_game_to_json,
    save_restricted_game_to_csv,
)

@pytest.fixture
def basic_restricted_game() -> RestrictedGame:
    n = 3
    game = Game(n)
    values = [
        ([], 0.0), ([0], 1.0), ([1], 2.0), ([2], 3.0),
        ([0, 1], 4.0), ([0, 2], 5.0), ([1, 2], 6.0), ([0, 1, 2], 7.0)
    ]
    game.set_values([(Coalition.from_players(p), v) for p, v in values])
    feasible_lists = [[], [0], [1], [2], [0, 1], [0, 2], [0, 1, 2]]
    ff = FeasibleFamily(n, [Coalition.from_players(p) for p in feasible_lists])
    return RestrictedGame(game, ff)


# ---------------------------------------------------------------------------
# TESTS JSON SAVER
# ---------------------------------------------------------------------------

def test_save_game_to_json(basic_restricted_game: RestrictedGame, tmpdir) -> None:
    file = tmpdir.join("test_save.json")
    save_restricted_game_to_json(basic_restricted_game, str(file))
    with open(file, "r") as f:
        data = json.load(f)

    assert data["n"] == 3
    assert [1, 2] not in data["feasible"]
    assert [0, 1] in data["feasible"]
    assert len(data["feasible"]) == 6


# ---------------------------------------------------------------------------
# TESTS CSV SAVER
# ---------------------------------------------------------------------------

def test_save_game_to_csv(basic_restricted_game: RestrictedGame, tmpdir) -> None:
    file = tmpdir.join("test_save.csv")
    save_restricted_game_to_csv(basic_restricted_game, str(file))
    with open(file, "r") as f:
        reader = csv.reader(f, delimiter=":")
        rows = list(reader)
    assert rows[0] == ["n", "3"]
    found_unfeasible = False
    for row in rows[1:]:
        if row[0] == "1,2":
            assert row[1] == "6.0"
            assert row[2] == "0" 
            found_unfeasible = True
        elif row[0] == "0,1":
            assert row[2] == "1" 
            
    assert found_unfeasible is True


def test_csv_same_separators(basic_restricted_game: RestrictedGame, tmpdir) -> None:
    file = tmpdir.join("test_fail.csv")
    with pytest.raises(ValueError):
        save_restricted_game_to_csv(
            basic_restricted_game,
            str(file),
            csv_separator=",",
            coalition_separator=","
        )