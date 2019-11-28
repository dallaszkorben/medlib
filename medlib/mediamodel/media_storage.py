import os
import subprocess
import platform

from medlib.constants import *
from medlib.handle_property import _

from medlib.mediamodel.media_base import MediaBase
from medlib.mediamodel.paths_storage import PathsStorage
from medlib.mediamodel.extra import QHLine

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QLabel, QScrollBar, QApplication
from PyQt5.QtWidgets import QPlainTextEdit

from PyQt5.QtGui import QTextCursor
from PyQt5.QtGui import QFont
from PyQt5.uic.Compiler.qtproxies import QtWidgets


class MediaStorage(MediaBase):
    """
    This object represents the MediaStorage 
    This container can contain
    """
    
    def __init__(self, pathsStorage, titles, control, general=None,  rating=None):
        """
        This is the constructor of the MediaStorage
        ___________________________________________
        input:
                pathsStorage    PathsStorage      paths to the media content (card.ini, image.jpg, media)

                titles          IniTitles         represents the [titles] section
                control         IniControl        represents the [control] section
                general         IniGeneral        represents the [general] section
                rating          IniRating         represents the [rating] section
        """
        super().__init__(titles, control, general, rating)
        
        assert issubclass(pathsStorage.__class__, PathsStorage)
        
        self.pathsStorage = pathsStorage
        self.media_appendix_list = []

    def getNameOfFolder(self):
        return self.pathsStorage.getNameOfFolder()
    
    def getPathOfImage(self):
        return self.pathsStorage.getPathOfImage()

    def getPathOfMedia(self):
        return self.pathsStorage.getPathOfMedia()

    def getBackgroundColor(self):
        return STORAGE_BACKGROUND_COLOR

    def getFolderType(self):
        return "storage" 
    
    def getHierarchyTitle(self, space):
        return space + "<S> " + self.getTranslatedTitle() + "\n"
     
    def setLanguage(self, language):
        """
        Sets the language, recursively, of the containers
        Sorts the order of the containers, recursively
        __________________________________________________
        input:
            language    string    like 'hu' or 'en' or ...
        """
        self.language = language
        for container in self.media_container_list:
            container.setLanguage(language)

        self.media_container_list.sort(key=lambda arg: arg.getTitle())
        
#    def getWidgetTitle(self, sizeRate):
#        widget = super().getWidgetTitle(sizeRate)        
#        return widget

    def addWidgetGeneralInfoStoryline(self, parent, sizeRate, grid_layout, row, title_id, value):
        if value:
            grid_layout.addWidget(QHLine(), row, 0, 1, 2)
            row = row + 1

            widget_key = QLabel(_(title_id) + ":", )
            widget_key.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Bold))
            widget_key.setAlignment(Qt.AlignTop)

            widget_value = QPlainTextEdit(parent)
            
            #widget_value.setLineWrapMode( QPlainTextEdit.WidgetWidth )
            widget_value.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            
            widget_value.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Normal))
            widget_value.setReadOnly(True)
            widget_value.setMinimumHeight( (PANEL_FONT_SIZE + 3) * sizeRate )

            [ widget_value.appendPlainText(line) for line in value.split('\\n')]
            #widget_value.insertPlainText(value)
            #widget_value.appendPlainText("hello")

            widget_value.moveCursor(QTextCursor.Start)
            # - eliminate the padding from the top - #            
            widget_value.document().setDocumentMargin(0)
            widget_value.setStyleSheet("QPlainTextEdit {padding-left:5px; padding-top:0px; border:0px;}")
            
            grid_layout.addWidget( widget_key, row, 0)            
            grid_layout.addWidget( widget_value, row, 1)        
            row = row + 1
            
        return row   

    def doOnClickImage(self):
        
        if platform.system() == 'Darwin':           # macOS
            subprocess.call(('open', self.getPathOfMedia()))
        elif platform.system() == 'Windows':        # Windows
            os.startfile(filepath)
        elif platform.system() == 'Linux':          # Linux:
            subprocess.call(('xdg-open', self.getPathOfMedia()))
        else:                                       # linux 
            subprocess.call(('xdg-open', self.getPathOfMedia()))

        