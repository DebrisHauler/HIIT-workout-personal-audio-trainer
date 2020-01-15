# HIIT workout personal audio trainer

HIIT stands for High Intensity Interval Training. You will repeatedly max out your speed and then recover as instructed by the voice. The workout routine can be applied to any kind of cardio such as running, cycling, or jumproping. HIIT needs to be somewhere between 20 - 45 minutes. 

This script scrapes youtube and creates your own mp3 that you can take offline with you to the gym. A personal trainer and DJ will guide you through a HIIT workout and keep you entertained all the while.

You want to get fit??!!!! Boy, you came to the right software!

This was developed and tested in python 3.7 on Windows. It might work with older versions of python. So far, I've tested this once in the gym which helped me to adjust the workout. I will continue to update the code as I have more revelations in the gym.

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
This is what my workout looks like on the treadmil, but you can adjust it for yourself!

4 minutes jogging at 5 mph

1 minute sprinting at 10 mph

2 minutes recovering at 4 mph

1 minute sprinting at 10 mph

2 minutes recovering at 4 mph

1 minute sprinting at 10 mph

2 minutes recovering at 4 mph

1 minute sprinting at 10 mph

2 minutes recovering at 4 mph

1 minute sprinting at 10 mph

2 minutes recovering at 4 mph

1 minute sprinting at 10 mph

2 minutes recovering at 4 mph

1 minute sprinting at 10 mph

2 minutes recovering at 4 mph

1 minute sprinting at 10 mph

2 minutes recovering at 4 mph

1 minute sprinting at 10 mph

2 minutes recovering at 4 mph

1 minute sprinting at 10 mph

4 minutes recovering at 4 mph

## License
[MIT](https://choosealicense.com/licenses/mit/)
