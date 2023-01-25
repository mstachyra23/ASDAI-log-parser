# ASDAI Log Parser
Executable script returns formatted csv with values by topic. Takes in path to 
folder with log(s). GUI enables selecting which log(s) to select from folder 
and which topics to grep for. 

## Set up
- Clone the repository with `git clone git@github.com:mstachyra23/ASDAI-log-parser.git`
- Change into the project directory /ASDAI-log-parser.
- `pipenv shell`  # pipenv is used to generate the python virtual environment
- `pipenv install`  # this installs project dependencies

## Usage
- `pipenv shell` # enters the virtual environment to gain access to used libraries
- Run `./main` in your terminal or, alternatively, double-click the executable called "main" in /dist.
- Select the folder with the log files.
- Select which log files to use and which topics to filter by.
