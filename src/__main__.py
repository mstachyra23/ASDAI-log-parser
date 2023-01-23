'''
Script to pass a log and data strings (e.g., topics) to filter entries by. 
Returns formatted csv.

Usage
python <module name> -i <path to log file> -d <string 1 to search for> 
  <string n to search for> -o <path to output file>

Example Usage
python src -i . -o testing.csv -d ROBOT_SUPPORT_STATE

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
	'''
	1  GUI returns selected log files
	2  These log files are saved to a temp folder
	3	 Grep filters out relevant lines from log files
	4	 These lines are formatted within a csv
	'''

	_in = args.inpath
	_out = args.outfile
	_data = args.data
	_regex = buildExtendedRegex(_data)
	_files = [file.name for file in pathlib.Path(_in).glob('*.log')]
	_options = [file.name for file in pathlib.Path(_in).glob('*')]

	# 1  QT5 GUI dropdown to select log files
	app = QApplication([])
	gui = GUI(_options)
	gui.show()
	app.exec()
	# TODO  run command to save selected log files
	# TODO  run command to save selected topics

	# 2  Move relevant log files to /temp	
	# TODO

	# 3  UNIX grep to extract relevant part of the file
	_command = "grep -iE '{0}' '{1}' > '{2}'".format(_regex, _in, _out)
	print(f"Grepping for {_regex} in {_in}.")
	os.system(_command)

	# 4  Format grepped lines in csv
	# TODO
