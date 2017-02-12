from flask import Flask, redirect, render_template
from flask_socketio import SocketIO, join_room
import random

app = Flask(__name__)
socketio = SocketIO(app)

GAME_ID_LENGTH=6

games = {}

def genID(length):
	chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
	ID = ""
	for i in range(length):
		ID += random.choice(chars)
	return ID

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/newgame")
def newGame():
	ID = genID(GAME_ID_LENGTH)
	games[ID] = {}
	return redirect("/games/" + ID)

@app.route("/games/<game_ID>")
def gameRoom(game_ID):
	if game_ID in games:
		return render_template("game.html", gameID = game_ID)
	else:
		return render_template("notfound.html", gameID = game_ID)

@socketio.on("game")
def join_Game(data):
	join_room(data["id"])
	#games[data["id"]]
	# need to uniquely identify players

if __name__ == "__main__":
    socketio.run(app,port=5001, debug=True)
