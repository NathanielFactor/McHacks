from flask import Flask, request, url_for, redirect, session, render_template
from flask import session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import sklearn
import numpy as np
import pickle

app = Flask(__name__)
app.secret_key = "super-secret-key"
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'
TOKEN_INFO = 'token_info'
CLIENT_ID = "e454cfe7332648138c6cd894bede3ea9"
CLIENT_SECRET = "dfb2a085a05e4a71bfa60d263a5e4d45"
USER_ID = "Nathaniel Factor"


JournalEntries = []

@app.route('/')
def index():
    return render_template('index.html',
                           token = TOKEN_INFO,
                           journalEntries = JournalEntries,
                           )

@app.route('/calendar')
def calendar():
    return render_template('calendar.html',
                           token = TOKEN_INFO,
                           journalEntries = JournalEntries,
                           )

@app.route('/journal')
def journal():
    return render_template('journal.html',
                           token = TOKEN_INFO,
                           journalEntries = JournalEntries,)

@app.route('/playlist')
def playlist():
    return render_template('playlist.html',
                           token = TOKEN_INFO,
                           journalEntries = JournalEntries,)

@app.route('/login')
def login():
     return render_template('login.html',
                            token = TOKEN_INFO,
                           journalEntries = JournalEntries,)


@app.route('/auth')
def authenticate():
    print('hello')
    auth_url = create_spotify_oauth().get_authorize_url()
    
    print(TOKEN_INFO)

    print(auth_url)

    time.sleep(2)

    return redirect(auth_url)

@app.route('/callback')
def callback():

    print(request.values)

    print("THIS IS THE CODE")
    code = request.values.get('code')
    print(code)

    print("THIS IS THE END OF THE CODE")
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info

    print(session[TOKEN_INFO])

    return redirect(url_for('generatePlaylist'))

@app.route('/generatePlaylist')
def generatePlaylist():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect('/callback')
    
    sp = spotipy.Spotify(auth=session.get(TOKEN_INFO)['access_token'])
    user_id = sp.current_user()['id']
    print(user_id)

    trackURIs, tracks = getTracks("sad", sp)
    features = getAudioFeatures(sp, trackURIs)

    model = pickle.load(open("model.sav", 'rb'))

    createPlaylist(sp, user_id, trackURIs, features, "sad", model)



    return("success")


def getTracks(mood, sp):
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect('/callback')
    
    results = []
    trackURIs = []
    tracks = []

	#total number of tracks to get
    numTracks = 500
    #max objects allowed for one API call
    maxObjects = 50
    #get numTracks most recent saved tracks from user
    for i in range(numTracks//maxObjects):
        savedTracks = sp.current_user_saved_tracks(limit=maxObjects, 
                                                offset=i*maxObjects)
        if (savedTracks != None):
            results.append(savedTracks)
        '''
        results.append(sp.current_user_top_tracks(limit=maxObjects, 
                                                    offset=i*maxObjects))
        '''
    #analyze information about songs
    for item in results:
        for info in item['items']:
            '''
            trackURIs.append(info['uri'])
            tracks.append(info['name'] + " by " + info['artists'][0]['name'])
            '''
            trackURIs.append(info['track']['uri'])
            tracks.append(info['track']['name'] + " by " +
                                info['track']['artists'][0]['name'])
    return trackURIs, tracks

def getAudioFeatures(sp, trackURIs):
    features = []
    featuresTotal = []
    #max number of API calls
    max = 100
    for i in range(0, len(trackURIs), max):
		#get audio features of max tracks at once
        audioFeatures = sp.audio_features(trackURIs[i:i+max])
        #space time between API calls
        time.sleep(1)
        for j in range(len(audioFeatures)):
            if (audioFeatures != None):
                features.append(audioFeatures[j]['danceability'])
                features.append(audioFeatures[j]['energy'])
                features.append(audioFeatures[j]['valence'])
                features.append(audioFeatures[j]['loudness'])
                featuresTotal.append(features)
            features = []
    return featuresTotal

def createPlaylist(sp, userID, trackURIs, features, mood, model):
	featuresArray = np.asarray(features, dtype=np.float32)
	predictions = model.predict(featuresArray)
	songs = []
	playlistSongs = []

	#get all songs that match user's current mood and adds
	#up to 30 of them to playlist
	for i in range(len(predictions)):
		if (predictions[i] == mood):
			playlistSongs.append(trackURIs[i])
		if (len(playlistSongs) >= 30):
			break
	#create new playlist for user
	playlist = sp.user_playlist_create(userID,name=mood,public=True)
	playlistID = playlist['id']
	#add songs to playlist
	sp.user_playlist_add_tracks(userID, playlistID, playlistSongs)

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        redirect(url_for('login'))
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        token_info = create_spotify_oauth().refresh_access_token(token_info['refresh_token'])

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri= 'http://127.0.0.1:5000/callback',
        scope="user-library-read playlist-modify-public playlist-modify-private user-read-recently-played user-top-read"
    )


AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1"

if __name__ == '__main__':
    app.run(debug=True)