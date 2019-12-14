#/usr/bin/python3
import numpy as np 
import pandas as pd
import spotipy
import spotipy.oauth2 as Auth 
import csv

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

def get_features(tid):
	# id_arr = np.asarray(ids)
	# print(id_arr[0])
	# analysis = spotify.audio_analysis(tid)
	# print(analysis)
	track = spotify.track(tid)
	# print(track)
	aid = track['album']['artists'][0]['id']
	artist = spotify.artist(aid)
	# print(artist)
	features = spotify.audio_features(tid)[0]
	features['artist_ids'] = aid
	features['artist_popularity'] = artist['popularity']
	features['year'] = '2017'
	print(features)
	with open('tracks.csv', mode='a') as csv_file:
	    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	    csv_writer.writerow(features.values())

	# return features
	# print(analysis)
	# print(features)

trackIDs = set()
for i in range(1,41):
	file_name = 'csv/regional-global-weekly-2017-'+str(i)+'.csv'
	trackIDs.update(get_track_ids(file_name)) #+= get_track_ids(file_name)
	# trackIDs = list(set(trackIDs))
print(len(trackIDs))
# print(trackIDs)

featurer = lambda t: get_features(t)
vfunc = np.vectorize(featurer)

ids = np.asarray(list(trackIDs))
# print(ids)
get_features(list(trackIDs)[0])
# vfunc(ids)
# info = list(map(get_features, ids))
# print(info)
# # get_features(ids)
	# print(analysis)
	# print(features)
# print(trackIDs)
# print(len(trackIDs))
	# with open('tracks.csv', mode='w') as csv_file:
	#     csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	#     for trk in trackIDs:
	#     	csv_writer.writerow(trk)
