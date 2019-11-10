from medlib.constants import *
from medlib.handle_property import _

from medlib.mediamodel.media_base import MediaBase
from medlib.mediamodel.media_appendix import MediaAppendix
from medlib.mediamodel.paths_storage import PathsStorage
from medlib.mediamodel.extra import QHLine

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPlainTextEdit

from PyQt5.QtGui import QTextCursor
from PyQt5.QtGui import QFont

class MediaStorage(MediaBase):
    """
    This object represents the MediaStorage 
    This container can contain
    """
    
    def __init__(self, paths_storage, titles, control, general=None,  rating=None):
        """
        This is the constructor of the MediaStorage
        ___________________________________________
        input:
                paths_storage PathsContent      paths to the media content (card.ini, image.jpg, media)

                titles        IniTitles         represents the [titles] section
                control       IniControl        represents the [control] section
                general       IniGeneral        represents the [general] section
                rating        IniRating         represents the [rating] section
        """
        super().__init__(titles, control, general, rating)
        
        assert issubclass(paths_storage.__class__, PathsStorage)
        
        self.paths_stirage = paths_storage
        self.media_appendix_list = []

    def getPathOfImage(self):
        return self.paths_stirage.getPathOfImage()

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
        
    def addMediaAppendix(self, media_appendix):
        """
        Adds a new MediaAppendix to this MediaStorage
        It is ordered accordingly the language by the control.orderby
        _____________________________________________________________
        input:
                media_appendix    MediaAppendix    the MediaAppendix to add
        """
        
        assert issubclass(media_appendix.__class__, MediaAppendix), media_appendix.__class__

        # Add the MediaStorage
        self.media_appendix_list.append(media_appendix)
        
        # Sort the list
        #self.sortMediaStorage()        

    def getMediaAppendixList(self):
        return self.media_appendix_list
        
    def getWidgetCardInformationText(self, sizeRate):
        """
            Appends the Links of MediaAppendixes to the bottom of the InformationText
        """
        super_widget = super().getWidgetCardInformationText(sizeRate)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(layout)

        layout.addWidget(super_widget)        
        layout.addWidget(QHLine())

        for media_appendix in self.getMediaAppendixList():
            layout.addWidget(media_appendix.getWidget(sizeRate))
        
        return widget

    def addWidgetGeneralInfoStoryline(self, parent, sizeRate, grid_layout, row, title_id, value):
        if value:
            widget_key = QLabel(_(title_id) + ":", )
            widget_key.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Bold))
            widget_key.setAlignment(Qt.AlignTop)

            widget_value = QPlainTextEdit(parent)
            widget_value.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Normal))
            widget_value.insertPlainText(value)
            widget_value.setReadOnly(True)
            widget_value.setMinimumHeight( (PANEL_FONT_SIZE + 3) * sizeRate )
            widget_value.moveCursor(QTextCursor.Start)
            
            grid_layout.addWidget( widget_key, row, 0)            
            grid_layout.addWidget( widget_value, row, 1)        
            row = row + 1
            
        return row   

        