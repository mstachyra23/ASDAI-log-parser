import sys

# QT for GUI
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
                            QComboBox, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QStandardItem


def buildExtendedRegex(data):
    return '|'.join(data)


def createCSV(path, data, dialect='excel'):
    with open(path, 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile)
        filewriter.writerow(data)


def grabSelected():
    '''Returns selected logs from the Tkinter GUI dropdown (listbox).
    '''
    return [listbox.get(i) for i in listbox.curselection()]


class LogComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.closeOnLineEditClick = False
        self.lineEdit().installEventFilter(self)
        self.view().viewport().installEventFilter(self)
        self.model().dataChanged.connect(self.updateLineEditField)


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
            print(item)
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



class GUI(QWidget):
    def __init__(self, options):
        super().__init__()
        self.window_width, self.window_height = 700, 300
        self.setMinimumSize(self.window_width, self.window_height)
        self.setStyleSheet('''
            QWidget {
                font-size: 15px;
            }''')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowTitle("ASDAI Log Parsing GUI")

        # Add 2 comboboxes (for the logs and for the topics)
        logComboBox = LogComboBox()
        logComboBox.addItems(options)
        self.layout.addWidget(logComboBox)

        # Add button to generate CSV file
        btn = QPushButton('Generate CSV', clicked=lambda: print(logComboBox.lineEdit().text()))
        self.layout.addWidget(btn)







