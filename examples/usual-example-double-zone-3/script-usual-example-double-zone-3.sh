echo "Example 6: Usual example with double zone 3"
echo "  Epsilon: 0.4"
echo "  Distance: 60"
echo "  Users: 5"
echo "  Double zone"
echo "Running BHI..."

../../evaluator/build/evaluator --method bhi -e 0.4 -d 60 -n 5 -f 2091 -r "reference/" -i "data/" --enable-double-zone  --verbose

echo "Done!"
