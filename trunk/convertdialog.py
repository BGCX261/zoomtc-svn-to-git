#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
import sys

from PIL import Image
from PyQt4 import QtCore, QtGui

import zoomtc_rc
from ui_convertdialog import Ui_convertDialog

# all supported image formats list here
EXTS = ('.bmp', '.im', '.msp', '.pcx', '.ppm', 
        '.spider', '.tiff', '.xbm', '.xv', '.jpg', '.jpeg', '.gif', '.png',)

class ConvertDialog(QtGui.QDialog, Ui_convertDialog):
    def __init__(self, parent=None, initDir= '.', initRate = 0.055):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        # English version UI messages
        self.messages = {
            'selectSrc': u'Please select picture source dir',
            'outDir': u'zoomtc_out',
            'progressFormat': u'processing: %d / %d',
            'cancel': u'Cancel',
            'processing': u'Processing...',
            'dirLabel': u'Picture Dir:',
            'rateLabel': u'Zoom Rate:',
            'helpLabel': u"<p>1.Drag & Drop picture directory on `Picture Dir'.<br/>"
                         u"2.Set `Zoom Rate' as R,the zoomed size will be SIZE*R.<br/>"
                         u"3.Zoomed pictures stored in 'zoomtc_out' under the same directory.</p>",
            'dirButton': u'Browser...',
            'convertButton': u'Zoom',
            'windowTitle': u'Zoomtc, a picture batch zoom tool',
            'criticalTitle': u'Something is Wrong',
            'criticalInfo': u'Check the zoom rate and picture format.\nPlease try again.',
        }
        

        # If system locale is Chinese, then we define Chinese version UI messages
        loc = QtCore.QLocale.system()
        if loc.country()==loc.China:
            self.messages = {
                'selectSrc': u'请选择图片源目录',
                'outDir': u'缩放输出目录',
                'progressFormat': u'进度: %d / %d',
                'cancel': u'取消',
                'processing': u"正在处理图片……",
                'dirLabel': u'图片源目录:',
                'rateLabel': u'缩放比例:',
                'helpLabel': u'<p>1.拖放图片目录到"图片源目录"<br/>'
                        u'2.设置"缩放比例"为R, 缩放后尺寸为"原尺寸*R"<br/>'
                        u'3.缩放后的文件保存在原图片目录下的“缩放输出目录"中</p>',
                'dirButton': u"浏览...",
                'convertButton': u"缩放",
                'windowTitle': u'Zoomtc, 图片批量缩放工具',
                'criticalTitle': u'错误',
                'criticalInfo': u'请检查是否正确设置了缩放比例.',
            }

        # set the UI, English or Chinese according to the system locale
        self.dirLabel.setText(self.messages['dirLabel'])
        self.rateLabel.setText(self.messages['rateLabel'])
        self.helpLabel.setText(self.messages['helpLabel'])
        self.dirButton.setText(self.messages['dirButton'])
        self.convertButton.setText(self.messages['convertButton'])
        self.setWindowTitle(self.messages['windowTitle'])

        self.setWindowIcon(QtGui.QIcon(":/logo.ico"))

        # enable Drag & Drop
        self.dirLineEdit.setAcceptDrops(False)
        self.rateLineEdit.setAcceptDrops(False)
        self.setAcceptDrops(True)

        self.connect(self.dirButton, QtCore.SIGNAL("clicked()"),
                self.getDir)
        self.connect(self.convertButton, QtCore.SIGNAL("clicked()"),
                self.doConvert)

        self.cwd = os.path.abspath(initDir)
        self.dirLineEdit.setText(self.cwd)
        self.rate = float(initRate)
        self.rateLineEdit.setText("%.3f"%round(self.rate, 3))

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if not urls:
            return
        fileName = urls[0].toLocalFile()
        if not fileName:
            return
        self.dirLineEdit.setText(fileName)

    # save rate value when closing
    def closeEvent(self, event):
        rate = float(self.rateLineEdit.text())
        settings = QtCore.QSettings(u"ctootc", u"zoomtc")
        settings.setValue("rate", QtCore.QVariant(rate))

    def getDir(self):
        dirName = QtGui.QFileDialog.getExistingDirectory(self, self.messages['selectSrc'],
                self.cwd)
        if dirName:
            self.dirLineEdit.setText(dirName)
            #self.cwd = os.path.basename(dirName)

    # process one image file
    def _processFile(self, fileName, rate, progressDialog):
        print 'process on:', fileName
        path = os.path.dirname(fileName)
        os.chdir(path)
        outdir = os.path.join(path, self.messages['outDir'])
        print 'outdir', outdir
        name = os.path.basename(fileName)
        print 'name', name
        self.processValue += 1
        progressDialog.setValue(self.processValue)
        progressDialog.setLabelText(self.messages['progressFormat'] % (self.processValue, self.processTotal))
        QtGui.qApp.processEvents()

        if progressDialog.wasCanceled():
            return
        n,ext = os.path.splitext(name)
        if ext.lower() in EXTS:
            im = Image.open(fileName)
            (w,h) = im.size
            iout = im.resize((int(w*rate),int(h*rate)), Image.ANTIALIAS)
            print 'outname', os.path.join(outdir, name)
            if not os.path.exists(outdir):
                os.mkdir(outdir)
            iout.save(os.path.join(outdir, name))

    # process all image files under this directories
    def _processDir(self, path, rate, progressDialog):
        print 'process on:', path
        os.chdir(path)
        outdir = os.path.join(path, self.messages['outDir'])
        print 'outdir', outdir
        for name in os.listdir(path):
            print 'name', name
            fullname = os.path.join(path, name)
            if os.path.isdir(fullname):
                self._processDir(fullname, rate, progressDialog)
            else:
                self._processFile(fullname, rate, progressDialog)

    # count image files need to be processed, we need this number to initialize ProgressDialog
    def _totalfiles(self, path):
        if os.path.isdir(path):
            total = 0
            for name in os.listdir(path):
                fullname = os.path.join(path, name)
                if os.path.isdir(fullname):
                    total += self._totalfiles(fullname)
                else:
                    total += 1
            return total
        else:
            return 1

    def doConvert(self):
        try:
            rate = float(self.rateLineEdit.text())
            path = unicode(self.dirLineEdit.text())
            progressDialog = QtGui.QProgressDialog(self)

            progressDialog.setCancelButtonText(self.messages['cancel'])

            self.processTotal = self._totalfiles(path)
            progressDialog.setRange(0, self.processTotal)
            progressDialog.setWindowTitle(self.messages['processing'])
            self.processValue = 0
            if os.path.isdir(path):
                self._processDir(path, rate, progressDialog)
            else:
                self._processFile(path, rate, progressDialog)
            progressDialog.close()
        except:
            QtGui.QMessageBox.critical(self, self.messages['criticalTitle'], self.messages['criticalInfo'])
            return

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    settings = QtCore.QSettings(u"ctootc", u"zoomtc")
    rate = settings.value("rate", QtCore.QVariant(0.5)).toDouble()[0]
    s = ConvertDialog(initRate=rate)
    s.show()
    sys.exit(app.exec_())
