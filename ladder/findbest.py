import os
rootdir = "E:\\lichess\\gamesdb-out\\"


with open("2700games-new.csv", "a") as TopFile:
	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			if len(file) < 8 or file[26:33] in {"2021-05", "2021-06"}:
				continue
			print(os.path.join(subdir, file))
			with open(os.path.join(subdir, file), "r") as InFile:
				for Line in InFile:
					if int(Line[91:95].strip()) > 2700:
						print(Line[29:49] + " -- " + Line.strip())
						TopFile.write(Line)
					if int(Line[96:100].strip()) > 2700:
						print(Line[50:70] + " -- " + Line.strip())
						TopFile.write(Line)