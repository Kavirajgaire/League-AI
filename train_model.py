import model
import scrape_data
import os
import pandas as pd
import get_last_game_data


def get_team_stats(team: list) -> list:
    stats = []
    for player in team:
        stats.extend(scrape_data.df_to_stats(scrape_data.scrape_data_from_profile(player.lower()))) # fix to get average stats from inner function
    return stats


def create_data():
    if os.path.exists((os.path.join(os.getcwd(), "training_data.csv"))):
        return
    columns = [str(i) for i in range(7*5)]
    df = pd.DataFrame(columns=columns)
    player_data = scrape_data.get_players(1)[:3]

    print(player_data)
    for i in player_data:
        team = get_last_game_data.get_last_game_from_profile(i.lower())
        team_stats = get_team_stats(team)
        team_df = pd.DataFrame(team_stats).T
        if len(team_stats) != 0:
            team_df.columns = df.columns
            df = pd.concat([df, team_df], ignore_index=True)
    df.to_csv("training_data.csv")


create_data()
