from moviepy.editor import *

import sys
import os

"""

This script requires moviepy.py
    It can be obtained through pip:
        pip install moviepy

Output file can be 'mp4', 'ogv', 'webm'
    You can modify script to output other files based off the codec.
        Further reasearch into moviepy.VideoFileClip.write_videofile

Usage: SnipMyVideo.py video.mp4 output.mp4 30-60 90-120
    E.g: This would create two snipets (unlimited snipets can be created),
        the first snipet resembles the time 30seconds to 60 seconds from video.mp4
        the second snipet is the video for the time 90- 120 in the video.mp4
        These snipets are then concatenated and written to output.mp4



Only a couple lines actually using moviepy.
This is a simple script that can only snip your video and return it back in one video

"""



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


def convert_to_sec(inp_list):
    """ expects format as [hour, min, sec] or [min, sec] or [sec], returns seconds as int """
    if len(inp_list) == 1:
        return int(inp_list[0])
    elif len(inp_list) == 2:
        return int(inp_list[0]) * 60 + int(inp_list[1])
    elif len(inp_list) == 3:
        return int(inp_list[0]) * 3600 + int(inp_list[1]) * 60 + int(inp_list[2])


def get_snipets():
    """
    Input: list of str of time range in format of sec, min:sec, or hour:min:sec
    Process: each value from input list becomes start and stop time in seconds as int
    Output: list of objects of VideoFileClip.subclip(start, stop)
    """
    snipets = []
    # e.g. input: ['6-12:06', '12:10-12:30', '0:50:22-1:10:0']
    # iterate through each input time range / snipet
    for arg in ARGS:
        if '-' in arg:
            time = [[x] for x in arg.split('-', 1)] # '6-12:06' => [['6'], ['12:06']]
            if len(time) != 2:
                print('Input needs to contain start & stop times with \'-\' between to indicate time range for input video, see README.md')
                sys.exit(7)

            # iterate through start then stop times
            for index in range(len(time)):
                if ':' in time[index][0]:
                    if time[index].count(':') > 2:
                        print('There shouldn\'t be more than 2 \':\' per start or stop time entered.')
                        sys.exit(8)
                    time[index] = time[index][0].split(':') # [['6'], ['12:06']] => [['6'], ['12', '06']]
                    # print('time[%s] after ":" split: %s' % (index, time[index])) # debug
                # check to see if snippets are valid
                for value in time[index]:
                    if not value.isdigit():
                        print "Input must be a number"
                        sys.exit(4)
                    if int(value) < 0:
                        print "Input must be a positive number"
                        sys.exit(5)
                # convert to seconds
                time[index] = convert_to_sec(time[index]) # [['6'], ['12', '06']] => [6, 726]
                # print('time[%s] after sec conversion: %s' % (index, time[index])) # debug

            start, stop = time[0], time[1]
            if start > stop:
                print('Start needs to be smaller than stop for snipet #%s, exiting.' % (index))
                sys.exit(6)
            snipets.append(VideoFileClip(FNAME).subclip(int(start), int(stop)))
            # print "Created Snippet:\n\tStarting: %s STOPPING: %s " % (start, stop) # debug

        elif '-' not in arg:
            print('Input needs to contain \'-\' to indicate time range for input video, see README.md')
            sys.exit(7)

    return snipets

def create_viedo(snipets):
    video = concatenate(snipets)
    print "Combined Snipets into one Video"
    print "Writing Video to " + OUT_FNAME
    video.write_videofile(OUT_FNAME)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "You have not given enough Arguments"
        print "usage: " + sys.argv[0] + " inputfile.mp4 outputfile.mp4 20-30"
        print "Time is in seconds"
    
    sys.exit(6)
    check_args()
    snipets = get_snipets()
    create_viedo(snipets)
