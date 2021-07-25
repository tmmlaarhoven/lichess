import json
import ndjson
import requests
import math
import time

with open("E:\\lichess\\APIToken.txt", "r") as TokenFile:
	for Line in TokenFile:
		APIToken = Line.strip()


GMList = []
with open("E:\\lichess\\tournaments\\rankings\\all\\all\\all_all_players_title.ndjson", "r") as File:
	for Line in File:
		Player = json.loads(Line)
		if Player["Title"] != "GM":
			break
		GMList.append(Player["Username"].lower())


GMList.sort()
with open("gmlist.txt", "w") as OutFile:	
	for Username in GMList:
		OutFile.write(Username + "\n")

GMListCopy = GMList.copy()

OutGMList = []
GroupSize = 200
for i in range(math.ceil(len(GMList) / GroupSize)):
	
	time.sleep(5)
	begin = i * GroupSize
	end = min(i * GroupSize + GroupSize, len(GMList))
	print(f"Group {i+1}: Users {GMList[begin]} to {GMList[end-1]}.")
	r = requests.post("https://lichess.org/api/users", headers = {"Authorization": "Bearer " + APIToken}, data = ",".join(GMList[begin:end]))
	if r.status_code == 429:
		print("RATE LIMIT!")
		time.sleep(100000)

	APIResponse = ndjson.loads(r.content)[0]	# List of dictionaries
	# No responses from closed accounts
	for PlayerInfo in APIResponse:
		if ("closed" in PlayerInfo) or ("tosViolation" in PlayerInfo):
			continue
		OutGMList.append((PlayerInfo["perfs"]["bullet"]["rating"], PlayerInfo["username"]))

OutGMList.sort(reverse = True)

for (Rating, Username) in OutGMList:
	print(f"{Username} ({Rating})")
	
for (Rating, Username) in OutGMList:
	if Username.lower() in GMListCopy:
		GMListCopy.remove(Username.lower())
		
for Username in GMListCopy:
	print(f"Not found: {Username}.")