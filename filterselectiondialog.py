from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QVBoxLayout, QHBoxLayout, QDialogButtonBox, QDialog, QSlider, QLabel, QLineEdit


class FilterSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super(FilterSelectionDialog, self).__init__(parent)

        self.parent = parent

        self.select_filter_type = QComboBox()
        self.select_filter_type2 = QComboBox()
        self.select_filter_type3 = QComboBox()
        self.select_filter_max_ripples = QComboBox()
        self.select_filter_min_attenuation = QLineEdit("60")

        self.input_1 = QSlider(Qt.Horizontal)
        self.input_2 = QSlider(Qt.Horizontal)

        self.indicator_1 = QLabel()
        self.indicator_2 = QLabel()

        self.arr_fir = ["triang", "blackman", "hamming", "hann", "bartlett"]
        self.arr_iir = ["butter", "cheby1", "cheby2", "ellip", "bessel"]
        self.ripples = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        type_selection_layout = QHBoxLayout()

        self.select_filter_type.addItems(["FIR filter", "IIR filter"])
        self.select_filter_type.currentIndexChanged.connect(self.on_filter_type_select)

        type_selection_layout.addWidget(self.select_filter_type)

        self.select_filter_type2.addItems(["Low-pass", "High-pass", "Band-pass", "Band-reject"])
        self.select_filter_type2.currentIndexChanged.connect(self.on_filter_type_select2)

        type_selection_layout.addWidget(self.select_filter_type2)

        self.select_filter_type3.addItems(self.arr_fir)
        self.select_filter_type3.currentIndexChanged.connect(self.on_filter_type_select3)

        type_selection_layout.addWidget(self.select_filter_type3)

        main_layout.addLayout(type_selection_layout)

        parameter_selection_layout = QHBoxLayout()

        label_max_ripples = QLabel("Max ripples")
        parameter_selection_layout.addWidget(label_max_ripples)

        self.select_filter_max_ripples.addItems(self.ripples)
        parameter_selection_layout.addWidget(self.select_filter_max_ripples)

        label_min_attenuation = QLabel("Min attenuation")
        parameter_selection_layout.addWidget(label_min_attenuation)

        parameter_selection_layout.addWidget(self.select_filter_min_attenuation)

        main_layout.addLayout(parameter_selection_layout)

        self.check_parameters_availability()

        self.input_1.setMinimum(0)
        self.input_1.setMaximum(50)
        self.input_1.setValue(0)
        self.input_1.setTickPosition(QSlider.TicksBelow)
        self.input_1.setTickInterval(5)
        self.input_1.valueChanged.connect(self.value_changed_1)

        self.indicator_1.setText("0.0")
        main_layout.addWidget(self.indicator_1)
        main_layout.addWidget(self.input_1)

        self.input_2.setMinimum(0)
        self.input_2.setMaximum(50)
        self.input_2.setValue(0)
        self.input_2.setTickPosition(QSlider.TicksBelow)
        self.input_2.setTickInterval(5)
        self.input_2.setEnabled(False)
        self.input_2.valueChanged.connect(self.value_changed_2)

        self.indicator_2.setText("Disabled")
        main_layout.addWidget(self.indicator_2)
        main_layout.addWidget(self.input_2)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        main_layout.addWidget(buttons)

        self.setWindowTitle("Filter parameters")

    def on_filter_type_select(self, i):
        # print("Current index", i, "selection changed ", self.select_filter_type.currentText())
        self.check_parameters_availability()

        if i == 0:
            self.select_filter_type3.clear()
            self.select_filter_type3.addItems(self.arr_fir)
        elif i == 1:
            self.select_filter_type3.clear()
            self.select_filter_type3.addItems(self.arr_iir)

    def on_filter_type_select3(self, i):
        self.check_parameters_availability()

    def on_filter_type_select2(self, i):
        self.input_2.setEnabled(i > 1)
        if i > 1:
            size = self.input_2.value()
            self.indicator_2.setText(str(size / 100))
        else:
            self.indicator_2.setText("Disabled")

    def check_parameters_availability(self):
        if self.select_filter_type.currentText() == "FIR filter":
            self.select_filter_max_ripples.setEnabled(False)
            self.select_filter_min_attenuation.setEnabled(False)
        else:
            if self.select_filter_type3.currentText() == "cheby1" or \
                    self.select_filter_type3.currentText() == "cheby2" or \
                    self.select_filter_type3.currentText() == "ellip":
                self.select_filter_max_ripples.setEnabled(True)
                self.select_filter_min_attenuation.setEnabled(True)
            else:
                self.select_filter_max_ripples.setEnabled(False)
                self.select_filter_min_attenuation.setEnabled(False)

    def value_changed_1(self):
        size = self.input_1.value()
        self.indicator_1.setText(str(size / 100))

    def value_changed_2(self):
        size = self.input_2.value()
        self.indicator_2.setText(str(size / 100))

    @staticmethod
    def show_dialog(parent=None):
        dialog = FilterSelectionDialog(parent)
        result = dialog.exec_()
        return (dialog.select_filter_type.currentText(), dialog.select_filter_type2.currentText(),
                dialog.input_1.value() / 100, dialog.input_2.value() / 100, dialog.select_filter_type3.currentText(),
                dialog.select_filter_max_ripples.currentText(), dialog.select_filter_min_attenuation.text(),
                result == QDialog.Accepted)
