import os
import platform
from subprocess import Popen

from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from medlib.handle_property import config_ini
from medlib.card_ini import CardIni
from builtins import FileNotFoundError

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
        
        self.toDoOnClick()
        
        """
        Delegate the Click on the Image as a SPACE key press to up. 
        This event can be catched it in the higher level Widget as a SPACE key press
        (for example in CardHolder)

        I could have made a direct selection in the media_collector/media_storage
        using the toDoOnClick() method, but I do not do this because in that case 
        I could not have the index of the selected Card  
        """
##        event = QKeyEvent(QEvent.KeyPress, QtCore.Qt.Key_Space, Qt.NoModifier, str(self.media.getCard().getIndexInDataList()))
#        event = QKeyEvent(QEvent.KeyPress, QtCore.Qt.Key_Space, Qt.NoModifier, str(self.media.getIndex()))
#        QtCore.QCoreApplication.postEvent(self, event)
#                
        event.accept()
#        event.ignore()
        return
               
    def toDoSelection(self):
        raise NotImplementedError
    
#    def playMedia(self, media_path, media_type):
#        """
#            Play media.
#            This method can be invoked from MediaAppendix.QLinkLabelToAppendixMedia or MediaStorage.QLabelWithLinkToMedia
#            
#            @param media_path: the path of the media to play. It can be a file or a link 
#            @param media_type: the type of the media to play. (video, audio, text, image, link) 
#        """
#        if config_ini["use_xdg"] == "y":
#
#            if platform.system() == 'Darwin':                   # macOS
#                Popen(['open', media_path])
#            elif platform.system() == 'Windows':                # Windows
#                os.startfile(media_path)
#            elif platform.system() == 'Linux':                  # Linux:
#                Popen(['xdg-open', media_path])
#            else:                                               # linux 
#                Popen(['xdg-open', media_path])                
#        else:        
#            # try fetch extension of media_file to identify the media_player and media_param
#            rematch = CardIni.getMediaFilePatternByMedia(media_type).match(media_path)      
#            if rematch:
#                extension = rematch.groups()[0]
#            else:
#                extension = ""
#            
#            # try to find the configuration of media_player and media_param by "media/extension"
#            try:
#                media_player = config_ini["player_" + media_type + "_" + extension + "_player"]
#                media_param = config_ini["player_" + media_type + "_" + extension + "_param"]
#            
#            # if not, then try to find the configuration only for "media"
#            except KeyError:
#                try:
#                    media_player = config_ini["player_" + media_type + "_player"]
#                    media_param = config_ini["player_" + media_type + "_param"] 
#                except KeyError:
#                    media_player = None
#                    media_param = ""
#                       
#            if media_player:
#                param_list = media_param.replace(" ", ",").split(",") if media_param else []
#                try:
#                    print(media_player, media_path, param_list)
#                    process = Popen([media_player, media_path] + param_list )
#                    print(process.pid)
#                except FileNotFoundError as e:
#                    print("File Not found:", e)
#                #process.communicate()                
#            else:
#                print("no player was found")
#            # find out mime type
