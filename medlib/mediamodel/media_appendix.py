import locale
import os

from medlib.constants import *
from medlib.handle_property import _
from builtins import object

from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication

from PyQt5.QtGui import QFont

from PyQt5.QtCore import Qt

from medlib.mediamodel.ini_titles import IniTitles

from medlib.mediamodel.paths_appendix import PathsAppendix

class MediaAppendix(object):

    class LinkWidget(QWidget):     
        def __init__(self, parent, sizeRate):
            super().__init__()
            
            layout = QHBoxLayout()
            layout.setAlignment(Qt.AlignLeft)
        
            layout.setSpacing(1)        
            layout.setContentsMargins(0, 0, 0, 0)
        
            self.setLayout(layout)

        #
        # Icon
        #
#        iconFileName = TITLE_ICON_PREFIX + "-" + self.getFolderType() + "-" + self.control.getMedia() + "-" + self.control.getCategory() + "." + TITLE_ICON_EXTENSION
#        pathToFile = resource_filename(__name__, os.path.join(TITLE_ICON_FOLDER, iconFileName))       
#        pixmap = QPixmap( pathToFile )
#
#        if pixmap.isNull():            
#            smaller_pixmap = QPixmap(TITLE_ICON_HEIGHT * sizeRate, TITLE_ICON_HEIGHT * sizeRate)
#            smaller_pixmap.fill(QColor(self.getBackgroundColor()))
#        else:
#            smaller_pixmap = pixmap.scaledToWidth(TITLE_ICON_HEIGHT * sizeRate)
#   
#        iconWidget = QLabel()
#        iconWidget.setPixmap(smaller_pixmap)
#
#        title_layout.addWidget(iconWidget)

            #
            # Title
            #
            titleWidget = QLabel(parent.titles.getTranslatedTitle())
            titleWidget.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Bold))

            layout.addWidget(titleWidget)

        def enterEvent(self):
            self.update()
            QApplication.setOverrideCursor(Qt.PointingHandCursor)
            
        def leaveEvent(self):
            self.update()
            QApplication.restoreOverrideCursor()
            
    """
    This object represents the MediaAppendix
    """
   
    @staticmethod
    def sort_key(arg):
        """
        """
        return locale.strxfrm(arg.getTranslatedTitle()) if arg.control.getOrderBy() == 'title' else arg.container_paths.getNameOfFolder() if arg.control.getOrderBy() == 'folder' else arg.container_paths.getNameOfFolder() 
    
    def __init__(self, paths_storage, titles):
        """
        This is the constructor of the MediaAppendix
        ________________________________________
        input:
                paths_storage     PathsAppendix     paths to the media content (card.ini, image.jpg, media)
                titles            IniTitles         represents the [titles] section
        """
        super().__init__()
        
        assert issubclass(paths_storage.__class__, PathsAppendix), paths_storage.__class__
        assert issubclass(titles.__class__, IniTitles), titles.__class__
        
        self.paths_storage = paths_storage
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
    def getWidget(self, sizeRate):
        """  _________________________________________
            | Icon | Title                            |
            |______|__________________________________|
        """
        widget = MediaAppendix.LinkWidget(self, sizeRate)
        return widget



    