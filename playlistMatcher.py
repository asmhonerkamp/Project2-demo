import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint


def get_user_playlist():
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp, sp.user_playlist('duskippy-us', '5PDSnjHBlEtgQckJijqKXF')


def create_track_key(track):
    return track['album']['name'] + ':' + track['name'] + ':' + track['artist']['name']


def get_playlist_keys(sp, playlist):
    playlist_tracks = sp.playlist_tracks(playlist['id'])
    playlist_keys = set()
    for track_obj in (playlist_tracks['items']):
        try:
            track_key = create_track_key(track_obj['track'])
            playlist_keys.add(track_key)
        except TypeError:
            pass
    return playlist_keys

# keys are in the form 'album name':'track name'


def search_all_spotify_playlists(sp, user_playlist):
    curr_offset = 0
    limit = 50
    while True:
        playlist_page = sp.user_playlists('spotify', limit, curr_offset)
        for playlist in playlist_page['items']:
            get_playlist_commonality(sp, user_playlist, playlist)
        curr_offset += 50
        if len(playlist_page['items']) < 50:
            break


def get_playlist_commonality(sp, playlist1, playlist2):
    playlist1_keys = get_playlist_keys(sp, playlist1)
    playlist2_keys = get_playlist_keys(sp, playlist2)

    matching_keys = playlist1_keys.intersection(playlist2_keys)
    if len(matching_keys) > 0:
        print(len(matching_keys), playlist2['name'], matching_keys)
        return len(matching_keys), playlist2['name'], matching_keys

#print(results['items'])
"""while playlists:
    comparison_playlist = set()
    for playlist in (playlists['items']):
        results = sp.playlist_tracks(playlist['id'])
        for item in (results['items']):
            try:
                comparison_playlist.add(item['track']['id'])
            except TypeError:
                print("can't add")
        matching_tracks_set = current_playlist_tracklist.intersection(comparison_playlist)
        if len(matching_tracks_set) > 0:
            print(len(matching_tracks_set), playlist['name'], matching_tracks_set)
            matching_tracks_set.clear()
        #print(results['items'])
        # print("%4d %s" % (i + 1 + playlists['offset'],  playlist['name']))
    '''if playlists['next']:
        playlists = sp.next(playlists)
    else:'''
    playlists = None
"""

""" for uri in pl_ids:

           results = self.sp.user_playlist_tracks(uri.split(':')[2], uri.split(':')[4])
           tracks = results['items']

           # Loops to ensure I get every track of the playlist
           while results['next']:
               results = self.sp.next(results)
               tracks.extend(results['items'])

       return tracks """


def main():
    user, user_playlist = get_user_playlist()
    search_all_spotify_playlists(user, user_playlist)

main()