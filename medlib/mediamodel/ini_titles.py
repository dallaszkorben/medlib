from medlib.handle_property import config_ini

from pkg_resources import resource_filename

from medlib.constants import *
from medlib.handle_property import _
from builtins import object

from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget


from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPixmap

from PyQt5.QtCore import Qt


class IniTitles(object):
    """
    This class represents the [titles] section in the card.ini file
    """
    
    def __init__(self, orig_title, title_list_by_language=None):
        """
        This is the constructor of the IniTitles class
        ___________________________________________
        input:
            orig_title                string        "The title in the original language"
            title_list_by_language    dictionary    {"hu":"Magyar cim", "en":"English title"}
        """
        self.orig_title = orig_title
        self.title_list_by_language = title_list_by_language if title_list_by_language else {}
    
    def getOrigTitle(self):
        return self.orig_title
        
    def getTranslatedTitle(self):
        """
        Returns back the title.
        If the title does not exists on the specific language, then the 'original' title will be returned
        _________________________________________________________________________________________________
        input:
        """
        title = self.title_list_by_language.get(config_ini['language'])
        if not title:
            title=self.getOrigTitle()
        return title
    
    def getJson(self):
        json = {}
        json.update({} if self.orig_title is None or not self.orig_title else {"orig": self.orig_title})
        
        json.update(
            {key: value for key, value in self.title_list_by_language.items()} if self.title_list_by_language else {}
            )
       
        return json
    
    
    def getWidget(self, parent, scale):
        """  _________________________________________
            | Icon | Title                            |
            |______|__________________________________|
        """
        title_layout = QHBoxLayout()
        title_layout.setAlignment(Qt.AlignLeft)
        
        # space between the three grids
        title_layout.setSpacing(10)
        
        # margin around the widget
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(title_layout)

        #
        # Icon
        #
        iconFileName = TITLE_ICON_PREFIX + "-" + parent.getFolderType() + ( "-" + parent.control.getMedia() if parent.control.getMedia() else "" ) + ( "-" + parent.control.getCategory() if parent.control.getCategory() else "" ) + "." + TITLE_ICON_EXTENSION
        pathToFile = resource_filename(__name__, os.path.join(TITLE_ICON_FOLDER, iconFileName))       
        pixmap = QPixmap( pathToFile )

        if pixmap.isNull():            
            smaller_pixmap = QPixmap(TITLE_ICON_HEIGHT * scale, TITLE_ICON_HEIGHT * scale)
            smaller_pixmap.fill(QColor(parent.getBackgroundColor()))
        else:
            smaller_pixmap = pixmap.scaledToWidth(TITLE_ICON_HEIGHT * scale)
   
        iconWidget = QLabel()
        iconWidget.setPixmap(smaller_pixmap)

        title_layout.addWidget(iconWidget)

        #
        # Title
        #
        
        series = parent.general.getSeries()
        episode = parent.general.getEpisode()
        titleWidget = QLabel(
            ("S" + series + "E" + episode + "-" if episode is not None and series is not None else "") + 
            self.getTranslatedTitle() + 
            ("-"+_("title_part").format(episode) if episode is not None and series is None else "") )
        titleWidget.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale * 1.8, weight=QFont.Bold))

        title_layout.addWidget(titleWidget)
        return widget
    
    
    
    
