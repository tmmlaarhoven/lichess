import requests
import re

Variants = {
	"3check": "Three-check",
	"antichess": "Antichess",
	"atomic": "Atomic",
	"blitz": "Blitz",
	"bullet": "Bullet",
	"chess960": "Chess960",
	"classical": "Classical",
	"crazyhouse": "Crazyhouse",
	"horde": "Horde",
	"hyperbullet": "HyperBullet",
	"koth": "King of the Hill",
	"racingkings": "Racing Kings",
	"rapid": "Rapid",
	"superblitz": "SuperBlitz",
	"ultrabullet": "UltraBullet"
}

ThematicNames = dict()
with open("thematicnames.txt") as ThematicNamesFile:
	for Line in ThematicNamesFile:
		ThematicNames[Line.strip()] = 1

	
Page = 21
r = requests.get(f"https://lichess.org/tournament/history/hourly?page={Page}")

if r.status_code == 429:
	print("RATE LIMIT!")
	time.sleep(1000000)

IDs = re.findall(f"/tournament/[0-9a-zA-Z]{{8}}\"><span class=\"name\">.{{0,40}} Arena", r.text)

print(f"Hmmm - {len(IDs)}")
for ID in IDs:
	if any(x in ID[41:-6] for x in {"Hourly", "&lt;1300", "&lt;1500", "&lt;1600", "&lt;1700", "&lt;2000"}):
		continue
	print(f".{ID[41:-6]}.")
	for V in Variants:
		if Variants[V] in ID[41:-6]:
			print(f"{ID[41:-6]} is a {V} arena!")
			
			
			