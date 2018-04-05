import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class FilterResponseDialog(QDialog):
    def __init__(self, parent=None):
        super(FilterResponseDialog, self).__init__(parent)

        self.parent = parent

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Filter response")

        layout = QVBoxLayout()

        layout.addWidget(self.canvas)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def show_figure(self, w1, h1):
        self.figure.clear()

        ax = self.figure.add_subplot(121)
        ax.plot(w1, 20 * np.log10(np.abs(h1)), 'b')
        ax1 = self.figure.add_subplot(122)
        ax1.plot(w1, np.abs(h1))
        self.canvas.draw()

    @staticmethod
    def show_dialog(parent=None, w1=[], h1=[]):
        dialog = FilterResponseDialog(parent)
        dialog.show_figure(w1, h1)
        result = dialog.exec_()
        return result == QDialog.Accepted
