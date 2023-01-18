# ASDAI-log-parser

Script to pass a log and data strings (e.g., topics) to filter entries by. 
Returns formatted csv.

## Usage
`python <module name> --file <path to log file> --data <string 1 to search for> <string n to search for>` 

## Example Usage
`python log-parsing --data 'ROBOT_SUPPORT_STATUS' 'ROBOT_SUPPORT_STATE' --file  'log-parsing/test.log'`
