sh clean.sh

python ../tools/osm_utility/osm_utility.py videos/VSUMM/v21.mpg ../user_summaries/VSUMM/v21 ../published_results/VSUMM2/v21 -bhi

sh run.sh

# cp output.txt DATA/output-"$(date +%d-%m-%H:%M:%S).txt"
# cp output.csv DATA/output-"$(date +%d-%m-%H:%M:%S).csv"