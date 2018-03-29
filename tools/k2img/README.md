# How to run

We highly recommend you to set a virtual env before installing new python packages. If you don't have one, take a look at [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
Once you are in the virtual env, run:

```
pip install -r requirement.txt
```

You'll also need the [OpenCV](https://opencv.org/) library. [Here](https://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/) are the installation
steps for Ubuntu.

Then, run:

```
python k2img.py video.mpg path/to/user_summaries/csv path/to/automatic_summarization/csv -bhi
```

Where,
- `video.mpg` the path to the video we're getting the frames from.
- `path/to/user_summaries/csv` the path to the CSV that contains the users summaries (without the file extension)
- `path/to/published_results/csv` the path to the CSV that contains the automatic summarization (without the file extension)
- `-bhi` (or `-cus`) the method we want to use to evaluate our summarization, used to generate the `run.sh` script.
