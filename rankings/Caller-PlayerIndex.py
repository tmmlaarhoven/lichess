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

BuildPlayerIndex()

print("\n=== Finished Caller.py ===\n")
