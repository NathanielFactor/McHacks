'''
This file gets the 500 most recent tracks saved to a user's profile. 
It uses the already trained machine learning model and mood of the 
listener to create a new playlist with up to 30 songs that fit the user's 
current mood that is titled with the current mood. 
If a playlist with that name already already exists, a new playlist will 
be created and named "mood" 2. 
'''

#Load libraries
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import os

import sys
import csv
import pickle
import numpy as np
import time

#Tries to obtain username from terminal 

username = "midgetlaser"

scopes = ("user-read-recently-played")

token = util.prompt_for_user_token(username,scopes,
								   client_id='e454cfe7332648138c6cd894bede3ea9',
								   client_secret='dfb2a085a05e4a71bfa60d263a5e4d45',
								   redirect_uri='http://127.0.0.1:5000/callback')
print(token)