import requests
import json
import ndjson
import time
import math
import matplotlib.pyplot as mpl
from matplotlib.colors import BoundaryNorm, LogNorm
from matplotlib.ticker import MaxNLocator
import numpy as np

# API token for requests
with open("E:\\lichess\\APIToken.txt", "r") as TokenFile:
	for Line in TokenFile:
		APIToken = Line.strip()

# Load list of players and numbers
Players = []
PlayersDict = dict()
with open("highestbulletsorted.txt", "r") as HighestFile:
	for Line in HighestFile:
		Players.append(json.loads(Line))
		PlayersDict[Players[-1]["Username"]] = Players[-1]["Number"]
		
#PlayersDict["DrNykterstein"] = 0
#Players[0]["Username"] = "DrNykterstein"

TableSize = 250	
PlayerScores = []
for Index1 in range(TableSize):
	PlayerScores.append([0 for _ in range(TableSize)])	

# Load data from triangle-file
NUsers = 0
with open("rivalries-all-triangle.txt", "r") as RivalriesFile:
	for Index1, Line in enumerate(RivalriesFile):
		NUsers = NUsers + 1
		UserID1 = Players[Index1]["Username"]
		print("Loading " + UserID1)
		ScoreDict = json.loads(Line)
		# ScoreDict = {"Number": 2, "Username": "alireza2003", "Highest": 3301, "Scores": {"drnykterstein": {"Total": 769.0, "Won": 332.0, "Lost": 437.0}}}
		if ScoreDict["Username"] != UserID1:
			print("HMMM??")
			time.pause(1000)
		for Index2 in range(Index1):
			UserID2 = Players[Index2]["Username"]
			#print(UserID1 + " - " + UserID2)
			PlayerScores[Index1][Index2] = ScoreDict["Scores"][UserID2]["Won"]
			PlayerScores[Index2][Index1] = ScoreDict["Scores"][UserID2]["Lost"]
		#print(PlayerScores[Index])


for Index1 in range(NUsers):
	OutList = []
	User1 = Players[Index1]["Username"].lower()
	TotalGames = 0
	TotalScore = 0.0
	NOpponents = 0
	
	for Index2 in range(NUsers):
		User2 = Players[Index2]["Username"].lower()
		ScoreDict = dict()
		ScoreDict["Username"] = User2
		ScoreDict["Games"] = round(PlayerScores[Index1][Index2] + PlayerScores[Index2][Index1])
		ScoreDict["Score"] = (PlayerScores[Index1][Index2], PlayerScores[Index2][Index1])
		if ScoreDict["Games"] > 0.5:
			NOpponents = NOpponents + 1
			TotalGames = TotalGames + ScoreDict["Games"]
			TotalScore = TotalScore + PlayerScores[Index1][Index2]
		OutList.append(ScoreDict)
	
	OutList.sort(key = lambda item: item["Username"])
	
	# Save to individual NDJSON files
	with open(f"E:\\GitHub\\lichess\\ladder\\bullet\\bullet_{User1}.ndjson", "w") as OutFile:
		for Index in range(len(OutList)):
			OutFile.write(json.dumps(OutList[Index]) + "\n")

	# Save overall stats to individual JSON files
	with open(f"E:\\GitHub\\lichess\\ladder\\bullet\\bullet_{User1}.json", "w") as OutFile:
		UserDict = dict()
		UserDict["Games"] = TotalGames
		UserDict["Score"] = (TotalScore, TotalGames - TotalScore)
		UserDict["Opponents"] = NOpponents
		OutFile.write(json.dumps(UserDict) + "\n")
		print(f"{User1:<25} -- {json.dumps(UserDict)}")

	
	


# ----------------------------------------------------------------------------------
# 5. Make density plot of games played
# ----------------------------------------------------------------------------------


mpl.style.use(['dark_background'])
mpl.rcParams.update({
	"axes.facecolor": 		(0.2, 0.2, 0.2, 1.0),  # green with alpha = 50%
	"savefig.facecolor": 	(0.0, 0.0, 1.0, 0.0),  # blue  with alpha = 20%
	"figure.figsize": 		(9.5, 9.5),
	"axes.labelsize": 		10,
	"xtick.labelsize": 		8,
	"ytick.labelsize": 		8,
	"legend.labelspacing": 	0.3,
	"legend.handlelength":	2.0,
	"legend.handletextpad": 0.3,
	"grid.color": 			(0.8, 0.8, 0.8),
	"grid.linestyle": 		":",
	"grid.linewidth": 		0.5,
	"legend.framealpha":	0.5,
	"font.family": 			['Roboto', 'serif'],
})

PlotSize = 50
MinMatchSize = 10

#ListToInclude = [x for x in range(PlotSize)]
#ListToInclude.remove(5)			# DrGrekenstein
#ListToInclude.remove(17)		# manwithavan
#ListToInclude.remove(19)		# grey_parrot
#ListToInclude.remove(34)		# sasha

def MakePlot():

	XTicks = []
	for i in range(PlotSize):
		XTicks.append("vs. " + Players[i]["Username"][0:2])

	YTicks = []
	for i in range(PlotSize):
		YTicks.append(Players[i]["Username"] + " (" + str(Players[i]["Highest"]) + ")")


	x = np.arange(-0.5, PlotSize, 1)  # len = 11
	y = np.arange(-0.5, PlotSize, 1)  # len = 7
	Z = np.random.rand(PlotSize, PlotSize)



	mpl.close()

	minZ = 10000000000
	maxZ = -10000000000
	for i in range(PlotSize):
		for j in range(PlotSize):
			if PlayerScores[j][i] + PlayerScores[i][j] < MinMatchSize - 0.5:
				Z[j][i] = None
			else:
				
				#Z[j][i] = PlayerScores[j][i] + PlayerScores[i][j]
				Z[j][i] = PlayerScores[j][i] / (PlayerScores[j][i] + PlayerScores[i][j])
				minZ = minZ if (minZ < Z[j][i]) else Z[j][i]
				maxZ = maxZ if (maxZ > Z[j][i]) else Z[j][i]



	fig, ax = mpl.subplots()

	im = ax.pcolormesh(x, y, Z, cmap = "RdYlGn", alpha = 0.5, antialiased = False, linewidth = 0.0, rasterized = True)
	#im = ax.pcolormesh(x, y, Z, cmap = "RdYlGn", norm = LogNorm(vmin = minZ + 0.01, vmax = maxZ), alpha = 0.5, antialiased = False, linewidth = 0.0, rasterized = True)
	cbar = fig.colorbar(im, ax = ax, fraction=0.046, pad=0.04)

	ax.set_xticks(np.arange(PlotSize), minor=False)
	ax.set_yticks(np.arange(PlotSize), minor=False)

	ax.set_xticklabels(XTicks, minor=False, rotation=90)
	ax.set_yticklabels(YTicks, minor=False)

	#ax.set(aspect = 0.5)
	ax.set_title("Average score between top bullet players (only matchups with >=" + str(MinMatchSize) + " games)", fontdict={'fontsize': 12})
	ax.set(aspect="equal")
	mpl.tight_layout()

	#mpl.show()

	mpl.savefig(f"scores.png")
	print(f"Saving scores.png\n\n")


#MakePlot()



# Expected score between two players
def ExpScore(RatingOwn, RatingOpp):
	return 1. / (1 + 10. ** ((RatingOpp - RatingOwn) / 400.))
	

	
def Rerank(NPlayers):

	print("\n\nStarting iterations...\n\n")

	PlayerRatings = [Players[x]["Highest"] for x in range(NPlayers)]
	PlayerRatingSequence = [[Players[x]["Highest"]] for x in range(NPlayers)]
	for it in range(200):
		
		AvgDelta = [0. for i in range(NPlayers)]
		for i in range(NPlayers):
			TotalExpScore = 0.
			TotalScore = 0.
			TotalGames = 0.
			for j in range(NPlayers):
				if i == j:
					continue
				NGames = PlayerScores[j][i] + PlayerScores[i][j]
				TotalScore = TotalScore + PlayerScores[i][j]
				TotalGames = TotalGames + NGames
				TotalExpScore = TotalExpScore + ExpScore(PlayerRatings[i], PlayerRatings[j]) * NGames
			
			AvgScore = TotalScore / TotalGames
			AvgExpScore = TotalExpScore / TotalGames
			AvgDelta[i] = AvgScore - AvgExpScore
			#print(f"{str(i):>4}. {Players[i]['Username'] + ' (' + str(Players[i]['Highest']) + ')':<30} -- Games: {str(TotalGames):<6} -- AvgScore: {AvgScore:.2f} -- ExpScore: {AvgExpScore:.2f} -- Delta: {AvgDelta[i]:.2f}")
		
		#print(f"Updating player ratings.")
		
		SumChanges = 0.0
		for i in range(NPlayers):
			NewRating = PlayerRatings[i] + AvgDelta[i] * 100.
			SumChanges = SumChanges + abs(AvgDelta[i] * 100.)
			#print(f"{str(i):>4}. {Players[i]['Username'] + ' (' + str(Players[i]['Highest']) + ')':<30} -- Old: {str(PlayerRatings[i]):<6} -- New: {NewRating:<6}")
			PlayerRatings[i] = NewRating
			if it % 20 == 0:
				PlayerRatingSequence[i].append(NewRating)
		
		if it % 20 == 0:
			print(f"{it:>4}. Total rating change in previous iteration: {SumChanges:.3f}")
	
	print("\n\nFinished iterations. Renormalizing...\n\n")

	TotalChange = 0.0
	for i in range(NPlayers):
		TotalChange = TotalChange + round(PlayerRatings[i]) - Players[i]['Highest']
	print(f"Total change: {TotalChange}")
	for i in range(NPlayers):
		PlayerRatings[i] = PlayerRatings[i] - TotalChange / NPlayers

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

	with open("E:\\GitHub\\lichess\\ladder\\bullet\\__ranking.txt", "w") as MatchFile:
		Indices = [(PlayerRatings[i], i) for i in range(NPlayers)]
		Indices.sort(reverse = True)
		for Index, (Rating, i) in enumerate(Indices):
			Sign = "" 
			if Players[i]['Highest'] <= round(PlayerRatings[i]):
				Sign = "+"
			print(f"{Index+1:>4}. ({i+1:>3}.) {Players[i]['Username']:<26} -- {round(PlayerRatings[i])} ({Sign}{round(PlayerRatings[i]) - Players[i]['Highest']})")
			MatchFile.write(f"{Index+1:>4} ({round(PlayerRatings[i])}) {Players[i]['Username']}\n")
	
	print("\n\nFinal charts:\n\n")
	
	Indices = [(PlayerRatings[i] - Players[i]['Highest'], i) for i in range(NPlayers)]
	Indices.sort(reverse = True)
	for (Rating, i) in Indices:
		Sign = "" 
		if Players[i]['Highest'] <= round(PlayerRatings[i]):
			Sign = "+"
		print(f"{str(i):>4}. {Players[i]['Username'] + ' (' + str(Players[i]['Highest']) + ')':<30} -- {round(PlayerRatings[i])} ({Sign}{round(PlayerRatings[i]) - Players[i]['Highest']})")


Rerank(239)



ToPrintStrings = []
for Index1 in range(NUsers):
	for Index2 in range(NUsers):
		User1 = Players[Index1]["Username"].lower()
		User2 = Players[Index2]["Username"].lower()
		Str = f"{User1},{User2},"
		ScoreDict = dict()
		ScoreDict["Games"] = round(PlayerScores[Index1][Index2] + PlayerScores[Index2][Index1])
		ScoreDict["Score"] = (PlayerScores[Index1][Index2], PlayerScores[Index2][Index1])
		Str = Str + json.dumps(ScoreDict) + "\n"
		ToPrintStrings.append(Str)
ToPrintStrings.sort()

with open("E:\\GitHub\\lichess\\ladder\\bullet\\bullet.txt", "w") as MatchFile:
	for Str in ToPrintStrings:
		MatchFile.write(Str)

	
for Index1 in range(NUsers):
	User1 = Players[Index1]["Username"].lower()
	
	# Save to individual NDJSON files
	with open(f"E:\\GitHub\\lichess\\ladder\\bullet\\bullet_{User1}.ndjson", "w") as OutFile:
		for Index in range(len(OutList)):
			OutFile.write(json.dumps(OutList[Index]) + "\n")

	# Save overall stats to individual JSON files
	with open(f"E:\\GitHub\\lichess\\ladder\\bullet\\bullet_{User1}.json", "w") as OutFile:
		UserDict = dict()
		UserDict["Games"] = TotalGames
		UserDict["Score"] = (TotalScore, TotalGames - TotalScore)
		UserDict["Opponents"] = NOpponents
		OutFile.write(json.dumps(UserDict) + "\n")


OutListStrings = []
for Index1 in range(NUsers):
	User1 = Players[Index1]["Username"].lower()
	UserDict = dict()
	UserDict["BulletHigh"] = 1111
	UserDict["Bullet"] = 1111
	UserDict["Title"] = "--"
	UserDict["Username"] = User1
	
	time.sleep(1)
	r = requests.get(f"https://lichess.org/api/user/{User1}", headers = {"Authorization": f"Bearer {APIToken}"})
	if r.status_code == 429:
		print("RATE LIMIT!")
		time.sleep(100000)
	
	OutDict = json.loads(r.text.strip())
	
	if "closed" in OutDict:
		UserDict["Closed"] = True
		
	else:
		UserDict["Title"] = OutDict.get("title", "--")
		UserDict["Bullet"] = OutDict["perfs"]["bullet"]["rating"]
		
		if "tosViolation" in OutDict:
			UserDict["Marked"] = True
			
		else:	
			r = requests.get(f"https://lichess.org/api/user/{User1}/perf/bullet", headers = {"Authorization": f"Bearer {APIToken}"})
			if r.status_code == 429:
				print("RATE LIMIT!")
				time.sleep(100000)
			
			OutDict = json.loads(r.text.strip())
			UserDict["BulletHigh"] = OutDict["stat"]["highest"]["int"]
		
	OutListStrings.append(json.dumps(UserDict) + "\n")
	print(f"{Index1}. {User1}")

OutListStrings.sort(reverse = True)
with open("E:\\GitHub\\lichess\\ladder\\bullet\\__users_new.ndjson", "w") as OutFile:
	for Line in OutListStrings:
		OutFile.write(Line)



