import locale
import os
import subprocess
import platform

from medlib.constants import *
from medlib.handle_property import _
from builtins import object

from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication

from PyQt5.QtGui import QFont, QPalette

from PyQt5.QtCore import Qt

from medlib.mediamodel.ini_titles import IniTitles

from medlib.mediamodel.paths_appendix import PathsAppendix

from medlib.mediamodel.qlabel_to_link_on_cllick import QLabelToLinkOnClick

class MediaAppendix(object):
            
    """
    This object represents the MediaAppendix
    """
   
    @staticmethod
    def sort_key(arg):
        """
        """
        return locale.strxfrm(arg.getTranslatedTitle()) if arg.control.getOrderBy() == 'title' else arg.container_paths.getNameOfFolder() if arg.control.getOrderBy() == 'folder' else arg.container_paths.getNameOfFolder() 
    
    def __init__(self, pathsAppendix, titles):
        """
        This is the constructor of the MediaAppendix
        ________________________________________
        input:
                pathsAppendix   PathsAppendix     paths to the media content (card.ini, image.jpg, media)
                titles          IniTitles         represents the [titles] section
        """
        super().__init__()
        
        assert issubclass(pathsAppendix.__class__, PathsAppendix), pathsAppendix.__class__
        assert issubclass(titles.__class__, IniTitles), titles.__class__
        
        self.pathsAppendix = pathsAppendix
        self.titles = titles

    def getTitles(self):
        """
        Returns back the [titles] section.
        _________________________________________________________________________________________________
        input:
        output:
                titles       IniTitles
        """
        return self.titles        

    # --------------------------------------------
    # ---------------- Widget --------------------
    # --------------------------------------------
    def getWidget(self, scale):
        """  _________________________________________
            | Icon | Title                            |
            |______|__________________________________|
        """
        #widget = MediaAppendix.LinkWidget(self, scale)
        widget = MediaAppendix.QLinkLabelToAppendixMedia(self.titles.getTranslatedTitle(), self.isSelected, self.getPathOfMedia(), scale)
        return widget
    
    def getPathOfMedia(self):
        return self.pathsAppendix.getPathOfMedia()
    
    def isSelected(self):
        return True

    class QLinkLabelToAppendixMedia( QLabelToLinkOnClick ):

        def __init__(self, text, funcIsSelected, pathOfMedia, scale):
            super().__init__(text, funcIsSelected)        
            self.pathOfMedia = pathOfMedia
            self.scale = scale
            self.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Bold))

        def toDoOnClick(self):
        
            if platform.system() == 'Darwin':                   # macOS
                subprocess.call(('open', self.pathOfMedia))
            elif platform.system() == 'Windows':                # Windows
                os.startfile(self.pathOfMedia)
            elif platform.system() == 'Linux':                  # Linux:
                subprocess.call(('xdg-open', self.pathOfMedia))
            else:                                               # linux 
                subprocess.call(('xdg-open', self.pathOfMedia))

        def enterEvent(self, event):
            super().enterEvent(event)
            font = self.font()
            font.setUnderline(True)
            self.setFont(font)

            self.origPalette = self.palette()
            palette = QPalette()
            palette.setColor(QPalette.Foreground,Qt.blue)
            
            self.setPalette(palette)            
            
        def leaveEvent(self, event):
            super().leaveEvent(event)
            font = self.font()
            font.setUnderline(False)
            self.setFont(font)
            
            self.setPalette(self.origPalette)

    def getJson(self):
        #json = super().getJson();
        json = {}
        
        json.update({'titles': self.titles.getJson()} if self.titles.getJson() else {})
        json['paths-appendix'] = self.pathsAppendix.getJson()
        
        return json

    