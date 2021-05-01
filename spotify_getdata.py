# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 19:11:41 2021

@author: Ashley
"""

import requests
#acess token 
CLIENT_ID = '2cac90860dea4fd196a6b398b2bc806d'
CLIENT_SECRET = '682f6c6ea0ac416596e608472a9b66ba'
AUTH_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/'
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})
auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}
# pull all artists albums
artist_id = '6TIYQ3jFPwQSRmorSezPxX'
r = requests.get(BASE_URL + 'artists/' + artist_id + '/albums', 
                 headers=headers, 
                 params={'include_groups': 'album', 'limit': 50})
d = r.json()


data = []   # will hold all track info
albums = [] # to keep track of duplicates
for album in d['items']:
    album_name = album['name']

    #skip over albums we've already grabbed
    trim_name = album_name.split('(')[0].strip()
    if trim_name.upper() in albums:
        continue
    albums.append(trim_name.upper()) # use upper() to standardize
    
    # this takes a few seconds so let's keep track of progress    
    #print(album_name)
    
    # pull all tracks from this album
    r = requests.get(BASE_URL + 'albums/' + album['id'] + '/tracks', 
        headers=headers)
    tracks = r.json()['items']
    
    for track in tracks:
        # get audio features (key, liveness, danceability, ...)
        f = requests.get(BASE_URL + 'audio-features/' + track['id'], 
            headers=headers)
        f = f.json()
        
        # combine with album info
        f.update({
            'track_name': track['name'],
            'album_name': album_name,
            'short_album_name': trim_name,
            'release_date': album['release_date'],
            'album_id': album['id']
        })
        
        data.append(f)

import pandas as pd
df = pd.DataFrame(data)
df['release_date'] = pd.to_datetime(df['release_date'])
df = df.sort_values(by='release_date')

df.to_csv('C:\\Users\\Ashley\\Documents\\GitHub\\Spotify\\spotify.csv', index=False)