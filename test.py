import os, fnmatch, alsaaudio, time
from audioplayer import AudioPlayer

result = []

def find(pattern, path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

find('*.mp3', '../')
for i in result:
    player = AudioPlayer(i)
    player.play()
