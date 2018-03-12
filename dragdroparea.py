from PyQt5.QtWidgets import QWidget, QComboBox, QLabel, QVBoxLayout


class ComboBox(QComboBox):

    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        print(e)

        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.addItem(e.mimeData().text())


class DragDropArea(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Type some text in textbox and drag it into combo box"))
        com = ComboBox()
        layout.addWidget(com)

        self.setLayout(layout)