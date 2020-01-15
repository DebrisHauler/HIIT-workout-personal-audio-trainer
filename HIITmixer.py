"""
Created on Sun Jan 12 01:02:06 2020

@author: DebrisHauler
"""
from __future__ import unicode_literals
import os, pydub, random, shutil, sys, time, youtube_dl

seed = 69

WarmupTime = 240 * 1000 #4 minutes of warmup music
Sets = 10 #10 high and low intensity segments
HighTime = 60 * 1000 #1 minute of high intensity music
LowTime = 120 * 1000 #2 minutes of low intensity music
CooldownTime = 120 * 1000 #2 minutes of cooldown


tips = ['Try changing the seed on line 9 to generate different audio mixes. Make a mix for each day at the gym!',
        'Need a different workout routine? You can modify the # of sets or interval durations on lines 11-15.',
        'Try putting your own youtube links to the uri text files. Make your workout your own.'
        ]

factoids = ['The DJ never lets a song play more than 3 minutes. Audience got a short attention span around here.',
            'When revisiting a previous intensity, the DJ will resume where he left a song.',
            'Songs are only downloaded from youtube when they are not locally available and when the DJ needs them in the mix.',
            'Don\'t worry about messing up the mix by choosing crazy long songs. The DJ around here is pretty smart.',
            'Don\'t worry about choosing songs that are too loud or too quiet. All the audio gets normalized in the end.',
            'You can use your audio mix for any kind of cardio workout. running, cycling, jumproping all work great.'
            ]

class Downloader(object):
    def __init__(self):
        # Download data and config
        self.download_options = {
                'format': 'bestaudio/best',
                'outtmpl': '%(title)s.%(ext)s',
                'postprocessors':[{
                        'key':'FFmpegExtractAudio',
                        'preferredcodec':'mp3',
                        'preferredquality':'192',
                    }],
                'restrictfilenames':True,
                'forcefilename':True,
        }

    def download(self, uri):
        with youtube_dl.YoutubeDL(self.download_options) as dl:
            dl.download([uri])
            
    def getFilename(self, uri):
        with youtube_dl.YoutubeDL(self.download_options) as dl:
            info = dl.extract_info(uri, download=False)
            return dl.prepare_filename(info).rpartition('.')[0]+".mp3"

DL = Downloader()

class Song(object):
    def __init__(self, uri):
        self.uri = uri
        self.localFile = None
        filename = DL.getFilename(uri)
        if os.path.isfile(filename):
            self.localFile = filename
        self.playhead = None
        self.cutoff = None
        self.data = None
        self.length = None
        
    def fetch(self):
        if(self.localFile == None):
            DL.download(self.uri)
            self.localFile = DL.getFilename(self.uri)
        if(self.data == None):
            self.data = pydub.AudioSegment.from_mp3(str(os.getcwd())+"\\"+self.localFile)
        self.length = len(self.data)
        self.playhead = random.randint(0,self.length-101)
        self.cutoff = min(self.playhead + (3*60*1000), self.length)
        
    def sample(self, milliseconds = None):
        #when milliseconds == None, play until cutoff point of song.
        oldPlayhead = self.playhead
        if(milliseconds == None):
            self.playhead = self.cutoff
            return self.data[oldPlayhead:self.cutoff]
        else:
            self.playhead += milliseconds
            return self.data[oldPlayhead:oldPlayhead+milliseconds]
        
    def timeLeft(self):
        return self.cutoff - self.playhead

class Segment(object):
    def __init__(self, uris):
        self.songs = []
        with open(uris,'r') as f:
            for song_uri in f:
                self.songs.append(Song(song_uri))
        self.numSongs = len(self.songs)
        self.songIndices = list(range(self.numSongs))
        random.shuffle(self.songIndices)
        self.songIdx = -1
        self.chooseSong()
        
    def chooseSong(self):
        self.songIdx += 1
        self.songIdx %= self.numSongs
        self.curSong().fetch()
        
    def curSong(self):
        return self.songs[self.songIndices[self.songIdx]]
        
    def generate(self, milliseconds):
        segmentItems = []
        deltaTime = 0
        while deltaTime < milliseconds:
            print('\t\tsampling from '+self.curSong().localFile)
            if (deltaTime + self.curSong().timeLeft() > milliseconds):
                segmentItems.append(self.curSong().sample(milliseconds-deltaTime))
            else:
                segmentItems.append(self.curSong().sample())
                self.chooseSong()
            deltaTime += len(segmentItems[-1])
        return segmentItems
    
class TrainerVoice(object):
    def __init__(self, relPath):
        self.introduction = pydub.AudioSegment.from_mp3(relPath+'Introduction.mp3')
        self.shiftUp = pydub.AudioSegment.from_mp3(relPath+'ShiftUp.mp3')
        self.shiftDown = pydub.AudioSegment.from_mp3(relPath+'ShiftDown.mp3')
        self.cooldown = pydub.AudioSegment.from_mp3(relPath+'Cooldown.mp3')
        self.complete = pydub.AudioSegment.from_mp3(relPath+'Complete.mp3')
        
def DurationReadout(millis):
    millis = int(millis)
    seconds=(millis/1000)%60
    seconds = int(seconds)
    minutes=(millis/(1000*60))%60
    minutes = int(minutes)
    hours=(millis/(1000*60*60))%24

    return "%d hours %d minutes %d seconds" % (hours, minutes, seconds)
    
#https://stackoverflow.com/questions/33720395/can-pydub-set-the-maximum-minimum-volume
def get_loudness(sound, slice_size=60*1000):
    return max(chunk.dBFS for chunk in pydub.utils.make_chunks(sound, slice_size))

def set_loudness(sound, target_dBFS):
    loudness_difference = target_dBFS - get_loudness(sound)
    return sound.apply_gain(loudness_difference)

random.seed(seed)

# Song Directory
if not os.path.exists('Songs'):
    os.mkdir('Songs')
if not os.path.exists('Output'):
    os.mkdir('Output')
os.chdir('Songs')

MrsG = TrainerVoice('../TrainerVoice/')
WarmupGenerator = Segment('../Warmup_uris.txt')
HighIntensityGenerator = Segment('../HighIntensity_uris.txt')
LowIntensityGenerator = Segment('../LowIntensity_uris.txt')
CooldownGenerator = Segment('../Cooldown_uris.txt')

playlist = pydub.AudioSegment.silent()
items = [MrsG.introduction]
print('generating warmup')
items += WarmupGenerator.generate(WarmupTime)
for i in range(Sets):
    print('\tgenerating set '+str(i+1)+' of '+str(Sets))
    print('\t\tgenerating high intensity segment')
    items += [MrsG.shiftUp]
    items += HighIntensityGenerator.generate(HighTime - len(items[-1]))
    print('\t\tgenerating low intensity segment')
    items += [MrsG.shiftDown]
    items += LowIntensityGenerator.generate(LowTime - len(items[-1]))
print('generating cooldown')
items += [MrsG.cooldown]
items += CooldownGenerator.generate(CooldownTime - len(items[-1]))
items += [MrsG.complete]


    
print('compiling workout and adjusting volumes')
for item in items:
    playlist = playlist.append(pydub.effects.normalize(set_loudness(item, target_dBFS=-10),0.2))

print('normalizing audio')
playlist = pydub.effects.normalize(playlist,0.2)

print('Workout length is '+DurationReadout(len(playlist)))
print('Fire estimation is '+str(random.randint(7,10))+'/10')
# save the result
exportPath = '../Output/HIIT-'+str(seed)+'.mp3'
print('Exporting to '+exportPath)
print('Please wait')
playlist.export(exportPath, format='mp3')
print('HIIT-'+str(seed)+'.mp3 exported')

print("If you choose to keep the downloaded mp3s, your next mix will generate faster.")
if input('Keep downloaded mp3 files? [y/n]:').upper() == 'N':
    os.chdir('..')
    print('removing downloaded songs')
    try:
        shutil.rmtree('Songs')
    except:
        print('Unexpected error:', sys.exc_info()[0])
    print('downloaded songs removed')
else:
    print('downloaded songs stay in the Songs folder for next time')

time.sleep(2)
print('\nHere are some configuration tips for next time.')
for tip in tips:
    time.sleep(0.5)
    print(tip)

time.sleep(2)
print('\nHere are some fun facts about the HIIT mixer.')
for factoid in factoids:
    time.sleep(0.5)
    print(factoid)

print('\ndone')
