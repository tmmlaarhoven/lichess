import requests
import json
import ndjson
import time
import math
import datetime
import pytz
import os

with open("E:\\lichess\\APIToken.txt", "r") as TokenFile:
	for Line in TokenFile:
		APIToken = Line.strip()

# Load list of players in order of relevance
PlayersDict = dict()
with open("2021-06--bullet-ladder-newer.ndjson", "r") as PlayerListFile:
	for Line in PlayerListFile:
		Dictio = json.loads(Line)
		PlayerID = Dictio["Username"].lower()
		PlayersDict[PlayerID] = Dictio

# Giant loop
for User in PlayersDict:		
	FromYear = 2001
	FromMonth = 1	# First month, not included
	ToYear = 2021
	ToMonth = 7		# Final month, included

	if FromMonth < 12:
		Start = round(1000 * datetime.datetime(FromYear,FromMonth+1,1,0,0,0,0,pytz.UTC).timestamp())
	else:
		Start = round(1000 * datetime.datetime(FromYear+1,1,1,0,0,0,0,pytz.UTC).timestamp())
	if ToMonth < 12:
		End = round(1000 * datetime.datetime(ToYear,ToMonth+1,1,0,0,0,0,pytz.UTC).timestamp())
	else:
		End = round(1000 * datetime.datetime(ToYear+1,1,1,0,0,0,0,pytz.UTC).timestamp())
	Matches = dict()

	# Process all bullet games 
	s = requests.Session()
	with s.get(f"https://lichess.org/api/games/user/{User}?since={Start}&until={End}&rated=true&perfType=bullet&moves=false&pgnInJson=false&tags=true", headers = {"Authorization": f"Bearer {APIToken}", "Accept": "application/x-ndjson"}, stream = True) as Response:
		for Line in Response.iter_lines():
			GameInfo = json.loads(Line)
			GameDate = datetime.datetime.fromtimestamp(round(GameInfo["createdAt"] / 1000))
			print(f"{GameDate.strftime('%m/%d/%Y, %H:%M:%S')}: {json.dumps(GameInfo)}")

			# Weird exception?
			if "id" not in GameInfo or "winner" not in GameInfo and GameInfo["status"] not in {"draw", "outoftime", "timeout", "stalemate"}:
				print("Hmmm?")
				print(GameInfo)
				time.sleep(100000)
					
			print(f"{GameInfo['id']}: {GameInfo['players']['white']['user']['id']} vs. {GameInfo['players']['black']['user']['id']}: {GameInfo.get('winner', 'draw')}.")
				
			# Parse text as white's score
			GameResult = GameInfo.get("winner", "draw")
			if GameResult == "white":
				WhiteScore = 1.0
			elif GameResult == "draw":
				WhiteScore = 0.5
			else: # GameResult == "black":
				WhiteScore = 0.0

			# Establish opponent's name
			UserIsWhite = False
			OppID = GameInfo["players"]["white"]["user"]["id"]
			OppName = GameInfo["players"]["white"]["user"]["name"]
			if OppID == User.lower():
				UserIsWhite = True
				OppID = GameInfo["players"]["black"]["user"]["id"]
				OppName = GameInfo["players"]["black"]["user"]["name"]
			
			# Initialize empty dictionary for new matches
			if OppID not in Matches:
				Matches[OppID] = {"Games": 0, "Score": 0, "First": 3000000000000, "FirstID": "xxxxxxxx", "Last": 1000000000000, "LastID": "yyyyyyyy", "RatingDiff": [0, 0], "Username": OppName}
			
			# Store game result in user scores
			Matches[OppID]["Games"] = Matches[OppID]["Games"] + 1
			if UserIsWhite:
				Matches[OppID]["Score"] += WhiteScore
				Matches[OppID]["RatingDiff"][0] += GameInfo["players"]["white"]["ratingDiff"]
				Matches[OppID]["RatingDiff"][1] += GameInfo["players"]["black"]["ratingDiff"]
			else:
				Matches[OppID]["Score"] += (1 - WhiteScore)
				Matches[OppID]["RatingDiff"][0] += GameInfo["players"]["black"]["ratingDiff"]
				Matches[OppID]["RatingDiff"][1] += GameInfo["players"]["white"]["ratingDiff"]
				
			# Potentially update first/last game times
			if Matches[OppID]["First"] > GameInfo["createdAt"]:
				Matches[OppID]["First"] = GameInfo["createdAt"]
				Matches[OppID]["FirstID"] = GameInfo["id"]
			if Matches[OppID]["Last"] < GameInfo["createdAt"]:
				Matches[OppID]["Last"] = GameInfo["createdAt"]
				Matches[OppID]["LastID"] = GameInfo["id"]
				
		
	# Store final match scores to file
	if not os.path.exists(f"{Year}\\{Month}\\"):
		os.makedirs(f"{Year}\\{Month}\\")

		
	with open(f"{Year}\\{Month}\\{Year}-{Month}-{User}.ndjson", "w") as OutFile:
		for OppID, Dict in sorted(Matches.items(), key = lambda item: item[1]["Username"].lower()):
			OutFile.write(json.dumps(Dict) + "\n")

	with open(f"{Year}\\{Month}\\{Year}-{Month}-{User}-favorites.ndjson", "w") as OutFile:
		for OppID, Dict in sorted(Matches.items(), key = lambda item: item[1]["Games"], reverse = True):
			OutFile.write(json.dumps(Dict) + "\n")
