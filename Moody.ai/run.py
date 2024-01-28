from flask import Flask, request, url_for, redirect, session, render_template, jsonify
from flask import session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import sklearn
import datetime
import numpy as np
import pickle
import htmloperations as htop
import bot2
import random
import pandas
import csv

app = Flask(__name__)
app.secret_key = "super-secret-key"
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'
TOKEN_INFO = 'token_info'
CLIENT_ID = "e454cfe7332648138c6cd894bede3ea9"
CLIENT_SECRET = "dfb2a085a05e4a71bfa60d263a5e4d45"
user_id = "midgetlaser"

def get_current_year():
    current_year = datetime.datetime.now().year
    return (current_year)

def get_current_month():
    current_month = datetime.datetime.now().month
    return (current_month)





def get_message_by_date(date):
    JOURNAL_ENTRIES = htop.get_messages_by_month(user_id, get_current_year(), get_current_month())
    print(JOURNAL_ENTRIES)
    for entry in JOURNAL_ENTRIES:
       print (entry)
       if entry[3] == date:
           return entry[2]
    return None

def get_mood_by_date(date):
    JOURNAL_ENTRIES = htop.get_messages_by_month(user_id, get_current_year(), get_current_month())
    for entry in JOURNAL_ENTRIES:
       if entry[3] == date:
           return entry[1]
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calendar')
def calendar():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect(url_for('login'))
    return render_template('calendar.html',
                           
                           )
@app.route('/submit', methods=['POST'])
def submit_entry():
    data = request.json
    date = data.get('date')
    concatenated_values = data.get('concatenatedValues')
    print(date)
    print(concatenated_values)
    htop.addMessage(user_id, concatenated_values, date)
    # Save to database (example code, depends on your database setup)
    return jsonify({"success": True, "message": "Data saved successfully."})

@app.route('/get_message')
def get_message():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        data = {'message': 'login'}
        return jsonify(data)
    date = request.args.get('date')
    message = get_message_by_date(date)
    print(message)
    mood = get_mood_by_date(date)  
    print(mood)
    if message:
        data ={'message': message, 'mood': mood}
        return jsonify(data)  # Assuming the column name is 'content'
    else:
        data = {'message': 'No message for this date'}
        return jsonify(data)

@app.route('/journal')
def journal():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect(url_for('login'))
    return render_template('journal.html',
                           
                           )



@app.route('/playlist')
def playlist():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect(url_for('login'))
    
    sp = spotipy.Spotify(auth=session.get(TOKEN_INFO)['access_token'])
    user_id = sp.current_user()['id']
    print(user_id)

    id = request.args.get('id')

    return render_template('playlist.html', id=id)

@app.route('/genPlaylist', methods=['GET'])
def genPlaylist():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect(url_for('login'))
    
    sp = spotipy.Spotify(auth=session.get(TOKEN_INFO)['access_token'])
    user_id = sp.current_user()['id']
    print(user_id)

    date = request.args.get('date')
    mood = get_mood_by_date(date)

    trackURIs, tracks = getTracks(mood, sp)
    features = getAudioFeatures(sp, trackURIs)

    model = pickle.load(open("model.sav", 'rb'))
    

    id = createPlaylist(sp, user_id, trackURIs, features, mood, date, model)

    return redirect(url_for('playlist', id=id))
                           

@app.route('/login')
def login():
     return render_template('login.html')


@app.route('/auth')
def authenticate():
    print('hello')
    auth_url = create_spotify_oauth().get_authorize_url()
    print(TOKEN_INFO)
    print(auth_url)
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

    return redirect(url_for('index'))


def getTracks(mood, sp):
    
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

def load_csv_and_select_uris_random(csv_file, mood, num_entries):
    dataset = pandas.read_csv("spotifyIds.csv")
    dataset = pandas.Series.tolist(dataset)
    all_entries = []
    for elem in dataset:
        res = elem[0].strip('][').replace("'", "").split(', ')
        if res[1] == mood:
            all_entries.append(res[0])


    # Shuffle the list of URIs to randomize the selection
    random.shuffle(all_entries)

    return all_entries[:num_entries]

def createPlaylist(sp, userID, trackURIs, features, mood, date, model):
    featuresArray = np.asarray(features, dtype=np.float32)
    predictions = model.predict(featuresArray)
    songs = []
    playlistSongs = []
    #get all songs that match user's current mood and adds
    #up to 30 of them to playlist
    for i in range(len(predictions)):
        if (predictions[i] == mood):
            playlistSongs.append(trackURIs[i])
    
    if playlistSongs != []:
        # Shuffle the playlistSongs list to randomize the added tracks
        random.shuffle(playlistSongs)
        
        # Add up to 30 matching tracks to the playlist
        playlistSongs = playlistSongs[:30]
    else:
        playlistSongs = load_csv_and_select_uris_random('spotifyIds.csv', mood, 20)
        print(playlistSongs)

    print(playlistSongs)
    playlist = sp.user_playlist_create(userID,name="Your Mood "+date, public=True)
    playlistID = playlist['id']
    sp.user_playlist_add_tracks(userID, playlistID, playlistSongs) 
    return playlistID

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
    
@app.route('/api/generate-quote', methods=['POST'])
def generate_quote():
    # Get the message from the POST request.
    mood = request.args.get('prompt')    
    # Use your OpenAI integration to generate a response based on the prompt
    generated_response = bot2.ai_response(mood)

    return jsonify({'quote': generated_response})


AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1"

if __name__ == '__main__':
    app.run(debug=True)