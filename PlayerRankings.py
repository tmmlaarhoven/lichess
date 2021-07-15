import os
import os.path
import ndjson
import json
from collections import OrderedDict

# All variants to update
PureVariants = {"3check", "antichess", "atomic", "blitz", "bullet", "chess960", "classical", "crazyhouse", "horde", "hyperbullet", "koth", "racingkings", "rapid", "superblitz", "ultrabullet"}
AllVariants = PureVariants.copy()
AllVariants.add("all")

# All events to consider
PureEvents = {"hourly", "2000", "1700", "1600", "1500", "1300", "thematic", "daily", "weekly", "monthly", "yearly", "eastern", "elite", "shield", "titled", "marathon", "liga"}
AllEvents = PureEvents.copy()
AllEvents.add("all")

def PrintMessage(V: str, E: str, Message: str):
	print(f"{V:<11} - {E:<8} - {Message}")	


for V in AllVariants:
	for E in AllEvents:
		
		if V == "all" and E == "all":
			break
		
		if not os.path.exists(f"E:\\lichess\\tournaments\\rankings\\{V}\\{E}\\{V}_{E}_arenas.ndjson") or not os.path.exists(f"E:\\lichess\\tournaments\\rankings\\{V}\\{E}\\players\\{V}_{E}__events.txt"):
			continue
		
		# 1. Fetch arenas that are in the rankings already
		ArenasRanking = dict()
		with open(f"E:\\lichess\\tournaments\\rankings\\{V}\\{E}\\{V}_{E}_arenas.ndjson", "r") as File:
			for Line in File:
				ArenaDict = json.loads(Line)
				ArenasRanking[ArenaDict["ID"]] = ArenaDict	

		# 2. Store in correct file
		SortedIDList = OrderedDict(sorted(ArenasRanking.items(), key = lambda item: item[0]))
		with open(f"E:\\lichess\\tournaments\\rankings\\{V}\\{E}\\players\\{V}_{E}__events.txt", "w") as File:
			for Arena in SortedIDList:
				File.write(Arena + "\n")





# Old stuff: unnecessary, as files already up to date

if False:


	# Do updates
	#for V in AllVariants:
	for V in {"3check"}:
		for E in {"hourly"}:
	#	for E in AllEvents:

			# File formats
			FileRankingEvents = f"E:\\lichess\\tournaments\\rankings\\{V}\\{E}\\{V}_{E}_arenas.ndjson"			# Dicts of arenas in website rankings (with V/E provided)
			FilePlayerEvents = f"E:\\lichess\\tournaments\\rankings\\{V}\\{E}\\players\\{V}_{E}__events.txt"	# List of IDs in player rankings
			FilePlayerList = f"E:\\lichess\\tournaments\\rankings\\{V}\\{E}\\players\\{V}_{E}.txt"				# List of player names for player rankings
			#FilePlayerInfo = f"E:\\lichess\\tournaments\\rankings\\{V}\\{E}\\players\\{V}_{E}_{Player}.json"	# Latest player statistics, as well as first/last ID, etc.
			#FilePlayerPlot = f"E:\\lichess\\tournaments\\rankings\\{V}\\{E}\\players\\{V}_{E}_{Player}.ndjson"	# All player statistics, for cumulative plots
			
			# 0. Check if rankings even exist at all
			if not os.path.exists(FileRankingEvents) or not os.path.exists(FilePlayerEvents) or not os.path.exists(FilePlayerList):
				PrintMessage(V, E, "Nothing to do, no rankings exist.")
			
			# 1. Fetch arenas that are in the rankings already
			ArenasRanking = dict()
			with open(FileRankingEvents, "r") as File:
				for Line in File:
					ArenaDict = json.loads(Line)
					ArenasRanking[ArenaDict["ID"]] = ArenaDict
			PrintMessage(V, E, f"Loaded {len(ArenasRanking)} detailed arenas in memory.")
			
			# 2. Fetch arenas that have been included in cumulative player rankings
			ArenasPlayers = dict()
			with open(FilePlayerEvents, "r") as File:
				for Line in File:
					ArenaID = Line.strip()
					ArenasPlayers[ArenaID] = 1
			PrintMessage(V, E, f"Loaded {len(ArenasPlayers)} preprocessed arenas in memory.")
			
			# 3. Make list of new arenas
			NewArenas = dict()
			for ArenaID in ArenasRanking:
				if ArenaID not in ArenasPlayers:
					NewArenas[ArenaID] = 1
			PrintMessage(V, E, f"Found {len(NewArenas)} new arena IDs.")		
			
			# 4. If they are the same, break
			if len(NewArenas) == 0:
				PrintMessage(V, E, f"Up to date, nothing to do.")	
				continue
			
			# 5. Fetch list of relevant players
			RelevantPlayers = dict()
			with open(FilePlayerList, "r") as File:
				for Line in File:
					UserID = Line.strip().lower()
					RelevantPlayers[UserID] = 1
			PrintMessage(V, E, f"Found {len(RelevantPlayers)} relevant players to process.")
			
			# 6. Fetch latest player infos
			UserJSON = dict()
			for UserID in RelevantPlayers:
				with open(f"E:\\lichess\\tournaments\\rankings\\{V}\\{E}\\players\\{V}_{E}_{UserID}.json", "r") as File:
					for Line in File:
						TempDict = json.loads(Line)
						UserJSON[UserID] = TempDict	
				
			# 7. Fetch total history of cumulative scores
			UserNDJSON = dict()
			for UserID in RelevantPlayers:
				HistoryList = []
				with open(f"E:\\lichess\\tournaments\\rankings\\{V}\\{E}\\players\\{V}_{E}_{UserID}.ndjson", "r") as File:
					for Line in File:
						TempDict = json.loads(Line)
						HistoryList.append(TempDict)
				UserNDJSON[UserID] = HistoryList
			
			# 8. For each arena not in cumulative rankings:
			UpdatedPlayers = dict()
			for ArenaID in NewArenas:
			
				# Indicate we are processing this arena now
				ArenasPlayers[ArenaID] = 1
				
				# Extract right variant and event, for mixed arenas
				ArenaV = ArenasRanking[ArenaID]["Variant"]
				ArenaE = ArenasRanking[ArenaID]["Event"]
				PrintMessage(ArenaV, ArenaE, f"Processing arena {ArenaID}...")
				
				# Fetch detailed results from right file (V, E)
				with open(f"E:\\lichess\\tournaments\\data\\{ArenaV}\\{ArenaE}\\{ArenaV}_{ArenaE}_{ArenaID}.ndjson", "r") as File:
					for Line in File:
						UserResult = json.loads(Line)
						# {"rank":1,"score":25,"rating":1646,"username":"Good_Luck_Have_Fun","performance":1927}
						
						# We are at the end when the score equals 0, as it is sorted
						if UserResult["score"] == 0:
							break
						
						# Update any relevant user we encounter			
						if UserResult["username"].lower() in RelevantPlayers and UserResult["score"] > 0:
							
							# Update JSON stats
							UserID = UserResult["username"].lower()
							if UserJSON[UserID]["FirstID"] == "-":
								UserJSON[UserID]["FirstID"] = ArenaID
							if len(UserJSON[UserID]["LastID"]) < 8 or (ArenasRanking[ArenaID]["Start"] > ArenasRanking[UserJSON[UserID]["LastID"]]["Start"]):
								UserJSON[UserID]["LastID"] = ArenaID
							if UserResult["rank"] == 1:
								UserJSON[UserID]["CumTrophies"][0] = UserJSON[UserID]["CumTrophies"][0] + 1
							elif UserResult["rank"] == 2:
								UserJSON[UserID]["CumTrophies"][1] = UserJSON[UserID]["CumTrophies"][1] + 1
							elif UserResult["rank"] == 3:
								UserJSON[UserID]["CumTrophies"][2] = UserJSON[UserID]["CumTrophies"][2] + 1
							UserJSON[UserID]["CumPoints"] = UserJSON[UserID]["CumPoints"] + UserResult["score"]
							UserJSON[UserID]["CumEvents"] = UserJSON[UserID]["CumEvents"] + 1
							UserJSON[UserID]["CumTopScore"] = max(UserJSON[UserID]["CumTopScore"], UserResult["score"])
							
							# Update NDJSON stats
							newdict = dict()
							newdict["ID"] = ArenaID
							newdict["Start"] = ArenasRanking[ArenaID]["Start"]
							newdict["CumTrophies"] = UserJSON[UserID]["CumTrophies"].copy()
							newdict["CumPoints"] = UserJSON[UserID]["CumPoints"]
							newdict["CumEvents"] = UserJSON[UserID]["CumEvents"]
							newdict["CumTopScore"] = UserJSON[UserID]["CumTopScore"]
							UserNDJSON[UserID].append(newdict)
							
							UpdatedPlayers[UserID] = 1


			PrintMessage(V, E, f"Processed {len(NewArenas)} arenas. Now {len(ArenasRanking)} in ranking and {len(ArenasPlayers)} in player history.")
			assert(len(ArenasRanking) == len(ArenasPlayers)), "WTF?"
			
			# Abort if nothing happened
			if len(UpdatedPlayers) == 0:
				PrintMessage(V, E, "No updated players. Done!")
				continue
			else:
				PrintMessage(V, E, f"Updated records for {len(UpdatedPlayers)} new players.")
				for UserID in UpdatedPlayers:
					PrintMessage(V, E, f"Example player that got updated: {UserID}")
					break

			# 9. Store processed IDs to files
			SortedIDList = OrderedDict(sorted(ArenasPlayers.items(), key = lambda item: item[0]))
			with open(FilePlayerEvents, "w") as File:
				for ArenaID in SortedIDList:
					File.write(ArenaID + "\n")
				
			# 10. Store latest player infos in files
			for UserID in UpdatedPlayers:
				PrintMessage(V, E, f"Storing {V}_{E}_{UserID}.json")
				with open(f"E:\\lichess\\tournaments\\rankings\\{V}\\{E}\\players\\{V}_{E}_{UserID}.json", "w") as File:
					json.dump(UserJSON[UserID], File)
				
			# 11. Store all cumulative player rankings in file
			for UserID in UpdatedPlayers:
				PrintMessage(V, E, f"Storing {V}_{E}_{UserID}.ndjson")
				with open(f"E:\\lichess\\tournaments\\rankings\\{V}\\{E}\\players\\{V}_{E}_{UserID}.ndjson", "w") as File:
					for Index in range(len(UserNDJSON[UserID])):
						File.write(json.dumps(UserNDJSON[UserID][Index]) + "\n")
			
			PrintMessage(V, E, f"All done!")
			
			