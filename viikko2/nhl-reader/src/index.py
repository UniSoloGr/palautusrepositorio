from player import Player, PlayerReader, PlayerStats
from rich.console import Console
from rich.text import Text
from rich.table import Table

console = Console()

def pretty_input(prefix, item_list, default = ""):

    text = Text()
    text.append(f"{prefix} ", style="white")
    text.append(
        f"[{'/'.join(item_list)}]",
        style="bold magenta"
    )
    text.append(f" ({default}):", style="bold cyan")

    console.print(text, end=" ")
    user_input = console.input()
    if user_input not in item_list:
        user_input = default 
    return user_input

def print_players(players: list[Player], season: str, nationality: str):

    table = Table(
        title=f"Season {season} players from {nationality}",
        title_style="italic white",
        header_style="bold white",
        border_style="white",
        show_lines=False,
        expand=True
    )

    table.add_column("Released", style="cyan", justify="left")
    table.add_column("teams", style="magenta", justify="left")
    table.add_column("goals", style="green", justify="right")
    table.add_column("assists", style="green", justify="right")
    table.add_column("points", style="green", justify="right")

    for player in players:
        table.add_row(
            player.name,
            player.team,
            str(player.goals),
            str(player.assists),
            str(player.goals + player.assists)
        )

    console.print(table)
     

def main():
    seasons = {
        "2018-19",
        "2019-20",
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25",
        "2025-26",
    }
    season = pretty_input("Season", list(seasons), "2024-25")
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    nationalities = stats.list_of_nationalities()
    while True:
        nationality = pretty_input("Nationality", nationalities)
        print_players(stats.top_scorers_by_nationality(nationality), season, nationality)

if __name__ == "__main__":
    main()
