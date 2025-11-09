from collections.abc import Iterable
from shapleypy.coalition import (
    Coalition,
    EMPTY_COALITION,
     )
from shapleypy.constants import (
    MAXIMUM_NUMBER_OF_PLAYERS,
    MINIMUM_NUMBER_OF_PLAYERS,
    COALITION_NUMBER_OF_PLAYERS_ERROR,
)
from shapleypy._typing import Player, Players


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
    def n(self) -> int:
        return self._n

    def coalitions(self) -> set[Coalition]:
        return set(self._F)

    def is_feasible(self, C: Coalition) -> bool:
        return C in self._F
    
    def add(
        self,
        S: Coalition | Players | Player,
        *,
        enforce_heredity: bool = True,
        enforce_union_closed: bool = False,
    ) -> None:
        
        C = self._to_coalition(S)
        n = self._n
        for i in C.get_players:
            if i >= n or i < 0:
                raise ValueError("Coalition contains a player outside {0, …, n-1}.")
        if C not in self._F:
            self._F.add(C)

        if enforce_heredity:
            for T in C.all_subcoalitions():
                self._F.add(T)

        if enforce_union_closed:
            self._close_under_union()


    def remove(self, S: Coalition | Players | Player) -> None:
        C = self._to_coalition(S)
        if C != EMPTY_COALITION:
            self._F.discard(C)

    def _close_under_union(self) -> None:
        changed = True
        while changed:
            changed = False
            to_add: set[Coalition] = set()
            L = list(self._F)
            for i, A in enumerate(L):
                for B in L[i:]:
                    U = A + B
                    if U not in self._F:
                        to_add.add(U)
            if to_add:
                self._F |= to_add
                changed = True

    def _to_coalition(self, obj: object) -> Coalition:
        if isinstance(obj, Coalition):
            return obj
        if isinstance(obj, int):
            return Coalition.from_players(obj) 
        if isinstance(obj, Iterable):
            return Coalition.from_players(obj) 
        raise TypeError("Expected Coalition | Player | Iterable[Player].")