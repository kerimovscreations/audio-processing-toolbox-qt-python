import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QDialogButtonBox, QLineEdit, QLabel, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class CepstrumDialog(QDialog):
    def __init__(self, parent=None):
        super(CepstrumDialog, self).__init__(parent)

        self.parent = parent

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.select_peak_num = QComboBox()
        self.peaks = []

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Graph")

        layout = QVBoxLayout()

        layout.addWidget(self.canvas)

        hor_layout = QHBoxLayout()

        label = QLabel("Number of peak")
        hor_layout.addWidget(label)

        hor_layout.addWidget(self.select_peak_num)

        layout.addLayout(hor_layout)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def show_figure(self, y):
        self.figure.clear()

        ax = self.figure.add_subplot(111)
        ax.plot(y)

        x = np.array(np.arange(0, len(y)))

        thresh_hold = 0.2
        temp_check = 10

        for x1 in range(0, len(y)):
            temp_check = temp_check + 1

            if y[x1] > thresh_hold and temp_check > 10:
                self.peaks.append(x1)
                temp_check = 0

        ax.plot(x[np.array(self.peaks)], y[np.array(self.peaks)], 'o')

        peak_nums = []
        for peak_num in range(0, len(self.peaks)):
            peak_nums.append(str(peak_num + 1))

        self.select_peak_num.addItems(peak_nums)

        self.canvas.draw()

    @staticmethod
    def show_dialog(parent=None, y=[]):
        dialog = CepstrumDialog(parent)
        dialog.show_figure(y)
        result = dialog.exec_()
        return dialog.peaks[dialog.select_peak_num.currentIndex()] - 1, result == QDialog.Accepted
