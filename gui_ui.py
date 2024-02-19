# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLayout,
    QMainWindow, QPushButton, QSizePolicy, QStatusBar,
    QTabWidget, QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1412, 838)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 1401, 821))
        self.maintab = QWidget()
        self.maintab.setObjectName(u"maintab")
        self.layoutWidget = QWidget(self.maintab)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(280, 0, 839, 789))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.connect_button = QPushButton(self.layoutWidget)
        self.connect_button.setObjectName(u"connect_button")

        self.verticalLayout_2.addWidget(self.connect_button)

        self.run_button = QPushButton(self.layoutWidget)
        self.run_button.setObjectName(u"run_button")

        self.verticalLayout_2.addWidget(self.run_button)

        self.stop_button = QPushButton(self.layoutWidget)
        self.stop_button.setObjectName(u"stop_button")

        self.verticalLayout_2.addWidget(self.stop_button)

        self.main_map = QVBoxLayout()
        self.main_map.setObjectName(u"main_map")
        self.main_map.setSizeConstraint(QLayout.SetMaximumSize)

        self.verticalLayout_2.addLayout(self.main_map)

        self.tabWidget.addTab(self.maintab, "")
        self.devtab = QWidget()
        self.devtab.setObjectName(u"devtab")
        self.gridLayoutWidget_2 = QWidget(self.devtab)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(10, 0, 1381, 791))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.gridLayoutWidget_2)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.magnet_plot = QVBoxLayout()
        self.magnet_plot.setObjectName(u"magnet_plot")

        self.gridLayout_2.addLayout(self.magnet_plot, 3, 0, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 0, 1, 1, 1)

        self.label_4 = QLabel(self.gridLayoutWidget_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 2, 1, 1, 1)

        self.distance_plot = QVBoxLayout()
        self.distance_plot.setObjectName(u"distance_plot")

        self.gridLayout_2.addLayout(self.distance_plot, 3, 1, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)

        self.robot_pos_plot = QVBoxLayout()
        self.robot_pos_plot.setObjectName(u"robot_pos_plot")

        self.gridLayout_2.addLayout(self.robot_pos_plot, 1, 1, 1, 1)

        self.sub_map = QVBoxLayout()
        self.sub_map.setObjectName(u"sub_map")

        self.gridLayout_2.addLayout(self.sub_map, 1, 0, 1, 1)

        self.label_5 = QLabel(self.gridLayoutWidget_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 0, 2, 1, 1)

        self.x_plot = QVBoxLayout()
        self.x_plot.setObjectName(u"x_plot")

        self.gridLayout_2.addLayout(self.x_plot, 1, 2, 1, 1)

        self.label_8 = QLabel(self.gridLayoutWidget_2)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 2, 2, 1, 1)

        self.y_plot = QVBoxLayout()
        self.y_plot.setObjectName(u"y_plot")

        self.gridLayout_2.addLayout(self.y_plot, 3, 2, 1, 1)

        self.tabWidget.addTab(self.devtab, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayoutWidget_7 = QWidget(self.tab)
        self.verticalLayoutWidget_7.setObjectName(u"verticalLayoutWidget_7")
        self.verticalLayoutWidget_7.setGeometry(QRect(10, 0, 1371, 791))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget_7)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.verticalLayoutWidget_7)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout.addWidget(self.label_6)

        self.textEdit = QTextEdit(self.verticalLayoutWidget_7)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout.addWidget(self.textEdit)

        self.label_7 = QLabel(self.verticalLayoutWidget_7)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout.addWidget(self.label_7)

        self.textEdit_2 = QTextEdit(self.verticalLayoutWidget_7)
        self.textEdit_2.setObjectName(u"textEdit_2")

        self.verticalLayout.addWidget(self.textEdit_2)

        self.tabWidget.addTab(self.tab, "")
        # MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        # MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Visualising App", None))
        self.connect_button.setText(QCoreApplication.translate("MainWindow", u"Connect to robot", None))
        self.run_button.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.stop_button.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.maintab), QCoreApplication.translate("MainWindow", u"Main", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Wall, mm*mm", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Robot, mm*mm", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Distance, mm", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Heading, degrees", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"X, mm", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Y, mm", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.devtab), QCoreApplication.translate("MainWindow", u"Variables plots", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Received data", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Sent data", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Logs", None))
    # retranslateUi

