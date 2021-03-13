import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy.util as util
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        scope = "user-library-read"
        username = 'duskippy-us'
        token = util.prompt_for_user_token(username, scope)

        if token:
            sp = spotipy.Spotify(auth=token)
            playlist_names = get_user_playlists(sp)
            return render_template('user.html', playlist_names=playlist_names)
    return render_template('login.html')


@app.route('/match/<other_user_name>/<playlist_id>', methods=['GET', 'POST'])
def process_user_input(other_user_name, playlist_id):
    scope = "user-library-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    print(playlist_id)
    user_playlist = sp.playlist(playlist_id)

    playlist_matches = compare_user_playlists(sp, user_playlist, other_user_name)

    return render_template('matches.html', playlist_matches=playlist_matches)

'''def get_user_playlist():
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp, sp.user_playlist('duskippy-us', '5PDSnjHBlEtgQckJijqKXF')
'''


def get_user_playlists(sp):
    playlists = []
    user_info = sp.me()
    playlists_info = sp.user_playlists(user_info['id'])
    for playlist in playlists_info['items']:
        playlists.append({'id': playlist['id'], 'name': playlist['name']})
        print(playlist)
    return playlists


def create_track_key(track):
    artist_name = ''
    for artist in track['artists']:
        artist_name += artist['name']
    return artist_name + ':' + track['album']['name'] + ':' + track['name']


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

# keys are in the form 'artist name':'album name':'track name'


def compare_user_playlists(sp, user1_playlist, user2):
    curr_offset = 0
    limit = 50
    playlist_match_entry_list = []
    while True and curr_offset <= 200:
        user2_playlist_page = sp.user_playlists(user2, limit, curr_offset)
        for playlist in user2_playlist_page['items']:
            # print(playlist['name'])
            match_entry = get_playlist_commonality(sp, user1_playlist, playlist)
            if match_entry and match_entry['num_matches'] > 0:
                playlist_match_entry_list.append(match_entry)
        curr_offset += 50
        if len(user2_playlist_page['items']) < 50:
            break
    return playlist_match_entry_list


def get_playlist_commonality(sp, playlist1, playlist2):
    playlist1_keys = get_playlist_keys(sp, playlist1)
    playlist2_keys = get_playlist_keys(sp, playlist2)

    matching_keys = playlist1_keys.intersection(playlist2_keys)
    if len(matching_keys) > 0:
        print(len(matching_keys), playlist2['name'], matching_keys)
        print(playlist2['images'])
        img_url = len(playlist2['images']) and playlist2['images'][0]['url'] or ''
        return {'img_url': img_url, 'num_matches': len(matching_keys), 'other_playlist_name': playlist2['name'],
                'common_songs': matching_keys}

#print(results['items'])

def fetch_playlist():
    while playlists:
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


""" for uri in pl_ids:

           results = self.sp.user_playlist_tracks(uri.split(':')[2], uri.split(':')[4])
           tracks = results['items']

           # Loops to ensure I get every track of the playlist
           while results['next']:
               results = self.sp.next(results)
               tracks.extend(results['items'])

       return tracks """


def main():

    app.run(debug=True)
    home()
    test1, test2 = get_user_playlist2()
    print(test1, test2)
    # user, user_playlist = get_user_playlist()
    # compare_user_playlists(user, user_playlist, 'maxroloff')

main()