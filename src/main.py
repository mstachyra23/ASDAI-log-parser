#!/usr/bin/env python3
'''
Executable script returns formatted csv with values by topic. Takes in path to 
folder with log(s). GUI enables selecting which log(s) to select from folder 
and which topics to grep for. 

Usage
		(1) Run $ ./main in your terminal or, alternatively, double-click the 
			  executable called "main" in /dist.
		(2) Select the folder with the log files.
		(3) Select which log files to use and which topics to filter by.

'''
from PyQt5.QtWidgets import QApplication  # used to generate GUI
from gui import GUI


if __name__ == "__main__":
	app = QApplication([])
	gui = GUI()
	gui.show()
	app.exec()
