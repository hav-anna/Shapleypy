import csv
import json

from shapleypy.coalition import Coalition
from shapleypy.restricted.game import RestrictedGame
from shapleypy.constants import CSV_SEPARATOR_ERROR


def _prepare_restricted_game_dict(restricted_game: RestrictedGame) -> dict:
    """
    Internal helper function to convert a RestrictedGame object into a dictionary 
    suitable for JSON serialization.

    Args:
        restricted_game (RestrictedGame): The restricted game to convert.

    Returns:
        dict: A dictionary representation containing the number of players ('n'),
            a mapping of coalitions to their values ('values'), and a list of 
            feasible coalitions ('feasible').
    """
    n = restricted_game.number_of_players
    values_dict = {}
    feasible_list = []
    
    for C in Coalition.all_coalitions(n):
        players = list(C.get_players)
        values_dict[str(players)] = restricted_game.base_game.get_value(C)
        if restricted_game.is_feasible(C):
            feasible_list.append(players)
            
    return {
        "n": n,
        "values": values_dict,
        "feasible": feasible_list
    }


def save_restricted_game_to_json(restricted_game: RestrictedGame, file: str) -> None:
    """
    Saves a RestrictedGame to a JSON file.

    Args:
        restricted_game (RestrictedGame): The restricted game to be saved.
        file (str): The path to the target JSON file.
    """
    data = _prepare_restricted_game_dict(restricted_game)
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


def save_restricted_game_to_csv(
    restricted_game: RestrictedGame,
    file: str,
    csv_separator: str = ":",
    coalition_separator: str = ","
) -> None:
    """
    Saves a RestrictedGame to a CSV file.

    Args:
        restricted_game (RestrictedGame): The restricted game to be saved.
        file (str): The path to the target CSV file.
        csv_separator (str, optional): The delimiter used to separate columns 
            in the CSV file. Defaults to ":".
        coalition_separator (str, optional): The delimiter used to separate 
            players within a coalition string. Defaults to ",".

    Raises:
        ValueError: If csv_separator and coalition_separator are identical.
    """
    if csv_separator == coalition_separator:
        raise ValueError(CSV_SEPARATOR_ERROR)

    n = restricted_game.number_of_players
    with open(file, mode="w", newline="") as f:
        writer = csv.writer(f, delimiter=csv_separator)
        writer.writerow(["n", n])
        
        for C in Coalition.all_coalitions(n):
            players = list(C.get_players)
            coalition_str = coalition_separator.join(map(str, players)) if players else ""
            value = restricted_game.base_game.get_value(C)
            is_feasible = 1 if restricted_game.is_feasible(C) else 0
            
            writer.writerow([coalition_str, value, is_feasible])