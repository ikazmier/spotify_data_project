from data_collector import get_playlist_data
from data_transformer import transform_json_into_df


json = get_playlist_data("37i9dQZEVXbLRQDuF5jeBp", "USA")
df_final = transform_json_into_df(json, json_path=["tracks", "items"])
