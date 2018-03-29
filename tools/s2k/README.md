# Superframe to Keyframe Converter

Given a CSV file as input, where each row represents an user and a sequence of 1's represents a supeframe,
produces a new CSV file where superframes are converted into keyframes.

# How to run

We highly recommend you to set a virtual env before installing new python packages. If you don't have one, take a look at [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
Once you are in the virtual env, run:

```
pip install -r requirement.txt
```

Then, run:

```
python s2k.py --input input.csv --output output.csv --frame first
```

Where,
- `--input` is the input csv file, that represents superframes for a video.
- `--output` is the output csv file, that will represents keyframes for a video.
- `--frame` is the frame of the interval we want to select as the keyframe. Possible values: `first`, `middle`, `last`, `random`.


Checkout the examples in the `examples` folder.
