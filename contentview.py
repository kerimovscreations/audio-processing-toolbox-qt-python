from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from dragdroparea import DragDropArea


class ContentView(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        drag_drop = DragDropArea(parent=self)
        main_layout.addWidget(drag_drop)

        player_layout = QHBoxLayout()

        noise_jc = QIcon('rate_ic.png')
        noise_btn = QPushButton('Add Noise')
        noise_btn.setIcon(noise_jc)

        player_layout.addWidget(noise_btn)

        play_jc = QIcon('play_ic.png')
        play_btn = QPushButton('Play')
        play_btn.setIcon(play_jc)

        player_layout.addWidget(play_btn)

        main_layout.addLayout(player_layout)

        self.setLayout(main_layout)

    def on_file_upload(self, file_url):
        print(file_url)