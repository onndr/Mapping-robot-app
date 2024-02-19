import datetime


class DataBlock():
    def __init__(self, *args):
        self.timestamp = datetime.datetime.now()

    def __str__(self):
        return f"Data block [datatime: {self.timestamp}]"


class MeasurementsDataBlock(DataBlock):
    def __init__(self, x, y, rotation, distance):
        super().__init__()
        self.x, self.y, self.rotation, self.distance = x, y, rotation, distance

    def __str__(self):
        return (
            f"Data block:\
              [datatime: {self.timestamp},\
               x: {self.x:.3f}, y: {self.y:.3f},\
               rotation: {self.rotation:.3f},\
               distance: {self.distance:.3f}]"
        )