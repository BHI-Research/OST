



sh clean.sh 

python ../tools/osm_utility/osm_utiity.py ../videos/VSUMM/v27.mpg ../user_summaries/VSUMM/v27 ../auto_summaries/VSUMM2/v27 -bhi 
 
sh run.sh	


cp output.txt DATA/output-"$(date +%d-%m-%H:%M:%S).txt"
cp output.csv DATA/output-"$(date +%d-%m-%H:%M:%S).csv"



