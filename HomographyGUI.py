# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HomographyGUI.ui'
#
# Created: Thu Dec  1 14:38:08 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(941, 697)
        self.srcbtn = QtGui.QPushButton(Form)
        self.srcbtn.setGeometry(QtCore.QRect(20, 10, 111, 27))
        self.srcbtn.setObjectName("srcbtn")
        self.tarbtn = QtGui.QPushButton(Form)
        self.tarbtn.setGeometry(QtCore.QRect(480, 10, 111, 27))
        self.tarbtn.setObjectName("tarbtn")
        self.srcimg = QtGui.QGraphicsView(Form)
        self.srcimg.setGeometry(QtCore.QRect(20, 50, 431, 471))
        self.srcimg.setObjectName("srcimg")
        self.acqbtn = QtGui.QPushButton(Form)
        self.acqbtn.setGeometry(QtCore.QRect(480, 540, 111, 27))
        self.acqbtn.setObjectName("acqbtn")
        self.co1 = QtGui.QLineEdit(Form)
        self.co1.setGeometry(QtCore.QRect(600, 540, 131, 27))
        self.co1.setObjectName("co1")
        self.effectlbl = QtGui.QLabel(Form)
        self.effectlbl.setGeometry(QtCore.QRect(540, 620, 62, 17))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.effectlbl.setFont(font)
        self.effectlbl.setObjectName("effectlbl")
        self.tarimg = QtGui.QGraphicsView(Form)
        self.tarimg.setGeometry(QtCore.QRect(480, 50, 431, 471))
        self.tarimg.setObjectName("tarimg")
        self.co2 = QtGui.QLineEdit(Form)
        self.co2.setGeometry(QtCore.QRect(780, 540, 131, 27))
        self.co2.setObjectName("co2")
        self.co3 = QtGui.QLineEdit(Form)
        self.co3.setGeometry(QtCore.QRect(600, 580, 131, 27))
        self.co3.setObjectName("co3")
        self.co4 = QtGui.QLineEdit(Form)
        self.co4.setGeometry(QtCore.QRect(780, 580, 131, 27))
        self.co4.setObjectName("co4")
        self.tfbtn = QtGui.QPushButton(Form)
        self.tfbtn.setGeometry(QtCore.QRect(480, 650, 111, 27))
        self.tfbtn.setObjectName("tfbtn")
        self.rstbtn = QtGui.QPushButton(Form)
        self.rstbtn.setGeometry(QtCore.QRect(620, 650, 111, 27))
        self.rstbtn.setObjectName("rstbtn")
        self.savebtn = QtGui.QPushButton(Form)
        self.savebtn.setGeometry(QtCore.QRect(800, 650, 111, 27))
        self.savebtn.setObjectName("savebtn")
        self.effectbox = QtGui.QComboBox(Form)
        self.effectbox.setGeometry(QtCore.QRect(600, 620, 311, 27))
        self.effectbox.setObjectName("effectbox")
        self.effectbox.addItem("")
        self.effectbox.addItem("")
        self.effectbox.addItem("")
        self.effectbox.addItem("")
        self.effectbox.addItem("")
        self.effectbox.addItem("")
        self.effectbox.addItem("")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.srcbtn.setText(QtGui.QApplication.translate("Form", "Load Source...", None, QtGui.QApplication.UnicodeUTF8))
        self.tarbtn.setText(QtGui.QApplication.translate("Form", "Load Target...", None, QtGui.QApplication.UnicodeUTF8))
        self.acqbtn.setText(QtGui.QApplication.translate("Form", "Acquire Points", None, QtGui.QApplication.UnicodeUTF8))
        self.effectlbl.setText(QtGui.QApplication.translate("Form", "Effect", None, QtGui.QApplication.UnicodeUTF8))
        self.tfbtn.setText(QtGui.QApplication.translate("Form", "Transform", None, QtGui.QApplication.UnicodeUTF8))
        self.rstbtn.setText(QtGui.QApplication.translate("Form", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.savebtn.setText(QtGui.QApplication.translate("Form", "Save...", None, QtGui.QApplication.UnicodeUTF8))
        self.effectbox.setItemText(0, QtGui.QApplication.translate("Form", "Nothing", None, QtGui.QApplication.UnicodeUTF8))
        self.effectbox.setItemText(1, QtGui.QApplication.translate("Form", "Rotate 90", None, QtGui.QApplication.UnicodeUTF8))
        self.effectbox.setItemText(2, QtGui.QApplication.translate("Form", "Rotate 180", None, QtGui.QApplication.UnicodeUTF8))
        self.effectbox.setItemText(3, QtGui.QApplication.translate("Form", "Rotate 270", None, QtGui.QApplication.UnicodeUTF8))
        self.effectbox.setItemText(4, QtGui.QApplication.translate("Form", "Flip Horizontally", None, QtGui.QApplication.UnicodeUTF8))
        self.effectbox.setItemText(5, QtGui.QApplication.translate("Form", "Flip Vertically", None, QtGui.QApplication.UnicodeUTF8))
        self.effectbox.setItemText(6, QtGui.QApplication.translate("Form", "Transpose", None, QtGui.QApplication.UnicodeUTF8))

