import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
USER_ID = "12143350697"
TOKEN = "BQCEqok9_vtwrl9a_nInctuOkt0JprPezsfeU9tQoHLoTjdfGqs-Eyp_BF1hyFJYpiC1nClfEfMs-CoPcdoXwe5Ay4RBFdESC-Pqs8maLQa6ZVhT5SjXKphqdrtrl_DXhJgYWBpml8jy-V60BoLqFwLE"

if __name__ == "__main__":

    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }

    r = requests.get("	https://api.spotify.com/v1/browse/new-releases", headers=headers)
    data = r.json()

    song_names = []
    artist_names = []
    timestamps = []

    for song in data["albums"]["items"]:
        song_names.append(song["name"])
        artist_names.append(song["artists"][0]["name"])
        timestamps.append(song["uri"])

    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "timestamp": timestamps
    }
    songs_df = pd.DataFrame(song_dict, columns=["song_name", "artist_name", "timestamp"])
    print(songs_df.head(5))

