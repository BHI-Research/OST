python ../superframe-to-keyframe.py --input input.csv --output first-v1.csv --frame first
python ../superframe-to-keyframe.py --input input.csv --output last-v1.csv --frame last
python ../superframe-to-keyframe.py --input input.csv --output middle-v1.csv --frame middle
python ../superframe-to-keyframe.py --input input.csv --output random-v1.csv --frame random

python ../../../tools/superframe-to-keyframe/superframe-to-keyframe.py  --input ../superframes/v1.csv --output first/v1.csv --frame first
