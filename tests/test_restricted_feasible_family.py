import pytest

from shapleypy.coalition import Coalition, EMPTY_COALITION
from shapleypy.restricted.feasible_family import FeasibleFamily

def test_feasible_family_init_and_contains() -> None:
    n = 3
    coalitions = [Coalition.from_players([0, 1])]
    ff = FeasibleFamily(n, coalitions)
    
    assert ff.n == 3
    assert len(ff) == 2 
    assert EMPTY_COALITION in ff
    assert Coalition.from_players([0, 1]) in ff

def test_feasible_family_invalid_player() -> None:
    n = 3
    with pytest.raises(ValueError):
        FeasibleFamily(n, [Coalition.from_players([3])])

def test_add_with_closures() -> None:

    n = 3
    ff = FeasibleFamily(n)
    ff.add([0, 1], enforce_heredity=True, enforce_union_closed=False)
    assert Coalition.from_players([0]) in ff
    assert Coalition.from_players([1]) in ff
    assert ff.is_hereditary() is True
    ff2 = FeasibleFamily(n, [Coalition.from_players([0]), Coalition.from_players([1])])
    assert ff2.is_union_closed() is False
    ff2.add([], enforce_heredity=False, enforce_union_closed=True)
    assert Coalition.from_players([0, 1]) in ff2
    assert ff2.is_union_closed() is True

def test_properties() -> None:
    n = 3
    ff = FeasibleFamily(n, [
        Coalition.from_players([0]), 
        Coalition.from_players([1]), 
        Coalition.from_players([0, 1])
    ])
    
    assert ff.is_hereditary() is True
    assert ff.is_accessible() is True