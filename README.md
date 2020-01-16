# HIIT workout personal audio trainer

You want to get fit??!!!! Boy, you came to the right software!

This script scrapes youtube and creates your own mp3 that you can take offline with you to the gym. A personal trainer and DJ will guide you through a HIIT workout and keep you entertained all the while.

HIIT stands for High Intensity Interval Training. You will repeatedly max out your speed and then recover as instructed by the voice. The workout routine can be applied to any kind of cardio such as running, cycling, or jumproping. HIIT needs to be somewhere between 20 - 45 minutes.

This was developed and tested in python 3.7 on Windows. It might work with older versions of python. I am testing this in the gym and improving the algorithm as I see fit.

## Getting started:

You need python (I used 3.7)

You need ffmpeg, and your environment variables point to it. Instructions:

[how to install ffmpeg](https://www.youtube.com/watch?v=qjtmgCb8NcE)

you need pydub:
```cmd
pip install pydub
```
for anaconda users:
```cmd
conda install -c conda-forge pydub
```
you need youtube_dl:

```cmd
pip install youtube_dl
```
for anaconda users:
```cmd
conda install -c conda-forge youtube_dl
```

Download this repository as a zip file then extract it anwhere you like.

Then just run HIITmixer.py

## Example Routine:

4ish minutes jogging at 5 mph

10 times:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1 minute sprinting at 11 mph

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2 minutes recovering at 4 mph

2ish minutes cooling down at 4 mph

This is what my (moderately fit male 25yo) workout looks like on the treadmill, but you can adjust it for yourself! I would recommend first understanding what your speed is to exert 100% effort. As you repeat this workout, try getting increasing this speed up to 11 mph. If you get comfortable with that routine, then start reducing the recovery time, from 120 seconds to 90 seconds, and finally to 60 seconds if you are basically Usain Bolt.



## License
[MIT](https://choosealicense.com/licenses/mit/)
