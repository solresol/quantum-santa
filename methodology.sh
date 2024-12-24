#!/bin/sh

if [ ! -e timezones-include-fraction.json ]
then
    ollama run llama3.3 "List all the timezones that would exist and be active on Christmas Day 2024. Remember to include offsets that aren't whole numbers of hours.  Output as a JSON-formatted list of dictionaries (where each dictionary has keys of 'name' and 'offset'" --format json | tee timezones-include-fraction.json
    git add timezones-include-fraction.json
fi

if [ ! -e latitudes.json ]
then
    ollama run llama3.3 'I want a jSON array of latitude ranges from 90S to 90N in 10 degree bands. i.e. the strings "between 90S and 80S","between 80S and 70S" and so on until "between 80N and 90N". Each element in the list should be a dictionary with keys "midrange" (an integer) and "range_text"' --format=json  > latitudes.json
    git add latitudes.json
fi


targets=""
rules=""
for j in $(seq 0 47)
do
    timezone=$(jq ".timezones[$j].name" < timezones-include-fraction.json)
    offset=$(jq  ".timezones[$j].offset" < timezones-include-fraction.json)
    for i in $(seq 0 17)
    do
	midrange=$(jq ".ranges[$i].midrange" < latitudes.json)
	range_text=$(jq ".ranges[$i].range_text" < latitudes.json)
	output_name="outputs/population-estimate,$offset,$midrange.json"
	targets="$targets $output_name"
	prompt="Estimate the number of households that Santa would have to visit in the timezone $timezone in the latitudes $range_text. The answer might well be none. Output in JSON format a dictionary with keys \"reasoning\" (some text explaining your answer), \"major_cities\" (a list of important cities), \"estimated_number_of_households\" (an integer)"
	rule="$output_name: Makefile\n\tollama run llama3.3 '$prompt' --format=json | tee $output_name\n\tgit add $output_name"
	rules="$rules\n$rule\n\n"
    done
done

echo ".PHONY: all" > Makefile
echo >> Makefile
echo "all: $targets" >> Makefile
echo "\techo Done" >> Makefile
echo >> Makefile
echo $rules >> Makefile

mkdir -p outputs
