from collections.abc import Iterable
from shapleypy.coalition import (
    Coalition,
    EMPTY_COALITION
     )
from shapleypy.constants import (
    MAXIMUM_NUMBER_OF_PLAYERS,
    MINIMUM_NUMBER_OF_PLAYERS,
    COALITION_NUMBER_OF_PLAYERS_ERROR,
)


class FeasibleFamily:

    def __init__(self, n_players: int, coalitions: Iterable[Coalition] | None = None) -> None:
        if n_players > MAXIMUM_NUMBER_OF_PLAYERS or n_players < MINIMUM_NUMBER_OF_PLAYERS:
            raise ValueError(COALITION_NUMBER_OF_PLAYERS_ERROR)

        self._n = int(n_players)
        self._F: set[Coalition] = set(coalitions or ())
        self._F.add(EMPTY_COALITION)
        for C in self._F:
            n = self._n
            for i in C.get_players:
                if i >= n or i < 0:
                    raise ValueError("Coalition contains a player outside {0, …, n-1}.")
        self._F.add(EMPTY_COALITION)

    def __repr__(self) -> str:
        return f"FeasibleFamily(n={self.n}, size={len(self._F)})"
    
    def __len__(self) -> int:
        return len(self._F)
    
    def __contains__(self, obj: object) -> bool:
        try:
            C = self._to_coalition(obj)
        except TypeError:
            return False
        return C in self._F