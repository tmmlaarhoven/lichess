#!/bin/bash
date_stamp=$(date +"%F %H:%M:%S")
git pull
# python3 ScanPlayers.py
# python3 LigaUpdater.py
python3 FetchData.py
python3 Caller.py
python3 DensityPlot.py
git add --all --verbose
git commit -m "Auto-updater - $date_stamp" --verbose
git push --verbose
