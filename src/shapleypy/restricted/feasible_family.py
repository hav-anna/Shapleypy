from collections.abc import Iterable
from shapleypy.coalition import (
    Coalition,
    EMPTY_COALITION,
     )
from shapleypy.constants import (
    MAXIMUM_NUMBER_OF_PLAYERS,
    MINIMUM_NUMBER_OF_PLAYERS,
    COALITION_NUMBER_OF_PLAYERS_ERROR,
    all_one_player_missing_subcoalitions,
)
from shapleypy._typing import Player, Players


class FeasibleFamily:

    def __init__(self, n_players: int, coalitions: Iterable[Coalition] | None = None) -> None:
        """
        Initialize a FeasibleFamily.

        Args:
            n_players (int): Number of players N, players are 0..n_players-1.
            coalitions (Iterable[Coalition] | None): Initial feasible coalitions.

        Raises:
            ValueError: If n_players is out of allowed bounds or any coalition
                contains a player outside {0, …, n_players-1}.
        """
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
        """
        Returns:
            str: Representation with n and number of coalitions.
        """
        return f"FeasibleFamily(n={self.n}, size={len(self._F)})"
    
    def __len__(self) -> int:
        """
        Returns:
            int: Number of feasible coalitions.
        """
        return len(self._F)
    
    def __contains__(self, obj: object) -> bool:
        """
        Checks if an object (Coalition | Player | Iterable[Player]) is feasible.

        Args:
            obj (object): Coalition, single Player, or Iterable[Player].

        Returns:
            bool: True if the corresponding coalition is in F, False otherwise.
        """
        try:
            C = self._to_coalition(obj)
        except TypeError:
            return False
        return C in self._F
    
    def n(self) -> int:
        """
        Returns:
            int: Number of players.
        """
        return self._n

    def coalitions(self) -> set[Coalition]:
        """
        Returns a copy of the feasible family (set of coalitions).

        Returns:
            set[Coalition]: A shallow copy of F.
        """
        return set(self._F)

    def is_feasible(self, C: Coalition) -> bool:
        """
        Test whether a coalition is feasible.

        Args:
            C (Coalition): Coalition to test.

        Returns:
            bool: True iff C ∈ F.
        """
        return C in self._F
    
    def add(
        self,
        S: Coalition | Players | Player,
        *,
        enforce_heredity: bool = True,
        enforce_union_closed: bool = False,
    ) -> None:
        """
        Add a coalition to F, optionally closing under subcoalitions and/or unions.

        Args:
            S (Coalition | Players | Player): Coalition or players description.
            enforce_heredity (bool): If True, add all subcoalitions of S (downward closure).
            enforce_union_closed (bool): If True, repeatedly add unions A∪B until fixed point.

        Raises:
            ValueError: If S contains a player outside {0, …, n-1}.
        """
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
        """
        Remove a coalition from F (does NOT remove ∅ and does NOT re-close).

        Args:
            S (Coalition | Players | Player): Coalition to remove.

        Notes:
            This operation does not maintain any closure properties automatically.
            If you want to keep e.g. heredity/union-closedness, re-run closure
            after removals or avoid removing elements that would break it.

        """
        C = self._to_coalition(S)
        if C != EMPTY_COALITION:
            self._F.discard(C)

    def is_hereditary(self) -> bool:
        """
        Check if F is downward closed: ∀C∈F, ∀T⊆C ⇒ T∈F.

        Returns:
            bool: True if hereditary, False otherwise.
        """
        F = self._F
        for C in F:
            for T in C.all_subcoalitions():
                if T not in F:
                    return False
        return True

    def is_accessible(self) -> bool:
        """
        Check accessibility: ∀C∈F, C≠∅ ⇒ ∃i∈C with C\\{i}∈F.

        Returns:
            bool: True if accessible, False otherwise.
        """
        F = self._F
        for C in F:
            if C != EMPTY_COALITION:
                if not any(P in F for P in all_one_player_missing_subcoalitions(C)):
                    return False
        return True

    def is_union_closed(self) -> bool:
        """
        Check union-closedness: ∀A,B∈F ⇒ A∪B ∈ F.

        Returns:
            bool: True if union-closed, False otherwise.
        """
        F = self._F
        L = list(F)
        for i, A in enumerate(L):
            for B in L[i:]:
                if (A + B) not in F:
                    return False
        return True

    

    def _close_under_union(self) -> None:
        """
        Repeatedly add A∪B for A,B ∈ F until a fixed point is reached.

        Notes:
            This is O(|F|^2) per iteration; for large families consider a more
            incremental strategy.
        """
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
        """
        Coerce input into a Coalition.

        Args:
            obj (object): Coalition | Player | Iterable[Player].

        Returns:
            Coalition: The corresponding coalition.

        Raises:
            TypeError: If obj cannot be interpreted as a coalition.
            ValueError: If players are outside global allowed bounds.
        """
        if isinstance(obj, Coalition):
            return obj
        if isinstance(obj, int):
            return Coalition.from_players(obj) 
        if isinstance(obj, Iterable):
            return Coalition.from_players(obj) 
        raise TypeError("Expected Coalition | Player | Iterable[Player].")
    