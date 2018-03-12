from PyQt5.QtWidgets import QWidget, QComboBox, QLabel, QVBoxLayout


class ComboBox(QComboBox):

    def __init__(self, parent=None):
        super().__init__()

        self.setAcceptDrops(True)

        self.parent = parent

    def dragEnterEvent(self, e):
        print(e)

        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.addItem(e.mimeData().text())
        self.parent.on_file_upload(e.mimeData().text())


class DragDropArea(QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Drag and drop music file here"))
        com = ComboBox(parent=self.parent)
        layout.addWidget(com)

        self.setLayout(layout)
