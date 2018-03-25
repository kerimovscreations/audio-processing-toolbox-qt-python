from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QVBoxLayout, QHBoxLayout, QDialogButtonBox, QDialog, QSlider, QLabel


class FilterSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super(FilterSelectionDialog, self).__init__(parent)

        self.parent = parent

        self.select_filter_type = QComboBox()
        self.select_filter_type2 = QComboBox()

        self.input_1 = QSlider(Qt.Horizontal)
        self.input_2 = QSlider(Qt.Horizontal)

        self.indicator_1 = QLabel()
        self.indicator_2 = QLabel()

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

        main_layout.addLayout(type_selection_layout)

        self.input_1.setMinimum(0)
        self.input_1.setMaximum(100)
        self.input_1.setValue(0)
        self.input_1.setTickPosition(QSlider.TicksBelow)
        self.input_1.setTickInterval(5)
        self.input_1.valueChanged.connect(self.value_changed_1)

        self.indicator_1.setText("0.0")
        main_layout.addWidget(self.indicator_1)
        main_layout.addWidget(self.input_1)

        self.input_2.setMinimum(0)
        self.input_2.setMaximum(100)
        self.input_2.setValue(0)
        self.input_2.setTickPosition(QSlider.TicksBelow)
        self.input_2.setTickInterval(5)
        self.input_2.valueChanged.connect(self.value_changed_2)

        self.indicator_2.setText("0.0")
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
        print("Current index", i, "selection changed ", self.select_filter_type.currentText())

    def on_filter_type_select2(self, i):
        print("Current index", i, "selection changed ", self.select_filter_type2.currentText())

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
                dialog.input_1.value(), dialog.input_2.value(), result == QDialog.Accepted)
