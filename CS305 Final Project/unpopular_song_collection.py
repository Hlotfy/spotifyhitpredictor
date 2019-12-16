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
    print(filename)
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

def avg_artist_popularity(artids):

    artists_pop = []
    artists = spotify.artists(artids)
    if len(artids) > 1:
        popularity = np.mean([a['popularity'] for a in artists['artists']])
    else:
        popularity = artists['artists'].pop()['popularity']
        
    return popularity

# files_17 = os.listdir('2017/')

# data = []
# all_ids = set()
# # for file in files_17:
# #     if not file.startswith('.'):
# #         ids = get_pop_track_ids('2017/'+file)
# #         all_ids.update(ids)

# track_data = pd.read_csv('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/clean_data/even_more_tracks.csv', skiprows=0, header=0)
# print(len(track_data))
# all_ids.update(track_data['id'])
# print(len(all_ids))

# d_2016 = d_2016[['id', 'acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence', 'track_popularity', 'artist_popularity', 'year', 'hit']]
# # d_2016.to_csv('2016_data.csv', index=False)
# 
# d_2019 = pd.read_csv('clean_data/2019_data.csv', skiprows=0, header=0)
# # d_2019 = d_2019[['id', 'acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence', 'track_popularity', 'artist_popularity', 'year', 'hit']]
# # d_2019.to_csv('2019_data.csv', index=False)
# # print(len(all_ids))
# all_ids.update(d_2016['id'])
# all_ids.update(d_2019['id'])
# print(len(all_ids))


#only keep the songs which are from between 2016-2019

# nh = os.listdir('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/nonhits/')

data = []
# hp_all_ids = set()
# for file in nh:
#     if not file.startswith('.'):
#         # print(file)
#         ids = get_track_ids('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/nonhits/'+file)
#         hp_all_ids.update(ids)
# # print(hp_all_ids)
# print(len(hp_all_ids))

# no_hits = hp_all_ids - all_ids
# print(len(no_hits))
# no_hits = list(no_hits)
nonhit_ids = pd.DataFrame(pd.read_csv('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/clean_data/nonhit_ids.csv', header=0))
no_hits = list(nonhit_ids['0'])
#only keep the songs which are from between 2016-2019
print('hi')
for i in range(len(no_hits)//50 + 1):
    prev = 50*(i)
    next100 = 50*(i+1)
    # print(prev, next100)
    if next100 >= len(no_hits):
        # print(no_hits[next100:])
        print('hi last 50')
        track_info = spotify.tracks(no_hits[prev:])

        print(track_info)
        features1 = spotify.audio_features(no_hits[prev:])
        # print(track_info)
    else:
        # print("hi")
        features1 = spotify.audio_features(no_hits[prev:next100])
        track_info = spotify.tracks(no_hits[prev:next100])
        # print(track_info['tracks'][0])
    # print(features1[0])
    # print(track_info)
    for i in range(len(features1)):
    	if features1[i]:
            features1[i]['year'] = int(track_info['tracks'][i]['album']['release_date'].split('-')[0])
            track_info['tracks'][i].pop('album')
            art_ids = [art['id'] for art in track_info['tracks'][i]['artists']]
            features1[i]['artist_popularity'] = avg_artist_popularity(art_ids)
            # track_info['tracks'][i].pop('release_date_precision')
            # features1[i].update(track_info['tracks'][i])
            features1[i]['track_popularity'] = track_info['tracks'][i]['popularity']
            # print(features1[i])
    # print(features1)
    # features1.pop('analysis_url')
    # features1.pop('external_urls')
            print(i)
            data += features1[i] 
# print(data


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

arr_data = pd.DataFrame([d for d in data if d]).drop(['analysis_url','uri','track_href'], axis=1)
arr_data.to_csv('/Users/hlotfy/spotifyhitpredictor/CS305 Final Project/no_hits_data_more.csv', encoding='utf-8-sig', index=False)
print(arr_data)

arr_data['hit'] = 0
arr_data = arr_data[arr_data.hit > 2015]
arr_data.to_csv('/Users/hlotfy/spotifyhitpredictor/CS305 Final Project/no_hits_data_more.csv', encoding='utf-8-sig', index=False)

# flattener = lambda t: flatten_dict(t)
# vfunc = np.vectorize(flattener)

# # data = vfunc(arr_data[arr_data!=None])
# data = [flatten_dict(d) for d in data if d]
# print(data)
# no_hits_df = pd.DataFrame(data).drop(['available_markets', 'analysis_url', 'uri', 'type', 'track_number', 'disc_number', 'spotify', 'href', 'track_href','preview_url','explicit','is_local','isrc','name'],axis=1)
# print(no_hits_df)
# no_hits_df['hit'] = 0
# # no_hits_df.to_csv('/Users/hlotfy/spotifyhitpredictor/CS305 Final Project/no_hits_data_more.csv', encoding='utf-8-sig')
# no_hits_df.to_csv('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/nonhits_dataa.csv', encoding='utf-8-sig', index=False)
# no_hits_df = no_hits_df[no_hits_df.year > 2015]
# # no_hits_df.rename({"popularity":"track_popularity"})
# no_hits_df = no_hits_df[['id', 'acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence', 'track_popularity', 'artist_popularity', 'year', 'hit']]
# no_hits_df.to_csv('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/nonhits_dataa_.csv', encoding='utf-8-sig', index=False)

# feat = list(no_hits_df.columns)
# print(feat)
# 
# print(no_hits_df.head())