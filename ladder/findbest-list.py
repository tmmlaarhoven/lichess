import json
import ndjson
import requests
import math
import time

with open("E:\\lichess\\APIToken.txt", "r") as TokenFile:
	for Line in TokenFile:
		APIToken = Line.strip()

Players = dict()
with open("2700games.csv", "r") as InFile:
	for Number, Line in enumerate(InFile):
		if Number % 10000 == 0:
			print(f"Line {Number}.")
		RatingWhite = int(Line[91:95].strip())
		UserWhite = Line[29:49].strip().lower()
		RatingBlack = int(Line[96:100].strip())
		UserBlack = Line[50:70].strip().lower()
		if RatingWhite > 2700:
			if RatingWhite > Players.get(UserWhite, -1):
				Players[UserWhite] = RatingWhite
		if RatingBlack > 2700:
			if RatingBlack > Players.get(UserBlack, -1):
				Players[UserBlack] = RatingBlack
				
PlayersList = [(Players[x], x) for x in Players]
PlayersList.sort(reverse = True)

IgnoreList = dict()
with open("ignorelist.txt", "r") as InFile:
	for Line in InFile:
		IgnoreList[Line.strip().lower()] = 1

CrossTableList = dict()
with open("E:\\lichess\\crosstable\\highestbulletsorted.txt", "r") as AllFile:
	for Line in AllFile:
		Dict = json.loads(Line)
		CrossTableList[Dict["Username"].lower()] = 1
		
DoCheck = []
for (Rating, User) in PlayersList:
	if User not in IgnoreList:
		#print(f"{User} ({Rating})")
		if User not in CrossTableList:
			print(f"Don't forget: {User}")
			DoCheck.append(User)
	if Rating < 2800:
		break
		
print(len(DoCheck))
GroupSize = 200
OutList = []
for i in range(math.ceil(len(DoCheck) / GroupSize)):
	
	time.sleep(5)
	begin = i * GroupSize
	end = min(i * GroupSize + GroupSize, len(DoCheck))
	print("Group " + str(i+1) + ": Users " + DoCheck[begin] + " to " + DoCheck[end-1] + ".")
	r = requests.post("https://lichess.org/api/users", headers = {"Authorization": "Bearer " + APIToken}, data = ",".join(DoCheck[begin:end]))
	if r.status_code == 429:
		print("RATE LIMIT!")
		time.sleep(100000)

	APIResponse = ndjson.loads(r.content)[0]	# List of dictionaries
	for PlayerInfo in APIResponse:
		if ("closed" in PlayerInfo) or ("tosViolation" in PlayerInfo) or ("title" not in PlayerInfo) or (PlayerInfo["title"] != "GM"):
			continue
		OutList.append((PlayerInfo["perfs"]["bullet"]["rating"], PlayerInfo["username"]))

print(len(OutList))
OutList.sort(key = lambda item: item[0], reverse = True)

for (Rating, User) in OutList:
	print(f"GM {User:<20} - {Rating}")