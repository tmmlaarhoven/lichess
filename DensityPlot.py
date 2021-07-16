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
from matplotlib.colors import BoundaryNorm
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
	return 0.5 * (dict["Games"] + dict["WhiteWins"] - dict["BlackWins"]) / dict["Games"]

# Percentage of draws
def Draws(dict):
	return (dict["Games"] - dict["WhiteWins"] - dict["BlackWins"]) / dict["Games"]

# Percentage of berserks
def Berserks(dict):
	return 0.5 * dict["Berserks"] / dict["Games"]

# Average rating
def Rating(dict):
	return dict["TotalRating"] / dict["Participants"]

# Average participation
def Participants(dict):
	return dict["Participants"] / dict["Events"]

# Total people ever participated
def TotalPlayers(dict):
	return dict["Players"]

# How long have these tournaments been running?
def TimeRange(dict):
	f = dict["FirstStart"]
	First = datetime.datetime(int(f[0:4]), int(f[5:7]), int(f[8:10]), 0, 0, 0)
	l = dict["LastStart"]
	Last = datetime.datetime(int(l[0:4]), int(l[5:7]), int(l[8:10]), 0, 0, 0)
	Duration = Last - First
	return Duration / datetime.timedelta(days = 1)





va = ["3check", "antichess", "atomic", "blitz", "bullet", "chess960", "classical", "crazyhouse", "horde", "hyperbullet", "koth", "racingkings", "rapid", "superblitz", "ultrabullet"]
ev = ["hourly", "2000", "1700", "1600", "1500", "1300", "thematic", "daily", "weekly", "monthly", "yearly", "eastern", "elite", "shield", "titled", "marathon", "liga"]
ev.reverse()

XTicks = []
for i in range(len(va)):
	XTicks.append(PureVariants[va[i]]["Name"])

YTicks = []
for i in range(len(ev)):
	YTicks.append(PureEvents[ev[i]]["Name"])

np.random.seed(19680801)

x = np.arange(-0.5, len(va), 1)  # len = 11
y = np.arange(-0.5, len(ev), 1)  # len = 7
Z = np.random.rand(len(ev), len(va))

for i in range(len(PureVariants)):
	V = va[i]
	for j in range(len(PureEvents)):
		E = ev[j]
		if not os.path.exists(f"E:\\lichess\\tournaments\\rankings\\{V}\\{E}\\{V}_{E}_players.ndjson"):
			Z[j][i] = None
		else:
			with open(f"E:\\lichess\\tournaments\\rankings\\{V}\\{E}\\{V}_{E}_ranking.json") as File:
				dict = json.load(File)
			Z[j][i] = 1. * dict["WhiteWins"] / dict["Games"]
			Z[j][i] = TotalPlayers(dict)
			#Z[j][i] = 0.5 * dict["Berserks"] / dict["Games"]
			#Z[j][i] = Rating(dict)
			#Z[j][i] = TimeRange(dict)



fig, ax = mpl.subplots()
ax.pcolormesh(x, y, Z, cmap="Greens")

ax.set_xticks(np.arange(len(va)), minor=False)
ax.set_yticks(np.arange(len(ev)), minor=False)

ax.set_xticklabels(XTicks, minor=False, rotation=90)
ax.set_yticklabels(YTicks, minor=False)

ax.set(aspect="equal")
ax.set_title("Distribution of events", fontdict={'fontsize': 14})
mpl.tight_layout()

mpl.show()