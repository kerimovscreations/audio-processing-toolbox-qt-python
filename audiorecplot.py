from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtMultimedia import (QAudioDeviceInfo, QAudioInput, QAudioFormat)
from PyQt5.QtWidgets import (QWidget, QVBoxLayout)
from PyQt5.QtCore import QIODevice

from xyseriesiodevice import XYSeriesIODevice


class AudioRecPlot(QWidget):

    def __init__(self):
        super().__init__()

        self.m_chart = QChart()

        chart_view = QChartView(self.m_chart)
        chart_view.setMinimumSize(800, 600)

        self.m_series = QLineSeries()
        self.m_chart.addSeries(self.m_series)

        axis_x = QValueAxis()
        axis_x.setRange(0, 2000)
        axis_x.setLabelFormat("%g")
        axis_x.setTitleText("Samples")

        axis_y = QValueAxis()
        axis_y.setRange(-1, 1)
        axis_y.setTitleText("Audio level")

        self.m_chart.setAxisX(axis_x, self.m_series)
        self.m_chart.setAxisY(axis_y, self.m_series)
        self.m_chart.setTitle("Data from the microphone")

        main_layout = QVBoxLayout()
        main_layout.addWidget(chart_view)
        self.setLayout(main_layout)

        format_audio = QAudioFormat()
        format_audio.setSampleRate(48000)
        format_audio.setChannelCount(1)
        format_audio.setSampleSize(8)
        format_audio.setCodec("audio/pcm")
        format_audio.setByteOrder(QAudioFormat.LittleEndian)
        format_audio.setSampleType(QAudioFormat.UnSignedInt)

        input_devices = QAudioDeviceInfo.defaultInputDevice()
        self.m_audio_input = QAudioInput(input_devices, format_audio)

        self.m_device = XYSeriesIODevice(self.m_series)
        self.m_device.open(QIODevice.WriteOnly)

        self.m_audio_input.start(self.m_device)

        self.init_ui()

    def init_ui(self):
        self.show()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.m_audio_input.stop()
        self.m_device.close()
