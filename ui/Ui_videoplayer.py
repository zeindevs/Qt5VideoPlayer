# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\zeindevs\Documents\ZEN\CODING\python-scripts-tools\videoplayer\ui\videoplayer.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VideoPlayer(object):
    def setupUi(self, VideoPlayer):
        VideoPlayer.setObjectName("VideoPlayer")
        VideoPlayer.resize(400, 347)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(VideoPlayer.sizePolicy().hasHeightForWidth())
        VideoPlayer.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(VideoPlayer)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.videoLayout = QtWidgets.QVBoxLayout()
        self.videoLayout.setObjectName("videoLayout")
        self.gridLayout.addLayout(self.videoLayout, 0, 0, 1, 1)

        self.retranslateUi(VideoPlayer)
        QtCore.QMetaObject.connectSlotsByName(VideoPlayer)

    def retranslateUi(self, VideoPlayer):
        _translate = QtCore.QCoreApplication.translate
        VideoPlayer.setWindowTitle(_translate("VideoPlayer", "Form"))
