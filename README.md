# ASDAI Log Parser
Executable script returns formatted csv with values by topic. 

Executable opens your file directory so you can select the folder with log files. It then opens a GUI where you can select which specific log files to parse and which topics to parse with.

## Set up
- Clone the repository with `git clone git@github.com:mstachyra23/ASDAI-log-parser.git`
- Change into the project directory `/ASDAI-log-parser`.
- `pipenv shell` NOTE  pipenv is used to generate the python virtual environment
- `pipenv install`  NOTE  this installs project dependencies

## Usage
- `pipenv shell` NOTE  enters the virtual environment to gain access to used libraries
- Run `./main` in your terminal or, alternatively, double-click the executable called "main" in `/ASDAI-log-parser/src/dist`.
- Select the folder with the log files.
- Select which log files to use and which topics to filter by.
