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
TOKEN = "BQB13eFDmtQbRSgih2sYQttzi7_13SMeFqtqpKmgBdAuuT7JG6QsPxDy8uDbMSxXcuYI-INdKrqZyKbZQV6NE8OFQU_MXLAalzfOyLcyAyoxmNuDK_j4zSLz60wyPvokq1vD-qJFiQpD-GzqAp7eGikz"

if __name__ == "__main__":

    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }

    r = requests.get("https://api.spotify.com/v1/playlists/{playlist_id}/tracks".format(playlist_id="37i9dQZF1DX5UTavgI6ivn"), headers=headers)
    data = r.json()
    #print(data)
    added_by = []
    song_names = []
    album_names = []
    href_list = []

    for song in data["items"]:
        added_by.append(song["added_by"]["id"])
        song_names.append(song["track"]["name"])
        album_names.append(song["track"]["album"]["name"])
        href_list.append(song["track"]["href"])

    song_dict = {
        "added_by":added_by,
        "song_name":song_names,
        "album_name":album_names,
        "href":href_list
    }
    song_df = pd.DataFrame(song_dict, columns=["added_by","song_name","album_name","href"])
    print(song_df.head(10))


