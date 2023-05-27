import ssl
import pandas as pd
import re
from urllib.request import urlopen

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE


def scrape_data_from_profile(username: str) -> pd.DataFrame:
    url = f"https://www.op.gg/summoners/na/{username}"
    page = urlopen(url)
    html = page.read().decode("utf-8")

    final_dataframe = pd.DataFrame()

    summoner_string_pattern = r'"summoner":{"id":\d+.*?"tier_image_url"'
    match = re.findall(summoner_string_pattern  , html)
    if match:
        regex_username = r'"internal_name":"([^"]+)"'
        aram_check_position = r'"position":null'
        for summoner_string in match:
            current_string_name = re.search(regex_username, summoner_string)
            is_aram_game = re.search(aram_check_position, summoner_string)
            if current_string_name is not None and current_string_name.group(1) == username and not is_aram_game:
                temp_dict = {}
                pattern = r'"([^"]+)":"([^"]*)"|"([^"]+)":(\d+|\w+)'
                matches = re.findall(pattern, summoner_string)
                for parameter in matches:
                    param = parameter[0] or parameter[2]
                    value = parameter[1] or parameter[3]
                    temp_dict[param] = [value]
                if final_dataframe.empty:
                    final_dataframe = pd.DataFrame(temp_dict)
                else:
                    final_dataframe = pd.concat([final_dataframe, pd.DataFrame(temp_dict)], ignore_index=True)
    return final_dataframe


def get_players(pages: int) -> list:
    url = f"https://www.op.gg/leaderboards/tier?page="
    players = []
    for i in range(1, pages + 1):
        page = urlopen(url + str(i), context=context)
        html = page.read().decode("utf-8")
        summoner_string_pattern = r'<strong class="summoner-name">(.*?)</strong>'
        match = re.findall(summoner_string_pattern, html)
        players.extend(match)
    players = [j.replace(" ", "%20") for j in players]
    return players

def df_to_stats(df: pd.DataFrame) -> list:
    new_df = df[["total_damage_dealt_to_champions", "kill", "death", "assist", "gold_earned", "minion_kill", "op_score"]]
    new_df = new_df.astype(int)
    stats = []
    for column in new_df.columns:
        column_average = new_df[column].mean()
        stats.append(column_average)
    return stats


if __name__ == "__main__":
    df = scrape_data_from_profile("fl4meandfury")
    df = df[["total_damage_dealt_to_champions", "kill", "death", "assist", "gold_earned", "minion_kill", "op_score"]]
    df.to_csv("test.csv")
    stats = []
    df = df.astype(int)
    for column in df.columns:
        column_average = df[column].mean()
        stats.append(column_average)
