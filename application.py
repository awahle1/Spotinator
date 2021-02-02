from flask import Flask, render_template, request, jsonify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyAuthBase
import spotipy.util as util
import json
import math

#znkum3uqbtji62g19resp3pwf


app = Flask(__name__)
cid = "4bbc1af5981941e498953237e9b31b32"
secret = "f38a971769a74d6fab8f5655af2784e5"
username = None

read = None
control = None

votes = 0
members = 0
required = 0


def make_auths(username):
	global read
	global control
	
	scope = 'user-read-currently-playing'
	token = util.prompt_for_user_token(username, scope,client_id=cid,client_secret=secret,redirect_uri='http://127.0.0.1:9090')
	read = spotipy.Spotify(auth=token)

	scope = 'streaming'
	token = util.prompt_for_user_token(username, scope,client_id=cid,client_secret=secret,redirect_uri='http://127.0.0.1:9090')
	control = spotipy.Spotify(auth=token)

def get_required(members):
	required = math.ceil(float(members+1)*.8)
	return(required)




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
	global members
	username = request.form.get("username")
	make_auths(username)
	current_track = read.current_user_playing_track()['item']['name']
	
	members = 1
	return render_template("session.html", track = current_track)

@app.route("/session_member")
def session_member():
	global members
	global votes
	current_track = read.current_user_playing_track()['item']['name']
	members +=1
	required = get_required(members)
	return render_template("session_member.html", track = current_track)

@app.route("/vote", methods=['post'])
def vote():
	global members
	global votes
	global required

	required = math.ceil(float(members+1)*.8)
	value = request.form.get("value")
	votes += int(value)

	current_track = read.current_user_playing_track()['item']['name']


	if votes>=required:
		control.next_track()
		current_track = read.current_user_playing_track()['item']['name']
		votes = 0
		response = {'count': votes, 'members': required, 'reset' :'yes', 'track': current_track}
	else:
		response = {'count': votes, 'members': required, 'reset': "no", 'track': current_track}

	
	return (json.dumps(response))	



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