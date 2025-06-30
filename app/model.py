import pandas as pd

#For reading and writing to ratings.csv


def load_ratings():
    return pd.read_csv("ratings.csv")

def append_rating(user_id, menu_item_id, rating):
    df = pd.DataFrame([[user_id, menu_item_id, rating]], columns=["userId", "menuItemId", "rating"])
    df.to_csv("ratings.csv", mode="a", header=False, index=False)
