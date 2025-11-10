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
        Accessor for the feasible family.

        Returns:
            FeasibleFamily: The feasible family F.
        """
        return self._F

    def is_feasible(self, S: Coalition) -> bool:
        return self._F.is_feasible(S)

    def get_value(self, S: Coalition) -> float:
        if not self.is_feasible(S):
            raise ValueError("Coalition is not feasible")
        return self._game.get_value(S)

    def set_value(self, S: Coalition, value: float) -> None:
        if not self.is_feasible(S):
            raise ValueError("Cannot set value: coalition not feasible")
        self._game.set_value(S, value)