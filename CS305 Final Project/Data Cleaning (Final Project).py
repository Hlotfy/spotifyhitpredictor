#!/usr/bin/env python
# coding: utf-8

# ## Final Project: Billboard 100 Song Predictor
# 
# Extract data from the Spotify Web API, without using the requests module. Spotipy is a python module that allows you easily authenticate your spotify web application.

# In[2]:


import numpy as np 
import pandas as pd
import spotipy
import spotipy.oauth2 as Auth 

CLIENT_ID = '60ddd115f669473890f90e8f1443e44c'
CLIENT_SECRET = '7861b9c48f4b4be0ad43a7ccf7b21a25'

spotifyAuth = Auth.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
token = spotifyAuth.get_access_token()
spotify = spotipy.Spotify(auth=token)

    
def get_track_ids(filename):
    DATA = pd.read_csv(filename, skiprows=0, header=1)
    data = np.asarray(DATA)
    track_links = list(data[:, -1])
    track_ids = [link.split('/')[-1] for link in track_links]
    return track_ids


import os
files_17 = os.listdir('2017/')

data = []
all_ids = set()
for file in files_17:
    if not file.startswith('.'):
        ids = get_track_ids('2017/'+file)
        all_ids.update(ids)
print(len(all_ids))
all_ids = list(all_ids)
for i in range(len(all_ids)//100 + 1):
    prev = 100*(i)
    next100 = 100*(i+1)
    if next100 < len(all_ids)/100:
        features1 = spotify.audio_features(all_ids[next100:])
    else:
        features1 = spotify.audio_features(all_ids[prev:next100])
    # print(features1)
    data += features1 
df_2017 = pd.DataFrame(data).drop(columns=['track_href', 'analysis_url', 'uri', 'type']) 
print(df_2017)

ids = list(df_2017['id'])
data2 =[]
for i in range((len(ids)//50 + 1)):
    prev = 50*(i)
    next100 = 50*(i+1)
    if next100 < len(ids)/50:
        features1 = spotify.tracks(ids[next100:], market=None)['tracks']
    else:
        features1 = spotify.tracks(ids[prev:next100], market=None)['tracks']
        
    data2 += features1 


df_tracks = pd.DataFrame(data2)
print(df_tracks)
df_2017['track_popularity'] = list(df_tracks.popularity)


artist_ids = []
for elt in df_tracks.artists:
    ids = [a['id'] for a in elt]
    artist_ids.append(ids)


artists_pop = []

for ids in artist_ids:
    artists = spotify.artists(ids)
    if len(ids) > 1:
        popularity = np.mean([a['popularity'] for a in artists['artists']])
    else:
        popularity = artists['artists'].pop()['popularity']
        
    artists_pop.append(popularity)


df_2017['artist_popularity'] = artists_pop


df_2017['hit'] = 1

print(df_2017)

df_2017.to_csv('2017_data.csv', index=False)


df_2017 = pd.read_csv('2017_data.csv', skiprows=0, header=0)


df_2017.insert(len(df_2017.columns)-1, 'year', 2017)

df_2017 = df_2017[['id', 'acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence', 'track_popularity', 'artist_popularity', 'year', 'hit']]

df_2017.to_csv('2017_data.csv', index=False)


