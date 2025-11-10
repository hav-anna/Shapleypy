from collections.abc import Iterable
from shapleypy._typing import Player, Players
from shapleypy.coalition import Coalition
from shapleypy.game import Game
from shapleypy.restrected.feasible_family import FeasibleFamily


class RestrictedGame:

    def __init__(self, base_game: Game, feasible: FeasibleFamily) -> None:
        """
        Initialize a RestrictedGame.

        Args:
            base_game (Game): The underlying TU-game.
            feasible (FeasibleFamily): The feasible family F restricting coalitions.

        Raises:
            ValueError: If the number of players in `base_game` and `feasible` differs.
        """
        if base_game.number_of_players != feasible.n:
            raise ValueError(
                "Number of players in Game and FeasibleFamily must match "
                f"({base_game.number_of_players} != {feasible.n})."
            )
        self._game = base_game
        self._F = feasible

    def __repr__(self) -> str:
        """
        Returns:
            str: Representation with the number of players and size of F.
        """
        return f"RestrictedGame(n={self.number_of_players}, |F|={len(self._F)})"

    @property
    def number_of_players(self) -> int:
        """
        Returns:
            int: Number of players N.
        """
        return self._game.number_of_players

    @property
    def base_game(self) -> Game:
        """
        Access to the underlying Game instance.

        Returns:
            Game: The underlying TU-game.
        """
        return self._game

    @property
    def feasible(self) -> FeasibleFamily:
        """
        Return a defensive copy of the feasible set F.

        Returns:
            set[Coalition]: Copy of feasible coalitions.
        """
        return self._F.coalitions()

    def is_feasible(self, S: Coalition | Player | Players | Iterable[Player]) -> bool:
        C = self._to_coalition(S)
        return self._F.is_feasible(C)

    def get_value(self, S: Coalition | Player | Players | Iterable[Player]) -> float:
        C = self._to_coalition(S)
        if not self._F.is_feasible(C):
            raise ValueError("Coalition is not feasible (S ∉ F).")
        return self._game.get_value(C)

    def set_value(self, S: Coalition | Player | Players | Iterable[Player], value: float) -> None:
        C = self._to_coalition(S)
        if not self._F.is_feasible(C):
            raise ValueError("Cannot set value: coalition is not feasible (S ∉ F).")
        self._game.set_value(C, float(value))

    def _to_coalition(self, S: Coalition | Player | Players | Iterable[Player]) -> Coalition:
        if isinstance(S, Coalition):
            return S
        if isinstance(S, int):
            return Coalition.from_players(S)
        if isinstance(S, Iterable):
            return Coalition.from_players(S)
        raise TypeError("Expected Coalition | Player | Iterable[Player].")