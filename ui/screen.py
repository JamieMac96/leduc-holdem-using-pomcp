# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


# Auto generated code from Qt Designer to define UI template
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1050, 690)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.fold_radio = QtWidgets.QRadioButton(self.centralwidget)
        self.fold_radio.setGeometry(QtCore.QRect(20, 440, 116, 22))
        self.fold_radio.setObjectName("fold_radio")
        self.call_radio = QtWidgets.QRadioButton(self.centralwidget)
        self.call_radio.setGeometry(QtCore.QRect(20, 490, 116, 22))
        self.call_radio.setObjectName("call_radio")
        self.bet_radio = QtWidgets.QRadioButton(self.centralwidget)
        self.bet_radio.setGeometry(QtCore.QRect(20, 540, 116, 22))
        self.bet_radio.setObjectName("bet_radio")
        self.raise_radio = QtWidgets.QRadioButton(self.centralwidget)
        self.raise_radio.setGeometry(QtCore.QRect(20, 590, 116, 22))
        self.raise_radio.setObjectName("raise_radio")
        self.take_action_button = QtWidgets.QPushButton(self.centralwidget)
        self.take_action_button.setGeometry(QtCore.QRect(160, 590, 98, 27))
        self.take_action_button.setObjectName("take_action_button")
        self.new_game_button = QtWidgets.QPushButton(self.centralwidget)
        self.new_game_button.setGeometry(QtCore.QRect(360, 590, 98, 27))
        self.new_game_button.setObjectName("new_game_button")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(-10, 10, 901, 391))
        self.graphicsView.setStyleSheet("background: url(game_table.png)")
        self.graphicsView.setObjectName("graphicsView")
        self.textbox = QtWidgets.QTextBrowser(self.centralwidget)
        self.textbox.setGeometry(QtCore.QRect(890, 10, 161, 391))
        self.textbox.setObjectName("textbox")
        self.total_winnings = QtWidgets.QTextBrowser(self.centralwidget)
        self.total_winnings.setGeometry(QtCore.QRect(720, 590, 170, 27))
        self.total_winnings.setObjectName("total_winnings")
        self.player_card = QtWidgets.QLabel(self.centralwidget)
        self.player_card.setGeometry(QtCore.QRect(410, 280, 71, 91))
        self.player_card.setObjectName("player_card")
        self.opponent_card = QtWidgets.QLabel(self.centralwidget)
        self.opponent_card.setGeometry(QtCore.QRect(410, 50, 66, 81))
        self.opponent_card.setObjectName("opponent_card")
        self.public_card = QtWidgets.QLabel(self.centralwidget)
        self.public_card.setGeometry(QtCore.QRect(410, 165, 66, 81))
        self.public_card.setObjectName("public_card")
        self.pot = QtWidgets.QTextBrowser(self.centralwidget)
        self.pot.setGeometry(QtCore.QRect(530, 190, 201, 51))
        self.pot.setStyleSheet("background-color: rgb(0,153,0);\n"
"border:none;")
        self.pot.setObjectName("pot")
        self.pot.setText("0")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1050, 25))
        self.menubar.setObjectName("menubar")
        self.menuFIle = QtWidgets.QMenu(self.menubar)
        self.menuFIle.setObjectName("menuFIle")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.toolBar_2 = QtWidgets.QToolBar(MainWindow)
        self.toolBar_2.setObjectName("toolBar_2")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_2)
        self.toolBar_3 = QtWidgets.QToolBar(MainWindow)
        self.toolBar_3.setObjectName("toolBar_3")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_3)
        self.toolBar_4 = QtWidgets.QToolBar(MainWindow)
        self.toolBar_4.setObjectName("toolBar_4")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_4)
        self.toolBar_5 = QtWidgets.QToolBar(MainWindow)
        self.toolBar_5.setObjectName("toolBar_5")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_5)
        self.toolBar_6 = QtWidgets.QToolBar(MainWindow)
        self.toolBar_6.setObjectName("toolBar_6")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_6)
        self.toolBar_7 = QtWidgets.QToolBar(MainWindow)
        self.toolBar_7.setObjectName("toolBar_7")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_7)
        self.toolBar_8 = QtWidgets.QToolBar(MainWindow)
        self.toolBar_8.setObjectName("toolBar_8")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_8)
        self.actionNew_Game = QtWidgets.QAction(MainWindow)
        self.actionNew_Game.setObjectName("actionNew_Game")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFIle.addAction(self.actionNew_Game)
        self.menuFIle.addAction(self.actionExit)
        self.menubar.addAction(self.menuFIle.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.fold_radio.setText(_translate("MainWindow", "fold"))
        self.call_radio.setText(_translate("MainWindow", "call"))
        self.bet_radio.setText(_translate("MainWindow", "bet"))
        self.raise_radio.setText(_translate("MainWindow", "raise"))
        self.take_action_button.setText(_translate("MainWindow", "Take Action"))
        self.new_game_button.setText(_translate("MainWindow", "New Round"))
        self.total_winnings.setText("Total Winnings: 0")
        self.textbox.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>"))
        self.player_card.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/my_cards/Ah.svg\"/></p></body></html>"))
        self.opponent_card.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/my_cards/back.png\"/></p></body></html>"))
        self.menuFIle.setTitle(_translate("MainWindow", "Game"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.toolBar_2.setWindowTitle(_translate("MainWindow", "toolBar_2"))
        self.toolBar_3.setWindowTitle(_translate("MainWindow", "toolBar_3"))
        self.toolBar_4.setWindowTitle(_translate("MainWindow", "toolBar_4"))
        self.toolBar_5.setWindowTitle(_translate("MainWindow", "toolBar_5"))
        self.toolBar_6.setWindowTitle(_translate("MainWindow", "toolBar_6"))
        self.toolBar_7.setWindowTitle(_translate("MainWindow", "toolBar_7"))
        self.toolBar_8.setWindowTitle(_translate("MainWindow", "toolBar_8"))
        self.actionNew_Game.setText(_translate("MainWindow", "New Game"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.pot.setFontPointSize(14)

import cards_resource
import sys

