import os

import numpy as np
import sounddevice as sd
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QComboBox, QErrorMessage, \
    QMessageBox

from scipy import fftpack
from scipy.io import wavfile
import scipy.signal as signal
from scipy.signal import lfilter
import cepstrum
import matplotlib.pyplot as plt
import librosa
import librosa.display

from dragdroparea import DragDropArea
from filterselectiondialog import FilterSelectionDialog
from muteinstrumentdialog import MuteInstrumentsDialog
from filterresponsedialog import FilterResponseDialog
from cepstrumdialog import CepstrumDialog


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

        self.pathForVocalMute = ""

        self.select_action_drop = QComboBox()

        self.echo_shift = 0.4
        self.echo_alpha = 0.5

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
        self.m_chart_3.setTitle("Processed signal time domain")

        chart_layout_2.addWidget(chart_view_3)

        # Chart 4
        chart_view_4 = QChartView(self.m_chart_4)
        chart_view_4.setMinimumSize(400, 300)

        self.m_chart_4.setTitle("Processed signal frequency domain")

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

        self.select_action_drop.addItems(["Add noise", "Filter", "Mute equipment",
                                          "Mute vocal", "Add echo", "Filter echo"])

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

        stop_jc = QIcon('stop_ic.png')
        stop_btn = QPushButton('Stop')
        stop_btn.setIcon(stop_jc)
        stop_btn.clicked.connect(self.on_stop)

        player_layout.addWidget(stop_btn)

        main_layout.addLayout(player_layout)

        self.setLayout(main_layout)

    ''''
        Toolbar actions
    '''

    def browse_file(self):
        path1 = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'), '*.wav')
        print(path1[0])

        rate, data = wavfile.read(path1[0])

        self.sampling_rate = rate
        self.y_original = data[:, 0]

        self.show_original_data()

    def on_file_upload(self, file_url):
        print(file_url[7:])

        self.pathForVocalMute = file_url[7:]

        rate, data = wavfile.read(file_url[7:])

        self.sampling_rate = rate
        self.y_original = data[:, 0]

        self.show_original_data()

    def on_save(self):
        print("on_save")
        if len(self.y_processed) > 0:
            path = QFileDialog.getSaveFileName(self, 'Save File', os.getenv('HOME'), 'audio/wav')
            if path[0] != '':
                data2 = np.asarray([self.y_processed, self.y_processed]).transpose()
                wavfile.write(path[0], self.sampling_rate, data2)
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("No path")
                msg.setInformativeText("You should define path to save file")
                msg.setWindowTitle("Error")
                msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("No data")
            msg.setInformativeText("No data to save, you should upload and process sound file")
            msg.setWindowTitle("Error")
            msg.exec_()

    ''''
        Action selection
    '''

    def on_action(self):
        if self.select_action_drop.currentText() == "Add noise":
            self.on_add_noise()
        elif self.select_action_drop.currentText() == "Filter":
            self.on_filter()
        elif self.select_action_drop.currentText() == "Mute equipment":
            self.on_mute_equipment()
        elif self.select_action_drop.currentText() == "Mute vocal":
            self.on_mute_voice()
        elif self.select_action_drop.currentText() == "Add echo":
            self.on_add_echo()
        elif self.select_action_drop.currentText() == "Filter echo":
            self.on_filter_echo()

    '''
        Noise addition
    '''

    def on_add_noise(self):
        if len(self.y_original) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Upload sound file")
            msg.setInformativeText("First you should add sound file to process")
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        noise = np.random.normal(0, self.y_original.max() / 30, len(self.y_original))
        arr1 = np.array(self.y_original)
        self.y_processed = arr1 + noise
        self.show_processed_data()

    def on_filter(self):
        print("on_filter")

        if len(self.y_original) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Upload sound file")
            msg.setInformativeText("First you should add sound file to process")
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        filter1, filter2, limit1, limit2, extra, max_ripple, min_attenuation, ok = FilterSelectionDialog.show_dialog(
            parent=self)
        print(filter1, filter2, limit1, limit2, extra, max_ripple, min_attenuation, ok)

        if ok:
            if filter1 == "FIR filter":
                self.on_fir_filter(filter2, limit1, limit2, extra)
            elif filter1 == "IIR filter":
                self.on_iir_filter(filter2, limit1, limit2, extra, max_ripple, min_attenuation)

    def on_mute_equipment(self):
        print("on_mute_equipment")

        check_piano, check_organ, check_flute, check_french_horn, check_trumpet, check_violin, \
        check_guitar_acoustic, check_guitar_bass, check_clarinet, \
        check_saxophone, ok = MuteInstrumentsDialog.show_dialog(parent=self)

        print(check_piano, check_organ, check_flute, check_french_horn, check_trumpet, check_violin,
              check_guitar_acoustic, check_guitar_bass, check_clarinet, check_saxophone, ok)

        '''
        Piano	A0 (28 Hz) to C8 (4,186 Hz or 4.1 KHz)
        Organ	C0 (16 Hz) to A9 (7,040 KHz)	
        Concert Flute	C4 (262 Hz) to B6 (1,976 Hz)	
        French Horn	A2 (110 Hz) to A5 (880 Hz)
        Trumpet	E3 (165 Hz) to B5 (988 Hz)
        Violin	G3 (196 Hz) - G7 (3,136 Hz) (G-D-E-A) (or C8 (4,186 Hz?)
        Guitar (Acoustic)	E2 (82 Hz) to F6 (1,397 Hz)
        Guitar (Bass)	4 string E1 (41 Hz) to C4 (262 Hz)
        Clarinet	E3 (165 Hz) to G6 (1,568 Hz)	
        Saxaphone Eb 138-830 (880)
        '''
        if ok:
            print(check_piano)

        limit1 = 0.1
        limit2 = 0.2
        if check_piano:
            pass
        elif check_organ:
            pass
        elif check_flute:
            limit1 = 262 / self.sampling_rate
            limit2 = 1976 / self.sampling_rate
            pass
        elif check_french_horn:
            limit1 = 110 / self.sampling_rate
            limit2 = 880 / self.sampling_rate
            pass
        elif check_trumpet:
            limit1 = 165 / self.sampling_rate
            limit2 = 988 / self.sampling_rate
            pass
        elif check_violin:
            limit1 = 196 / self.sampling_rate
            limit2 = 3136 / self.sampling_rate
            pass
        elif check_guitar_acoustic:
            limit1 = 82 / self.sampling_rate
            limit2 = 1397 / self.sampling_rate
            pass
        elif check_guitar_bass:
            limit1 = 41 / self.sampling_rate
            limit2 = 262 / self.sampling_rate
            pass
        elif check_clarinet:
            limit1 = 165 / self.sampling_rate
            limit2 = 1568 / self.sampling_rate
            pass
        elif check_saxophone:
            limit1 = 138 / self.sampling_rate
            limit2 = 880 / self.sampling_rate
            pass

        print(limit1, limit2)

        print([0.0, 0.0001, limit1 - 0.0001, limit1, limit2, limit2 + 0.0001, 0.9991, 1.0],
              [0, 1, 1, 0, 0, 1, 1, 0])
        design_filter = signal.firwin2(1000000,
                                       [0.0, 0.0001, limit1 - 0.0001, limit1, limit2, limit2 + 0.0001, 0.9991, 1.0],
                                       [0, 1, 1, 0, 0, 1, 1, 0])

        self.y_processed = signal.convolve(self.y_original, design_filter, mode='same')

        w1, h1 = signal.freqz(design_filter)

        result = FilterResponseDialog.show_dialog(parent=self, w1=w1, h1=h1)

        if result:
            self.show_processed_data()

    def on_mute_voice(self):
        y, sr = librosa.load(self.pathForVocalMute, sr=self.sampling_rate)

        S_full, phase = librosa.magphase(librosa.stft(y))

        S_filter = librosa.decompose.nn_filter(S_full,
                                               aggregate=np.median,
                                               metric='cosine',
                                               width=int(librosa.time_to_frames(2, sr=sr)))

        S_filter = np.minimum(S_full, S_filter)

        margin_i, margin_v = 2, 10
        power = 2

        mask_i = librosa.util.softmask(S_filter,
                                       margin_i * (S_full - S_filter),
                                       power=power)

        mask_v = librosa.util.softmask(S_full - S_filter,
                                       margin_v * S_filter,
                                       power=power)

        S_foreground = mask_v * S_full
        S_background = mask_i * S_full

        self.y_processed = librosa.istft(S_background)

        self.show_processed_data()

    def on_add_echo(self):
        if len(self.y_original) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Upload sound file")
            msg.setInformativeText("First you should add sound file to process")
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        num_shift = int(self.sampling_rate * self.echo_shift)
        zeros = np.zeros(num_shift)

        original = np.append(self.y_original, zeros)
        echo = np.append(zeros, self.y_original) * self.echo_alpha

        self.y_processed = original + echo

        np.delete(self.y_processed, np.arange(len(self.y_processed) - len(zeros), len(self.y_processed)))

        self.show_processed_data()

    def on_filter_echo(self):
        ceps = cepstrum.real_cepstrum(np.array(self.y_original))

        index, result = CepstrumDialog.show_dialog(self, ceps)

        if result:
            print(index)

            b = np.array([1])

            a = np.zeros(index + 1)
            a[0] = 1
            a[len(a) - 1] = self.echo_alpha

            zi = signal.lfilter_zi(b, a)

            self.y_processed, _ = signal.lfilter(b, a, self.y_original, axis=0, zi=zi*self.y_original[0])

            w1, h1 = signal.freqz(b, a)

            result = FilterResponseDialog.show_dialog(parent=self, w1=w1, h1=h1)

            if result:
                self.show_processed_data()

    '''
        Filters
    '''
    def on_fir_filter(self, filter_type, limit1, limit2, extra):
        if filter_type == "Low-pass":
            design_filter = signal.firwin(41, limit1, window=extra)
        elif filter_type == "High-pass":
            temp = np.zeros(41)
            temp[20] = 1
            design_filter = temp - np.array(signal.firwin(41, limit1, window=extra))
        elif filter_type == "Band-pass":
            temp = np.zeros(41)
            temp[20] = 1
            design_filter = temp - np.array(signal.firwin(41, [limit1, limit2], window=extra))
        elif filter_type == "Band-reject":
            design_filter = signal.firwin(41, [limit1, limit2], window=extra)

        self.y_processed = signal.convolve(self.y_original, design_filter, mode='same')

        w1, h1 = signal.freqz(design_filter)

        result = FilterResponseDialog.show_dialog(parent=self, w1=w1, h1=h1)

        if result:
            self.show_processed_data()

    def on_iir_filter(self, filter_type, limit1, limit2, extra, max_ripple, min_attenuation):
        if filter_type == "Low-pass":
            b, a = signal.iirfilter(4, limit1, rp=int(max_ripple), rs=int(min_attenuation), btype='lowpass',
                                    ftype=extra)
        elif filter_type == "High-pass":
            b, a = signal.iirfilter(4, limit1, rp=int(max_ripple), rs=int(min_attenuation), btype='highpass',
                                    ftype=extra)
        elif filter_type == "Band-pass":
            b, a = signal.iirfilter(4, [limit1, limit2], rp=int(max_ripple), rs=int(min_attenuation), btype='bandpass',
                                    ftype=extra)
        elif filter_type == "Band-reject":
            b, a = signal.iirfilter(4, [limit1, limit2], rp=int(max_ripple), rs=int(min_attenuation), btype='bandstop',
                                    ftype=extra)

        self.y_processed = signal.lfilter(b, a, self.y_original)

        w1, h1 = signal.freqz(b, a)

        result = FilterResponseDialog.show_dialog(parent=self, w1=w1, h1=h1)

        if result:
            self.show_processed_data()

    '''
        Audio controls
    '''

    def on_play(self):
        print("on_play")

        if len(self.y_processed) > 0:
            data2 = np.asarray(self.y_processed)
            sd.play(data2, self.sampling_rate)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Upload sound file")
            msg.setInformativeText("First you should upload and process sound file to play")
            msg.setWindowTitle("Error")
            msg.exec_()

    def on_stop(self):
        sd.stop()

    def on_play_orig(self):
        print("on_play_orig")

        if len(self.y_original) > 0:
            data = np.asarray(self.y_original)
            sd.play(data, self.sampling_rate)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Upload sound file")
            msg.setInformativeText("First you should add sound file to play")
            msg.setWindowTitle("Error")
            msg.exec_()

    '''
        Signal plots
    '''

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

        self.m_series_3.clear()
        self.m_series_4.clear()

    def show_processed_data(self):
        # Time domain
        y_data_scaled = np.interp(self.y_processed, (self.y_processed.min(), self.y_processed.max()), (-10, +10))

        points_3 = []

        sample_size = len(self.y_processed)
        x_data = np.linspace(0., 100., sample_size)

        for k in range(len(y_data_scaled)):
            points_3.append(QPointF(x_data[k], y_data_scaled[k]))

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
