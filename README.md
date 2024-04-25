# aaxconverter
Convert aax files to MP3

ffmpeg logic is like this

ffmpeg -activation_bytes XXXX -i audiobook.aax -c copy audiobook.m4a

ffmpeg -i filename.m4b -c:v copy -c:a libmp3lame -q:a 4 filename.mp3

Most of the python code comes from here: https://github.com/phiresky
I just updated it to work with python3, to not be for video chapters only, and to also convert from aax
Requires an activation code for your Audible DRM, expected in a file in the working directory

Usage:
convertaaxtomp3.py -f [filename]
