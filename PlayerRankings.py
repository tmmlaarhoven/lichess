import requests
import re
import os
import time
import os.path
import ndjson
import json
import math
import datetime
import numpy as np
import matplotlib.pyplot as mpl
import random
from collections import OrderedDict
from typing import List, Union
from matplotlib.ticker import PercentFormatter
from itertools import product


PureVariants = {"3check", "antichess", "atomic", "blitz", "bullet", "chess960", "classical", "crazyhouse", "horde", "hyperbullet", "koth", "racingkings", "rapid", "superblitz", "ultrabullet"}
AllVariants = PureVariants.copy().add("all")

PureEvents = {"hourly", "2000", "1700", "1600", "1500", "1300", "thematic", "daily", "weekly", "monthly", "yearly", "eastern", "elite", "shield", "titled", "marathon", "liga"}
AllEvents = PureEvents.copy().add("all")

# Do updates
for V in AllVariants:
	for E in AllEvents:

		# Pure vs. mixed pairings, for fetching data
		Mixed = (False if (self._V in PureVariants and self._E in PureEvents) else True)

		# File formats
		FileRankingEvents = f"E:\\lichess\\tournaments\\rankings\\{V}\\{E}\\{V}_{E}_arenas.ndjson"			# Dicts of arenas in website rankings (with V/E provided)
		FilePlayerEvents = f"E:\\lichess\\tournaments\\rankings\\{V}\\{E}\\players\\{V}_{E}__events.txt"	# List of IDs in player rankings
		FilePlayerList = f"E:\\lichess\\tournaments\\rankings\\{V}\\{E}\\players\\{V}_{E}.txt"				# List of player names for player rankings
		#FilePlayerInfo = f"E:\\lichess\\tournaments\\rankings\\{V}\\{E}\\players\\{V}_{E}_{Player}.json"	# Latest player statistics, as well as first/last ID, etc.
		#FilePlayerPlot = f"E:\\lichess\\tournaments\\rankings\\{V}\\{E}\\players\\{V}_{E}_{Player}.ndjson"	# All player statistics, for cumulative plots
		
		# 1. Fetch arenas that are in the rankings already
		
		# 2. Fetch arenas that have been included in cumulative player rankings
		
		# 3. If they are the same, break
		
		# 4. Fetch list of relevant players
		
		# 5. for each relevant player:
			# a. Fetch latest player infos
			# b. Fetch total history of cumulative scores
		
		# 6. For each arena not in cumulative rankings:
			# a. Fetch detailed results from right file (V, E)
			# b. Update any relevant user we encounter, and remember we encountered them
			# c. For relevant users we missed, update with 0 new events, etc.
			
		# 7. Store results to files
			# a. Store arena IDs in playing rankings
			# b. Store latest player infos in files
			# c. Store all cumulative player rankings in files

		
			
		
		
		