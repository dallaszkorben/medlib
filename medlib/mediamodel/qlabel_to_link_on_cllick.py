import os
import subprocess
import platform

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication

class QLabelToLinkOnClick(QLabel):

    def __init__(self, text, funcIsSelected):
        super().__init__( text )
        self.funcIsSelected = funcIsSelected 
        
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
        
        self.toDoOnClick() 
                
        event.accept()
        
    def toDoOnClick(self):
        raise NotImplementedError
        
