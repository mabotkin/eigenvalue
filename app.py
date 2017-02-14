from flask import Flask, redirect, render_template, request
from flask_socketio import SocketIO, emit
import uuid
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
	games[ID] = {"players":{},"data":{}}
	return redirect("/games/" + ID)

@app.route("/games/<game_ID>")
def gameRoom(game_ID):
	if game_ID in games:
		return render_template("game.html", gameID = game_ID)
	else:
		return render_template("notfound.html", gameID = game_ID)

@socketio.on("joinGame")
def join_Game(data):
	print request.sid + " joined game"
	if request.sid not in games[data["id"]]["players"]:
		newPlayer = {}
		newPlayer["username"] = data["name"]
		newPlayer["score"] = 0
		games[data["id"]]["players"][request.sid] = newPlayer
		for user in games[data["id"]]["players"]:
			emit("update",games[data["id"]]["players"], room=user)
		print games

@socketio.on("disconnect")
def disc():
	print request.sid + " left game"
	for game in games:
		if request.sid in games[game]["players"]:
			games[game]["players"].pop(request.sid,None)
			for user in games[game]["players"]:
				emit("update",games[game]["players"], room=user)
	print games

if __name__ == "__main__":
    socketio.run(app,port=5001, debug=True)
