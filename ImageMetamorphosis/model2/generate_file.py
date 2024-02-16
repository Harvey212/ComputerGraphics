from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(360, 280)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.WrapFeatureLine = QtWidgets.QPushButton(self.centralwidget)
        self.WrapFeatureLine.setGeometry(QtCore.QRect(110, 50, 140, 30))
        self.WrapFeatureLine.setObjectName("WrapFeatureLine")
        self.WrapImage = QtWidgets.QPushButton(self.centralwidget)
        self.WrapImage.setGeometry(QtCore.QRect(110, 100, 140, 30))
        self.WrapImage.setObjectName("WrapImage")
        self.Animation = QtWidgets.QPushButton(self.centralwidget)
        self.Animation.setGeometry(QtCore.QRect(110, 150, 140, 30))
        self.Animation.setObjectName("Animation")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 360, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.WrapFeatureLine.setText(_translate("MainWindow", "WrapFeatureLine"))
        self.WrapImage.setText(_translate("MainWindow", "WrapImage"))
        self.Animation.setText(_translate("MainWindow", "Animation"))
