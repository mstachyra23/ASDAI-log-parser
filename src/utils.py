import os  # used for UNIX grep command call
import csv  # used to read and format the outfile csv
import json  # used to format the outfile csv
import shutil  # used for clearing temp/ after each call
import requests  # used for grabbing url page
import tzlocal  # used to get the local timezone for timestamp
import datetime  # used to parse UNIX time to timestamp
from bs4 import BeautifulSoup  # used for parsing html with topics



def getTopicsFromHTML(url):
    '''
    Return list of robotic drive topics parsed from the html page on pinter.
    '''
    try:
        page = requests.get(url).text
    except Exception as e:
        page = open('roboticdrive.html', r)
    finally:
        soup = BeautifulSoup(page, 'html.parser')
        parsef = lambda c : (c.isupper() or c=='_' or c=='|' or c=='(' or c==')')
        topics = [list(tag['id']) for tag in soup.select('dt[id]')]
        topics = [''.join(topic_chars)[6:]
                  for topic_chars in topics 
                  if all([parsef(char) for char in ''.join(topic_chars)[6:]])]
        return topics


def clearTemp():
    '''
    Removes copied log files from /temp directory after grep is called.
    '''
    for filename in os.listdir('temp'):
       file_path = os.path.join('temp', filename)
       try:
           if os.path.isfile(file_path) or os.path.islink(file_path):
               os.unlink(file_path)
           elif os.path.isdir(file_path):
               shutil.rmtree(file_path)
       except Exception as e:
           print('Failed to delete %s. Reason: %s' % (file_path, e)) 


def copyFiles(directory, logs):
    '''
    Copy select logs from inpath to /temp within current directory.
    '''
    files = [os.path.join(directory, log) for log in logs]
    for f in files:
        shutil.copy(f, 'temp/')


def UNIXgrepFiles(topics, outfile):
    '''
    Grep logs in temp/ for topics and move to outfile (csv). Cleans 
      up after grep by deleting copies in /temp.
    '''
    regex = '|'.join(topics)
    command = "grep -irE '{0}' temp/ > '{1}'".format(regex, 'temp.csv')
    os.system(command)
    clearTemp()  # removes the copied logs from /temp as no longer needed


def formatCSV(outfile):
    '''
    Format outfile csv to be human readable according to Clincal Development
      Engineering's with headers 'Time', 'Topic', '<Topic Value 1>', '<Topic 
      Value n>'
    '''
    with open('temp.csv') as readcsv, open(outfile, "w") as writecsv:
        csvreader = csv.reader(readcsv, delimiter='\n')
        csvwriter = csv.writer(writecsv, delimiter='\n')
        for row in csvreader:
            # Convert row to JSON
            string = row[0]
            jsonstring = string[(string.find(':')+1):]  # strip the file id
            jsonobj = json.loads(jsonstring)

            # Timestamp
            timezone = tzlocal.get_localzone() 
            unixtime = jsonobj['packet']['timestamp']
            timestamp = datetime.datetime.fromtimestamp(unixtime, timezone)

            # Topic


            # Topic values

















