'''
Script to pass a log and data strings (e.g., topics) to filter entries by. 
Returns formatted csv.

Usage
python <module name> --file <path to log file> --data <string 1 to search for> 
  <string n to search for> 

Example Usage
python log-parsing --data 'ROBOT_SUPPORT_STATUS' 'ROBOT_SUPPORT_STATE' --file 
  'log-parsing/test.log'

Last modified
18 Jan 2023
'''

import csv        # used to capture the parsed log strings in csv format
import argparse   # used to specify the parameters the script takes
import subprocess # used to make UNIX grep call and capture stdout
from utils import buildExtendedRegex

# command line
parser = argparse.ArgumentParser(description = 'Return formatted csv, for \
								 	inputted log, for inputted \
									data strings to filter by.')
parser.add_argument('-f', 
					'--file', 
					required=True, 
					help="Path to the log file.")
parser.add_argument('-d', 
					'--data', 
					required=True,
					nargs='+', 
					help="Data string to query for, such as Topics, stored as \
						string in a list, e.g., ['ROBOT_SUPPORT_STATE']")
parser.add_argument('-t', 
					'--time', 
					help="The start and end time for which to filter the logs.")
args = parser.parse_args()


# grep to create new, smaller log
_fname = args.file
_data = args.data
_time = args.time  # TODO  Make this work
_grep_regex = buildExtendedRegex(_data)
result = subprocess.run(['grep', '-iE', _grep_regex, _fname], 
						 capture_output=True, 
						 text=True)


# TODO  create csv
# e.g.,
# timestamp, topic, value
# X, Y, [YA, YB, YC, ...]