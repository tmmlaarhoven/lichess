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


if True:
	# Expand the table
	
	Players = []
	PlayersDict = dict()
	with open("highestbulletsorted.txt", "r") as HighestFile:
		for Line in HighestFile:
			Players.append(json.loads(Line))
			PlayersDict[Players[-1]["Username"]] = 1
			
	with open("rivalries-all-triangle.txt", "r") as RivalriesFile:
		Completed = 0
		for Line in RivalriesFile:
			Completed = Completed + 1

	TableSize = 1000
	PlayerScores = []
	for Index1 in range(TableSize):
		PlayerScores.append([0 for _ in range(TableSize)])

	while True:
		print("\n\nDoing: " + Players[Completed]["Username"])
			
		Index1 = Completed
		User1 = Players[Completed]
		for Index2 in range(Index1):
			User2 = Players[Index2]
			print("\nRivalry: " + User1["Username"] + " vs. " + User2["Username"])
			s = requests.Session()
			with s.get(f"https://lichess.org/api/games/user/{User1['Username']}?vs={User2['Username']}&perfType=bullet&pgnInJson=false&tags=true", headers = {"Authorization": f"Bearer {APIToken}", "Accept": "application/x-ndjson"}, stream = True) as Response:
				for Line in Response.iter_lines():
					GameInfo = json.loads(Line)
					#print(GameInfo)
					
					# Weird exception?
					if "id" not in GameInfo or "winner" not in GameInfo and GameInfo["status"] not in {"draw", "outoftime", "timeout", "stalemate"}:
						print("Hmmm?")
						print(GameInfo)
						time.sleep(100000)
						
					print(GameInfo["id"] + ": " + GameInfo["players"]["white"]["user"]["id"] + " vs. " + GameInfo["players"]["black"]["user"]["id"] + ": " + GameInfo.get("winner", "draw"))
					
					# Parse text as white's score
					GameResult = GameInfo.get("winner", "draw")
					if GameResult == "white":
						GameScore = 1.0
					elif GameResult == "draw":
						GameScore = 0.5
					else:
						GameScore = 0.0
					
					# Store game result in user scores
					if GameInfo["players"]["white"]["user"]["id"].lower() == User1["Username"].lower():
						PlayerScores[Index1][Index2] += GameScore
						PlayerScores[Index2][Index1] += (1 - GameScore)
					else:
						PlayerScores[Index1][Index2] += (1 - GameScore)
						PlayerScores[Index2][Index1] += GameScore
			
			print("Rivalry: " + User1["Username"] + " vs. " + User2["Username"] + " -- Overall score: " + str(PlayerScores[Index1][Index2]) + " - " + str(PlayerScores[Index2][Index1]) + ".")
			
			time.sleep(5)		
	
	
		print("Appending to file...")
		
		with open("rivalries-all-triangle.txt", "a") as RivalriesFile:
			PlayerScoresWon = [str(PlayerScores[Index1][x]) for x in range(Index1)]
			PlayerScoresLost = [str(PlayerScores[x][Index1]) for x in range(Index1)]
			PlayerScoresGames = [str(PlayerScores[Index1][x] + PlayerScores[x][Index1]) for x in range(Index1)]
			Opponents = [Players[x]["Username"] for x in range(Index1)]
			RivalriesFile.write("{\"Number\": " + str(Index1 + 1) + ", \"Username\": \"" + User1["Username"] + "\", \"Highest\": " + str(User1["Highest"]) + ", \"Scores\": {")
			for x in range(Index1):
				RivalriesFile.write("\"" + Opponents[x] + "\": {\"Total\": " + PlayerScoresGames[x] + ", \"Won\": " + PlayerScoresWon[x] + ", \"Lost\": " + PlayerScoresLost[x] + "}")
				if x < Index1 - 1:
					RivalriesFile.write(", ")
			RivalriesFile.write("}}\n")
		
		time.sleep(10)
		
		
		Completed = Completed + 1
		
		
	
	