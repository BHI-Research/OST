echo "Example 1: Usual example"
echo "  Epsilon: 0.4"
echo "  Users: 5"
echo "  Simple zone"
echo "Running CUS..."

../../build/osm --method cus -e 0.4 -n 5 -f 2091 -r "reference/" -i "data/"  --verbose

echo "Done!"
