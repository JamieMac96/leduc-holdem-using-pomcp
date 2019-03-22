# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created: Fri Mar 22 22:47:16 2019
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1050, 690)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.fold_radio = QtGui.QRadioButton(self.centralwidget)
        self.fold_radio.setGeometry(QtCore.QRect(20, 440, 116, 22))
        self.fold_radio.setObjectName(_fromUtf8("fold_radio"))
        self.call_radio = QtGui.QRadioButton(self.centralwidget)
        self.call_radio.setGeometry(QtCore.QRect(20, 490, 116, 22))
        self.call_radio.setObjectName(_fromUtf8("call_radio"))
        self.bet_radio = QtGui.QRadioButton(self.centralwidget)
        self.bet_radio.setGeometry(QtCore.QRect(20, 540, 116, 22))
        self.bet_radio.setObjectName(_fromUtf8("bet_radio"))
        self.raise_radio = QtGui.QRadioButton(self.centralwidget)
        self.raise_radio.setGeometry(QtCore.QRect(20, 590, 116, 22))
        self.raise_radio.setObjectName(_fromUtf8("raise_radio"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(160, 590, 98, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(-10, 10, 901, 391))
        self.graphicsView.setStyleSheet(_fromUtf8("background: url(/home/jamie/Desktop/Y4S2/product_FYP/leduc-holdem-using-pomcp/ui/game_table.png)"))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.textBrowser = QtGui.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(890, 10, 161, 391))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.player_card = QtGui.QGraphicsView(self.centralwidget)
        self.player_card.setGeometry(QtCore.QRect(420, 280, 171, 0))
        self.player_card.setMinimumSize(QtCore.QSize(171, 0))
        self.player_card.setMaximumSize(QtCore.QSize(171, 241))
        self.player_card.setStyleSheet(_fromUtf8("background: url(/home/jamie/Desktop/Y4S2/product_FYP/leduc-holdem-using-pomcp/ui/cards/AH.svg)"))
        self.player_card.setObjectName(_fromUtf8("player_card"))
        self.player_card_2 = QtGui.QLabel(self.centralwidget)
        self.player_card_2.setGeometry(QtCore.QRect(410, 280, 71, 91))
        self.player_card_2.setObjectName(_fromUtf8("player_card_2"))
        self.opponent_card = QtGui.QLabel(self.centralwidget)
        self.opponent_card.setGeometry(QtCore.QRect(410, 50, 66, 81))
        self.opponent_card.setObjectName(_fromUtf8("opponent_card"))
        self.textBrowser_2 = QtGui.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(530, 190, 201, 51))
        self.textBrowser_2.setStyleSheet(_fromUtf8("background-color: rgb(0,153,0);\n"
"border:none;"))
        self.textBrowser_2.setObjectName(_fromUtf8("textBrowser_2"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1050, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFIle = QtGui.QMenu(self.menubar)
        self.menuFIle.setObjectName(_fromUtf8("menuFIle"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.toolBar_2 = QtGui.QToolBar(MainWindow)
        self.toolBar_2.setObjectName(_fromUtf8("toolBar_2"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_2)
        self.toolBar_3 = QtGui.QToolBar(MainWindow)
        self.toolBar_3.setObjectName(_fromUtf8("toolBar_3"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_3)
        self.toolBar_4 = QtGui.QToolBar(MainWindow)
        self.toolBar_4.setObjectName(_fromUtf8("toolBar_4"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_4)
        self.toolBar_5 = QtGui.QToolBar(MainWindow)
        self.toolBar_5.setObjectName(_fromUtf8("toolBar_5"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_5)
        self.toolBar_6 = QtGui.QToolBar(MainWindow)
        self.toolBar_6.setObjectName(_fromUtf8("toolBar_6"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_6)
        self.toolBar_7 = QtGui.QToolBar(MainWindow)
        self.toolBar_7.setObjectName(_fromUtf8("toolBar_7"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_7)
        self.toolBar_8 = QtGui.QToolBar(MainWindow)
        self.toolBar_8.setObjectName(_fromUtf8("toolBar_8"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_8)
        self.actionNew_Game = QtGui.QAction(MainWindow)
        self.actionNew_Game.setObjectName(_fromUtf8("actionNew_Game"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuFIle.addAction(self.actionNew_Game)
        self.menuFIle.addAction(self.actionExit)
        self.menubar.addAction(self.menuFIle.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.fold_radio.setText(_translate("MainWindow", "fold", None))
        self.call_radio.setText(_translate("MainWindow", "call", None))
        self.bet_radio.setText(_translate("MainWindow", "bet", None))
        self.raise_radio.setText(_translate("MainWindow", "raise", None))
        self.pushButton.setText(_translate("MainWindow", "Take Action", None))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This is some text</p></body></html>", None))
        self.player_card_2.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/my_cards/Ah.svg\"/></p></body></html>", None))
        self.opponent_card.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/my_cards/back.png\"/></p></body></html>", None))
        self.menuFIle.setTitle(_translate("MainWindow", "Game", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.toolBar_2.setWindowTitle(_translate("MainWindow", "toolBar_2", None))
        self.toolBar_3.setWindowTitle(_translate("MainWindow", "toolBar_3", None))
        self.toolBar_4.setWindowTitle(_translate("MainWindow", "toolBar_4", None))
        self.toolBar_5.setWindowTitle(_translate("MainWindow", "toolBar_5", None))
        self.toolBar_6.setWindowTitle(_translate("MainWindow", "toolBar_6", None))
        self.toolBar_7.setWindowTitle(_translate("MainWindow", "toolBar_7", None))
        self.toolBar_8.setWindowTitle(_translate("MainWindow", "toolBar_8", None))
        self.actionNew_Game.setText(_translate("MainWindow", "New Game", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))

import cards_resource

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

