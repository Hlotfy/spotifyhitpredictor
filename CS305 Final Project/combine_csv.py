import numpy as np 
import pandas as pd
import spotipy
import os
import spotipy.oauth2 as Auth 

# total = pd.DataFrame(pd.read_csv('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/clean_data/even_more_tracks.csv'))
# d16 = pd.DataFrame(pd.read_csv('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/clean_data/2016_data.csv'))
# d17 = pd.DataFrame(pd.read_csv('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/clean_data/2017_data.csv'))
# d18 = pd.DataFrame(pd.read_csv('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/clean_data/2018_data.csv'))
# d19 = pd.DataFrame(pd.read_csv('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/clean_data/2019_data.csv'))
# hit_ids = set(d16['id'])
# hit_ids.update(d17['id'])
# hit_ids.update(d18['id'])
# hit_ids.update(d19['id'])
# print(len(hit_ids))
# df = pd.DataFrame(list(hit_ids))
# print(df.head())
# df.to_csv('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/clean_data/hit_ids.csv', encoding='utf-8-sig',index=False)

def get_track_ids(filename):
    DATA = pd.read_csv(filename, skiprows=0, header=1)
    data = np.asarray(DATA)
    track_links = list(data[:, 0])
    track_ids = [link.split(':')[-1] for link in track_links]
    return track_ids

nh = os.listdir('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/nonhits/')

hit_ids = pd.DataFrame(pd.read_csv('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/clean_data/hit_ids.csv', header=0))
# print(hit_ids['0'])
set_hi = set(hit_ids['0'])
print(len(set_hi))
nonhit_ids = pd.DataFrame(pd.read_csv('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/clean_data/nonhit_ids.csv', header=0))
set_nhi = set(nonhit_ids['0'])
print(len(set_nhi))
thi = set_nhi - set_hi
print(len(thi))
# data = []
# hp_all_ids = set()
# for file in nh:
#     if not file.startswith('.'):
#         # print(file)
#         ids = get_track_ids('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/nonhits/'+file)
#         hp_all_ids.update(ids)
# # print(hp_all_ids)
# print(len(hp_all_ids))
# nh_df = pd.DataFrame(list(hp_all_ids))
# print(nh_df.head())
pd.DataFrame(thi).to_csv('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/clean_data/nonhit_ids.csv', encoding='utf-8-sig',index=False)
# more = pd.DataFrame(pd.read_csv('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/no_hits_data_morer_f.csv'))
# total = total[['id', 'acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence', 'track_popularity', 'artist_popularity', 'year', 'hit']]
# # more = more[more.year > 2015]
# print(len(total))
# # more.to_csv('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/no_hits_data_morer.csv', encoding='utf-8-sig')
# complete = pd.concat([total,more],axis=0)
# # complete.drop(['Unnamed: 0'])
# print(complete.head())
# total_len = len(complete)
# print(len(complete))
# total_nonhit = len(complete[complete.hit==0])
# print(total_nonhit)
# total.to_csv('/Users/halalotfy/CS305/spotifyhitpredictor/CS305 Final Project/clean_data/even_more_tracks.csv', encoding='utf-8-sig',index=False)
# id_set = set(total['id'])
# print(len(id_set))
# total = total[total['id'].isin(id_set)]
# print(len(total))