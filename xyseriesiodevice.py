from PyQt5.QtCore import QIODevice, QPointF


class XYSeriesIODevice(QIODevice):
    def __init__(self, series):
        super().__init__()

        self.m_series = series

    def writeData(self, bytes):
        range_temp = 2000
        old_points = self.m_series.pointsVector()
        points = []
        resolution = 4

        if len(old_points) < range_temp:
            points = self.m_series.pointsVector()
        else:
            for i in range(int(len(bytes) / resolution), len(old_points)):
                points.append(QPointF(i - len(bytes) / resolution, old_points[i].y()))

        size = len(points)
        for k in range(int(len(bytes) / resolution)):
            points.append(QPointF(k + size, (bytes[resolution * k] - 128) / 128.0))

        self.m_series.replace(points)

        return len(bytes)
