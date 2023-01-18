def buildExtendedRegex(data):
    return '|'.join(data)


def createCSV(path, data, dialect='excel'):
    with open(path, 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile)
        filewriter.writerow(data)