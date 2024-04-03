import json
import os
import requests
import datetime

DriveRootWindows = "E:\\lichess\\"
DriveRootLinux = "/media/thijs/SED/lichess/"
DriveRoot = DriveRootLinux

APIToken = ""
with open(f"{DriveRoot}APItoken.txt", "r") as TokenFile:
	for Line in TokenFile:
		APIToken = Line.strip()


def PrintMessage(Message: str):
	print(f"{'all':<11} - {'liga':<8} - {Message}", end = "")

SuperBlitzList = dict()
BlitzList = dict()

print("\n=== Starting LigaUpdater.py ===\n")

# Load previous IDs

with open(f"{DriveRoot}tournaments{os.sep}data{os.sep}superblitz{os.sep}liga{os.sep}superblitz_liga.txt", "r") as SuperBlitzFile:
	for Line in SuperBlitzFile:
		SuperBlitzList[Line.strip()] = 1

print(f"Currently {len(SuperBlitzList)} superblitz ligas in ranking.")

with open(f"{DriveRoot}tournaments{os.sep}data{os.sep}blitz{os.sep}liga{os.sep}blitz_liga.txt", "r") as BlitzFile:
	for Line in BlitzFile:
		BlitzList[Line.strip()] = 1

print(f"Currently {len(BlitzList)} blitz ligas in ranking.")


# Load new IDs and stop when e.g. 100 Collisions

Collisions = 0
requests.packages.urllib3.util.connection.HAS_IPV6 = False
s = requests.Session()
with s.get("https://lichess.org/api/user/jeffforever/tournament/created", headers = {"Authorization": f"Bearer {APIToken}"}, stream = True) as Response:
	for Line in Response.iter_lines():
		dict = json.loads(Line)
		PrintMessage(f"New ID ({dict.get('id', 'Nothing')}) at {datetime.datetime.fromtimestamp(dict['startsAt']/1000).strftime('%Y-%m-%d %H:%M:%S. ')}")

		if ("liga" not in dict["fullName"].lower()):
			print("Skipping (not bundesliga).")
			continue

		if ("secondsToStart" in dict) or ("secondsToFinish" in dict):
			print("Skipping (future ID).")
			continue

		if dict["clock"]["limit"] == 180 and dict["clock"]["increment"] == 0:
			if dict["id"] not in SuperBlitzList:
				SuperBlitzList[dict["id"]] = 1
				print("New superblitz arena!")
			else:
				print("Skipping (already in superblitz list).")
				Collisions = Collisions + 1
		else:
			if dict["id"] not in BlitzList:
				BlitzList[dict["id"]] = 1
				print("New blitz arena!")
			else:
				print("Skipping (already in blitz list).")
				Collisions = Collisions + 1

		if Collisions > 100:
			break





TempList = []
for ID in SuperBlitzList:
	TempList.append(ID)
TempList.sort()
with open(f"{DriveRoot}tournaments{os.sep}data{os.sep}superblitz{os.sep}liga{os.sep}superblitz_liga.txt", "w") as SuperBlitzFile:
	for ID in TempList:
		SuperBlitzFile.write(ID + "\n")


TempList = []
for ID in BlitzList:
	TempList.append(ID)
TempList.sort()
with open(f"{DriveRoot}tournaments{os.sep}data{os.sep}blitz{os.sep}liga{os.sep}blitz_liga.txt", "w") as BlitzFile:
	for ID in TempList:
		BlitzFile.write(ID + "\n")

print("\n=== Finished LigaUpdater.py ===\n")
