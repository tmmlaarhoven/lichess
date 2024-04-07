import requests
import re
import os
import time
import collections
import os.path
import ndjson
import shutil
from Utilities import *

print("\n=== Starting Caller.py ===\n")

# Default: No plots
DrawPlots = True

BuildIndexPage()
BuildPlayerIndex()

Cat = dict()
for V in AllVariants:
	if V in {"3check", "antichess", "atomic", "blitz", "bullet", "chess960", "classical", "crazyhouse", "horde", "hyperbullet", "koth", "racingkings", "rapid", "superblitz", "ultrabullet"}:
		continue
		
	Cat[V] = dict()
	for E in AllEvents:

		
		# Always first update everything else
		Cat[V][E] = ArenaCategory(V, E)
		Cat[V][E].LoadRankings()
		Cat[V][E].UpdateRankings()
		if DrawPlots:
			Cat[V][E].UpdatePlots()
		Cat[V][E].UpdateWebsite()
		del Cat[V][E]

print("\n=== Finished Caller.py ===\n")
