import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog
from audiorecplot import AudioRecPlot
from contentview import ContentView


class MainApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.toolbar = self.addToolBar("File")

        self.init_ui()

    def init_ui(self):
        new = QAction(QIcon("new_ic.png"), "New", self)
        self.toolbar.addAction(new)

        open = QAction(QIcon("open_ic.png"), "Open", self)
        self.toolbar.addAction(open)

        save = QAction(QIcon("save_ic.png"), "Save", self)
        self.toolbar.addAction(save)

        self.toolbar.actionTriggered[QAction].connect(self.toolbar_btn_click)

        self.setCentralWidget(ContentView())
        self.setWindowTitle("Toolbar")

        self.show()

    def toolbar_btn_click(self, a):
        if a.text() == "New":
            self.setCentralWidget(AudioRecPlot())
        elif a.text() == "Open":
            self.open_file()
        elif a.text() == "Save":
            self.save_file()

    def open_file(self):
        QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'), 'audio/pcm')

    def save_file(self):
        QFileDialog.getSaveFileName(self, 'Save File', os.getenv('HOME'), 'audio/pcm')


app = QApplication(sys.argv)
widget = MainApp()
sys.exit(app.exec_())
