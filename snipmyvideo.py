from moviepy.editor import *

import sys
import os

"""

This script requires moviepy.py
    Is can be obtained through pip:
        pip install moviepy

Output file can be '.mp4', 'ogv', 'webm'
    You can modify script to output other files based off the codec.
        Further reasearch into moviepy.VideoFileClip.write_videofile

Usage: SnipMyVideo.py video.mp4 output.mp4 30-60 90-120
    E.g: This would create two snipets (unlimited snipets can be created),
        the first snipet resembles the time 30seconds to 60 seconds from video.m94
        These snipets are then concatenated and written to output.mp4



Only a couple lines actually using moviepy.
This is a simple script that can only snip your code and return it back in one video

"""

if len(sys.argv) < 4:
    print "You have not given enough Arguments"
    print "usage: " + sys.argv[0] + " inputfile.mp4 outputfile.mp4 20-30"
    print "Time is in seconds"
    sys.exit(6)

SCRIPT_NAME = sys.argv[0]
args = sys.argv[1:]  # Trimming of SCRIPT_NAME
FNAME = args[0]
args = args[1:]  # Timming off fname
OUT_FNAME = args[0]
ARGS = args[1:] # Trimming off the output filename
del args # Delete old args (REPLACED BY GLOBAL)

def check_args():
    """
    Make sure arguments are in the write format

    """
    if not os.path.isfile(FNAME):
        print "The Input file does not exist."
        sys.exit(1)

    if os.path.isfile(OUT_FNAME):
        print "Output file already exists"
        sys.exit(2)

    if not os.path.isdir(os.path.abspath(OUT_FNAME).rstrip(os.path.basename(OUT_FNAME))):
        print "Output file directory does not exists"
        sys.exit(3)


    for arg in ARGS:
        if '-' in arg:
            list_arg = arg.split('-', 1)
            num = 5

            for arg in list_arg:
                if not arg.isdigit():
                    print "Input must be a number"
                    sys.exit(4)
                if int(arg) < 0:
                    print "Input must be a positive number"
                    sys.exit(5)

def get_snipets():
    snipets = []
    for arg in ARGS:
        start, stop = arg.split('-', 1)
        snipets.append(VideoFileClip(FNAME).subclip(int(start), int(stop)))
        print "Created Snippet:\n\tStarting: " + start + " STOPPING: " + stop
    return snipets

def create_viedo(snipets):
    video = concatenate(snipets)
    print "Combined Snipets into one Video"
    print "Writing Video to " + OUT_FNAME
    video.write_videofile(OUT_FNAME)


if __name__ == "__main__":
    check_args()
    snipets = get_snipets()
    create_viedo(snipets)


