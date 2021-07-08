PrevLine = ""
NextLine = ""
OpeningList = dict()
with open("openings.txt", "r") as InFile:
	for Line in InFile:
		PrevLine = NextLine
		NextLine = Line
		if len(NextLine) > 3 and NextLine[0:3] == "FEN":
			OpeningName = (PrevLine.strip())[1:-2].split(":")[0].strip()
			OpeningList[OpeningName] = 1

print(len(OpeningList))
with open("thematicnames.txt", "w") as OutFile:
	for OpeningName in OpeningList:
		OutFile.write(f"{OpeningName}\n")
	
			