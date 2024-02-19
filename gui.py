import argparse
import sys
import random
from time import sleep
import numpy as np
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QWidget, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import pyplot as plt, animation as animation
from matplotlib.ticker import FuncFormatter
from communication.data_processing import ProcessedDataSubscriber

from bt_socket_mock import BluetoothSocketMock
from gui_ui import Ui_MainWindow
from communication.connection import *
from communication.data_processing import *
from communication.commands_processing import *
from calc import *

ROBOT_BT_MAC = "00:13:EF:01:11:98"


class BluetoothSub(ProcessedDataSubscriber):
    def __init__(self, update_callbacks):
        self.wall_xs = []
        self.wall_ys = []
        self.robot_xs = []
        self.robot_ys = []
        self.distances = []
        self.magnet_measurements = []
        self.received_blocks = []
        self.updates = 0
        self.update_cbs = update_callbacks

    def update(self, data_block: MeasurementsDataBlock):
        math_angle = normalize_angle(data_block.rotation)
        heading_angle = math_to_heading(math_angle)
        distance_mm = data_block.distance
        robot_x = 10 * data_block.x
        robot_y = 10 * data_block.y
        wall_x, wall_y = wall_point(robot_x, robot_y, math_angle, distance_mm)
        self.distances.append(distance_mm)
        if 100 <= distance_mm <= 500:
            self.wall_xs.append(wall_x)
            self.wall_ys.append(wall_y)
        self.robot_xs.append(robot_x)
        self.robot_ys.append(robot_y)
        self.magnet_measurements.append(math.degrees(math_angle))
        self.received_blocks.append(data_block)
        self.updates += 1
        for cb in self.update_cbs:
            cb()


class MyForm(QtWidgets.QWidget):
    def __init__(self, bt_mac_address="", points_on_plot=30):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.run_button.clicked.connect(self.run_action)
        self.ui.stop_button.clicked.connect(self.stop_action)
        self.ui.connect_button.clicked.connect(self.connect_button_pressed)
        self.ui.run_button.setEnabled(False)
        self.ui.stop_button.setEnabled(False)

        self.create_main_plot()
        self.create_sub_plot()
        self.create_robot_pos_plot()
        self.create_magnet_plot()
        self.create_distance_plot()
        self.create_x_plot()
        self.create_y_plot()

        self.points_on_plot = points_on_plot
        self.bt_mac_address = bt_mac_address

        if self.bt_mac_address:
            self.bt = BluetoothSocket()
        else:
            self.bt = BluetoothSocketMock()

        self.sub = BluetoothSub(
            [lambda: self.update_plot(), lambda: self.print_received_block()]
        )
        self.processor = DataProcessor(10)
        self.cmd_processor = CommandProcessor()
        self.bt.subscribe(self.processor)
        self.processor.subscribe(self.sub)

    def init_bt_connection(self):
        port = 1
        if self.bt_mac_address:
            self.bt.connect(self.bt_mac_address, port)
        else:
            self.bt.connect(ROBOT_BT_MAC, port)

    def create_x_plot(self):
        figure = plt.figure()
        self.x_canvas = FigureCanvas(figure)
        self.x_plot = figure.add_subplot(111)

        self.x_canvas.setFixedSize(350, 350)

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.x_canvas)
        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)

        self.ui.x_plot.addWidget(container)

    def create_y_plot(self):
        figure = plt.figure()
        self.y_canvas = FigureCanvas(figure)
        self.y_plot = figure.add_subplot(111)

        self.y_canvas.setFixedSize(350, 350)

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.y_canvas)
        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)

        self.ui.y_plot.addWidget(container)

    def create_main_plot(self):
        figure = plt.figure()
        self.main_canvas = FigureCanvas(figure)
        self.main_plot = figure.add_subplot(111)

        self.main_canvas.setFixedSize(700, 700)

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.main_canvas)
        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)

        self.ui.main_map.addWidget(container)

    def create_sub_plot(self):
        figure = plt.figure()
        self.sub_canvas = FigureCanvas(figure)
        self.sub_plot = figure.add_subplot(111)

        self.sub_canvas.setFixedSize(350, 350)

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.sub_canvas)
        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)

        self.ui.sub_map.addWidget(container)

    def create_robot_pos_plot(self):
        figure = plt.figure()
        self.pos_canvas = FigureCanvas(figure)
        self.pos_plot = figure.add_subplot(111)
        self.pos_plot.set_aspect("equal")

        self.pos_canvas.setFixedSize(350, 350)

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.pos_canvas)
        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)

        self.ui.robot_pos_plot.addWidget(container)

    def create_magnet_plot(self):
        figure = plt.figure()
        self.magnet_canvas = FigureCanvas(figure)
        self.magnet_plot = figure.add_subplot(111)
        self.magnet_plot.set_ylim(-180, 180)

        self.magnet_canvas.setFixedSize(350, 350)

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.magnet_canvas)
        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)

        self.ui.magnet_plot.addWidget(container)

    def create_distance_plot(self):
        figure = plt.figure()
        self.distance_canvas = FigureCanvas(figure)
        self.distance_plot = figure.add_subplot(111)

        self.distance_canvas.setFixedSize(350, 350)

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.distance_canvas)
        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)

        self.ui.distance_plot.addWidget(container)

    def _update_main_plot(self, offset=100):
        self.main_plot.clear()
        max_value = (
            max(
                max(self.sub.wall_xs, default=0),
                max(self.sub.robot_xs, default=0),
                max(self.sub.wall_ys, default=0),
                max(self.sub.robot_ys, default=0),
            )
            + offset
        )
        min_value = (
            min(
                min(self.sub.wall_xs, default=0),
                min(self.sub.robot_xs, default=0),
                min(self.sub.wall_ys, default=0),
                min(self.sub.robot_ys, default=0),
            )
            - offset
        )
        self.main_plot.set_xlim(min_value, max_value)
        self.main_plot.set_ylim(min_value, max_value)
        self.main_plot.plot(
            self.sub.wall_xs, self.sub.wall_ys, "o-", color="black", label="wall, mm*mm"
        )
        self.main_plot.plot(
            self.sub.robot_xs,
            self.sub.robot_ys,
            "o-",
            color="blue",
            label="robot, mm*mm",
        )
        self.main_plot.legend()
        self.main_canvas.draw()

    def _update_sub_plot(self, offset=100):
        self.sub_plot.clear()
        max_value = (
            max(max(self.sub.wall_xs, default=0), max(self.sub.wall_ys, default=0))
            + offset
        )
        min_value = (
            min(min(self.sub.wall_xs, default=0), min(self.sub.wall_ys, default=0))
            - offset
        )
        self.sub_plot.set_xlim(min_value, max_value)
        self.sub_plot.set_ylim(min_value, max_value)
        self.sub_plot.plot(self.sub.wall_xs, self.sub.wall_ys, "o-", color="black")
        self.sub_canvas.draw()

    def _update_pos_plor(self, offset=100):
        self.pos_plot.clear()
        max_value = (
            max(max(self.sub.robot_xs, default=0), max(self.sub.robot_ys, default=0))
            + offset
        )
        min_value = (
            min(min(self.sub.robot_xs, default=0), min(self.sub.robot_ys, default=0))
            - offset
        )
        self.pos_plot.set_xlim(min_value, max_value)
        self.pos_plot.set_ylim(min_value, max_value)
        self.pos_plot.plot(self.sub.robot_xs, self.sub.robot_ys, "o-", color="blue")
        self.pos_canvas.draw()

    def _update_magnet_plot(self):
        self.magnet_plot.clear()
        self.magnet_plot.set_ylim(-180, 180)
        self.magnet_plot.set_yticks(np.arange(-180, 180 + 45, step=45))
        self.magnet_plot.plot(
            self.sub.magnet_measurements[-self.points_on_plot :], "o-", color="red"
        )
        self.magnet_canvas.draw()

    def _update_distance_plot(self):
        self.distance_plot.clear()
        self.distance_plot.plot(
            self.sub.distances[-self.points_on_plot :], "o-", color="green"
        )
        self.distance_canvas.draw()

    def _update_x_plot(self):
        self.x_plot.clear()
        self.x_plot.plot(
            self.sub.wall_xs[-self.points_on_plot :], "o-", color="black", label="wall"
        )
        self.x_plot.plot(
            self.sub.robot_xs[-self.points_on_plot :], "o-", color="blue", label="robot"
        )
        self.x_plot.legend()
        self.x_canvas.draw()

    def _update_y_plot(self):
        self.y_plot.clear()
        self.y_plot.plot(
            self.sub.wall_ys[-self.points_on_plot :], "o-", color="black", label="wall"
        )
        self.y_plot.plot(
            self.sub.robot_ys[-self.points_on_plot :], "o-", color="blue", label="robot"
        )
        self.y_plot.legend()
        self.y_canvas.draw()

    def update_plot(self):
        self._update_main_plot()
        self._update_sub_plot()
        self._update_pos_plor()
        self._update_magnet_plot()
        self._update_distance_plot()
        self._update_x_plot()
        self._update_y_plot()

    def print_received_block(self):
        self.ui.textEdit.append("Received: " + str(self.sub.received_blocks[-1]))

    def print_sent_blocks(self):
        self.ui.textEdit_2.append("Sent: " + str(self.bt.sent_data[-1]))

    def connect_button_pressed(self):
        self.init_bt_connection()
        self.ui.connect_button.setEnabled(False)
        self.ui.run_button.setEnabled(True)
        self.ui.stop_button.setEnabled(False)

    def run_action(self):
        self.ui.run_button.setEnabled(False)
        self.ui.stop_button.setEnabled(True)
        self.cmd_processor.handle_command(self.bt, "run")
        self.print_sent_blocks()
        self.bt.run_recv_thread()

    def stop_action(self):
        self.ui.stop_button.setEnabled(False)
        self.ui.run_button.setEnabled(True)
        self.cmd_processor.handle_command(self.bt, "stop")
        self.print_sent_blocks()
        self.bt.stop_recv_thread()


def main():
    parser = argparse.ArgumentParser(description="Process Bluetooth MAC address.")
    parser.add_argument(
        "--mac_address", type=str, default="", help="Robot's Bluetooth MAC address"
    )

    args = parser.parse_args()

    app = QtWidgets.QApplication(sys.argv)
    window = MyForm(args.mac_address)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
