from medlib.constants import *
from medlib.mediamodel.media_base import MediaBase
from medlib.mediamodel.media_storage import MediaStorage
from medlib.mediamodel.paths_collector import PathsCollector

from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QTextCursor
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from medlib.mediamodel.extra import QHLine

from medlib.mediamodel.qlabel_to_link_on_cllick import QLabelToLinkOnClick

class MediaCollector(MediaBase):
    """
    This object represents the MediaCollector
    This container can contain more MediaContainers and/or
    one MediaContent
    """
    def __init__(self, pathsCollector, titles, control, general=None, rating=None):  
        """
        This is the constructor of the MediaCollector
        ________________________________________
        input:
                pathsCollector    PathsCollector    paths to the collector elements (card.ini, image.jpg ...)
        
                titles            IniTitles         represents the [titles] section
                control           IniControl        represents the [control] section
                general           IniGeneral        represents the [general] section
                rating            IniRating         represents the [rating] section
        """
        super().__init__(titles, control, general, rating)
        
#        NoneType = type(None)
#        assert issubclass(parentCollector.__class__, (MediaCollector, NoneType)), general.__class__
        assert issubclass(pathsCollector.__class__, PathsCollector)
        
        self.pathsCollector = pathsCollector
        self.media_collector_list = []
        self.media_storage_list = []
        
        self.nextLevelListener = None
  
    def getNameOfFolder(self):
        return self.pathsCollector.getNameOfFolder()
    
    def getPathOfImage(self):
        return self.pathsCollector.getPathOfImage()
    
    def getPathOfCard(self):
        return self.pathsCollector.getPathOfCard()
    
    def getBackgroundColor(self):
        return COLLECTOR_BACKGROUND_COLOR
        
    def getFolderType(self):
        return "collector" 
        
    def addMediaCollector(self, mediaCollector):
        """
        Adds a new MediaCollector to this MediaCollector
        It is ordered accordingly the language by the control.orderby
        _____________________________________________________________
        input:
                mediaCollector    MediaCollector    the MediaCollector to add
        """
        
        assert issubclass(mediaCollector.__class__, MediaCollector)
        
        mediaCollector.setParentCollector(self)
        
        # Add the MediaCollector
        self.media_collector_list.append(mediaCollector)
        
        # Sort the list
        self.sortMediaCollector()
        
    def addMediaStorage(self, mediaStorage):
        """
        Adds a new MediaStorage to this MediaCollector
        It is ordered accordingly the language by the control.orderby
        _____________________________________________________________
        input:
                mediaStorage    MediaStorage    the MediaStorage to add
        """
        
        assert issubclass(mediaStorage.__class__, MediaStorage) 

        mediaStorage.setParentCollector(self)

        # Add the MediaStorage
        self.media_storage_list.append(mediaStorage)
        
        # Sort the list
        self.sortMediaStorage()
    
    def getPathsCollector(self):
        return self.pathsCollector
        
    def getMediaStorageList(self):
        return self.media_storage_list
    
    def getMediaCollectorList(self):
        return self.media_collector_list    
    
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

        self.sortMediaCollector()
        self.sortMediaContent()        
        
    def sortMediaCollector(self):
        """
        Sort the MediaCollectors regarding to the control.orderby
           = title
           = folder
           = series
        """
        self.media_collector_list.sort(key=lambda arg: MediaCollector.sort_key(arg))
        
    def sortMediaStorage(self):
        """
        Sort the MediaStorage regarding to the control.orderby
           = title
           = folder
           = series
        """
        self.media_storage_list.sort(key=lambda arg: MediaStorage.sort_key(arg))

                
    def getHierarchyTitle(self, space):
        out = space + "<C> " + self.getTranslatedTitle() + "\n"        
        
        for collector in self.media_collector_list:
            out += collector.getHierarchyTitle(space + "   ")
            
        for storage in self.media_storage_list:
            out += storage.getHierarchyTitle(space + "   ")        
        return out

    def addWidgetGeneralInfoStoryline(self, parent, sizeRate, grid_layout, row, title_id, value):
        if value:
            grid_layout.addWidget(QHLine(), row, 0, 1, 2)
            row = row + 1
            
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
            
            grid_layout.addWidget( widget_value, row, 1)        
            row = row + 1
            
        return row

    def setNextLevelListener(self, nextLevelListener):
        """
            From outside, it is needed to provide a METHOD as the nextLevelListener parameter, 
            which will handle the selection of the actual MediaCollector - goes one level deeper 
            ________________________________________
            input:
                    nextLevelListener    Function    handles the selection of this mediaCollector

        """
        self.nextLevelListener = nextLevelListener
        
    def getQLabelToKeepImage(self):
        """
            Gives back a class extending QLabel which will keep the image.
            This class has to implement the 'toDoOnClick' method which
            handles the selection of this MediaCollector
        """
        return MediaCollector.QLabelWithLinkToNextLevel(self)


    class QLabelWithLinkToNextLevel( QLabelToLinkOnClick ):

        def __init__(self, collector):
            super().__init__(None, collector.isSelected)
            self.collector = collector

        def toDoOnClick(self):                 
            if self.collector.nextLevelListener is not None:
                self.collector.nextLevelListener(self.collector)

    def getJson(self):
        json = super().getJson();
        
        json['paths-collector'] = self.getPathsCollector().getJson()
                
        json['collectors'] = [c.getJson() for c in self.media_collector_list]
        json['storages'] = [c.getJson() for c in self.media_storage_list]
        return json
        