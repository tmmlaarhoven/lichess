# =============== JSON FORMAT ===============
# {"nbPlayers": 22560,
# "id": "spring22",
# "startsAt": "2022-04-16T00:00:00.000Z",
# "fullName": "2022 Spring Marathon",
# "clock": {"limit": 120, "increment": 1},
# "stats": {"games": 291490, "moves": 20542071, "whiteWins": 142477, "blackWins": 134541, "draws": 14472, "berserks": 67883, "averageRating": 1677, "points": 789207},
# "podium": [
#    {"name": "HomayooonT", "rank": 1, "rating": 2876, "score": 901, "sheet": {}, "title": "GM", "nb": {"game": 296, "berserk": 22, "win": 248}, "performance": 2847},
#    {"name": "Experience_Chess", "rank": 2, "rating": 2865, "score": 801, "sheet": {"fire": true}, "title": "GM", "nb": {"game": 273, "berserk": 31, "win": 225}, "performance": 2856},
#    {"name": "papasi", "rank": 3, "rating": 2514, "score": 712, "sheet": {"fire": true}, "title": "CM", "nb": {"game": 366, "berserk": 191, "win": 197}, "performance": 2522}
# ],
# "standing": {"page": 1, "players": [
#    {"name": "HomayooonT", "rank": 1, "rating": 2876, "score": 901, "sheet": {"scores": "04444222222444442204222444442302244220204444444422004442202222120444423020004220244444444422120044445444444320442224444222442202204444442201224444444220044444444444444221020444444444444442224444444442204442204444444232444444444444444444220444445222444444220454444444444444554545453203244320332532"}, "title": "GM"},
#    ...
#    {"name": "Serg_01", "rank": 10, "rating": 2603, "score": 565, "sheet": {"scores": "30300031033002330300300331033000030302022422112020222000021242200004220444442204221202120244442202202203004220212044442202022001004444444442224444422022244444442204220444444422044220444444444444444444444444444444422244444230454444444422"}}
# ]},

# =============== NDJSON FORMAT ===============
# {"rank":1,"score":901,"rating":2876,"username":"HomayooonT","title":"GM","performance":2847}
# {"rank":2,"score":801,"rating":2865,"username":"Experience_Chess","title":"GM","performance":2856}
# {"rank":3,"score":712,"rating":2514,"username":"papasi","title":"CM","performance":2522}
# {"rank":4,"score":681,"rating":2536,"username":"Ragehunter","performance":2559}
# {"rank":5,"score":673,"rating":2543,"username":"Artem_0degov","title":"FM","performance":2511}
# {"rank":6,"score":635,"rating":2546,"username":"Nacho_Varga","performance":2510}
# {"rank":7,"score":584,"rating":2766,"username":"Crest64","title":"GM","performance":2695}
# {"rank":8,"score":584,"rating":2588,"username":"nfds","title":"FM","performance":2593}
# {"rank":9,"score":569,"rating":2679,"username":"Gakolchess765","performance":2602}
# {"rank":10,"score":565,"rating":2603,"username":"Serg_01","performance":2620}
# {"rank":11,"score":564,"rating":2555,"username":"Lance5500","title":"LM","performance":2544}
# ...
# {"rank":22351,"score":0,"rating":600,"username":"Manikandanamma"}
# ...

import requests
import re
import time
import bz2
import os
import json
import ndjson
import matplotlib.pyplot as mpl
import datetime

# For API calls, use following file with API token
api_token_filename = "/media/thijs/SED/lichess/APItoken.txt"

# from scipy import stats
# from scipy.spatial import ConvexHull, convex_hull_plot_2d

# Set global plot settings
mpl.style.use(['dark_background'])
mpl.rcParams.update({
	"axes.facecolor": 		(0.2, 0.2, 0.2, 1.0),
	"savefig.facecolor": 	(0.0, 0.0, 1.0, 0.0),
	"figure.figsize": 		(4.5, 4.5),
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
	"savefig.facecolor":	"#262421",
})

# Load Lichess logo background for plots
LichessLogo = mpl.imread(f"logo.png")

trophy_rankings = [1, 10, 50, 100, 500]
marathons = dict()
players = dict()

# Load all marathon data into memory
for sub_dir, dir, files in os.walk("."):

	# Skip documents/scripts in root
	if sub_dir == "." or sub_dir == "./sheets" or sub_dir == "./plots" or sub_dir == "./api":
		continue

	print(sub_dir)
	# Register new time control
	tc = sub_dir[2:]
	if tc not in marathons:
		marathons[tc] = dict()

	# Traverse all marathons in this directory
	for file_name in files:

		# Fetch and register potentially new arena ID
		if file_name.split(".")[1] not in {"json", "ndjson"}:
			continue

		id = (file_name.split(".")[0])[-8:]
		if id not in marathons[tc]:
			marathons[tc][id] = dict()

		# Load marathon info
		if file_name[-5:] == ".json":
			with open(os.path.join(sub_dir, file_name), "r") as in_file:
				marathons[tc][id]["info"] = json.load(in_file)

		# Load marathon results
		if file_name[-7:] == ".ndjson":
			with open(os.path.join(sub_dir, file_name), "r") as in_file:
				marathons[tc][id]["results"] = []
				for index, line in enumerate(in_file):
					score_dict = json.loads(line)
					marathons[tc][id]["results"].append(score_dict)

					# No trophies below 500
					if (index >= 500):
						continue
					# No trophies below 100 for events on/before spring21
					elif (index >= 100) and (int(id[-2:]) <= 20 or id == "spring21"):
						continue
					# No trophies below 50 for summer15 and autumn15
					elif (index >= 50) and (id == "summer15" or id == "autumn15"):
						continue
					else:
						player_id = score_dict["username"]

						# MANUALLY EXCLUDE UNAWARDED TROPHIES
						# These players finished outside the top 100 when the marathon ended and trophies were awarded
						# However, after cheaters were later removed from the standings, they finished just inside the top 100
						# They did not get any trophies for these events, as the cheaters were removed later on, so these are not counted for standings
						if player_id.lower() == "alexr58" and id == "winter20":				# After cheater correction finished 99th
							continue
						if player_id.lower() == "arvids_andrejevs" and id == "spring21":	# After cheater correction finished 99th
							continue

						if player_id not in players:
							players[player_id] = [0, 0, 0, 0, 0]
						if index >= 100:
							players[player_id][4] += 1
						elif index >= 50:
							players[player_id][3] += 1
						elif index >= 10:
							players[player_id][2] += 1
						elif index >= 1:
							players[player_id][1] += 1
						else:
							players[player_id][0] += 1


# ===================================================
# Data set cleaning
# ===================================================

def GetPlayerPages():

	# Get API token
	api_token = ""
	with open(api_token_filename, "r") as token_file:
		for line in token_file:
			api_token = line.strip()

	# Fetch detailed score sheet pages
	for tc in marathons:
		for id in marathons[tc]:
			print(id)
			for page in range(50, 51):
				time.sleep(2)
				r = requests.get(f"https://lichess.org/api/tournament/{id}?page={page}", headers = {"Authorization": f"Bearer {api_token}"})
				if r.status_code == 429:
					print("RATE LIMIT!")
					time.sleep(100000)
				with open(f"sheets/{id}_{page}.txt", "wb") as ArenaResultsFile:
					ArenaResultsFile.write(r.content)

# ===================================================
# Add more metadata (WDL, games, point distribution) to the results from the API, based on score sheets
# ===================================================

def UpdateResults():

	# Fetch detailed score sheet pages
	for tc in marathons:
		for id in marathons[tc]:
			for page in range(1, 51):
				with open(f"sheets/{id}_{page}.txt", "r") as sheets_file:
					for line in sheets_file:
						arena_info = json.loads(line)
						for i in range(10):
							marathons[tc][id]["results"][10*(page-1) + i]["sheet"] = arena_info["standing"]["players"][i]["sheet"]["scores"][::-1]
							marathons[tc][id]["results"][10*(page-1) + i]["username"] = arena_info["standing"]["players"][i]["name"]
							marathons[tc][id]["results"][10*(page-1) + i]["score"] = arena_info["standing"]["players"][i]["score"]
							marathons[tc][id]["results"][10*(page-1) + i]["rating"] = arena_info["standing"]["players"][i]["rating"]
			with open(f"{tc}/{id}.ndjson", "w") as results_file:
				for i in range(len(marathons[tc][id]["results"])):
					if "performance" in marathons[tc][id]["results"][i]:
						del marathons[tc][id]["results"][i]["performance"]

					if i < 500:
						marathons[tc][id]["results"][i]["games"] = len(marathons[tc][id]["results"][i]["sheet"])
						marathons[tc][id]["results"][i]["points"] = [0, 0, 0, 0, 0, 0]
						marathons[tc][id]["results"][i]["wdl"] = [0, 0, 0]
						win_streak = 0
						for j in range(marathons[tc][id]["results"][i]["games"]):
							charr = marathons[tc][id]["results"][i]["sheet"][j]
							marathons[tc][id]["results"][i]["points"][int(charr)] += 1
							if charr == "0":
								marathons[tc][id]["results"][i]["wdl"][2] += 1
								win_streak = 0
							elif charr == "1" or (charr == "2" and win_streak > 2):
								marathons[tc][id]["results"][i]["wdl"][1] += 1
								win_streak = 0
							else:
								marathons[tc][id]["results"][i]["wdl"][0] += 1
								win_streak += 1
					results_file.write(json.dumps(marathons[tc][id]["results"][i]) + "\n")
			with open(f"{tc}/{id}.json", "w") as info_file:
				info_file.write(json.dumps(marathons[tc][id]["info"]))








# ===================================================
# Compute top rankings for most trophies, and print them for blog post
# ===================================================

def ShowTrophyRankings():
	for index, (user, trophies) in enumerate(sorted(players.items(), key = lambda item: sum(item[1][i] * (1 + 2 ** (-10-3*i)) for i in range(5)), reverse = True)):
		if index >= 100:
			break

		print(f"| {index+1}. | [{user}](https://lichess.org/@/{user}) | **{sum(trophies)}** | ", end="")
		print(*trophies, sep = " | ", end = " |\n")


# ===================================================
# Players vs. Date (point per marathon, color per TC)
# ===================================================

def PlotPlayers():
	for rank in trophy_rankings:
		mpl.close()
		mpl.figure()
		Legend = []

		for tc in marathons:
			X = []
			Y = []
			Legend.append(tc)
			for id in marathons[tc]:
				X.append(datetime.datetime.strptime(marathons[tc][id]["info"]["startsAt"][:-5], "%Y-%m-%dT%H:%M:%S"))
				Y.append(marathons[tc][id]["info"]["nbPlayers"])

			X, Y = zip(*sorted(zip(X, Y)))
			mpl.scatter(X, Y, antialiased = True)#, color = UserColor, linestyle = UserStyle, marker = UserMarker, markevery = 0.1)

		X = []
		Y = []
		for tc in marathons:
			for id in marathons[tc]:
				X.append(datetime.datetime.strptime(marathons[tc][id]["info"]["startsAt"][:-5], "%Y-%m-%dT%H:%M:%S"))
				Y.append(marathons[tc][id]["info"]["nbPlayers"])

		X, Y = zip(*sorted(zip(X, Y)))
		mpl.plot([X[0], X[-1]], [Y[0], Y[-1]], linestyle=":", color="white", antialiased = True)

		# Processing plot
		mpl.gca().set_ylim([0, None])
		mpl.legend(Legend, loc = 'upper left', fontsize = 11, title = "Time Control", title_fontsize = 11)

		# Post-processing for all plots
		mpl.xticks(rotation = 45)
		mpl.grid(alpha = 0.5)
		mpl.title(f"Players per marathon")
		mpl.ylabel("Players")
		mpl.tight_layout()

		# Add lichess logo as background, and fix aspect ratio to 1
		XMin, XMax = mpl.gca().get_xlim()
		YMin, YMax = mpl.gca().get_ylim()
		mpl.gca().imshow(LichessLogo, extent = [XMin, XMax, YMin, YMax], aspect = 'auto', alpha = 0.1)
		mpl.gca().set_aspect(abs((XMax - XMin) / (YMax - YMin)))

		# Export figure to file
		mpl.savefig(f"plots/players.png")
		mpl.clf()


# ===================================================
# Trophy points vs. Date (point per marathon, line per TC, plot per ranking)
# ===================================================

def PlotTrophyPoints():
	for rank in trophy_rankings:
		mpl.close()
		mpl.figure()
		Legend = []

		for tc in marathons:
			X = []
			Y = []
			Legend.append(tc)
			for id in marathons[tc]:
				X.append(datetime.datetime.strptime(marathons[tc][id]["info"]["startsAt"][:-5], "%Y-%m-%dT%H:%M:%S"))
				Y.append(marathons[tc][id]["results"][rank - 1]["score"])

			X, Y = zip(*sorted(zip(X, Y)))
			mpl.plot(X, Y, marker="o", antialiased = True)#, color = UserColor, linestyle = UserStyle, marker = UserMarker, markevery = 0.1)

		# Processing plot
		mpl.gca().set_ylim([0, None])
		mpl.legend(Legend, loc = 'upper left', fontsize = 11, title = "Time Control", title_fontsize = 11)

		# Post-processing for all plots
		mpl.xticks(rotation = 45)
		mpl.grid(alpha = 0.5)
		mpl.title(f"Score of #{rank}")
		mpl.ylabel("Scores")
		mpl.tight_layout()

		# Add lichess logo as background, and fix aspect ratio to 1
		XMin, XMax = mpl.gca().get_xlim()
		YMin, YMax = mpl.gca().get_ylim()
		mpl.gca().imshow(LichessLogo, extent = [XMin, XMax, YMin, YMax], aspect = 'auto', alpha = 0.1)
		mpl.gca().set_aspect(abs((XMax - XMin) / (YMax - YMin)))

		# Export figure to file
		mpl.savefig(f"plots/top{rank}.png")
		mpl.clf()


# ===================================================
# Trophy points vs. Date (point per marathon, line per TC, plot per ranking)
# ===================================================

def PlotTrophyPointsTC():
	for tc in marathons:
		mpl.close()
		mpl.figure()
		Legend = []

		for r in trophy_rankings:
			X = []
			Y = []
			Legend.append((f"Top {r}" if r > 1 else "Winner"))
			for (id, dict) in sorted(marathons[tc].items(), key = lambda item: item[1]["info"]["startsAt"], reverse = True):
				X.append(datetime.datetime.strptime(marathons[tc][id]["info"]["startsAt"][:-5], "%Y-%m-%dT%H:%M:%S"))
				Y.append(marathons[tc][id]["results"][r - 1]["score"])

			X, Y = zip(*sorted(zip(X, Y)))
			mpl.plot(X, Y, marker="o", antialiased = True)#, color = UserColor, linestyle = UserStyle, marker = UserMarker, markevery = 0.1)

		# Processing plot
		mpl.gca().set_ylim([0, None])
		mpl.legend(Legend, loc = "upper left", fontsize = 11, title = "Trophies", title_fontsize = 11)

		# Post-processing for all plots
		mpl.xticks(rotation = 45)
		mpl.grid(alpha = 0.5)
		mpl.title(f"Scores per trophy ({tc})")
		mpl.ylabel("Scores")
		mpl.tight_layout()

		# Add lichess logo as background, and fix aspect ratio to 1
		XMin, XMax = mpl.gca().get_xlim()
		YMin, YMax = mpl.gca().get_ylim()
		mpl.gca().imshow(LichessLogo, extent = [XMin, XMax, YMin, YMax], aspect = 'auto', alpha = 0.1)
		mpl.gca().set_aspect(abs((XMax - XMin) / (YMax - YMin)))

		# Export figure to file
		mpl.savefig(f"plots/{tc}_top.png")
		mpl.clf()


# ===================================================
# Points vs. Ranking (point per player, line per marathon, plot per TC)
# ===================================================

def PlotPointsRanking():

	for tc in marathons:
		mpl.close()
		mpl.figure()
		Legend = []

		#for id in marathons[tc]:
		for (id, dict) in sorted(marathons[tc].items(), key = lambda item: item[1]["info"]["startsAt"], reverse = True):
			X = []
			Y = []
			Legend.append(id)
			for i in range(len(marathons[tc][id]["results"])):
				if marathons[tc][id]["results"][i]["score"] < 10 or i > 10 ** 3:
					break
				X.append(i + 1)
				Y.append(marathons[tc][id]["results"][i]["score"])
			mpl.plot(X, Y, antialiased = True)#, color = UserColor, linestyle = UserStyle, marker = UserMarker, markevery = 0.1)

		# Processing plot

		#mpl.gca().set_ylim([, None])
		mpl.legend(Legend, loc = "lower left", fontsize = 11, title = "Marathons", title_fontsize = 11)

		mpl.xticks(rotation = 45)

		mpl.grid(which = "both", alpha = 0.5)
		mpl.title(f"Scores for each ranking ({tc})")
		mpl.ylabel("Scores")
		mpl.xlabel("Ranking")
		mpl.tight_layout()

		mpl.xscale("log")
		mpl.yscale("log")
		mpl.gca().axvline(1, color='green')
		mpl.gca().axvline(10, color='green')
		mpl.gca().axvline(50, color='green')
		mpl.gca().axvline(100, color='green')
		mpl.gca().axvline(500, color='green')

		# Export figure to file
		mpl.savefig(f"plots/{tc}_points.png")
		mpl.clf()


# ===================================================
# Ratings vs. Trophies (rating distribution per trophy, one violin per trophy, one plot per marathon)
# ===================================================

def PlotRatingTrophy():
	for tc in marathons:
		for id in marathons[tc]:
			mpl.close()
			mpl.figure()
			fig, ax = mpl.subplots()
			X = []

			for r in trophy_rankings:
				X.append([])

				for i in range(r):
					if "rating" not in marathons[tc][id]["results"][i]:
						continue
					X[-1].append(marathons[tc][id]["results"][i]["rating"])

			bp = mpl.violinplot(X, positions=range(len(trophy_rankings)), widths=0.8)
			mpl.setp(ax, xticks=[y for y in range(len(trophy_rankings))], xticklabels=["Winner", "Top 10", "Top 50", "Top 100", "Top 500"])

			mpl.title(f"Rating per trophy ({tc}/{id})")
			mpl.ylabel("Rating")
			mpl.tight_layout()
			mpl.grid(alpha = 0.5)

			# Add lichess logo as background, and fix aspect ratio to 1
			XMin, XMax = mpl.gca().get_xlim()
			YMin, YMax = mpl.gca().get_ylim()
			mpl.gca().imshow(LichessLogo, extent = [XMin, XMax, YMin, YMax], aspect = 'auto', alpha = 0.1)
			mpl.gca().set_aspect(abs((XMax - XMin) / (YMax - YMin)))

			# Export figure to file
			mpl.savefig(f"plots/{id}_rating_violin.png")
			mpl.clf()
			mpl.close(fig)


# ===================================================
# Ratings vs. Trophies (rating distribution per trophy, one violin per trophy/marathon, one plot per TC)
# ===================================================

def PlotRatingTrophyTC():
	for tc in marathons:
		mpl.close()
		mpl.figure()
		fig, ax = mpl.subplots()
		Legend = []
		LegendCols = []

		#for id in marathons[tc]:
		for (id, dict) in sorted(marathons[tc].items(), key = lambda item: item[1]["info"]["startsAt"], reverse = True):
			X = []
			Legend.append(id)

			for r in trophy_rankings:
				X.append([])

				for i in range(r):
					if "rating" not in marathons[tc][id]["results"][i]:
						continue
					X[-1].append(marathons[tc][id]["results"][i]["rating"])

			bp = mpl.violinplot(X, positions=range(len(trophy_rankings)), widths=0.8)
			LegendCols.append(bp["cbars"])
			mpl.setp(ax, xticks=[y for y in range(len(trophy_rankings))], xticklabels=["Winner", "Top 10", "Top 50", "Top 100", "Top 500"])

		mpl.legend(LegendCols, Legend, loc = "lower left", fontsize = 11, title = "Marathons", title_fontsize = 11)
		mpl.title(f"Rating per trophy ({tc})")
		mpl.ylabel("Rating")
		mpl.tight_layout()
		mpl.grid(alpha = 0.5)

		# Add lichess logo as background, and fix aspect ratio to 1
		XMin, XMax = mpl.gca().get_xlim()
		YMin, YMax = mpl.gca().get_ylim()
		mpl.gca().imshow(LichessLogo, extent = [XMin, XMax, YMin, YMax], aspect = 'auto', alpha = 0.1)
		mpl.gca().set_aspect(abs((XMax - XMin) / (YMax - YMin)))

		# Export figure to file
		mpl.savefig(f"plots/{tc}_rating_violin.png")
		mpl.clf()
		mpl.close(fig)


# ===================================================
# Games vs. Ratings for trophy winners (one point per trophy winner, one plot per marathon)
# ===================================================

def PlotGamesRating():
	for tc in marathons:
		for id in marathons[tc]:
			mpl.close()
			mpl.figure()
			fig, ax = mpl.subplots()
			Legend = []

			for j in range(len(trophy_rankings)):
				r = trophy_rankings[j]
				prev_r = (0 if j == 0 else trophy_rankings[j-1])
				X = []
				Y = []
				Legend.append((f"Top {r}" if r > 1 else "Winner"))
				for i in range(prev_r, r):
					X.append(marathons[tc][id]["results"][i]["rating"])
					Y.append(marathons[tc][id]["results"][i]["games"])

				mpl.scatter(X, Y)

				# # Linear regression
				# slope, intercept, rr, pp, std_err = stats.linregress(X, Y)
				# mymodel = list(map(lambda y: slope * y + intercept, X))
				# mpl.plot(X, mymodel)

				# # Showing a convex hull
				# if r > 3:
				#	XY = [[float(x), float(y)] for [x, y] in zip(X, Y)]
				#	hull = ConvexHull(XY)
				#	convex_hull_plot_2d(hull)

			mpl.legend(Legend, loc = "lower left", fontsize = 11, title = "Trophies", title_fontsize = 11)
			mpl.title(f"Ratings/games per trophy ({tc}/{id})")
			mpl.xlabel("Rating")
			mpl.ylabel("Games")
			mpl.gca().set_ylim([0, None])
			mpl.tight_layout()
			mpl.grid(alpha = 0.5)

			# Add lichess logo as background, and fix aspect ratio to 1
			XMin, XMax = mpl.gca().get_xlim()
			YMin, YMax = mpl.gca().get_ylim()
			mpl.gca().imshow(LichessLogo, extent = [XMin, XMax, YMin, YMax], aspect = 'auto', alpha = 0.1)
			mpl.gca().set_aspect(abs((XMax - XMin) / (YMax - YMin)))

			# Export figure to file
			mpl.savefig(f"plots/{id}_rating_games.png")
			mpl.clf()
			mpl.close(fig)


# Data fetching/processing
#GetPlayerPages()
#UpdateResults()

# Text-form list of players by trophies
ShowTrophyRankings()

# Generating various types of plots
PlotPlayers()
PlotTrophyPoints()
PlotTrophyPointsTC()
PlotPointsRanking()
PlotRatingTrophy()
PlotRatingTrophyTC()
PlotGamesRating()
