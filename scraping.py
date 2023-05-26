import re
from urllib.request import urlopen
import pandas as pd


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
            if current_string_name.group(1) == username and not is_aram_game:
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


