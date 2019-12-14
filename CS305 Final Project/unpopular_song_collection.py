import numpy as np 
import pandas as pd
import spotipy
import os
import spotipy.oauth2 as Auth 

CLIENT_ID = '60ddd115f669473890f90e8f1443e44c'
CLIENT_SECRET = '7861b9c48f4b4be0ad43a7ccf7b21a25'

spotifyAuth = Auth.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
token = spotifyAuth.get_access_token()
spotify = spotipy.Spotify(auth=token)

def get_track_ids(filename):
    DATA = pd.read_csv(filename, skiprows=0, header=1)
    data = np.asarray(DATA)
    track_links = list(data[:, 0])
    track_ids = [link.split(':')[-1] for link in track_links]
    return track_ids


def get_pop_track_ids(filename):
    DATA = pd.read_csv(filename, skiprows=0, header=1)
    data = np.asarray(DATA)
    track_links = list(data[:, -1])
    track_ids = [link.split('/')[-1] for link in track_links]
    return track_ids

files_17 = os.listdir('2017/')

data = []
all_ids = set()
for file in files_17:
    if not file.startswith('.'):
        ids = get_pop_track_ids('2017/'+file)
        all_ids.update(ids)

d_2016 = pd.read_csv('2016_data.csv', skiprows=0, header=0)
d_2016 = d_2016[['id', 'acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence', 'track_popularity', 'artist_popularity', 'year', 'hit']]
d_2016.to_csv('2016_data.csv', index=False)

d_2019 = pd.read_csv('2019_data.csv', skiprows=0, header=0)
d_2019 = d_2019[['id', 'acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence', 'track_popularity', 'artist_popularity', 'year', 'hit']]
d_2019.to_csv('2019_data.csv', index=False)
print(len(all_ids))
all_ids.update(d_2016['id'])
all_ids.update(d_2019['id'])
print(len(all_ids))


#only keep the songs which are from between 2016-2019

nh = os.listdir('nonhits/')

data = []
hp_all_ids = set()
for file in nh:
    if not file.startswith('.'):
        ids = get_track_ids('nonhits/'+file)
        hp_all_ids.update(ids)
# print(hp_all_ids)
print(len(hp_all_ids))

no_hits = hp_all_ids - all_ids
print(len(no_hits))
no_hits = list(no_hits)
#only keep the songs which are from between 2016-2019
for i in range(len(no_hits)//50 + 1):
    prev = 50*(i)
    next100 = 50*(i+1)
    if next100 < len(no_hits)/50:
        features1 = spotify.audio_features(no_hits[next100:])
        track_info = spotify.tracks(no_hits[next100:])
        # print(track_info)
    else:
        features1 = spotify.audio_features(no_hits[prev:next100])
        track_info = spotify.tracks(no_hits[prev:next100])
        # print(track_info)
    # print(features1[0])
    # print(track_info)
    for i in range(len(features1)):
    	if features1[i]:
    		track_info['tracks'][i]['year'] = track_info['tracks'][i]['album']['release_date'].split('-')[0]
    		track_info['tracks'][i].pop('album')
    		# track_info['tracks'][i].pop('release_date_precision')
	    	features1[i].update(track_info['tracks'][i])
	    	# print(features1[i])
    # print(features1)
    # features1.pop('analysis_url')
    # features1.pop('external_urls')
    
    data += features1 
# print(data

def avg_artist_popularity(artids):

	artists_pop = []
	artists = spotify.artists(artids)
	if len(artids) > 1:
	    popularity = np.mean([a['popularity'] for a in artists['artists']])
	else:
	    popularity = artists['artists'].pop()['popularity']
	    
	return popularity


def flatten_dict(d):
	flat_d = {}
	for k in d:
		if type(d[k]) == dict:
			# print(d[k])
			flat_d.update(flatten_dict(d[k]))
		elif type(d[k]) == list and k == 'artists':
			artids = [art['id'] for art in d[k]]
			flat_d['artist_popularity'] = avg_artist_popularity(artids)
		else:
			flat_d[k] = d[k]
	# print(flat_d)
	return flat_d

print("\n unflattened: ", data[0])
print("\n\n flattened: ", flatten_dict(data[0]))

arr_data = np.asarray(data)

flattener = lambda t: flatten_dict(t)
vfunc = np.vectorize(flattener)

data = vfunc(arr_data)
# data = [flatten_dict(d) for d in data if d]

no_hits_df = pd.DataFrame(data).drop(columns=['available_markets', 'analysis_url', 'uri', 'type', 'track_number', 'disc_number', 'spotify', 'href', 'track_href','preview_url','explicit','is_local','isrc','name'])
no_hits_df['hit'] = 0
feat = list(no_hits_df.columns)
print(feat)
no_hits_df.to_csv('no_hits_data.csv', encoding='utf-8-sig')

print(no_hits_df.head())

