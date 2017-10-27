# OSM++ - Open Summarization Metrics

Open Summarization Metrics (OSM) is a evaluation method for video summaries. It is written in C++ and based on OpenCV. OSM improves [CUS evaluation method](https://sites.google.com/site/vsummsite/home). The most relevant benefits are the support of Cohen's Kappa coefficient, a flexible evaluation framework, and a faster evaluation time.

## How OSM works

OSM compares the keyframes of a summarization method with the keyframes selected by human users to quantify the quality of the abstraction. The frames are compared extracting a HSV color space histogram. If the correlation between two histograms is higher that an threshold, the frames are considered equivalent. OSM offers three metrics to the user. The first is Cohen's Kappa coefficient. The second metric is F-measure coefficient. Finally, it offers CUSa and CUSe as a compatibility feature.

## Compile from source
At this first version, OpenCV is required.
You can see how to install OpenCV on Debian from [here](http://www.javieriparraguirre.net/installing-opencv-debian/).
If you are using an Ubuntu-based distribution, check out the [official site](http://docs.opencv.org/3.0-beta/doc/tutorials/introduction/linux_install/linux_install.html) to get the installation steps.


Compile from source:
```
$ git clone git@github.com:leanbalma/OSM.git
$ cd OSM/
$ mkdir build
$ cd build
$ cmake ../src
$ make
```

## Tested enviroments
* Linux Mint 18 (x64)
* OpenCV 3.0.0

## Usage

OSM is a very customizable evaluation method. You can edit the following parameters:

* Method (`--method`): besides running our evaluation method, you can also run CUS specifing `cus` instead of `bhi` for this parameter.
* Epsilon (e): value that determines the maximum distance between the histograms of two matched keyframes. Recommended value: 0.4
* Distance (d): maximum distance (in frames number) between the two keyframes that will be compared. Recommended value: 120.
* Number of users (n): the number of users summaries that will be used to evaluate the summarization method.
* Reference path (r): path to the method keyframes.
* User path (i): path to the user keyframes.
* Enable double zone (`--enable-double-zone`): If the argument is used, the distance 'd' is considered at both sides of the user keyframe (the real distance is 2\*d). If the argument is NOT used, only the forward keyframes from the user keyframe will be considered.
* Verbose (`--verbose`): this argument allows you to run a big number of iterative executions and redirect the output to a text file for post analysis. If the argument is used, the result will be showed with full information. If the argument is NOT used, the result will be showed as:

    [ CUSa ] ( Tab ) [ CUSe ] ( Tab ) [ F-meter ] ( Tab ) [ Cohen's Kappa ]

You can 

Example of usage:

```
$ ./osm --method bhi -e 0.4 -d 120 -n 5 -f 2091 -r "reference/" -i "data/"  -- enable-double-zone --verbose

CUSa: 0.538462
CUSe: 0.176923
F-meter: 0.627803
Cohen's Kappa: 0.626701
```

## Examples
You can find some usage examples in the "examples" folder. Just compile the source code and run the scripts file.
```
$ cd examples/usual-example
$ sh script-usual-example-bhi.sh 
Example 1: Usual example
  Epsilon: 0.4
  Distance: 120
  Users: 5
  Simple zone
Running BHI...
CUSa: 0.474359
CUSe: 0.241026
F-meter: 0.553064
Cohen's Kappa: 0.551868
Done!

$ sh script-usual-example-cus.sh 
Example 1: Usual example
  Epsilon: 0.4
  Users: 5
  Simple zone
Running CUS...
CUSa: 0.474359
CUSe: 0.241026
F-meter: 0.553064
Cohen's Kappa: 0.551868
Done!
```

## Future work
* Windows and Mac portability.


## Contributors

* Iparraguirre, Javier [ j.iparraguirre@computer.org ]
* Balmaceda, Leandro M. [ balmacedalm@gmail.com ]

## License

This project is licensed and distributed under the GNU General Public License v3.
