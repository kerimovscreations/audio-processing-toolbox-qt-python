import os

import numpy as np
import sounddevice as sd
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QComboBox
from scipy import fftpack
from scipy.io import wavfile
import scipy.signal as signal
import matplotlib.pyplot as plt

from dragdroparea import DragDropArea
from filterselectiondialog import FilterSelectionDialog


class ContentView(QWidget):

    def __init__(self):
        super().__init__()

        self.m_chart_1 = QChart()
        self.m_chart_2 = QChart()
        self.m_chart_3 = QChart()
        self.m_chart_4 = QChart()
        self.m_series_1 = QLineSeries()
        self.m_series_2 = QLineSeries()
        self.m_series_3 = QLineSeries()
        self.m_series_4 = QLineSeries()

        self.y_original = []
        self.x_data = []
        self.y_processed = []
        self.sampling_rate = 0

        self.select_action_drop = QComboBox()

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Drag&Drop area
        drag_drop = DragDropArea(parent=self)
        main_layout.addWidget(drag_drop)

        # Chart layout
        chart_layout_1 = QHBoxLayout()
        chart_layout_2 = QHBoxLayout()

        # Chart 1
        chart_view_1 = QChartView(self.m_chart_1)
        chart_view_1.setMinimumSize(400, 300)

        self.m_chart_1.addSeries(self.m_series_1)

        pen = self.m_series_1.pen()
        pen.setColor(Qt.red)
        pen.setWidthF(.1)
        self.m_series_1.setPen(pen)
        self.m_series_1.setUseOpenGL(True)

        axis_x = QValueAxis()
        axis_x.setRange(0, 100)
        axis_x.setLabelFormat("%g")
        axis_x.setTitleText("Samples")

        axis_y = QValueAxis()
        axis_y.setRange(-10, 10)
        axis_y.setTitleText("Audio level")

        self.m_chart_1.setAxisX(axis_x, self.m_series_1)
        self.m_chart_1.setAxisY(axis_y, self.m_series_1)
        self.m_chart_1.setTitle("Original signal time domain")

        chart_layout_1.addWidget(chart_view_1)

        # Chart 2
        chart_view_2 = QChartView(self.m_chart_2)
        chart_view_2.setMinimumSize(400, 300)

        self.m_chart_2.setTitle("Original signal frequency domain")

        pen = self.m_series_2.pen()
        pen.setColor(Qt.blue)
        pen.setWidthF(.1)
        self.m_series_2.setPen(pen)
        self.m_series_2.setUseOpenGL(True)

        self.m_chart_2.addSeries(self.m_series_2)

        chart_layout_1.addWidget(chart_view_2)

        # Chart 3
        chart_view_3 = QChartView(self.m_chart_3)
        chart_view_3.setMinimumSize(400, 300)

        self.m_chart_3.addSeries(self.m_series_3)

        pen = self.m_series_3.pen()
        pen.setColor(Qt.green)
        pen.setWidthF(.1)
        self.m_series_3.setPen(pen)
        self.m_series_3.setUseOpenGL(True)

        axis_x = QValueAxis()
        axis_x.setRange(0, 100)
        axis_x.setLabelFormat("%g")
        axis_x.setTitleText("Samples")

        axis_y = QValueAxis()
        axis_y.setRange(-10, 10)
        axis_y.setTitleText("Audio level")

        self.m_chart_3.setAxisX(axis_x, self.m_series_3)
        self.m_chart_3.setAxisY(axis_y, self.m_series_3)
        self.m_chart_3.setTitle("Noisy signal time domain")

        chart_layout_2.addWidget(chart_view_3)

        # Chart 4
        chart_view_4 = QChartView(self.m_chart_4)
        chart_view_4.setMinimumSize(400, 300)

        self.m_chart_4.setTitle("Noisy signal frequency domain")

        pen = self.m_series_4.pen()
        pen.setColor(Qt.magenta)
        pen.setWidthF(.1)
        self.m_series_4.setPen(pen)
        self.m_series_4.setUseOpenGL(True)

        self.m_chart_4.addSeries(self.m_series_4)

        chart_layout_2.addWidget(chart_view_4)

        main_layout.addLayout(chart_layout_1)
        main_layout.addLayout(chart_layout_2)

        # Action buttons
        player_layout = QHBoxLayout()

        self.select_action_drop.addItems(["Add noise", "Filter"])
        self.select_action_drop.currentIndexChanged.connect(self.on_action_drop_select)

        player_layout.addWidget(self.select_action_drop)

        noise_jc = QIcon('rate_ic.png')
        noise_btn = QPushButton('Process')
        noise_btn.setIcon(noise_jc)
        noise_btn.clicked.connect(self.on_action)

        player_layout.addWidget(noise_btn)

        play_jc = QIcon('play_ic.png')
        play_orig_btn = QPushButton('Play Original')
        play_orig_btn.setIcon(play_jc)
        play_orig_btn.clicked.connect(self.on_play_orig)

        player_layout.addWidget(play_orig_btn)

        play_jc = QIcon('play_ic.png')
        play_btn = QPushButton('Play Processed')
        play_btn.setIcon(play_jc)
        play_btn.clicked.connect(self.on_play)

        player_layout.addWidget(play_btn)

        main_layout.addLayout(player_layout)

        self.setLayout(main_layout)

    def browse_file(self):
        path1 = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'), '*.wav')
        print(path1[0])

        rate, data = wavfile.read(path1[0])

        self.sampling_rate = rate
        self.y_original = data[:, 0]

        self.show_original_data()

    def on_file_upload(self, file_url):
        print(file_url[7:])

        rate, data = wavfile.read(file_url[7:])

        self.sampling_rate = rate
        self.y_original = data[:, 0]

        self.show_original_data()

    def on_action_drop_select(self, i):
        print("Items in the list are :")

        for count in range(self.select_action_drop.count()):
            print(self.select_action_drop.itemText(count))
        print("Current index", i, "selection changed ", self.select_action_drop.currentText())

    def on_action(self):
        if self.select_action_drop.currentText() == "Add noise":
            self.on_add_noise()
        elif self.select_action_drop.currentText() == "Filter":
            self.on_filter()

    def on_add_noise(self):
        if len(self.y_original) > 0:
            noise = np.random.normal(0, self.y_original.max() / 30, len(self.y_original))
            arr1 = np.array(self.y_original)
            self.y_processed = arr1 + noise
            self.show_processed_data()
        else:
            print("Not data to process")

    def on_filter(self):
        print("on_filter")

        filter1, filter2, limit1, limit2, ok = FilterSelectionDialog.show_dialog(parent=self)
        print(filter1, filter2, limit1, limit2, ok)

        if ok:
            if filter1 == "FIR filter":
                self.on_fir_filter(filter2, limit1, limit2)
            elif filter1 == "IIR filter":
                self.on_iir_filter(filter2, limit1, limit2)

    def on_fir_filter(self, filter_type, limit1, limit2):
        if filter_type == "Low-pass":
            design_filter = signal.firwin(41, limit1)
        elif filter_type == "High-pass":
            temp = np.zeros(41)
            temp[20] = 1
            design_filter = temp - np.array(signal.firwin(41, limit1))
        elif filter_type == "Band-pass":
            temp = np.zeros(41)
            temp[20] = 1
            design_filter = temp - np.array(signal.firwin(41, [limit1, limit2]))
        elif filter_type == "Band-reject":
            design_filter = signal.firwin(41, [limit1, limit2])

        self.y_processed = signal.convolve(self.y_original, design_filter, mode='same')

        # w1, h1 = signal.freqz(design_filter)
        # plt.title('Digital filter frequency response')
        # plt.plot(w1, 20 * np.log10(np.abs(h1)), 'b')
        # plt.ylabel('Amplitude Response (dB)')
        # plt.xlabel('Frequency (rad/sample)')
        # plt.grid()
        # plt.show()

        self.show_processed_data()

    def on_iir_filter(self, filter_type, limit1, limit2):
        if filter_type == "Low-pass":
            b, a = signal.iirfilter(4, limit1, rp=5, rs=60, btype='lowpass', ftype='ellip')
        elif filter_type == "High-pass":
            b, a = signal.iirfilter(4, limit1, rp=5, rs=60, btype='highpass', ftype='ellip')
        elif filter_type == "Band-pass":
            b, a = signal.iirfilter(4, [limit1, limit2], rp=5, rs=60, btype='bandpass', ftype='ellip')
        elif filter_type == "Band-reject":
            b, a = signal.iirfilter(4, [limit1, limit2], rp=5, rs=60, btype='bandstop', ftype='ellip')

        self.y_processed = signal.filtfilt(b, a, self.y_original)

        # w1, h1 = signal.freqz(b, a)
        # plt.title('Digital filter frequency response')
        # plt.plot(w1, 20 * np.log10(np.abs(h1)), 'b')
        # plt.ylabel('Amplitude Response (dB)')
        # plt.xlabel('Frequency (rad/sample)')
        # plt.grid()
        # plt.show()

        self.show_processed_data()

    def on_play(self):
        if len(self.y_processed) > 0:
            print("on_play")
            data2 = np.asarray(self.y_processed, dtype=np.int16)
            sd.play(data2, self.sampling_rate)
        else:
            print("not data to play")

    def on_play_orig(self):
        if len(self.y_processed) > 0:
            print("on_play")
            data = np.asarray(self.y_original, dtype=np.int16)
            sd.play(data, self.sampling_rate)
        else:
            print("not data to play")

    def on_save(self):
        if len(self.y_processed) > 0:
            print("on_save")
            path = QFileDialog.getSaveFileName(self, 'Save File', os.getenv('HOME'), 'audio/wav')
            if path[0] != '':
                data2 = np.asarray([self.y_processed, self.y_processed], dtype=np.int16).transpose()
                wavfile.write(path[0], self.sampling_rate, data2)
            else:
                print("not path found")
        else:
            print("not data to save")

    def show_original_data(self):
        # Time domain
        y_data_scaled = np.interp(self.y_original, (self.y_original.min(), self.y_original.max()), (-10, +10))

        sample_size = len(self.y_original)
        self.x_data = np.linspace(0., 100., sample_size)

        points_1 = []

        for k in range(len(y_data_scaled)):
            points_1.append(QPointF(self.x_data[k], y_data_scaled[k]))

        self.m_series_1.replace(points_1)

        # Frequency domain
        y_freq_data = np.abs(fftpack.fft(self.y_original))
        y_freq_data = np.interp(y_freq_data, (y_freq_data.min(), y_freq_data.max()), (0, +10))
        x_freq_data = fftpack.fftfreq(len(self.y_original)) * self.sampling_rate

        axis_x = QValueAxis()
        axis_x.setRange(0, self.sampling_rate / 2)
        axis_x.setLabelFormat("%g")
        axis_x.setTitleText("Frequency [Hz]")

        axis_y = QValueAxis()
        axis_y.setRange(np.min(y_freq_data), np.max(y_freq_data))
        axis_y.setTitleText("Magnitude")

        self.m_chart_2.setAxisX(axis_x, self.m_series_2)
        self.m_chart_2.setAxisY(axis_y, self.m_series_2)

        points_2 = []

        for k in range(len(y_freq_data)):
            points_2.append(QPointF(x_freq_data[k], y_freq_data[k]))

        self.m_series_2.replace(points_2)

    def show_processed_data(self):
        # Time domain
        y_data_scaled = np.interp(self.y_processed, (self.y_processed.min(), self.y_processed.max()), (-10, +10))

        points_3 = []

        for k in range(len(y_data_scaled)):
            points_3.append(QPointF(self.x_data[k], y_data_scaled[k]))

        self.m_series_3.replace(points_3)

        # Frequency domain
        y_freq_data = np.abs(fftpack.fft(self.y_processed))
        y_freq_data = np.interp(y_freq_data, (y_freq_data.min(), y_freq_data.max()), (0, +10))
        x_freq_data = fftpack.fftfreq(len(self.y_processed)) * self.sampling_rate

        axis_x = QValueAxis()
        axis_x.setRange(0, self.sampling_rate / 2)
        axis_x.setLabelFormat("%g")
        axis_x.setTitleText("Frequency [Hz]")

        axis_y = QValueAxis()
        axis_y.setRange(np.min(y_freq_data), np.max(y_freq_data))
        axis_y.setTitleText("Magnitude")

        self.m_chart_4.setAxisX(axis_x, self.m_series_4)
        self.m_chart_4.setAxisY(axis_y, self.m_series_4)

        points_4 = []

        for k in range(len(y_freq_data)):
            points_4.append(QPointF(x_freq_data[k], y_freq_data[k]))

        self.m_series_4.replace(points_4)

    def on_select_filter(self, filter_type, filter_type2, limit1, limit2):
        print(filter_type, filter_type2, limit1, limit2)
