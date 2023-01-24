#!/usr/bin/env python3
'''
Script returns formatted csv with values by topic. Takes in path to folder with
log(s). GUI enables selecting which log(s) to select from folder and which
topics to grep for. 

Usage
		$ python src -i <required: folder with logs> -o \
			<optional: output file name; default is 'output.csv>

		The -i tells it where to look for the logs.
		The -o tells it where to output the csv and what to name it.

Example Usage
		$ python src -i '/Downloads/logs/monday/'  

'''

import os  # used to make UNIX grep call and capture stdout
import requests # used to grab robotic drive html page for topics
import argparse  # used to specify the parameters the script takes
import pathlib  # used to grab log file names for inputted path
from PyQt5.QtWidgets import QApplication  # used to generate GUI

# Relative imports
from utils import getTopicsFromHTML, processInpath
from gui import GUI


# CLI 
# parser = argparse.ArgumentParser(description = 'Return formatted csv, for \
# 								 	inputted log, for inputted \
# 									data strings to filter by.')
# parser.add_argument('-i', 
# 					'--inpath', 
# 					required=True, 
# 					help="Path to the log files.")
# parser.add_argument('-o', 
# 					'--outfile', 
# 					help="Desired path/filename for outputted csv; 'output.csv' by \
# 					default")
# args = parser.parse_args()


if __name__ == "__main__":
	# Key variables for GUI
	_in = processInpath(args.inpath)
	_out = args.outfile if args.outfile else args.inpath + 'output.csv'
	_logs = [file.name for file in pathlib.Path(_in).glob('*.log')]
	_url = 'http://pinter.local/doc/roboticdrive/master/ipc.html'
	_topics = getTopicsFromHTML(_url)

	# Launch GUI, where the user select which logs and topics.
	#   The GUI class calls on methods in utils.py for things 
	#   like copying files, grepping the logs, and formatting 
	#		the csv to be human readable.
	app = QApplication([])
	gui = GUI(_in, _out, _logs, _topics)
	gui.show()
	app.exec()
