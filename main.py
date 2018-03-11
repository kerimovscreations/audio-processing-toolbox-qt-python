import sys
from PyQt5.QtWidgets import QApplication
from widget import Widget

app = QApplication(sys.argv)
widget = Widget()
sys.exit(app.exec_())
