import sys
import re
from PySide.QtCore import *
from PySide.QtGui import *
from HomographyGUI import *
from Homography import *
import scipy.misc
import numpy as np
import os
class HomographyApp(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(HomographyApp, self).__init__(parent)
        self.setupUi(self)

        #initial state
        self.srcimg.setDisabled(True)
        self.tarimg.setDisabled(True)
        self.acqbtn.setDisabled(True)
        self.co1.setDisabled(True)
        self.co1.setReadOnly(True)
        self.co2.setDisabled(True)
        self.co2.setReadOnly(True)
        self.co3.setDisabled(True)
        self.co3.setReadOnly(True)
        self.co4.setDisabled(True)
        self.co4.setReadOnly(True)
        self.effectlbl.setDisabled(True)
        self.effectbox.setDisabled(True)
        self.tfbtn.setDisabled(True)
        self.rstbtn.setDisabled(True)
        self.savebtn.setDisabled(True)

        #member variables
        self.flag = False
        self.flagtransform = False
        self.effect = None
        self.sourceimg = None
        self.targetimg = None
        #click the src button or target button
        self.srcbtn.clicked.connect(lambda: self.loadData(1))
        self.tarbtn.clicked.connect(lambda: self.loadData(2,))
        self.acqbtn.clicked.connect(lambda: self.acquirepts())
        self.acqbtn.setCheckable(True)
        self.savebtn.clicked.connect(lambda: self.savefunct())
        self.tfbtn.clicked.connect(lambda: self.transform())
        self.rstbtn.clicked.connect(lambda: self.reset())
        #text box field
        self.pointlist = [self.co1,self.co2, self.co3, self.co4]
        #iterator for textboxes
        self.pointiter = 0
    def reset(self):
        scene = QGraphicsScene()
        pixmap = QPixmap(self.targfilepath)
        pix = scene.addPixmap(pixmap)
        self.tarimg.setDisabled(False)
        self.tarimg.setScene(scene)
        self.tarimg.fitInView(pix,Qt.KeepAspectRatio)
        self.tarimg.show()
        self.targetimg = scipy.misc.imread(self.targfilepath)
        self.readystate()
    def transform(self):
        self.effect = self.effectbox.currentIndex()
        if self.effect == 0:
            self.effect = None
        else:
            self.effect = Effect(self.effect)
        if self.sourceimg.ndim == 2 and self.targetimg.ndim == 2:
            tform = Transformation(self.sourceimg)
        elif self.sourceimg.ndim == 2 and self.targetimg.ndim == 3:
            #tform = Transformation(self.sourceimg)
            tform = np.dstack([self.sourceimg,self.sourceimg, self.sourceimg])
            tform = ColorTransformation(tform)
        elif self.sourceimg.ndim == 3 and self.targetimg.ndim == 2:
            tform = ColorTransformation(self.sourceimg)
            self.targetimg = np.dstack([self.targetimg, self.targetimg, self.targetimg])
        else:
            tform = ColorTransformation(self.sourceimg)
        l1 = []
        for values in self.pointlist:
            temp = values.text().split(',')
            l1.append(temp[0].strip())
            l1.append(temp[1].strip())
        pts = np.array(l1,dtype=np.float64).reshape(4,2)
        tform.setupTransformation(targetPoints=pts,effect=self.effect)
        value = tform.transformImageOnto(self.targetimg)
        scipy.misc.imsave("TestImages/tempimg.png", value)
        scene = QGraphicsScene()
        pixmap = QPixmap("TestImages/tempimg.png")
        pix = scene.addPixmap(pixmap)
        self.tarimg.setScene(scene)
        self.tarimg.fitInView(pix,Qt.KeepAspectRatio)
        self.tarimg.show()
        self.targetimg = scipy.misc.imread("TestImages/tempimg.png")
        os.remove("TestImages/tempimg.png")
        self.transformed()
    def transformed(self):
        self.tarimg.mousePressEvent = QEvent.ignore
        self.tarimg.keyPressEvent = QEvent.ignore
        self.flagtransform = True
        self.acqbtn.setDisabled(True)
        self.co1.setDisabled(True)
        self.co2.setDisabled(True)
        self.co3.setDisabled(True)
        self.co4.setDisabled(True)
    def savefunct(self):
        filePath, _ = QFileDialog.getSaveFileName(self, caption='Save Image', filter="Images (*.png)")
        if not filePath:
            return
        scipy.misc.imsave(filePath,self.targetimg)
        ##add image stuff over here
    def loadData(self,srcortarg):
        filePath, _ = QFileDialog.getOpenFileName(self, caption='Open Image', filter="Images (*.png)")
        if not filePath:
            return
        self.loadDataFromFile(filePath,srcortarg)
    def loadDataFromFile(self, filePath,srcortarg):
        scene = QGraphicsScene()
        pixmap = QPixmap(filePath)
        pix = scene.addPixmap(pixmap)
        if srcortarg == 1:
            self.srcimg.setDisabled(False)
            self.srcimg.setScene(scene)
            self.srcimg.fitInView(pix, Qt.KeepAspectRatio)
            self.srcimg.show()
            self.sourceimg = scipy.misc.imread(filePath)
            if self.flagtransform:
                self.loadstate()
                self.flagtransform = False
                scene = QGraphicsScene()
                pixmap = QPixmap(self.targfilepath)
                pix = scene.addPixmap(pixmap)
                self.tarimg.setDisabled(False)
                self.tarimg.setScene(scene)
                self.tarimg.fitInView(pix,Qt.KeepAspectRatio)
                self.tarimg.show()
                self.targetimg = scipy.misc.imread(self.targfilepath)
        else:
            self.tarimg.setDisabled(False)
            self.tarimg.setScene(scene)
            self.tarimg.fitInView(pix,Qt.KeepAspectRatio)
            self.tarimg.show()
            self.targfilepath = filePath
            self.targetimg = scipy.misc.imread(filePath)
            if self.flag:
                self.loadstate()
                self.flag = False
            if self.flagtransform:
                self.loadstate()
                self.flagtransform = False
        if self.tarimg.isEnabled() and self.srcimg.isEnabled():
            self.acqbtn.setEnabled(True)
            self.co1.setEnabled(True)
            self.co2.setEnabled(True)
            self.co3.setEnabled(True)
            self.co4.setEnabled(True)
    def acquirepts(self):
        if self.acqbtn.isChecked() and not (self.co1.text() != "" and self.co2.text() != "" and self.co3.text() != "" and self.co4.text() != ""):
            self.pointsel()
        elif self.co1.text() != "" and self.co2.text() != "" and self.co3.text() != "" and self.co4.text() != "":
            self.readystate()
            if self.acqbtn.isChecked():
                self.pointsel()
        else:
            self.loadstate()
    def pointsel(self):
        self.co1.setText("")
        self.co2.setText("")
        self.co3.setText("")
        self.co4.setText("")
        self.srcbtn.setDisabled(True)
        self.tarbtn.setDisabled(True)
        self.effectlbl.setDisabled(True)
        self.effectbox.setDisabled(True)
        self.tfbtn.setDisabled(True)
        self.rstbtn.setDisabled(True)
        self.savebtn.setDisabled(True)
        self.tarimg.mousePressEvent = self.ptsacquire
        self.tarimg.keyPressEvent = self.backspace
        self.pointiter = 0
    def readystate(self):
        self.srcimg.setEnabled(True)
        self.tarimg.setEnabled(True)
        self.acqbtn.setEnabled(True)
        self.co1.setEnabled(True)
        self.co2.setEnabled(True)
        self.co3.setEnabled(True)
        self.co4.setEnabled(True)
        self.effectlbl.setEnabled(True)
        self.effectbox.setEnabled(True)
        self.tfbtn.setEnabled(True)
        self.rstbtn.setEnabled(True)
        self.savebtn.setEnabled(True)
        self.srcbtn.setEnabled(True)
        self.tarbtn.setEnabled(True)
        self.tarimg.mousePressEvent = QEvent.ignore
        self.tarimg.keyPressEvent = QEvent.ignore
        self.flag = True
    def loadstate(self):
        self.co1.setText("")
        self.co2.setText("")
        self.co3.setText("")
        self.co4.setText("")
        self.srcbtn.setEnabled(True)
        self.tarbtn.setEnabled(True)
        self.effectlbl.setDisabled(True)
        self.effectbox.setDisabled(True)
        self.tfbtn.setDisabled(True)
        self.rstbtn.setDisabled(True)
        self.savebtn.setDisabled(True)
        self.tarimg.mousePressEvent = QEvent.ignore
        self.tarimg.keyPressEvent = QEvent.ignore
        self.pointiter = 0
    def ptsacquire(self,event):
        x = self.tarimg.mapToScene(event.pos()).x()
        y = self.tarimg.mapToScene(event.pos()).y()
        if (self.tarimg.itemAt(event.pos()) and self.pointiter <= 3):
            self.pointlist[self.pointiter].setText("{0:.1f}, {1:.1f}".format(x,y))
            self.pointiter += 1
        if (self.pointiter == 4):
            self.pointiter = 3
        print(self.pointiter)
    def backspace(self, event):
        if event.key() == QtCore.Qt.Key_Backspace and self.pointiter >= 0:
            if self.pointiter == 3 and self.co4.text() != "":
                self.pointiter = 4
            self.pointiter -= 1
            if (self.pointiter == -1):
                self.pointiter = 0
            self.pointlist[self.pointiter].setText("")
if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = HomographyApp()

    currentForm.show()
    currentApp.exec_()