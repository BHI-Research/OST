echo "Example 3: Same data"
echo "  Epsilon: 0.4"
echo "  Users: 1"
echo "  Simple zone"
echo "Running CUS..."

../../evaluator/build/evaluator --method cus -e 0.4 -n 1 -f 2091 -r "reference/" -i "data/" --verbose

echo "Done!" 

