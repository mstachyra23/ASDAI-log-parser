'''
Script to pass a log and data strings (e.g., topics) to filter entries by. 
Returns formatted csv.

Usage
python <module name> -i <path to log file> -d <string 1 to search for> 
  <string n to search for> -o <path to output file>

Example Usage
python log-parsing -i log-parsing/test.log -o log-parsing/testing.csv 
  -d ROBOT_SUPPORT_STATE

'''

import os  # used to make UNIX grep call and capture stdout
import sys  # used by PyQT5 to start the GUI app
import csv  # used to capture the parsed log strings in csv format
import json  # used to convert the grepped string into JSON format
import argparse  # used to specify the parameters the script takes
import pathlib  # used to grab log file names for inputted path
from PyQt5.QtWidgets import QApplication  # used to generate GUI

from utils import buildExtendedRegex, GUI


# CLI
parser = argparse.ArgumentParser(description = 'Return formatted csv, for \
								 	inputted log, for inputted \
									data strings to filter by.')
parser.add_argument('-i', 
					'--inpath', 
					required=True, 
					help="Path to the log files.")
parser.add_argument('-o', 
					'--outfile', 
					required=True, 
					help="Desired path/filename for outputted csv.")
parser.add_argument('-d', 
					'--data', 
					required=True,
					nargs='+', 
					help="Data string to query for, such as Topics, stored as \
						string in a list, e.g., ['ROBOT_SUPPORT_STATE']")
args = parser.parse_args()


if __name__ == "__main__":
	# UNIX grep to extract relevant part of the file
	_in = args.inpath
	_out = args.outfile
	_data = args.data
	_regex = buildExtendedRegex(_data)
	_files = [file.name for file in pathlib.Path(_in).glob('*.log')]
	_command = "grep -irE '{0}' '{1}' > '{2}'".format(_regex, _in, _out)
	print(f"Grepping for {_regex} in {_in}.")
	os.system(_command)


	# QT5 GUI dropdown to select log files
	_options = [file.name for file in pathlib.Path(_in).glob('*')]
	app = QApplication([])
	gui = GUI(_options)
	gui.show()
	app.exec()

	# TODO  create csv
	# e.g.,
	# timestamp, topic, value
	# X, Y, [YA, YB, YC, ...]