@ECHO OFF
setlocal enabledelayedexpansion

rem Wait at least 6 hours (=21600 seconds) until quarter past an hour
:wait
set /a "hour=%hour:~0,2%"
set /a "hour=!hour: =!"
set /a "minu=%time:~3,2%"
set /a "minu=!minu: =!"
if !minu! LEQ 15 (
	set /a "delay=(15-!minu!)*60+21600"
)
if !minu! GTR 15 (
	set /a "delay=(75-!minu!)*60+21600"
)
timeout !delay!

rem Main loop: pull, fetch data, update rankings, and push
:loop
set updtime=%date%, %time%
git pull
rem ScanPlayers.py
LigaUpdater.py
FetchData.py
Caller.py
DensityPlot.py
git add --all --verbose
git commit -m "Auto-updater - %updtime%" --verbose
git push --verbose
goto wait
