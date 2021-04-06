import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
USER_ID = "12171821724"
TOKEN = "BQBnIFnnyWAV6Mc5Z9UuBLdVsxnAsVpPatwozGuh1NPt15KAGDAbVigU7DWt5713oTk83GkgeKUuwNof6UJxh26b_gUPavub4oCtb370YvL4P8f4Kr1TRD88nQOHGUgrA7BPn7xBEVV72lw7oO81aL6x"


def check_if_valid_data(df: pd.DataFrame) -> bool:
    # Check if DataFrame is empty
    if df.empty:
        print("No songs downloaded. Finished execution.")
        return False

    # Primary Key Check
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Primary Key Check is violated")

    # Check for nulls
    if df.isnull().values.any():
        raise Exception("Null valued found")

    yesterday = datetime.datetime.now() - datetime.timedelta(days=10)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    timestamps = df["timestamp"].tolist()
    for timestamp in timestamps:
        if datetime.datetime.strptime(timestamp, '%Y-%m-%d') != yesterday:
            #raise Exception("At least one of the returned songs does not come from within the last 24 hours")
            pass

    return True


if __name__ == "__main__":

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN)
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=4)
    yesterday_unix_timestamp = int(yesterday.timestamp( )) * 1000

    try:
        r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}&limit=5".format(
            time=yesterday_unix_timestamp), headers=headers)
        r.raise_for_status()
    except requests.HTTPError as e:
        print(e)
    data = r.json()

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamp": timestamps
    }

    songs_df = pd.DataFrame(song_dict, columns=["song_name", "artist_name", "played_at", "timestamp"])

    # Validate
    if check_if_valid_data(songs_df):
        print("Data valid, proceed to Load stage")
        print(songs_df)