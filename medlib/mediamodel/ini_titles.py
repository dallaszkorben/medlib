import os

from medlib.handle_property import config_ini

from pkg_resources import resource_filename

from medlib.constants import PANEL_FONT_TYPE
from medlib.constants import PANEL_FONT_SIZE
from medlib.constants import TITLE_ICON_EXTENSION
from medlib.constants import TITLE_ICON_FOLDER
from medlib.constants import TITLE_ICON_HEIGHT
from medlib.constants import TITLE_ICON_PREFIX

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
        Returns back the raw title.
        If the title does not exists on the specific language, then the 'original' title will be returned
        _________________________________________________________________________________________________
        input:
        """
        title = self.title_list_by_language.get(config_ini['language'])
        if not title:
            title=self.getOrigTitle()
        return title
    
    def getFormattedTitle(self, media):
        """
        Returns back the modified title with episodes and seasons if there is
        
        If Season-Collector:
            "Season n" regardless the getTranslatedTitle()
        If MiniSeries (episode is set but the parent Collector has no season):
            If keep-hierarchy:
                getTranslatedTitle() - Part n
            else
                parentCollector.getTranslatedTitle() - getTranslatedTitle() - Part n
        If Series (episode is set and parentCollector has season):
            If keep-hierarchy:
                S{season}E{episode} - getTranslatedTitle()
            else
                SeriesTitle - S{season}E{episode} - getTranslatedTitle()
        """
        formatted_title = self.getTranslatedTitle()
        
        episode = media.general.getEpisode()
        season = media.general.getSeason()
        
        parent_collector = media.getParentCollector()
        
        if parent_collector:
            parent_season = parent_collector.general.getSeason()
        
            # Season-Collector
            if season:
                formatted_title = _("title_season").format(season)
        
            # Miniseries
            elif episode and not parent_season:
                formatted_title = formatted_title + "-" + _("title_part").format(episode)

                parent_title = parent_collector.getTranslatedTitle()
                        
                # bulk list - The series title is not visible and 
                # the raw title of the episode is not the same as the row title of the Container's title - you have to attache it
                if config_ini["keep_hierarchy"] == "n" and parent_title != self.getTranslatedTitle():
                    formatted_title = parent_title + ": " + formatted_title
            # series
            elif episode and parent_season:
                formatted_title = "(S" + parent_season.zfill(2) + "E" + episode.zfill(2) + ") " + formatted_title

                parent_parent_collector = parent_collector.getParentCollector()
                series_title = parent_parent_collector.getTranslatedTitle()
            
                # bulk list - The series title is not visible - you have to attache it
                if config_ini["keep_hierarchy"] == "n":
                    formatted_title = series_title + ": " + formatted_title
            
        return formatted_title    
          
            
            
    
    def getJson(self):
        json = {}
        json.update({} if self.orig_title is None or not self.orig_title else {"orig": self.orig_title})
        
        json.update(
            {key: value for key, value in self.title_list_by_language.items()} if self.title_list_by_language else {}
            )
       
        return json
    
    
    def getWidget(self, media, scale):
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
        # media-{collector/storage}-{media}-{category}.png
        #
        iconFileName = TITLE_ICON_PREFIX + "-" + media.getFolderType() + ( "-" + media.control.getMedia() if media.control.getMedia() else "" ) + ( "-" + media.control.getCategory() if media.control.getCategory() else "" ) + "." + TITLE_ICON_EXTENSION
        pathToFile = resource_filename(__name__, os.path.join(TITLE_ICON_FOLDER, iconFileName))       
        pixmap = QPixmap( pathToFile )

        if pixmap.isNull():            
            smaller_pixmap = QPixmap(TITLE_ICON_HEIGHT * scale, TITLE_ICON_HEIGHT * scale)
            smaller_pixmap.fill(QColor(media.getBackgroundColor()))
        else:
            smaller_pixmap = pixmap.scaledToWidth(TITLE_ICON_HEIGHT * scale)
   
        iconWidget = QLabel()
        iconWidget.setPixmap(smaller_pixmap)

        title_layout.addWidget(iconWidget)

        #
        # Title
        #
        
#        season = media.general.getSeason()
#        episode = media.general.getEpisode()
        
        
        # Storage-Series/Miniseries
#        if episode:
            
        # Container
#        elif season:
        
        
        titleWidget = QLabel(self.getFormattedTitle(media))
        
#        titleWidget = QLabel(
#            ("S" + season + "E" + episode + "-" if episode is not None and season is not None else "") + 
#            self.getTranslatedTitle() + 
#            ("-"+_("title_part").format(episode) if episode is not None and season is None else "") )
        titleWidget.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale * 1.8, weight=QFont.Bold))

        title_layout.addWidget(titleWidget)
        return widget
    
    
    
    
