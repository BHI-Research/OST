echo "Example 1: Usual example"
echo "  Epsilon: 0.4"
echo "  Distance: 120"
echo "  Users: 5"
echo "  Simple zone"
echo "Running BHI..."

../../evaluator/build/evaluator --method bhi -e 0.4 -d 120 -n 5 -f 2091 -r "reference/" -i "data/"  --verbose

echo "Done!"
