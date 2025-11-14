#!/bin/bash
set +e
# kill youtube.py if running
pgrep -f youtube.py | xargs kill -9 2>/dev/null
# kill geckodriver if running
pgrep -f geckodriver | xargs kill -9 2>/dev/null
# kill firefox if running
pgrep -f firefox | xargs kill -9 2>/dev/null
# export path for geckodriver
export PATH="$PATH:/home/situser/Documents/youtube-selenium/driver/geckodriver"
# change directory
cd /home/situser/Documents/youtube-selenium/
# activate virtual environment
source /home/situser/Documents/youtube-selenium/.venv/bin/activate
# run youtube.py in background
nohup python youtube.py >> /home/situser/Documents/youtube-selenium/youtube.out 2>&1 < /dev/null & 
# deactivate virtual environment
deactivate