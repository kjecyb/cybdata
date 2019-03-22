#!/bin/bash
mkdir -p parsers
for F in `find ../../../../netwitness/nw-logparsers/devices -type f -name \*.xml -print`
do
  echo $B
  B=$(basename $F)
  D=$(dirname $F)
  J=$(echo $B | sed -e 's/\.xml/.json/')
  touch parsers/$J
  tail -n +2 $F | \
  ~/anaconda3/bin/python ../../../../hay/xml2json/xml2json.py -t xml2json -o parsers/$J 
done