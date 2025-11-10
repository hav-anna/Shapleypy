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

