import model
import scrape_data
import os
import pandas as pd


def get_team_stats(team: list) -> list:
    stats = []
    for player in team:
        stats.extend(scrape_data.df_to_stats(scrape_data.scrape_data_from_profile(player.lower()))) # fix to get average stats from inner function
    return stats


def create_data():
    if os.path.exists((os.path.join(os.getcwd(), "training_data.csv"))):
        print("data already exists")
        return
    columns = [str(i) for i in range(7*5 + 1)]
    df = pd.DataFrame(columns=columns)
    player_data = scrape_data.get_players(1, 1)
    for count, i in enumerate(player_data):
        team = scrape_data.get_last_game_from_profile(i.lower())
        team_stats = get_team_stats(team[:-1])
        team_df = pd.DataFrame(team_stats).T
        team_df[36] = team[-1]
        if len(team_stats) != 0:
            team_df.columns = df.columns
            df = pd.concat([df, team_df], ignore_index=True)
        if count % 10 == 0:
            print(count)
    df.to_csv("training_data.csv")
    print("complete")


if __name__ == "__main__":
    create_data()
