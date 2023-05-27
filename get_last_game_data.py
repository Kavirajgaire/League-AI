import re
from urllib.request import urlopen
import pandas as pd


def get_last_game_from_profile(username: str) -> pd.DataFrame:

    url = f"https://www.op.gg/summoners/na/{username}"
    page = urlopen(url)
    html = page.read().decode("utf-8")

    final_dataframe = pd.DataFrame()

    summoner_string_pattern = r'"summoner":{"id":\d+.*?"tier_image_url"'
    match = re.findall(summoner_string_pattern  , html)
    if match:
        num_users_data = 0
        aram_check_position = r'"position":null'
        for summoner_string in match:
            is_aram_game = re.search(aram_check_position, summoner_string)
            if not is_aram_game:
                temp_dict = {}
                username_pattern = r'"internal_name":"([^"]+)"'
                obtained_name = re.search(username_pattern, summoner_string)
                is_win = re.findall(r'WIN', summoner_string)
                if is_win:
                    temp_dict[num_users_data] = [obtained_name.group(1), "WIN"]
                else:
                    temp_dict[num_users_data] = [obtained_name.group(1), "LOSE"]
                if final_dataframe.empty:
                    final_dataframe = pd.DataFrame(temp_dict)
                else:
                    final_dataframe = pd.concat([final_dataframe, pd.DataFrame(temp_dict)], ignore_index=True)
            num_users_data += 1
            if num_users_data == 10:
                return final_dataframe
    return final_dataframe


t = get_last_game_from_profile("fl4meandfury")
print(t.to_string())
