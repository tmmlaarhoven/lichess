import json
import requests
import datetime

APIToken = ""
with open("E:\\lichess\\APIToken.txt", "r") as TokenFile:
	for Line in TokenFile:
		APIToken = Line.strip()


sblist = dict()
blist = dict()



# Load previous IDs

with open("E:\\lichess\\tournaments\\data\\superblitz\\liga\\superblitz_liga.txt", "r") as sbfile:
	for Line in sbfile:
		sblist[Line.strip()] = 1

print(f"Currently {len(sblist)} superblitz ligas in ranking.")

with open("E:\\lichess\\tournaments\\data\\blitz\\liga\\blitz_liga.txt", "r") as bfile:
	for Line in bfile:
		blist[Line.strip()] = 1
	
print(f"Currently {len(blist)} blitz ligas in ranking.")


# Load new IDs and stop when e.g. 100 collisions

collisions = 0
s = requests.Session()
with s.get("https://lichess.org/api/user/jeffforever/tournament/created", headers = {"Authorization": f"Bearer {APIToken}"}, stream = True) as Response:
	for Line in Response.iter_lines():
		dict = json.loads(Line)
		print(dict.get("id", "Nothing") + " " + datetime.datetime.fromtimestamp(dict["startsAt"]/1000).strftime('%Y-%m-%d %H:%M:%S '), end = "")
		if ("liga" not in dict["fullName"].lower()) or ("secondsToStart" in dict):
			print("skip")
			continue

		if dict["clock"]["limit"] == 180 and dict["clock"]["increment"] == 0:
			if dict["id"] not in sblist:
				sblist[dict["id"]] = 1
				print("new superblitz id!")
			else:
				print("already in list!")
				collisions = collisions + 1
		else:
			if dict["id"] not in blist:
				blist[dict["id"]] = 1	
				print("new blitz id!")
			else:
				print("already in list!")
				collisions = collisions + 1

		if collisions > 100:
			break





templist = []
for ID in sblist:
	templist.append(ID)
templist.sort()
with open("E:\\lichess\\tournaments\\data\\superblitz\\liga\\superblitz_liga.txt", "w") as sbfile:
	for ID in templist:
		sbfile.write(ID + "\n")


templist = []
for ID in blist:
	templist.append(ID)
templist.sort()
with open("E:\\lichess\\tournaments\\data\\blitz\\liga\\blitz_liga.txt", "w") as bfile:
	for ID in templist:
		bfile.write(ID + "\n")
