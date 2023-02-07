import os  # used for UNIX grep command call
import csv  # used to read and format the outfile csv
import json  # used to format the outfile csv
import shutil  # used for clearing temp/ after each call
import platform  # used to check whether os
import requests  # used for grabbing url page
import tzlocal  # used to get the local timezone for timestamp
import datetime  # used to parse UNIX time to timestamp
from bs4 import BeautifulSoup  # used for parsing html with topics



def getTopicsFromHTML(url):
    '''Return list of robotic drive topics parsed from the html page on pinter.
    '''
    try:
        page = requests.get(url).text # get html page
    except Exception as e:  # when no access to pinter / VPN 
        page = open('roboticdrive.html', "r")
    finally:
        # parse html page and extract the topics from the dt tags
        soup = BeautifulSoup(page, 'html.parser')
        topics = [''.join(list(tag['id']))[6:] for tag in soup.select('dt[id]')]

        # remove strings that aren't topics
        filtf = lambda c:(c.isupper() or c=='_' or c=='|' or c=='(' or c==')')
        topics = [''.join(chars)
                  for chars in topics
                  if all([filtf(c) for c in ''.join(chars)])]

        # split combined topics, e.g., ROBOT_(ARM|CAMERA|SUPPORT)_COUNTERS
        for chars in topics:
            if "|" in chars:
                lpart = chars.find("(")
                rpart = chars.rfind(")")
                mparts = chars[lpart+1:rpart].split("|")
                splittopics = ["{0}{1}{2}".format(chars[:lpart], p, chars[rpart+1:]) 
                               for p in mparts]  
                topics.extend(splittopics)
        topics = [topic for topic in topics if "|" not in topic]

        return topics


def clearTemp():
    '''Removes copied log files from /temp directory after grep is called.
    '''
    for filename in os.listdir(os.path.join(os.getcwd(), '..', 'temp')):
        file_path = os.path.join(os.getcwd(), '..', 'temp', filename)
        try:
           if os.path.isfile(file_path) or os.path.islink(file_path):
               os.unlink(file_path)
           elif os.path.isdir(file_path):
               shutil.rmtree(file_path)
        except Exception as e:
           print('Failed to delete %s. Reason: %s' % (file_path, e)) 


def copyFiles(src, dest, logs):
    '''Copy logs to temp folder (dest) from src. Creates temp folder if it doesn't exist.
    '''
    if not os.path.exists(dest):
        print(f"[INFO] {dest} didn't exist. Created.")
        os.makedirs(dest)

    # (log src path, log dest path) pairs
    src_dest_pairs = [[os.path.join(src, log), os.path.join(dest, log)] for log in logs]
    for src, dest in src_dest_pairs:
        shutil.copy(src, dest)


def filterLogs(topics, outfile):
    '''Filters logs in temp/ for topics and move to outfile (csv). Cleans 
        up after filter by deleting copies in /temp. If Windows, runs "Findstr" command;
        if Linux, runs "grep" command.
    '''
    regex = '|'.join(topics)
    searchpath = os.path.join(os.getcwd(), '..', 'temp')
    if platform.system()=="Windows":
        command = "Findstr /R '{0}' '{1}' > '{2}'".format(regex, searchpath, outfile)
    else:
        command = "grep -irE '{0}' {1} > '{2}'".format(regex, searchpath, outfile)
    os.system(command)
    clearTemp()  # removes the copied logs from /temp as no longer needed


def formatCSV(outfile):
    '''Format outfile csv to be human readable according to Clincal Development
        Engineering's with headers 'Time', 'Topic', '<Topic Value 1>', '<Topic 
        Value n>'
    '''
    header = ['timestamp', 'topic']
    topics = []
    rowstowrite = []

    # Read grepped csv and extract topics and values
    with open(outfile) as readcsv:
        csvreader = csv.reader(readcsv, delimiter='\n')
        for row in csvreader:
            # Generate JSON
            string = row[0]
            jsonstring = string[(string.find(':')+1):]  # strip the file id
            jsonobj = json.loads(jsonstring)

            # Get topic and values
            timestamp = datetime.datetime.fromtimestamp(
                jsonobj['packet']['timestamp'], 
                tzlocal.get_localzone()).strftime("%H:%M:%S")
            topic = jsonobj['packet']['topic']
            f = lambda k : k!="sender_id" and k!="timestamp" and k!="topic"
            packetdict = {k:v for k,v in jsonobj['packet'].items() if f(k)}

            # Add topic values to column headers if new topic
            if topic not in topics:
                for key in packetdict.keys():
                    header.append(key)
                topics.append(topic)

            # Store new row to be written to csv
            rowstowrite.append(
                generateRowForCSV(header, timestamp, topic, packetdict))

    # Write topics and values
    with open(outfile, "w") as writecsv:
        csvwriter = csv.writer(writecsv, delimiter=',')
        csvwriter.writerow(header)
        for row in rowstowrite:
            csvwriter.writerow(row)
    print(f'[INFO] Csv written to {outfile}.')
    print(f'[INFO] Ready to generate another CSV. Otherwise, Exit.')



def generateRowForCSV(header, timestamp, topic, packetdict):
    '''Return row for CSV as string with values in correct positions according
        to the column headers captured in header.

       Example

            timestamp, topic, , , , value 1, ..., value n
                            |     |
                               ^
                               |
                            spacers to align values to col header pos
    '''
    try:
        # key used to get position in header where to start appending values
        uniqueKey = list(packetdict.keys())[0]  

        # spacers are 'n/a' in header col positions of irelevant values
        spacers = ['n/a'] * (header.index(uniqueKey) - 2) # -2 (timestamp, topic)

        # get values and convert to string for join
        values = list(packetdict.values())  # packetdict values by col header
        values = [str(v) for v in values]  

        # generate row 
        row = [timestamp, topic]
        row.extend(spacers) 
        row.extend(values)

        return row
    except Exception as e:
        print(f"Failed to generate row for CSV. Exception: {e}. Thrown for \
            {topic} with values {packetdict}.")