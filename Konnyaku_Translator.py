import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtTest

from win32.lib import win32con
from win32.win32api import SendMessage
from win32.win32gui import ReleaseCapture
import win32con
import win32api

from ctypes.wintypes import  MSG

import pyautogui

import os

from paddleocr import PaddleOCR

from googletrans import Translator

import re

import gooTrans

class translationDemo(QWidget):
    BORDER_WIDTH = 5

    def __init__(self):
        super().__init__()

        # set frame less window and make the window stay on the top
        self.setWindowFlags(Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint)
        # to set the translucent background must set frameless window first
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.autoOCRFlag = False    # A flag to control the auto OCR

        self.initUI()

    def initUI(self):

        # create the basic frame
        self.minButton = QtWidgets.QPushButton(
            "Minimize")      # Minimize window buttown
        self.closeButton = QtWidgets.QPushButton(
            "Close")       # Close window button

        self.minButton.clicked.connect(self.window().showMinimized)
        self.closeButton.clicked.connect(self.window().closeButtonCliked)

        hframe = QHBoxLayout()  # A QHbox layout to load the frame

        # A Qlabel you can drag it to drag the entire window
        self.frameLabel = QLabel(self)
        self.frameLabel.setStyleSheet('QWidget{background-color: white}')
        self.frameLabel.setText('Drag here')
        self.frameLabel.setAlignment(Qt.AlignCenter)

        hframe.addWidget(self.frameLabel)
        hframe.addWidget(self.minButton, alignment=QtCore.Qt.AlignRight)
        hframe.addWidget(self.closeButton, alignment=QtCore.Qt.AlignRight)

        # This is a transparent qwidget, it is used to locate pyautogui.screenshot
        self.originWindow = QtWidgets.QWidget()

        self.getbutton = QtWidgets.QPushButton(
            'Get')   # Get scrennshot to OCR button
        self.getbutton.clicked.connect(self.getButtonClicked)

        self.autoGetButton = QtWidgets.QPushButton(
            'Auto get')  # auto get scrennshots to OCR button
        self.autoGetButton.clicked.connect(self.autoGetButtonClicked)

        self.stopAutoGetButton = QtWidgets.QPushButton(
            'Stop auto')   # stop auto get scrennshots to OCR button
        self.stopAutoGetButton.clicked.connect(self.stopAutoGetButtonClicked)

        self.transButton = QtWidgets.QPushButton(
            "Translation")     # translation button
        self.transButton.clicked.connect(self.translationButtonClicked)

        # clean the screenshot in buffer / also clean the text box
        self.cleanButton = QtWidgets.QPushButton('Clean')
        self.cleanButton.clicked.connect(self.cleanBufferImage)

        hbuttonbox = QHBoxLayout()  # A QHboxLayout to load buttons
        hbuttonbox.addWidget(self.getbutton)
        hbuttonbox.addWidget(self.autoGetButton)
        hbuttonbox.addWidget(self.stopAutoGetButton)
        hbuttonbox.addWidget(self.transButton)
        hbuttonbox.addWidget(self.cleanButton)

        # A text editor used to fill in the content recognized by OCR
        self.OCRtextEdit = QTextEdit()
        self.OCRtextEdit.setFixedHeight(50)

        # A text editor used to fill in the translated text
        self.translationBox = QTextEdit()
        self.translationBox.setFixedHeight(50)
        self.translationBox.setStyleSheet('QWidget{background-color: white}')

        # A text editor used to show the current state of the program
        self.statusText = QtWidgets.QLineEdit()
        self.statusText.setStyleSheet('QWidget{background-color: white}')

        vbox = QVBoxLayout()
        vbox.addLayout(hframe)
        vbox.addWidget(self.originWindow)
        vbox.addLayout(hbuttonbox)
        vbox.addWidget(self.OCRtextEdit)
        vbox.addWidget(self.translationBox)
        vbox.addWidget(self.statusText)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('translation')
        self.show()

    def getButtonClicked(self):

        self.autoOCRFlag = False

        r = self.geometry()
        height = self.getbutton.y()-self.originWindow.y()

        # take a screenshot at the transparent window
        img = pyautogui.screenshot(region=[r.left()+self.originWindow.x(), r.top()+self.originWindow.y(), r.width(), height])  # x,y,w,h
        img.save('screenshot.png')

        self.statusText.setText('Process the OCR to screenshot.')
        ocr = PaddleOCR(lang="japan")
        img_path = 'screenshot.png'
        result = ocr.ocr(img_path)
        ocrResult = ""
        ocrText = ""  
        for line in result:
            ocrResult = re.search("(?<=[\']).*(?=]])", str(line))
            if ocrResult is None:
                continue
            else:
                # print(ocrResult.group())
                ocrText = ocrText+ocrResult.group()+'\n'

            print(line)
        self.OCRtextEdit.setPlainText(ocrText)
        self.statusText.setText('Translate the text.')
        self.translateText(ocrText)

    def autoGetButtonClicked(self):
        self.count = 5
        self.autoOCRFlag = True
        while(self.autoOCRFlag == True):
            self.statusText.setText("auto translating")
            r = self.geometry()
            height = self.getbutton.y()-self.originWindow.y()
            img = pyautogui.screenshot(region=[r.left(
            )+self.originWindow.x(), r.top()+self.originWindow.y(), r.width(), height])  # x,y,w,h
            img.save('screenshot.png')

            ocr = PaddleOCR(lang="japan")
            img_path = 'screenshot.png'
            result = ocr.ocr(img_path)
            ocrResult = ""
            ocrText = "" 
            for line in result:
                ocrResult = re.search("(?<=[\']).*(?=]])", str(line))
                if ocrResult is None:
                    continue
                else:
                    ocrText = ocrText+ocrResult.group()+'\n'

                print(line)
            self.OCRtextEdit.setPlainText(ocrText)
            self.translateText(ocrText)

            self.statusText.setText("waiting")
            QtTest.QTest.qWait(2000)
            self.statusText.setText("auto translating")
            QtTest.QTest.qWait(1000)

    def addCount(self):
        self.count = self.count-1

    def stopAutoGetButtonClicked(self):
        self.autoOCRFlag = False
        self.statusText.setText("stop auto translating")

    def closeButtonCliked(self):
        if os.path.exists('screenshot.png'):
            os.remove('screenshot.png')
        QApplication.quit()

    def translationButtonClicked(self):
        print(self.OCRtextEdit.toPlainText())
        self.statusText.setText('Translate the text.')
        self.translateText(self.OCRtextEdit.toPlainText())

    def translateText(self, sourceText):

        list = sourceText.split("\n")
        t = ""
        temp = ""
        for i in range(0, len(list)):

            temp = re.search("(?:^|\n).*(?=\',)", list[i])
            if temp is None:
                continue
            else:
                t = t+temp.group()+" "
        if len(t) > 0:

            # translator = Translator()
            # translated = translator.translate(t, dest='zh-cn', src='ja')
            # self.translationBox.setPlainText(translated.text)

            translated = gooTrans.translate(t,"zh-CN","ja")
            self.translationBox.setPlainText(translated)


    def isPointInDragRegion(self, pos) -> bool:
        # Check whether the point pressed by the mouse belongs to the area where dragging is allowed
        x = pos.x()
        condX = (60 < x < self.width() - 57 * 3)
        return condX

    def mousePressEvent(self, event):
        # moving the window
        if self.isPointInDragRegion(event.pos()):
            ReleaseCapture()
            SendMessage(self.window().winId(), win32con.WM_SYSCOMMAND,
                        win32con.SC_MOVE + win32con.HTCAPTION, 0)
            event.ignore()
            # can also implement window dragging by calling the interface function of windowEffect.dll
            # self.windowEffect.moveWindow(HWND(int(self.parent().winId())))

    def nativeEvent(self, eventType, message):
        # Handling Windows messages
        msg = MSG.from_address(message.__int__())
        # Handle mouse drag messages
        if msg.message == win32con.WM_NCHITTEST:

            xPos = (win32api.LOWORD(msg.lParam) -
                    self.frameGeometry().x()) % 65536
            yPos = win32api.HIWORD(msg.lParam) - self.frameGeometry().y()
            w, h = self.width(), self.height()

            lx = xPos - 9 <= self.BORDER_WIDTH
            rx = xPos + 9 >= w - self.BORDER_WIDTH
            ty = yPos - 9 <= self.BORDER_WIDTH
            by = yPos + 9 >= h - self.BORDER_WIDTH

            # left top
            if (lx and ty):
                return True, win32con.HTTOPLEFT
            # right bottom
            elif (rx and by):
                return True, win32con.HTBOTTOMRIGHT
            # right top
            elif (rx and ty):
                return True, win32con.HTTOPRIGHT
            # left bottom
            elif (lx and by):
                return True, win32con.HTBOTTOMLEFT
            # top
            elif ty:
                return True, win32con.HTTOP
            # bottom
            elif by:
                return True, win32con.HTBOTTOM
            # left
            elif lx:
                return True, win32con.HTLEFT
            # right
            elif rx:
                return True, win32con.HTRIGHT

        return QWidget.nativeEvent(self, eventType, message)

    def cleanBufferImage(self, event):  # Clean the buffer image
        if os.path.exists('screenshot.png'):
            os.remove('screenshot.png')
            self.statusText.setText('Clean the buffer.')
        else:
            self.statusText.setText('Not fund.')

        self.statusText.setText("Clean the textbox")
        self.OCRtextEdit.clear()
        self.translationBox.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    translation = translationDemo()

    sys.exit(app.exec_())
