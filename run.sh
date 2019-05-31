#!/bin/bash
# Script to calculate average page load time for each of the 
# top 10,000 ALEXA-ranked websites today
alias chrome="/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
ALEXA_ZIP_FILE_URL="http://s3.amazonaws.com/alexa-static/top-1m.csv.zip"
ALEXA_ZIP_FILE_LOC="./alexa_src_csv.zip"
ALEXA_ZIP_FILE_NAME="top-1m.csv"
Q="performance.getEntries()[0].duration;"
HTTP="http://"
HTTPS="https://"
function request {
  echo "performance.getEntries()[0].duration; " | /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --headless --disable-gpu --repl --crash-dumps-dir=./tmp $1 
}

function download_alexa_and_unzip {
  wget -O $ALEXA_ZIP_FILE_LOC $ALEXA_ZIP_FILE_URL
  unzip $ALEXA_ZIP_FILE_LOC
}

function to_txt {
  for line in `tac $ALEXA_ZIP_FILE_NAME`; do
    pline=`echo $line | tr "," " "`
    rank=`echo $pline | awk '{print $1;}'`
    site=`echo $pline | awk '{print $2;}'`
    let brank=1000000-rank
    if [ "$brank" -gt "$2" ]; then
      return 0
    elif [ "$brank" -gt "$1"  ]; then
      echo "aggregating "$brank" "$site
      for ((i=0; i<3; i++)); do
        bigline=$pline" HTTP: "`request $HTTP$site`
        bigline=$bigline"|"$pline" HTTPS: "`request $HTTPS$site`
        bigline=$bigline"|"
        echo $bigline >> $3;
      done
    fi
  done
}
#download_alexa_and_unzip
to_txt 0 5000 1_5000_REV.txt
#to_txt 5001 10000 5001_10000.txt
echo " -* done *-"

