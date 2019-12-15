import numpy as np 
import pandas as pd
import spotipy
import os
import spotipy.oauth2 as Auth 

total = pd.DataFrame(pd.read_csv('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/clean_data/more_tracks.csv'))

more = pd.DataFrame(pd.read_csv('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/no_hits_data_morer_f.csv'))
more = more[['id', 'acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence', 'track_popularity', 'artist_popularity', 'year', 'hit']]
# more = more[more.year > 2015]
print(len(more))
# more.to_csv('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/no_hits_data_morer.csv', encoding='utf-8-sig')
complete = pd.concat([total,more],axis=0)
# complete.drop(['Unnamed: 0'])
print(complete.head())
total_len = len(complete)
print(len(complete))
total_nonhit = len(complete[complete.hit==0])
print(total_nonhit)
complete.to_csv('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/clean_data/even_more_tracks.csv', encoding='utf-8-sig')
