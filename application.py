from flask import Flask, render_template, request, jsonify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyAuthBase
import spotipy.util as util
import json

#znkum3uqbtji62g19resp3pwf


app = Flask(__name__)
cid = "4bbc1af5981941e498953237e9b31b32"
secret = "f38a971769a74d6fab8f5655af2784e5"
username = None

read = None
control = None


def make_auths(username):
	global read
	global control
	
	scope = 'user-read-currently-playing'
	token = util.prompt_for_user_token(username, scope,client_id=cid,client_secret=secret,redirect_uri='http://127.0.0.1:9090')
	read = spotipy.Spotify(auth=token)

	scope = 'streaming'
	token = util.prompt_for_user_token(username, scope,client_id=cid,client_secret=secret,redirect_uri='http://127.0.0.1:9090')
	control = spotipy.Spotify(auth=token)





@app.route("/")
def index():
	return render_template("index.html")

@app.route("/create")
def create():
	return render_template("create.html")

@app.route("/join")
def join():
	return render_template("join.html")

@app.route("/pausePlay", methods=['post'])
def pause_play():
	value = request.form.get("value")
	print("-----------------------------------")
	print(value)
	if value == "play":
		control.start_playback()
		response = {'word':'pause'}
	else:
		control.pause_playback()
		response = {'word':'play'}

	return (json.dumps(response))

@app.route("/session", methods=['post'])
def session():
	global username
	username = request.form.get("username")
	make_auths(username)
	current_track = read.current_user_playing_track()['item']['name']
	return render_template("session.html", track = current_track)



	# @app.route("/playlists", methods=["POST"])
# def playlists():
# 	global username
# 	username = request.form.get("username")
# 	make_auths(username)
# 	#get all of the user's playlists
	
# 	playlists_raw = read.current_user_playlists()['items']
# 	playlists = []
# 	for playlist in playlists_raw:
# 		playlists.append(playlist['name'])




# 	return render_template("playlists.html", playlists = playlists)