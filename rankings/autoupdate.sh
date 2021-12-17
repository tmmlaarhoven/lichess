#!/bin/bash
updtime=$(date)
git pull
# rem ScanPlayers.py
LigaUpdater.py
FetchData.py
Caller.py
DensityPlot.py
git add --all --verbose
git commit -m "Auto-updater - %updtime%" --verbose
git push --verbose
