# aaxconverter
Convert aax files to MP3

ffmpeg -activation_bytes XXXX -i audiobook.aax -c copy audiobook.m4a

ffmpeg -i TheChoiceofMagicArtoftheAdeptBook1.m4b -c:v copy -c:a libmp3lame -q:a 4 TheChoiceofMagicArtoftheAdeptBook1.mp3
