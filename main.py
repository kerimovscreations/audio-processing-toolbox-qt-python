import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction
from contentview import ContentView


class MainApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.toolbar = self.addToolBar("File")
        self.contentView = ContentView()

        self.init_ui()

    def init_ui(self):
        new_btn = QAction(QIcon("new_ic.png"), "New", self)
        self.toolbar.addAction(new_btn)

        open_btn = QAction(QIcon("open_ic.png"), "Open", self)
        self.toolbar.addAction(open_btn)

        save_btn = QAction(QIcon("save_ic.png"), "Save", self)
        self.toolbar.addAction(save_btn)

        self.toolbar.actionTriggered[QAction].connect(self.toolbar_btn_click)

        self.setCentralWidget(self.contentView)
        self.setWindowTitle("Audio signal toolbox")

        self.show()

    def toolbar_btn_click(self, a):
        if a.text() == "New":
            # self.setCentralWidget(AudioRecPlot())
            self.contentView.reset_data()
        elif a.text() == "Open":
            self.contentView.browse_file()
        elif a.text() == "Save":
            self.contentView.on_save()


app = QApplication(sys.argv)
widget = MainApp()
sys.exit(app.exec_())
