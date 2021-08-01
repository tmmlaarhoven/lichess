import requests
import json
import ndjson
import time
import math
import matplotlib.pyplot as mpl
from matplotlib.colors import BoundaryNorm, LogNorm
from matplotlib.ticker import MaxNLocator
import numpy as np

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

# Initialize empty matchup dictionary
MatchesDict = dict()
for User1 in PlayersDict:
	MatchesDict[User1.lower()] = dict()
	for User2 in PlayersDict:
		MatchesDict[User1.lower()][User2.lower()] = dict()

# Load past match scores
with open("matches.txt", "r") as MatchesFile:
	for Line in MatchesFile:
		Parts = Line.split(",", 2)
		if (Parts[0].lower() in PlayersDict) and (Parts[1].lower() in PlayersDict):
			MatchesDict[Parts[0].lower()][Parts[1].lower()] = json.loads(Parts[2])


# Expand one by one
for Index1, User1 in enumerate(PlayersDict):
	#if (Index1 >= 10):
	#	break
	
	print(f"-------------------\nDoing {User1}.")
		
	# Loop over other previous candidates
	for Index2, User2 in enumerate(PlayersDict):
		if Index2 >= Index1:
			break
		
		if "Games" in MatchesDict[User1][User2]:
			print(f"\nRivalry: {User1} vs. {User2} -- Already processed.")
			print(f"Rivalry: {User1} vs. {User2} -- Overall score: {MatchesDict[User1][User2]['Score'][0]} - {MatchesDict[User1][User2]['Score'][1]}.")
			continue
		
		MatchesDict[User1][User2] = dict()
		MatchesDict[User2][User1] = dict()
		MatchesDict[User1][User2]["Games"] = 0
		MatchesDict[User2][User1]["Games"] = 0
		MatchesDict[User1][User2]["Score"] = [0, 0]
		MatchesDict[User2][User1]["Score"] = [0, 0]
		
		print(f"\nRivalry: {User1} vs. {User2} -- Downloading...")
		
		s = requests.Session()
		with s.get(f"https://lichess.org/api/games/user/{User1}?vs={User2}&perfType=bullet&pgnInJson=false&tags=true", headers = {"Authorization": f"Bearer {APIToken}", "Accept": "application/x-ndjson"}, stream = True) as Response:
			for Line in Response.iter_lines():
				GameInfo = json.loads(Line)
				#print(GameInfo)
				
				# Weird exception?
				if "id" not in GameInfo or "winner" not in GameInfo and GameInfo["status"] not in {"draw", "outoftime", "timeout", "stalemate"}:
					print("Hmmm?")
					print(GameInfo)
					time.sleep(100000)
					
				print(f"{GameInfo['id']}: {GameInfo['players']['white']['user']['id']} vs. {GameInfo['players']['black']['user']['id']}: {GameInfo.get('winner', 'draw')}.")
				
				# Parse text as white's score
				GameResult = GameInfo.get("winner", "draw")
				if GameResult == "white":
					GameScore = 1.0
				elif GameResult == "draw":
					GameScore = 0.5
				else: # GameResult == "black":
					GameScore = 0.0
				
				# Store game result in user scores
				MatchesDict[User1][User2]["Games"] = MatchesDict[User1][User2]["Games"] + 1
				MatchesDict[User2][User1]["Games"] = MatchesDict[User2][User1]["Games"] + 1
				if GameInfo["players"]["white"]["user"]["id"].lower() == User1.lower():
					MatchesDict[User1][User2]["Score"][0] += GameScore
					MatchesDict[User1][User2]["Score"][1] += (1 - GameScore)
					MatchesDict[User2][User1]["Score"][0] += (1 - GameScore)
					MatchesDict[User2][User1]["Score"][1] += GameScore
				else:
					MatchesDict[User1][User2]["Score"][0] += (1 - GameScore)
					MatchesDict[User1][User2]["Score"][1] += GameScore
					MatchesDict[User2][User1]["Score"][0] += GameScore
					MatchesDict[User2][User1]["Score"][1] += (1 - GameScore)
					
		print(f"Rivalry: {User1} ({Index1}) vs. {User2} ({Index2}) -- Overall score: {MatchesDict[User1][User2]['Score'][0]} - {MatchesDict[User1][User2]['Score'][1]}.")
		
		# Store results in files immediately
		with open("matches.txt", "a") as SaveFile:
			SaveFile.write(f"{User1},{User2},{json.dumps(MatchesDict[User1][User2])}\n")
			SaveFile.write(f"{User2},{User1},{json.dumps(MatchesDict[User2][User1])}\n")
		
		time.sleep(2)

	print(f"\nFinished {User1}.\n")

	#time.sleep(10)
	
	

# Write final matches to file
with open("matches-new.txt", "w") as MatchesFile2:
	for Index1, User1 in enumerate(PlayersDict):
		#if Index1 >= 10:
		#	break
		for Index2, User2 in enumerate(PlayersDict):
			if Index2 >= Index1:
				break
			MatchesFile2.write(f"{User1},{User2},{json.dumps(MatchesDict[User1][User2])}\n")
			MatchesFile2.write(f"{User2},{User1},{json.dumps(MatchesDict[User2][User1])}\n")
	

