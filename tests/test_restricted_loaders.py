import json
import pytest

from shapleypy.coalition import Coalition
from shapleypy.game import Game
from shapleypy.restricted.feasible_family import FeasibleFamily
from shapleypy.restricted.rc_game import RestrictedGame
from shapleypy.restricted.loaders import load_restricted_game_from_json, load_restricted_game_from_csv


@pytest.fixture
def perfect_restricted_game() -> RestrictedGame:
    n = 3
    game = Game(n)
    
    values = [
        ([], 0.0), ([0], 1.0), ([1], 2.0), ([2], 3.0),
        ([0, 1], 4.0), ([0, 2], 5.0), ([1, 2], 6.0), ([0, 1, 2], 7.0)
    ]
    coalition_values = [(Coalition.from_players(p), v) for p, v in values]
    game.set_values(coalition_values)
    feasible_lists = [[], [0], [1], [2], [0, 1], [0, 2], [0, 1, 2]]
    ff = FeasibleFamily(n, [Coalition.from_players(p) for p in feasible_lists])
    return RestrictedGame(game, ff)


# ---------------------------------------------------------------------------
# JSON LOADERS
# ---------------------------------------------------------------------------

def test_json_input(perfect_restricted_game: RestrictedGame, tmpdir) -> None:
    json_data = {
        "n": 3,
        "values": {
            "[]": 0.0, "[0]": 1.0, "[1]": 2.0, "[2]": 3.0,
            "[0, 1]": 4.0, "[0, 2]": 5.0, "[1, 2]": 6.0, "[0, 1, 2]": 7.0
        },
        "feasible": [[], [0], [1], [2], [0, 1], [0, 2], [0, 1, 2]]
    }
    
    file = tmpdir.join("test_game.json")
    with open(file, "w") as f:
        json.dump(json_data, f)
        
    loaded_rg = load_restricted_game_from_json(str(file))
    
    assert loaded_rg.number_of_players == 3
    assert loaded_rg.base_game.get_value(Coalition.from_players([0, 1, 2])) == 7.0
    
    assert loaded_rg.is_feasible(Coalition.from_players([0, 1])) is True
    assert loaded_rg.is_feasible(Coalition.from_players([1, 2])) is False


def test_json_missing_feasible(tmpdir) -> None:
    json_data = {
        "n": 3,
        "values": {"[0]": 1.0}
    }
    file = tmpdir.join("fallback.json")
    with open(file, "w") as f:
        json.dump(json_data, f)
        
    loaded_rg = load_restricted_game_from_json(str(file))
    assert loaded_rg.number_of_players == 3
    assert len(list(loaded_rg.feasible)) == 8

# ---------------------------------------------------------------------------
# CSV LOADERS
# ---------------------------------------------------------------------------

def test_csv_input(perfect_restricted_game: RestrictedGame, tmpdir) -> None:
    csv_content = """n:3
:0.0:1
0:1.0:1
1:2.0:1
0,1:4.0:1
2:3.0:1
0,2:5.0:1
1,2:6.0:0
0,1,2:7.0:1"""

    file = tmpdir.join("test_game.csv")
    with open(file, "w") as f:
        f.write(csv_content)
        
    loaded_rg = load_restricted_game_from_csv(str(file))
    
    assert loaded_rg.number_of_players == 3
    assert loaded_rg.base_game.get_value(Coalition.from_players([1, 2])) == 6.0
    assert loaded_rg.is_feasible(Coalition.from_players([0, 1])) is True
    assert loaded_rg.is_feasible(Coalition.from_players([1, 2])) is False


def test_csv_same_separators() -> None:
    with pytest.raises(ValueError):
        load_restricted_game_from_csv(
            "dummy_path.csv",
            csv_separator=",",
            coalition_separator=",",
        )