#!/bin/bash

params=$1
conn=$(cat $params | jq -r '."conn"')
start=$(cat $params | jq -r '."start"')
end=$(cat $params | jq -r '."end"')
geoid=$(cat $params | jq -r '."geoid"')
min=$(cat $params | jq -r '."min"')
max=$(cat $params | jq -r '."max"')
input=$(cat $params | jq -r '."input"')
output=$(cat $params | jq -r '."output"')
tablename=$(cat $params | jq -r '."tablename"')
echo "conn: $conn"
echo "start: $start"
echo "end: $end"
echo "geoid: $geoid"
echo "min: $min"
echo "max: $max"
echo "input: $input"
echo "output: $output"
echo "tablename: $tablename"

node /app/tile_cover.js -s $start -e $end -g $geoid --min $min --max $max --input $input --output $output
echo "tile_cover.js: Done!"

python3 /app/tile_cover.py --input $output --table $tablename --zoom $max --conn $conn
echo "tile_cover.py: Done!"
