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

#depend_on_makefile="Makefile"
depend_on_makefile=""

targets=""
rules=""
number_of_timezones=$(jq '.timezones[].name' < timezones-include-fraction.json  | wc -l)
last_timezone=$(expr $number_of_timezones - 1)
for j in $(seq 0 $last_timezone)
do
    timezone=$(jq ".timezones[$j].name" < timezones-include-fraction.json)
    offset=$(jq  ".timezones[$j].offset" < timezones-include-fraction.json)
    for i in $(seq 0 17)
    do
	midrange=$(jq -r ".ranges[$i].midrange" < latitudes.json)
	range_text=$(jq -r ".ranges[$i].range_text" < latitudes.json)
	output_name="outputs/population-estimate,$offset,$midrange.json"
	targets="$targets $output_name"
	prompt="Pretend that Santa exists. Estimate the number of households that Santa would have to visit in the timezone $timezone in the latitudes $range_text. In your answer, consider how many cities there are, and then estimate the proportion of households where someone might believe in Santa. Output that number. The answer might be none if there are non cities, or if those cities are in countries without a Santa tradition. Output in JSON format a dictionary with keys \"reasoning\" (some text explaining your answer), \"major_cities\" (a list of important cities in that timezone and latitude range), \"estimated_number_of_households\" (an integer)"
	rule="$output_name: $depend_on_makefile\n\tollama run llama3.3 '$prompt' --format=json | tee $output_name\n\tgit add $output_name"
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
