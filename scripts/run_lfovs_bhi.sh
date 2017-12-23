sh clean.sh
rm run.sh
#VSUMM
python ../tools/osm_utility/osm_utiity.py ../videos/VSUMM ../user_summaries/VSUMM ../auto_summaries/VSUMM1 -bhi -g -lfovs -lfovs_s 0.05 -lfovs_n 0.98 -lfovs_d 0.15 -lfovs_t 20 -lfovs_e 60

sh run.sh

python ../tools/get_average/get_average.py output.csv averange.txt TUNNER


cp output.txt DATA/output-"$(date +%d-%m-%H_%M_%S).txt"
cp output.csv DATA/output-"$(date +%d-%m-%H_%M_%S).csv"
cp averange.txt DATA/output-averange-"$(date +%d-%m-%H_%M_%S).csv"
rm output.txt
rm output.csv
rm averange.txt
