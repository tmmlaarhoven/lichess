import requests
import re
import os
import time
import os.path
import ndjson
import json
import math
import datetime

import matplotlib.pyplot as mpl
from matplotlib.colors import BoundaryNorm, LogNorm
from matplotlib.ticker import MaxNLocator
import numpy as np

mpl.style.use(['dark_background'])
mpl.rcParams.update({
	"axes.facecolor": 		(0.2, 0.2, 0.2, 1.0),  # green with alpha = 50%
	"savefig.facecolor": 	(0.0, 0.0, 1.0, 0.0),  # blue  with alpha = 20%
	"figure.figsize": 		(6.5, 6.5),
	"axes.labelsize": 		12,
	"xtick.labelsize": 		11,
	"ytick.labelsize": 		11,
	"legend.labelspacing": 	0.3,
	"legend.handlelength":	2.0,
	"legend.handletextpad": 0.3,
	"grid.color": 			(0.8, 0.8, 0.8),
	"grid.linestyle": 		":",
	"grid.linewidth": 		0.5,
	"legend.framealpha":	0.5,
	"font.family": 			['Roboto', 'serif'],
})



PureVariants = {
	"3check": 		{"Name": "Three-check", 		"RGB": (204,121,167), 	"WebOrder": 11,		"Code": "3c",	"Icon": "."},
	"antichess": 	{"Name": "Antichess",			"RGB": (223, 83, 83),	"WebOrder": 12,		"Code": "an",	"Icon": "@"},
	"atomic": 		{"Name": "Atomic",				"RGB": (102, 85,140),	"WebOrder": 13,		"Code": "at",	"Icon": ">"},
	"blitz": 		{"Name": "Blitz",				"RGB": (  0,114,178),	"WebOrder": 5,		"Code": "bz",	"Icon": ")"},
	"bullet": 		{"Name": "Bullet",				"RGB": ( 86,180,233),	"WebOrder": 3,		"Code": "bu",	"Icon": "T"},
	"chess960": 	{"Name": "Chess960",			"RGB": (230,159,  0),	"WebOrder": 9,		"Code": "c9",	"Icon": "'"},
	"classical": 	{"Name": "Classical",			"RGB": ( 69,159, 59),	"WebOrder": 7,		"Code": "cl",	"Icon": "+"},
	"crazyhouse": 	{"Name": "Crazyhouse",			"RGB": ( 86,180,233),	"WebOrder": 8,		"Code": "ch",	"Icon": "&#xe00b;"},
	"horde": 		{"Name": "Horde",				"RGB": (153,230,153),	"WebOrder": 14,		"Code": "ho",	"Icon": "_"},
	"hyperbullet": 	{"Name": "HyperBullet",			"RGB": ( 86,180,233),	"WebOrder": 2,		"Code": "hb",	"Icon": "T"},
	"koth": 		{"Name": "King of the Hill",	"RGB": (213, 94,  0),	"WebOrder": 10,		"Code": "kh",	"Icon": "("},
	"racingkings": 	{"Name": "Racing Kings",		"RGB": (255,174,170),	"WebOrder": 15,		"Code": "rk",	"Icon": "&#xe00a;"},
	"rapid": 		{"Name": "Rapid",				"RGB": (  0,158,115),	"WebOrder": 6,		"Code": "ra",	"Icon": "#"},
	"superblitz": 	{"Name": "SuperBlitz",			"RGB": (  0,114,178),	"WebOrder": 4,		"Code": "sb",	"Icon": ")"},
	"ultrabullet": 	{"Name": "UltraBullet",			"RGB": (  0,158,115),	"WebOrder": 1,		"Code": "ub",	"Icon": "{"}
}

PureEvents = {
	"hourly": 		{"Name": "Hourly",				"RGB": (  0,158,115),	"WebOrder": 1,		"Code": "ho"},
	"2000": 		{"Name": "<2000",				"RGB": (  0,158,115),	"WebOrder": 2,		"Code": "20"},
	"1700": 		{"Name": "<1700",				"RGB": (  0,158,115),	"WebOrder": 3,		"Code": "17"},
	"1600": 		{"Name": "<1600",				"RGB": (  0,158,115),	"WebOrder": 4,		"Code": "16"},
	"1500": 		{"Name": "<1500",				"RGB": (  0,158,115),	"WebOrder": 5,		"Code": "15"},
	"1300": 		{"Name": "<1300",				"RGB": (  0,158,115),	"WebOrder": 6,		"Code": "13"},
	"thematic":		{"Name": "Thematic",			"RGB": (  0,158,115),	"WebOrder": 7,		"Code": "th"},
	"daily": 		{"Name": "Daily",				"RGB": (  0,158,115),	"WebOrder": 8,		"Code": "da"},
	"weekly": 		{"Name": "Weekly",				"RGB": (  0,158,115),	"WebOrder": 9,		"Code": "we"},
	"monthly": 		{"Name": "Monthly",				"RGB": (  0,158,115),	"WebOrder": 10,		"Code": "mo"},
	"yearly": 		{"Name": "Yearly",				"RGB": (  0,158,115),	"WebOrder": 11,		"Code": "ye"},
	"eastern": 		{"Name": "Eastern",				"RGB": (  0,158,115),	"WebOrder": 12,		"Code": "ea"},
	"elite": 		{"Name": "Elite",				"RGB": (  0,158,115),	"WebOrder": 13,		"Code": "el"},
	"shield": 		{"Name": "Shield",				"RGB": (  0,158,115),	"WebOrder": 14,		"Code": "sh"},
	"titled": 		{"Name": "Titled",				"RGB": (  0,158,115),	"WebOrder": 15,		"Code": "ti"},
	"marathon": 	{"Name": "Marathon",			"RGB": (  0,158,115),	"WebOrder": 16,		"Code": "ma"},
	"liga": 		{"Name": "Liga",				"RGB": (  0,158,115),	"WebOrder": 17,		"Code": "li"}
}




# White scoring percentage
def WhiteScore(dict):
	return 50. * (dict["Games"] + dict["WhiteWins"] - dict["BlackWins"]) / dict["Games"]

# Percentage of draws
def Draws(dict):
	return 100. * (dict["Games"] - dict["WhiteWins"] - dict["BlackWins"]) / dict["Games"]

# Percentage of berserks
def Berserks(dict):
	return 50. * dict["Berserks"] / dict["Games"]

# Average rating
def Rating(dict):
	return dict["TotalRating"] / dict["Participants"]

# Average participation
def Participants(dict):
	return dict["Participants"] / dict["Events"]

# Total people ever participated
def TotalPlayers(dict):
	return dict["Players"]
	
# Total events ever happened
def TotalEvents(dict):
	return dict["Events"]
	
# Total events ever happened
def TotalGames(dict):
	return dict["Games"]

# How long have these tournaments been running?
def TimeRange(dict):
	f = dict["FirstStart"]
	First = datetime.datetime(int(f[0:4]), int(f[5:7]), int(f[8:10]), 0, 0, 0)
	l = dict["LastStart"]
	Last = datetime.datetime(int(l[0:4]), int(l[5:7]), int(l[8:10]), 0, 0, 0)
	Duration = Last - First
	return Duration / datetime.timedelta(days = 1)

def TopScore(dict):
	return dict["TopScore"]
	
# Total events ever happened
def MovesPerGame(dict):
	return dict["Moves"] / dict["Games"] / 2.

# Total events ever happened
def PointsPerPlayer(dict):
	return dict["TotalPoints"] / dict["Participants"]
	
# Total events ever happened
def MaxUsers(dict):
	return dict["MaxUsers"]


#TopScore
#MaxUsers
#TotalPoints
#Moves
#Games


va = ["ultrabullet", "hyperbullet", "bullet", "superblitz", "blitz", "rapid", "classical", "crazyhouse", "chess960", "koth", "3check", "antichess", "atomic", "horde", "racingkings"]
ev = ["1300", "1500", "1600", "1700", "2000", "thematic", "eastern", "hourly", "daily", "weekly", "monthly", "yearly", "shield", "elite", "titled", "marathon", "liga"]
ev.reverse()

XTicks = []
for i in range(len(va)):
	XTicks.append(PureVariants[va[i]]["Name"])

YTicks = []
for i in range(len(ev)):
	YTicks.append(PureEvents[ev[i]]["Name"])


x = np.arange(-0.5, len(va), 1)  # len = 11
y = np.arange(-0.5, len(ev), 1)  # len = 7
Z = np.random.rand(len(ev), len(va))


def MakePlot(params):

	mpl.close()

	minZ = 10000000000
	maxZ = -10000000000
	for i in range(len(PureVariants)):
		V = va[i]
		for j in range(len(PureEvents)):
			E = ev[j]
			if not os.path.exists(f"E:\\lichess\\tournaments\\rankings\\{V}\\{E}\\{V}_{E}_players.ndjson"):
				Z[j][i] = None
			else:
				with open(f"E:\\lichess\\tournaments\\rankings\\{V}\\{E}\\{V}_{E}_ranking.json") as File:
					dict = json.load(File)
				#Z[j][i] = 1. * dict["WhiteWins"] / dict["Games"]
				#Z[j][i] = TotalPlayers(dict)
				#Z[j][i] = 0.5 * dict["Berserks"] / dict["Games"]
				#Z[j][i] = Rating(dict)
				Z[j][i] = params[0](dict)
				minZ = minZ if (minZ < Z[j][i]) else Z[j][i]
				maxZ = maxZ if (maxZ > Z[j][i]) else Z[j][i]



	fig, ax = mpl.subplots()
	
	if params[3]:
		im = ax.pcolormesh(x, y, Z, cmap = params[4], norm = LogNorm(vmin = minZ + 0.01, vmax=maxZ), alpha = 0.5, antialiased = False, linewidth = 0.0, rasterized = True)
	else:
		im = ax.pcolormesh(x, y, Z, cmap = params[4], alpha = 0.5, antialiased = False, linewidth = 0.0, rasterized=True)
	cbar = fig.colorbar(im, ax = ax)

	ax.set_xticks(np.arange(len(va)), minor=False)
	ax.set_yticks(np.arange(len(ev)), minor=False)

	ax.set_xticklabels(XTicks, minor=False, rotation=90)
	ax.set_yticklabels(YTicks, minor=False)

	#ax.set(aspect = 0.5)
	ax.set_title(params[1], fontdict={'fontsize': 14})
	mpl.tight_layout()

	#mpl.show()

	mpl.savefig(f"E:\\GitHub\\lichess\\rankings\\density_{params[2]}.png")
	print(f"Saving density_{params[2]}.png")



# params: (1) function, (2) plot title, (3) filename, (4) logscale?, (5) colors
# cmaps['Sequential'] = [
#            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
#            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
#            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']

paramsets = [
	[TimeRange, 	"Time span of events (days)", 			"time", 		True,		"Blues"],
	[WhiteScore, 	"White's score (percentage)", 			"white", 		False,		"Purples"],
	[Draws, 		"Number of draws (percentage)", 		"draws", 		False,		"Greens"],
	[Berserks, 		"Number of berserks (percentage)", 		"berserks", 	False,		"Oranges"],
	[Rating, 		"Average ratings", 						"rating", 		False,		"Reds"],
	[TotalGames, 	"Total number of games", 				"games", 		True,		"YlOrBr"],
	[Participants, 	"Average number of participants", 		"participants", True,		"OrRd"],
	[TotalPlayers, 	"Total number of (unique) players", 	"players", 		True,		"BuPu"],
	[TotalEvents, 	"Total number of events", 				"events", 		True,		"YlGn"],
	[MovesPerGame, 	"Average moves per game", 				"moves", 		False,		"RdPu"],
	[PointsPerPlayer, 	"Average points per player", 		"points", 		False,		"PuRd"],
	[MaxUsers, 		"All-time maximum participants", 		"maxusers", 	True,		"GnBu"],
	[TopScore, 		"All-time high score", 					"highscore", 	True,		"PuBu"]
]

for params in paramsets:
	MakePlot(params)


