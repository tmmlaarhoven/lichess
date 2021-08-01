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





# Expected score between two players
def ExpScore(RatingOwn, RatingOpp):
	return 1. / (1 + 10. ** ((RatingOpp - RatingOwn) / 400.))


# Function to compute new ranking for players	
def Rerank(NPlayers):

	# Initialize to maximum ratings
	TotalRating = 0
	for Index, User in enumerate(PlayersDict):
		if Index >= NPlayers:
			PlayersDict[User]["RealRating"] = -1
		else:
			PlayersDict[User]["RealRating"] = PlayersDict[User]["BulletMax"]
			PlayersDict[User]["TotalGames"] = 0
			PlayersDict[User]["TotalScore"] = 0.0
			TotalRating = TotalRating + PlayersDict[User]["BulletMax"]
	
	for Index1, User1 in enumerate(PlayersDict):
		if Index1 >= NPlayers:
			break
		PlayersDict[User1]["TotalGames"] = 0
		PlayersDict[User1]["TotalScore"] = 0.0
		for Index2, User2 in enumerate(PlayersDict):
			if Index2 >= NPlayers:
				break
			if Index2 == Index1:
				continue
			PlayersDict[User1]["TotalGames"] = PlayersDict[User1]["TotalGames"] + MatchesDict[User1][User2]["Games"]
			PlayersDict[User1]["TotalScore"] = PlayersDict[User1]["TotalScore"] + MatchesDict[User1][User2]["Score"][0]
		if PlayersDict[User1]["TotalGames"] == 0:
			print(f"{Index1}. {User1} has no games!")
	#PlayerRatingSequence = [[Players[x]["Highest"]] for x in range(NPlayers)]
	
	# Run iterations
	print("\n\nStarting iterations...\n\n")
	for it in range(200):
		
		AvgDelta = [0. for _ in range(NPlayers)]
		for Index1, User1 in enumerate(PlayersDict):
			if Index1 >= NPlayers:
				break
			
			TotalExpScore = 0.
			TotalScore = 0.
			TotalGames = 0.
			for Index2, User2 in enumerate(PlayersDict):
				if Index2 == Index1:
					continue
				if Index2 >= NPlayers:
					break
				
				NGames = MatchesDict[User1][User2]["Games"]
				TotalScore = TotalScore + MatchesDict[User1][User2]["Score"][0]
				TotalGames = TotalGames + NGames
				TotalExpScore = TotalExpScore + ExpScore(PlayersDict[User1]["RealRating"], PlayersDict[User2]["RealRating"]) * NGames
			
			AvgScore = TotalScore / TotalGames
			AvgExpScore = TotalExpScore / TotalGames
			AvgDelta[Index1] = AvgScore - AvgExpScore
			#print(f"{str(i):>4}. {Players[i]['Username'] + ' (' + str(Players[i]['Highest']) + ')':<30} -- Games: {str(TotalGames):<6} -- AvgScore: {AvgScore:.2f} -- ExpScore: {AvgExpScore:.2f} -- Delta: {AvgDelta[i]:.2f}")
		
		#print(f"Updating player ratings.")
		
		SumChanges = 0.0
		for Index1, User1 in enumerate(PlayersDict):
			if Index1 >= NPlayers:
				break
			NewRating = PlayersDict[User1]["RealRating"] + AvgDelta[Index1] * 100.
			SumChanges = SumChanges + abs(AvgDelta[Index1] * 100.)
			#print(f"{str(i):>4}. {Players[i]['Username'] + ' (' + str(Players[i]['Highest']) + ')':<30} -- Old: {str(PlayerRatings[i]):<6} -- New: {NewRating:<6}")
			PlayersDict[User1]["RealRating"] = NewRating
			#if it % 20 == 0:
			#	PlayerRatingSequence[i].append(NewRating)
		
		if it % 20 == 0:
			print(f"{it:>4}. Total rating change in previous iteration: {SumChanges:.3f}")
	
	print("\n\nFinished iterations. Renormalizing...\n\n")

	TotalChange = 0.0
	for Index1, User1 in enumerate(PlayersDict):
		if Index1 >= NPlayers:
			break
		TotalChange = TotalChange + round(PlayersDict[User1]["RealRating"]) - PlayersDict[User1]["BulletMax"]
	print(f"Total change: {TotalChange}")
	for Index1, User1 in enumerate(PlayersDict):
		PlayersDict[User1]["RealRating"] = PlayersDict[User1]["RealRating"] - TotalChange / NPlayers

	# print("\n\nRatings change chart: \n\n")
	# for i in range(NPlayers):
	#	Sign = "" 
	#	if Players[i]['Highest'] <= round(PlayerRatings[i]):
	#		Sign = "+"
	#	print(f"{str(i):>4}. {Players[i]['Username'] + ' (' + str(Players[i]['Highest']) + ')':<30} -- Final: {round(PlayerRatings[i])} ({Sign}{round(PlayerRatings[i]) - Players[i]['Highest']})")
	#
	# print("\n\nRating update sequence:\n\n")
	#
	# for i in range(NPlayers):
	#	print(f"{str(i):>4}. {Players[i]['Username'] + ' (' + str(Players[i]['Highest']) + ')':<30} -- Sequence: [" + ", ".join(map(str, map(round, PlayerRatingSequence[i]))) + "].")

	print("\n\nFinal ranking:\n")

	with open("E:\\GitHub\\lichess\\ladder\\bullet\\__ranking-new-all.txt", "w") as MatchFile:
		SortedDict = sorted(PlayersDict.items(), key = lambda item: item[1]["RealRating"], reverse = True)
		MatchFile.write("   # (RTNG:MAXM)     USERNAME                    ( Games :  Score )\n---------------------------------------------------------------------\n")
		for Index1, (User1, Dic) in enumerate(SortedDict):
			if Index1 >= NPlayers:
				break
			OutString = f"{Index1+1:>4} ({round(Dic['RealRating'])}:{Dic['BulletMax']}) {Dic['Title']:>3} {Dic['Username']:<25}   ({Dic['TotalGames']:>6} : {Dic['TotalScore']:>7})"
			print(OutString)
			MatchFile.write(f"{OutString}\n")
	

Rerank(345)

