import os  # used for generating outfile path
import sys  # used by PyQT5 to start the GUI app
import pathlib  # used to grab log file names for inputted path
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
                            QComboBox, QHBoxLayout, QVBoxLayout, QLabel, \
                            QFileDialog
from PyQt5.QtCore import Qt, QEvent, QCoreApplication
from PyQt5.QtGui import QStandardItem

from utils import getTopicsFromHTML, copyFiles, filterLogs, formatCSV



class ComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.closeOnLineEditClick = False
        self.lineEdit().installEventFilter(self)
        self.view().viewport().installEventFilter(self)
        self.model().dataChanged.connect(self.updateLineEditField)
        name = "Select logs"
        self.setAccessibleName(name)
        label = QLabel(self.accessibleName(), self)
        label.setGeometry(200, 100, 200, 30) 


    def eventFilter(self, widget, event):
        if widget == self.lineEdit():
            if event.type() == QEvent.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
            return super().eventFilter(widget, event)

        if widget == self.view().viewport():
            if event.type() == QEvent.MouseButtonRelease:
                idx = self.view().indexAt(event.pos())
                item = self.model().item(idx.row())

                if item.checkState() == Qt.Checked:
                    item.setCheckState(Qt.Unchecked)
                else:
                    item.setCheckState(Qt.Checked)
                return True
        return super().eventFilter(widget, event)


    def hidePopup(self):
        super().hidePopup()
        self.startTimer(100)


    def addItems(self, items, itemList=None):
        for i, item in enumerate(items):
            try:
                data = itemList[i]
            except (TypeError, IndexError):
                data = None
            self.addItem(item, data)


    def addItem(self, text, userData=None):
        item = QStandardItem()
        item.setText(text)
        if userData is not None:
            item.setData(userData)

        # Add checkbox functionality to each item
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        item.setData(Qt.Unchecked, Qt.CheckStateRole)
        self.model().appendRow(item)


    def updateLineEditField(self):
        text_container = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                text_container.append(self.model().item(i).text())
        text_string = ', '.join(text_container)
        self.lineEdit().setText(text_string)


    def updateLogs(self, logs):
        logs = self.lineEdit().text()


class LogComboBox(ComboBox):
    def __init__(self):
        super().__init__()


    def returnLogs(self):
        logs = self.lineEdit().text()
        logs = [log.strip() for log in logs.split(',')]
        print(f'[LOGS]')
        for l in logs: print(f'{l}')
        return logs


class TopicComboBox(ComboBox):
    def __init__(self):
        super().__init__()

    def returnTopics(self):
        topics = self.lineEdit().text()
        topics = [topic.strip() for topic in topics.split(',')]
        print(f'[TOPICS]')
        for t in topics: print(f'{t}')
        return topics


class GUI(QWidget):
    '''
    Creates csv with selected data. A user selects a folder with the logs, then select which 
    logs and which topics to output to csv. Csv naming convention is the first 10 characters of
    a log, which corresponds to the date.
    '''
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.url = 'http://pinter.local/doc/roboticdrive/master/ipc.html'
        self.topics = getTopicsFromHTML(self.url)
        self.root = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

        # Specify GUI window
        self.setContentsMargins(20, 20, 20, 20) 
        self.move(800, 300)
        self.setStyleSheet('''
            QWidget {
                font-size: 15px;
            }''')
        self.setWindowTitle("ASDAI Log Parsing GUI")

        # Add dialgoue to enter folder with logs
        self.logsdir = QFileDialog.getExistingDirectory(self, 'Select folder with logs')
        self.logs = [file.name for file in pathlib.Path(self.logsdir).glob('*.log')]

        # Specify name of the output csv to contain the date of the logs
        self.outfile = os.path.join(self.logsdir, 
            "{0}_output.csv".format(self.logs[0][:10]))
        if not os.path.exists(self.outfile):
            with open(self.outfile, 'w') as f:
                pass

        # Add drop down for logs
        self.logLabel = QLabel("Select logs", self)
        self.logComboBox = LogComboBox()
        self.logComboBox.addItems(self.logs)

        # Add drop down for topics
        self.topicLabel = QLabel("Select topics", self)
        self.topicComboBox = TopicComboBox()
        self.topicComboBox.addItems(self.topics)

        # Add button to generate CSV file
        self.btn = QPushButton('Generate CSV', clicked = self.generateCSV)
        self.closebtn = QPushButton('Exit', clicked = self.closeApp)


        # Configure layout with 2 drop downs and 1 button
        self.layout = QVBoxLayout()  # vertical layout
        self.layout.addWidget(self.logLabel)
        self.layout.addWidget(self.logComboBox)
        self.layout.addWidget(self.topicLabel)
        self.layout.addWidget(self.topicComboBox)
        self.layout.addWidget(self.btn)
        self.layout.addWidget(self.closebtn)
        self.layout.setSpacing(15)
        self.setLayout(self.layout)


    def closeApp(self):
        self.app.quit()


    def generateCSV(self):
        self.logs = self.logComboBox.returnLogs()
        self.topics = self.topicComboBox.returnTopics()
        copyFiles(self.logsdir, # src
                  os.path.join(self.root, 'temp'), # dest
                  self.logs)  # logs to move from 'src' to 'dest'
        filterLogs(self.root, self.topics, self.outfile)  # grep logs in /temp for topics; generate csv
        formatCSV(self.outfile)  # format the generated csv
