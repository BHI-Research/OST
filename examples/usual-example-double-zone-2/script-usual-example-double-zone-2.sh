echo "Example 5: Usual example with double zone 2"
echo "  Epsilon: 0.8"
echo "  Distance: 120"
echo "  Users: 5"
echo "  Double zone"
echo "Running BHI..."

../../evaluator/build/evaluator --method bhi -e 0.8 -d 120 -n 5 -f 2091 -r "reference/" -i "data/" --enable-double-zone  --verbose

echo "Done!"
