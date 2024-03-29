import pandas as pd
import numpy as np

# Preprocess Spotify data
def preprocess_spotify():
    df = pd.read_csv("start_data\spotify-2023.csv", encoding='latin-1')
    df = df.rename(columns={
        "danceability_%": "danceability",
        "valence_%": "valence",
        "energy_%": "energy",
        "acousticness_%": "acousticness",
        "instrumentalness_%": "instrumentalness",
        "liveness_%": "liveness",
        "speechiness_%": "speechiness"
    })

    # bpm name column to tempo
    df = df.rename(columns={"artist(s)_name":"artist_name", "bpm":"tempo"})

    # change Major to 0 and Minor to 1
    df['mode'] = df['mode'].map({'Major': 0, 'Minor': 1})

    # change musical key to 0-11 range
    key_mapping = {
        'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 
        'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11
    }
    df['key'] = df['key'].map(key_mapping)
    
    df['released_year'] = df['released_year'].astype(str)
    df['released_month'] = df['released_month'].astype(str)
    df['released_day'] = df['released_day'].astype(str)
    df['artist_count'] = df['artist_count'].astype(str)

    return df
 
# Preprocess TikTok data   
def preprocess_tiktok():
    df = pd.read_csv("start_data\TikTok_songs_2022.csv", encoding='latin-1')
    columns_to_multiply = [
        'danceability', 
        'energy', 
        'acousticness', 
        'instrumentalness', 
        'liveness', 
        'valence'
    ]
    
    df[columns_to_multiply] = df[columns_to_multiply].mul(100).round(1)
    df = df.rename(columns={"duration_ms":"duration"})
    df.astype({'duration': 'float64'}).dtypes
    df['duration'] = df['duration'].div(1000)
    df['duration'] = pd.to_datetime(df['duration'], unit='s').dt.strftime('%M:%S')

    return df
  
def create_artist_table(data):
    data = data.explode('artist_name')
    artists = data['artist_name'].drop_duplicates()
    artists = [(idx, val) for idx, val in enumerate(artists)]
    artist_table = pd.DataFrame(artists, columns=['artist_id', 'artist_name'])
    artist_table.to_csv('artists.csv',index=False) # write artist id table to csv
    return artist_table
    
def create_track_table(data, dict_id_name_mapping):
    
    data['artist_name'] = data['artist_name'].apply(lambda x: dict_id_name_mapping.get(x[0], "unknown"))
    tracks = data.drop_duplicates(subset=['track_name']).copy() # drop duplicates
    track_id = [idx for idx, _ in enumerate(tracks['track_name'])]
    tracks.insert(0, 'track_id', track_id)
    table = tracks.copy() # create copy for returing
    tracks.fillna('unknown', inplace=True)
    tracks.to_csv('tracks.csv',index=False) # write tracks to csv
    return table
 
def create_chart_table(data):
    chart = data.loc[:, ('track_id','in_spotify_charts', 'in_apple_charts', 'in_deezer_charts', 'in_shazam_charts')]
    chart.dropna(subset=['in_spotify_charts', 'in_apple_charts', 'in_deezer_charts', 'in_shazam_charts'], inplace=True)
    chart['in_shazam_charts'] = chart['in_shazam_charts'].str.replace(',', '').astype(int)
    sort_chart = chart.sort_values(by=['in_spotify_charts', 'in_apple_charts', 'in_deezer_charts', 'in_shazam_charts'], ascending=False)
    chart_id = [idx for idx, _ in enumerate(chart.loc[:, ('track_id')])]
    sort_chart.insert(0, 'chart_id', chart_id)
    sort_chart[['in_spotify_charts', 'in_apple_charts', 'in_deezer_charts', 'in_shazam_charts']] = sort_chart[['in_spotify_charts', 'in_apple_charts', 'in_deezer_charts', 'in_shazam_charts']].astype(int)
    sort_chart.to_csv('charts.csv',index=False) # write charts to csv
    
def create_playlist_table(data):
    playlist = data.loc[:, ('track_id','in_spotify_playlists', 'in_apple_playlists', 'in_deezer_playlists')]
    playlist.dropna(subset=['in_spotify_playlists', 'in_apple_playlists', 'in_deezer_playlists'], inplace=True)
    playlist['in_deezer_playlists'] = playlist['in_deezer_playlists'].str.replace(',', '').astype(int) # , removen met str.replace
    playlist['in_spotify_playlists'] = playlist['in_spotify_playlists'].astype(int) # .0 removen met astype(int)
    playlist['in_apple_playlists'] = playlist['in_apple_playlists'].astype(int) # .0 removen met astype(int)
    sort_playlist = playlist.sort_values(by=['in_spotify_playlists', 'in_apple_playlists', 'in_deezer_playlists'], ascending=False)
    playlist_id = [idx for idx, _ in enumerate(playlist.loc[:, ('track_id')])]
    sort_playlist.insert(0, 'playlist_id', playlist_id)
    sort_playlist.to_csv('playlists.csv',index=False) # write playlists to csv

def create_music_table(data):
    music = data.loc[:, ('track_id','danceability', 'energy', 'key', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo')]
    music_id = [idx for idx, _ in enumerate(music.loc[:, ('track_id')])]
    music.insert(0, 'music_id', music_id)
    music.fillna(-1, inplace=True) # NaN naar -1
    music = music.astype(int, errors='ignore') # .0 removen met
    music['mode'] = music['mode'].replace({0: "major", 1: "minor"}) # 0 naar False en 1 naar True mode
    music.to_csv('music.csv',index=False) # write music to csv
    
if __name__ == "__main__":
    
    # Preprocess data
    df_spotify = preprocess_spotify()
    df_tiktok = preprocess_tiktok()
    
    # Merge data
    merged = pd.concat([df_spotify, df_tiktok], ignore_index=True)
    merged['artist_name'] = merged['artist_name'].str.split(', ')
    
    merged['artist_count'] = merged['artist_count'].fillna(1) # fix artist count 1 not in chart
    
    merged['artist_pop'] = merged['artist_pop'].fillna(-1) # fix artist pop -1 not in chart
    
    merged['track_pop'] = merged['track_pop'].fillna(-1) # fix track pop -1 not in chart
    
    merged['duration'] = merged['duration'].fillna(0) # fix duration 0 not in chart
    
    merged['released_year'] = merged['released_year'].fillna(0) # fix released year 0 not in chart
    merged['released_month'] = merged['released_month'].fillna(0) # fix released month 0 not in chart
    merged['released_day'] = merged['released_day'].fillna(0) # fix released day 0 not in chart
    # Create artist table
    artist_table = create_artist_table(merged)
        
    # Create track table
    dict_from_columns = dict(zip(artist_table['artist_name'], artist_table['artist_id'])) # create dict from artist table
    tracks = create_track_table(merged, dict_from_columns) # main table
    
    # Create Chart table
    create_chart_table(tracks)
    
    # Create Playlist table
    create_playlist_table(tracks)
    
    # Create Music table
    create_music_table(tracks)
    
    
    
    
