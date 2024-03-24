from data_collector import get_playlist_data
import pandas as pd


def transform_json_into_df(json, json_path=["tracks", "items"]):
    df_from_normalized_json = pd.json_normalize(json, json_path)

    # create artist_name and artis_id from unnested artists column
    df_from_normalized_json["artist_name"] = df_from_normalized_json.apply(
        lambda row: extract_parameter_list_from_nested_column(
            row, "track.artists", "name"
        ),
        axis=1,
    )
    df_from_normalized_json["artist_id"] = df_from_normalized_json.apply(
        lambda row: extract_parameter_list_from_nested_column(
            row, "track.artists", "id"
        ),
        axis=1,
    )

    # add playlist metadata from json
    df_from_normalized_json["playlist_id"] = json["id"]
    df_from_normalized_json["playlist_name"] = json["name"]
    df_from_normalized_json["number_of_followers"] = json["followers"]["total"]

    # create final dataframe
    df_final = df_from_normalized_json[
        [
            "playlist_id",
            "playlist_name",
            "number_of_followers",
            "added_at",
            "track.name",
            "track.id",
            "track.popularity",
            "track.duration_ms",
            "track.album.name",
            "track.album.id",
            "artist_name",
            "artist_id",
        ]
    ]

    # rename columns
    df_final.columns = [
        "playlist_id",
        "name",
        "number of followers",
        "timestamp when track was added",
        "song_name",
        "song_id",
        "song_popularity",
        "song_duration_ms",
        "album_name",
        "album_id",
        "artist_name",
        "artist_id",
    ]
    return df_final


def extract_parameter_list_from_nested_column(row, nested_column_name, parameter_name):
    parameter_list = []
    nested_column = row[nested_column_name]
    for item in nested_column:
        if parameter_name in item:
            parameter_list.append(item[parameter_name])
    return parameter_list
