#!/usr/bin/env python3
import os
import re
import subprocess as sp
from subprocess import *
from optparse import OptionParser

#ffmpeg -activation_bytes XXXX -i audiobook.aax -c copy audiobook.m4a

#ffmpeg -i TheChoiceofMagicArtoftheAdeptBook1.m4b -c:v copy -c:a libmp3lame -q:a 4 TheChoiceofMagicArtoftheAdeptBook1.mp3

def parseChapters(filename):
  chapters = []
  command = [ "ffmpeg", '-i', filename]
  output = ""
  try:
    # ffmpeg requires an output file and so it errors 
    # when it does not get one so we need to capture stderr, 
    # not stdout.
    output = sp.check_output(command, stderr=sp.STDOUT, universal_newlines=True)
  except CalledProcessError as e:
    output = e.output 
   
  for line in iter(output.splitlines()):
    m = re.match(r".*Chapter #(\d+:\d+): start (\d+\.\d+), end (\d+\.\d+).*", line)
    num = 0 
    if m != None:
      chapters.append({ "name": m.group(1), "start": m.group(2), "end": m.group(3)})
      num += 1
  return chapters

def getChapters():
  parser = OptionParser(usage="usage: %prog [options] filename", version="%prog 1.0")
  parser.add_option("-f", "--file",dest="infile", help="Input File", metavar="FILE")
  (options, args) = parser.parse_args()
  if not options.infile:
    parser.error('Filename required')
  chapters = parseChapters(options.infile)
  fbase = os.path.basename(options.infile).split(".")[0]
  #print(fbase)
  os.mkdir(fbase)
  for chap in chapters:
    #print("start:" +  chap['start'])
    chap['outfile'] = f"./{fbase}/{fbase}-ch-{chap['name'].split(':')[1]}.mp3"
    chap['origfile'] = options.infile
    #print (chap['outfile'])
  return chapters

def convertChapters(chapters):
  for chap in chapters:
    print ("start:" +  chap['start'])
    print (chap)
    #ffmpeg -i TheChoiceofMagicArtoftheAdeptBook1.m4b -c:v copy -c:a libmp3lame -q:a 4 TheChoiceofMagicArtoftheAdeptBook1.mp3
    filehandle = open('./activation','r')
    activation = filehandle.read(8)
    filehandle.close()
    command = [
        "ffmpeg", 
        '-activation_bytes', activation,
        '-i', chap['origfile'],
        '-c:v', 'copy',
        '-c:a', 'libmp3lame',
        '-q:a', '4',
        '-ss', chap['start'],
        '-to', chap['end'],
        chap['outfile']]
    output = ""
    try:
      # ffmpeg requires an output file and so it errors 
      # when it does not get one
      output = sp.check_output(command, stderr=sp.STDOUT, universal_newlines=True)
    except CalledProcessError as e:
      output = e.output
      raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))

if __name__ == '__main__':
  chapters = getChapters()
  convertChapters(chapters)
