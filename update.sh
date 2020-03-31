#!/bin/bash

# 
# 1: update the covid-19 data.
# 
echo 'update.sh: Pulling fresh data from GitHub...'
cd ../covid19-data
git pull origin master
cd ../covid19-anal
echo 'update.sh: Done pulling GitHub data.'

# 
# 2: run the analyzer script.
# 
echo 'update.sh: Initiating covid19_analyzer...'
python3 ./covid19_analyzer.py
echo 'update.sh: Done running covid19_analyzer.'

# 
# 3: done.
# 
echo 'update.sh: Done.'

