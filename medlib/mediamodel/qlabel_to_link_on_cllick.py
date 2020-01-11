import os
import subprocess
import platform

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
from PyQt5.QtGui import QKeyEvent

class QLabelToLinkOnClick(QLabel):

    def __init__(self, media, text, funcIsSelected):
        super().__init__( text )
        self.funcIsSelected = funcIsSelected
        self.media = media
        self.mouse_pressed_for_click = False
    
    def enterEvent(self, event):
        self.update()
        QApplication.setOverrideCursor(Qt.PointingHandCursor)
        
        #if self.pathOfMedia:
        #    self.setStyleSheet('background: gray')
            
        event.ignore()
        
    def leaveEvent(self, event):
        self.update()
        QApplication.restoreOverrideCursor()
        
        #if self.pathOfMedia:
        #    self.setStyleSheet('background:black')
        
        event.ignore()
        
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.funcIsSelected():
            self.mouse_pressed_for_click = True
            event.accept()
        else:
            event.ignore()
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.mouse_pressed_for_click = False
            event.accept()
        else:
            event.ignore()
            
    def mouseReleaseEvent(self, event):
        if event.button() != Qt.LeftButton or not self.mouse_pressed_for_click:
            self.mouse_pressed_for_click = False
            event.ignore()
            return 
        
        self.mouse_already_pressed = False
        
#        self.toDoOnClick()
        
        """
        I delegate the Click on the Image as a SPACE key press to up. 
        I can catch it in the CardHolder as a SPACE key press

        I could have made a direct selection in the media_collector/media_storage
        using the toDoOnClick() method, but I do not do this because in that case 
        I could not have the index of the selected Card  
        """
        event = QKeyEvent(QEvent.KeyPress, QtCore.Qt.Key_Space, Qt.NoModifier, str(self.media.getIndexInDataList()))
        QtCore.QCoreApplication.postEvent(self, event)
                
        event.accept()
#        event.ignore()
#        return
               
    def toDoSelection(self):
        raise NotImplementedError
              
