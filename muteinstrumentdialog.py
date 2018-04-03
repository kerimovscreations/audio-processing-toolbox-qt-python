from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QDialogButtonBox, QDialog, QRadioButton


class MuteInstrumentsDialog(QDialog):
    def __init__(self, parent=None):
        super(MuteInstrumentsDialog, self).__init__(parent)

        self.parent = parent

        self.check_piano = QRadioButton("Piano")
        self.check_organ = QRadioButton("Organ")
        self.check_flute = QRadioButton("Flute")
        self.check_french_horn = QRadioButton("French horn")
        self.check_trumpet = QRadioButton("Trumpet")
        self.check_violin = QRadioButton("Violin")
        self.check_guitar_acoustic = QRadioButton("Guitar acoustic")
        self.check_guitar_bass = QRadioButton("Guitar bass")
        self.check_clarinet = QRadioButton("Clarinet")
        self.check_saxophone = QRadioButton("Saxophone")

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        main_layout.addWidget(self.check_piano)
        main_layout.addWidget(self.check_organ)
        main_layout.addWidget(self.check_flute)
        main_layout.addWidget(self.check_french_horn)
        main_layout.addWidget(self.check_trumpet)
        main_layout.addWidget(self.check_violin)
        main_layout.addWidget(self.check_guitar_acoustic)
        main_layout.addWidget(self.check_guitar_bass)
        main_layout.addWidget(self.check_clarinet)
        main_layout.addWidget(self.check_saxophone)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        main_layout.addWidget(buttons)

        self.setWindowTitle("Mute instruments")

    @staticmethod
    def show_dialog(parent=None):
        dialog = MuteInstrumentsDialog(parent)
        result = dialog.exec_()
        return (dialog.check_piano.isChecked(), dialog.check_organ.isChecked(), dialog.check_flute.isChecked(),
                dialog.check_french_horn.isChecked(),
                dialog.check_trumpet.isChecked(), dialog.check_violin.isChecked(),
                dialog.check_guitar_acoustic.isChecked(),
                dialog.check_guitar_bass.isChecked(), dialog.check_clarinet.isChecked(),
                dialog.check_saxophone.isChecked(), result == QDialog.Accepted)
