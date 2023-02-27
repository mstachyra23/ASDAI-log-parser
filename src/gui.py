import os  # used for generating outfile path
import pathlib  # used to grab log file names for inputted path
from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, \
                            QVBoxLayout, QLabel, QFileDialog, \
                            QGroupBox, QGridLayout, QCalendarWidget, \
                            QMessageBox, QDateEdit, QLineEdit
from PyQt5.QtCore import Qt, QEvent, QDate
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


class LogsComboBox(ComboBox):
    def __init__(self):
        super().__init__()

    def returnLogs(self):
        logs = self.lineEdit().text()
        logs = [log.strip() for log in logs.split(',')]
        print(f'[LOGS]')
        for l in logs: print(f'{l}')
        return logs


class TopicsComboBox(ComboBox):
    def __init__(self):
        super().__init__()

    def returnTopics(self):
        topics = self.lineEdit().text()
        topics = [topic.strip() for topic in topics.split(',')]
        print(f'[TOPICS]')
        for t in topics: print(f'{t}')
        return topics


class Calendar(QWidget):
    def __init__(self):
        super().__init__()
        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.cal.move(20, 20)
        self.cal.clicked[QDate].connect(self.showDate)
    
    def showDate(self):
        date = self.cal.selectedDate()
        date = date.toString()
        return date



class GUI(QWidget):
    '''GUI has 4 areas to interact with
        1  Calendar - calendar to enter date / marks online as source
        2  Path(s) - paths to logs and videos locally / marks local file paths as source
        3  Log(s) - dropdown to select logs and topics from source
        4  Video(s) - dropdown to select videos and time intervals from source
    '''
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.url = 'http://pinter.local/doc/roboticdrive/master/ipc.html'
        self.topics = getTopicsFromHTML(self.url)
        self.root = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

        # self.logsdir = QFileDialog.getExistingDirectory(self, 'Select folder with logs')
        self.logsdir = self.root 

        self.logs = [file.name for file in pathlib.Path(self.logsdir).glob('*.log')]
        self.outfile = os.path.join(self.logsdir, 
            "{0}_output.csv".format(self.logs[0][:10]))
        if not os.path.exists(self.outfile):
            with open(self.outfile, 'w') as f:
                pass


        # GUI setup as grid of 4 group boxes each with their own layout             
        self.dateBox = QGroupBox("Select date of surgery")
        self.dirBox = QGroupBox("Optional override: Select local directories for logs and/or videos")
        self.logsBox = QGroupBox("Prepare logs for export") # logs, topics
        self.videosBox = QGroupBox("Prepare videos for export") # videos, time intervals
        self.grid = QGridLayout()
        self.btn = QPushButton('Export', clicked = self.exportFiles)  #TODO(ms): update for videos
        self.closebtn = QPushButton('Exit', clicked = self.closeApp)


        # date layout
        calendar = Calendar()
        self.dateLayout = QVBoxLayout()
        self.dateLayout.addWidget(calendar)
        self.date = calendar.showDate()


        # file dialog layout
        self.fileDialogLayout = QGridLayout()

        logsDirSelectBtn = QPushButton('...')
        videosDirSelectBtn = QPushButton('...')

        logsDirSelectBtn.clicked.connect(self.openDialog)
        videosDirSelectBtn.clicked.connect(self.openDialog)

        self.logsDirEdit = QLineEdit()
        self.videosDirEdit = QLineEdit()

        self.fileDialogLayout.addWidget(QLabel("Logs directory:"), 0, 0)
        self.fileDialogLayout.addWidget(self.logsDirEdit, 0, 1)
        self.fileDialogLayout.addWidget(logsDirSelectBtn, 0, 2)
        self.fileDialogLayout.addWidget(QLabel("Videos directory:"), 1, 0)
        self.fileDialogLayout.addWidget(self.videosDirEdit, 1, 1)
        self.fileDialogLayout.addWidget(videosDirSelectBtn, 1, 2)


        # logs layout - logs, topics
        self.logsLayout = QGridLayout() 

        self.logsLabel = QLabel(self)
        self.topicsLabel = QLabel(self)
        self.logsLabel.setText("Logs:")
        self.topicsLabel.setText("Topics:")

        self.logsComboBox = LogsComboBox()
        self.topicsComboBox = TopicsComboBox()
        self.logsComboBox.addItems(self.logs) 
        self.topicsComboBox.addItems(self.topics)

        self.logsLayout.addWidget(self.logsLabel, 0, 0)
        self.logsLayout.addWidget(self.logsComboBox, 0, 1)
        self.logsLayout.addWidget(self.topicsLabel, 1, 0)
        self.logsLayout.addWidget(self.topicsComboBox, 1, 1)


        # videos layout - time intervals, videos
        self.videosLayout = QGridLayout() 

        self.videosLabel = QLabel(self)
        self.timeIntervalsLabel = QLabel(self)
        self.videosLabel.setText("Videos:")
        self.timeIntervalsLabel.setText("Time intervals:")

        self.videosCombobox = LogsComboBox() # TODO(ms): create videos combo box
        self.timeIntervalsCombobox = LogsComboBox()  # TODO(ms): create time intervals combo box

        self.videosLayout.addWidget(self.videosLabel, 0, 0)
        self.videosLayout.addWidget(self.videosCombobox, 0, 1)
        self.videosLayout.addWidget(self.timeIntervalsLabel, 1, 0)
        self.videosLayout.addWidget(self.timeIntervalsCombobox, 1, 1)


        # compose layouts
        self.dateBox.setLayout(self.dateLayout)
        self.dirBox.setLayout(self.fileDialogLayout)
        self.logsBox.setLayout(self.logsLayout) 
        self.videosBox.setLayout(self.videosLayout) 
        # TODO(ms): path entry @ (1, 0)
        self.grid.addWidget(self.logsBox, 0, 1)
        self.grid.addWidget(self.videosBox, 1, 1)
        self.grid.addWidget(self.dateBox, 0, 0)
        self.grid.addWidget(self.dirBox, 1, 0)
        self.grid.addWidget(self.closebtn)
        self.grid.addWidget(self.btn)
        self.grid.setSpacing(20)
        self.setLayout(self.grid)

        # msg = QMessageBox()
        # msg.setIcon(QMessageBox.Warning)
        # msg.setText('Error: Choose date or choose a local folder.')
        # msg.exec_()

        # additional style tweaks
        # self.setContentsMargins(20, 20, 20, 20) 
        self.setGeometry(500, 500, 1000, 500)
        self.setStyleSheet('''
            QWidget {
                font-size: 13px;
            }''')
        self.setWindowTitle("...")


    def closeApp(self):
        self.app.quit()


    def openDialog(self):
        dir = QFileDialog.getExistingDirectory(self, "Select a directory")
        if dir:
            path = pathlib.Path(dir)
            self.dirEdit(str(path))


    def exportFiles(self):
        #TODO(ms): refactor to handle logs and videos

        # self.logs = self.logComboBox.returnLogs()
        # self.topics = self.topicComboBox.returnTopics()
        # copyFiles(self.logsdir, # src
        #           os.path.join(self.root, 'temp'), # dest
        #           self.logs)  # logs to move from 'src' to 'dest'
        # filterLogs(self.root, self.topics, self.outfile)  # grep logs in /temp for topics; generate csv
        # formatCSV(self.outfile)  # format the generated csv
        pass

    
