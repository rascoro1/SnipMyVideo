from moviepy.editor import *
from moviepy import Clip

import sys
import os

"""
This is a simple script that can only snip your code and return it back in one video

This script requires moviepy.py
    Is can be obtained through pip:
        pip install moviepy

Output file can be '.mp4', 'ogv', 'webm'
    You can modify script to output other files based off the codec.
        Further reasearch into moviepy.VideoFileClip.write_videofile

Usage: SnipMyVideo.py video.mp4 output.mp4 30-60 90-120 20:20-20:40 1:20:15-1:30:15
    E.g: This would create two snipets (unlimited snipets can be created),
        the first snipet resembles the time 30seconds to 60 seconds from video.m94
        These snipets are then concatenated and written to output.mp4



Only a couple lines actually using moviepy.


"""

###################### Declaring Globals ##################################
SCRIPT_NAME = "" # Name of the script
FNAME = "" # Input filename
OUT_FNAME = "" # Output filename
SNIPPETS = [] # Raw Snippet times given as arguments by the user
SNIPPET_TIMES = [] # Snippet times in seconds
VERBOSE = True # Turn to false if you would not like verbose information
IS_AUDIO_FILE = False

def check_num_of_arguments():
    """
    Quick check to make sure the correct number of argumets are portrayed.
    First function that is called
    :return:
    """
    if len(sys.argv) < 4:
        print("You have not given enough Arguments")
        print("usage: " + sys.argv[0] + " inputfile.mp4 outputfile.mp4 20-30")
        print("Time is in seconds")
        sys.exit(6)


def trim_arguments():
    """
    This trims all of the input arguments from the user
    and assagins information to the according global variable
    :return:
    """
    global SCRIPT_NAME, FNAME, OUT_FNAME, SNIPPETS
    SCRIPT_NAME = sys.argv[0]
    args = sys.argv[1:]  # Trimming of SCRIPT_NAME
    FNAME = args[0]
    args = args[1:]  # Timming off fname
    OUT_FNAME = args[0]
    SNIPPETS = args[1:]  # Trimming off the output filename
    del args  # Delete old args (REPLACED BY GLOBAL)


def check_args():
    """
    Make sure arguments are in the write format

    """
    if not os.path.isfile(FNAME):
        print("The Input file does not exist.")
        sys.exit(1)

    if os.path.isfile(OUT_FNAME):
        print("Output file already exists")
        sys.exit(2)

    if not os.path.isdir(os.path.abspath(OUT_FNAME).rstrip(os.path.basename(OUT_FNAME))):
        print("Output file directory does not exists")
        sys.exit(3)

def check_time(time, min, max):
    """
    Check time submitted by user to make sure time is correct and follows a correct format
    :param time: time requested by user
    :param min: min possible value
    :param max: max possible value
    :return:
    """
    if int(time) >= min and int(time) <= max:
        return True
    else:
        return False

def convert_human_readable_time(time):
    """
    Convert human readable format of time into seconds

    :param time: human readable string format of 1:20:30 or 20:38 or 38
    :return: int time in seconds
    """
    if ':' in time:  # The time follows the min:sec format and must be converted
        time = time.split(':')
        if len(time) == 2:  # Min:Sec format
            min, sec = time
            verbose("convert_human_readable_time("+str(time)+")",  "Min:Sec Format")
            if check_time(min, 0, 59) and check_time(sec, 0, 59): # Making sure the times are between possible amounts
                verbose("convert_human_readable_time(" + str(time) + ")", "time = " + str(min) + " * 60 + " + sec)
                time = int(min) * 60 + int(sec)
            else:
                print(("Incorrect Time has been submitted: " + str(time) + " min:sec 0:0-59:60"))
                sys.exit(10)

        elif len(time) == 3:  # Hour:Min:Sec format
            hour, min, sec = time
            verbose("convert_human_readable_time("+str(time)+")",  "Hour:Min:Sec Format")
            if check_time(hour, 0, 23) and check_time(min, 0, 59) and check_time(sec, 0, 59): # Making sure the times are between possible amounts
                verbose("convert_human_readable_time(" + str(time) + ")", "time = " + str(hour) + " * 3600 + " + str(min) + " * 60 + " + sec)
                time = int(hour) * 3600 + int(min) * 60 + int(sec)
            else:
                print(("Incorrect Time has been submitted: " + str(time) + " hour:min:sec 0:0:0-23:59:59"))
                sys.exit(10)


    try:
        time = int(time)
    except ValueError as e:
        print("Value Error: Given time is not a digit" + e.message)
        sys.exit(8)

    verbose("convert_human_readable_time(" + str(time) + ")", "Returned time is -> " + str(time))
    return time # If the time  does not need to be converted (does not contain ':') it will still be appened

def get_snippet_time(snippet):
    """
    This allows for easier use of snipping longer videos
    conversion of
        hour:min:sec & min:sec & sec e.g 1:20:15 & 20:48 & secs
        to seconds

    :param args: One snippet of time start and end time
    :return: Dict of snippet e.g. {'start':20, 'stop': 40}
    """
    if "-" not in snippet: # Checking to see if snippet time was inputted correctly
        print(("The arguments for the snippet time is not in the correct format: " + snippet))
        print("Correct usage is: 20-30 or 20:30-20:35 or 1:20:30-1:20:35 ")
        sys.exit(7)

    start, stop = snippet.split('-', 1)  # start and stop times of snippet
    start = convert_human_readable_time(start)
    stop = convert_human_readable_time(stop)
    snippet = {'start': start, 'stop': stop}

    return snippet

def get_all_snippet_times():
    """
    Get all the snippet times in seconds
    :return:
    """
    for snippet in SNIPPETS:
        snippet = get_snippet_time(snippet)
        for key in snippet:
            if snippet[key] < 0:
                print("Input must be a positive number")
                sys.exit(5)

        if snippet['start'] > snippet['stop']:
            print('Start needs to be smaller than stop for snipet, exiting.')
            verbose("check_args()", "start=" + str(snippet['start']) + ", stop="+str(snippet['stop']))
            sys.exit(6)

        SNIPPET_TIMES.append(snippet)

def determine_if_audio_file():
    """
    """
    global IS_AUDIO_FILE
    audio_file_extensions = (".mp3", ".m4a")
    IS_AUDIO_FILE = True if FNAME.endswith(audio_file_extensions) else False

def get_snippets():
    """

    :return: List of moviepy.subclip objects
    """
    snippets = []
    clip = AudioFileClip(FNAME) if IS_AUDIO_FILE else VideoFileClip(FNAME)
    for snippet in SNIPPET_TIMES:
        snippets.append(clip.subclip(snippet['start'], snippet['stop']))
        print("Created Snippet:\n\tStarting: " + str(snippet['start']) + " STOPPING: " + str(snippet['stop']))

    return snippets

def create_video(snippets):
    """
    Concatinate all the snippets together into one movie and write
    :param snippets: THis is a list of moviepy.subclip
    :return: write out one file
    """
    if not IS_AUDIO_FILE:
        video = concatenate(snippets)
        print("Combined Snipets into one Video")
        print("Writing Video to " + OUT_FNAME)
        video.write_videofile(OUT_FNAME)
    else:
        audio = concatenate_audioclips(snippets)
        print("Combined Snipets into one Audio File")
        print("Writing Video to " + OUT_FNAME)
        audio.write_audiofile(OUT_FNAME)


def verbose(title, info):
    """
    Loggin verbose notes when VERBOSE is True
    Used for debuging and is very helpful
    :param title:
    :param info:
    :return:
    """
    if VERBOSE:
        print(SCRIPT_NAME + " -> " + str(title) + ": " + info)


def run():
    check_num_of_arguments()  # Make sure we have the correct number of arguments
    trim_arguments()  # Trim the args to just have the snippets at the end
    check_args()  # check the args for correctness
    get_all_snippet_times()  # All snippet times in seconds and organized Also checked for correctness
    determine_if_audio_file()
    snippets = get_snippets()  # Get all the moviepy.subclip objects for each snippet
    create_video(snippets)  # Concatinate the Snippets together


if __name__ == "__main__":
    run()
