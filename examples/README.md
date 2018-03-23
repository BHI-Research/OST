# OSM++ - Examples

This folder contains examples that you can use to easily test the OST's Evaluator. Just compile the source code following the instructions in the `evaluator` folder and
run the scripts that you'll find in each folder.

* half-same-data: the half of the summarization data is the same as the user reference. In this case, F-measure should be 0.5.
* same-data: the summarization data is the same as the user data. In this case, F-measure should be 1.
* non-match-data: there are no matches between the summarization data and the user reference. In this case, F-measure should be 0.
* usual-example: a typical example that we've taken from our results.
* usual-example-double-zone-\*: a typical example using the double zone feature, provided by the **BHI** evaluation method.
