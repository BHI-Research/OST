echo "Example 4: Usual example with double zone"
echo "  Epsilon: 0.4"
echo "  Distance: 120"
echo "  Users: 5"
echo "  Double zone"
echo "Running..."

../../build/osm -e 0.4 -d 120 -n 5 -f 2091 -r "reference/" -i "data/" --enable-double-zone  --verbose

echo "Done!"