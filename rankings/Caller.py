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
DrawPlots = False

BuildIndexPage()

Cat = dict()
for V in AllVariants:
	Cat[V] = dict()
	for E in AllEvents:

		# Always first update everything else
		Cat[V][E] = ArenaCategory(V, E)
		Cat[V][E].LoadRankings()
		Cat[V][E].UpdateRankings()
		if DrawPlots or E in {"marathon", "titled"}:
			Cat[V][E].UpdatePlots()
		Cat[V][E].UpdateWebsite()
		del Cat[V][E]

print("\n=== Finished Caller.py ===\n")
