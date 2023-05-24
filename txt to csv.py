import pandas as pd

dataframe1 = pd.read_csv("league ai training data.txt")

dataframe1.to_csv("Game Data.csv", index = False)
