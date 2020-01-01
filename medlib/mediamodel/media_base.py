import locale

from medlib.constants import PANEL_HEIGHT

from builtins import object

from medlib.mediamodel.ini_general import IniGeneral
from medlib.mediamodel.ini_classification import IniClassification
from medlib.mediamodel.ini_titles import IniTitles
from medlib.mediamodel.ini_control import IniControl

from medlib.mediamodel.media_appendix import MediaAppendix

from medlib.mediamodel.extra import QHLine

from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QWidget

from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPixmap

from PyQt5.QtCore import Qt

from medlib.card_ini import JSON_SECTION_TITLES
from medlib.card_ini import JSON_SECTION_GENERAL
from medlib.card_ini import JSON_SECTION_STORYLINE
from medlib.card_ini import JSON_SECTION_TOPIC
from medlib.card_ini import JSON_SECTION_LYRICS
from medlib.card_ini import JSON_SECTION_CLASSIFICATION
from medlib.card_ini import JSON_SECTION_CONTROL
from medlib.card_ini import JSON_NODE_APPENDIXES

class MediaBase(object):
    """
    This object represents the MediaBase
    """
   
    @staticmethod
    def sort_key(arg):
        """
        """
        return locale.strxfrm(arg.getTranslatedTitle()) if arg.control.getOrderBy() == 'title' else arg.getNameOfFolder() if arg.control.getOrderBy() == 'folder' else arg.getNameOfFolder() 
    
    def __init__(self, titles, control, general=None, classification=None):
        """
        This is the constructor of the MediaCollector
        ________________________________________
        input:
                titles             IniTitles         represents the [titles] section
                control            IniControl        represents the [control] section
                general            IniGeneral        represents the [general] section
                classification     IniClassification represents the [classification] section
        """
        super().__init__()
        
        NoneType = type(None)
        assert issubclass(titles.__class__, IniTitles)
        assert issubclass(control.__class__, IniControl)
        assert issubclass(general.__class__, (IniGeneral, NoneType)), general.__class__
        assert issubclass(classification.__class__, (IniClassification, NoneType)), classification.__class__
        
        self.parentCollector = None
        self.mediaAppendixList = []
        self.titles = titles
        self.control = control
        self.general = general if general else IniGeneral()
        self.classification = classification if classification else IniClassification()
        
        self.neededTagField = False
        self.widget = None
#        self.searchFunction = None

    def search(self, withShift, forWho, byWhat):
        """
        searchFunction( forWho, byWhat )    - A search function when you click on a link on the card.
                                              For example on a Director or Actor ...
                                              It has two parameters:
                                                -forWho is the text you clicked on
                                                -byWhat is the title_id of the group. for example for the
                                                 directors: title_director or actors: title_actor ...
        """
        print("Search for '" + forWho + "' by " + byWhat, "With Shift" if withShift else "")
        
    def getRoot(self):
        """
            Gives back the root of the media hierarchy
            Basically it is a MediaCollector
        """
        pc = self.getParentCollector()
        if pc:
            return pc.getRoot()
        else:
            return self
        
        
 #   def setSearchFunction(self, searchFunction ):
 #       """
 #           searchFunction( forWho, byWhat )    - A search function when you click on a link on the card.
 #                                                 For example on a Director or Actor ...
 #                                                 It has two parameters:
 #                                                 -forWho is the text you clicked on
 #                                                 -byWhat is the title_id of the group. for example for the
 #                                                  directors: title_director or actors: title_actor ...
 #       """
 #       self.searchFunction = searchFunction

    def getParentCollector(self):
        return self.parentCollector
        
    def setParentCollector(self, parentCollector):
        self.parentCollector = parentCollector
        
    def getNameOfFolder(self):
        raise NotImplementedError
        
    def getPathOfImage(self):
        raise NotImplementedError
    
    def getPathOfCard(self):
        raise NotImplementedError

    def getBackgroundColor(self):
        raise NotImplementedError
    
    def getFolderType(self):
        raise NotImplementedError
            
    def getTranslatedTitle(self):
        return self.titles.getTranslatedTitle()
    
    def getTranslatedStoryline(self, storyline):
        return storyline.getTranslatedStoryline()

    def getTranslatedGenreList(self):
        return self.general.getTranslatedGenreList(self.control.getCategory())
    
    def getTranslatedThemeList(self):
        return self.general.getTranslatedThemeList()

    def getTitles(self):
        """
        Returns back the [titles] section.
        _________________________________________________________________________________________________
        input:
        output:
                titles       IniTitles
        """
        return self.titles
    
    def getControl(self):
        """
        Returns back the [control] section.
        _________________________________________________________________________________________________
        input:
        output:
                control       IniControl
        """
        return self.control
    
    def getGeneral(self):
        """
        Returns back the [general] section.
        _________________________________________________________________________________________________
        input:
        output:
                general       IniGeneral
        """
        return self.general

    def getClassification(self):
        """
        Returns back the [classification] section.
        _________________________________________________________________________________________________
        input:
        output:
                general       IniClassification
        """
        return self.classification

    def addMediaAppendix(self, mediaAppendix):
        """
        Adds a new MediaAppendix to this MediaStorage
        It is ordered accordingly the language by the control.orderby
        _____________________________________________________________
        input:
                mediaAppendix    MediaAppendix    the MediaAppendix to add
        """
        
        assert issubclass(mediaAppendix.__class__, MediaAppendix), mediaAppendix.__class__

        # Add the MediaStorage
        self.mediaAppendixList.append(mediaAppendix)
        
        # Sort the list
        #self.sortMediaStorage()        

    # --------------------------------------------
    # --------------- Image ---------------------
    # --------------------------------------------
    def getWidgetImage(self, scale):

        # layout of this widget => three columns
        image_layout = QHBoxLayout()
        
        # space between the three grids
        image_layout.setSpacing(1)
        
        # margin around the widget
        image_layout.setContentsMargins(0, 0, 0, 0)
        
        widget = self.getQLabelToKeepImage()
        widget.setStyleSheet('background: black')
        widget.setAlignment(Qt.AlignCenter)
        widget.setLayout(image_layout)

        pixmap = QPixmap( self.getPathOfImage( ) )

        # if card image was not found
        if pixmap.isNull():            

            # then a blank image appears
            smaller_pixmap = QPixmap(PANEL_HEIGHT * scale, PANEL_HEIGHT * scale)
            smaller_pixmap.fill(QColor('gray'))
        elif pixmap.width() >= pixmap.height():
            smaller_pixmap = pixmap.scaledToWidth(PANEL_HEIGHT * scale)
        else:
            smaller_pixmap = pixmap.scaledToHeight(PANEL_HEIGHT * scale)

        widget.setMinimumWidth(PANEL_HEIGHT * scale)
        widget.setPixmap(smaller_pixmap)
        
        return widget         
        
    # --------------------------------------------
    # ------------- Middle - Text part -----------
    # --------------------------------------------
    def getWidgetCardInformationText(self, scale):
        """  _________________________________________
            |  Title                                  |
            |_________________________________________|       
            |  One line Info                          |
            |_________________________________________|       
            |  General Info                           |
            |_________________________________________|
            |  Media Appendix                         |
            |_________________________________________|            
        """
        
        # layout of this widget => three columns
        cardinfo_layout = QVBoxLayout()
        cardinfo_layout.setAlignment(Qt.AlignTop)
        
        # space between the three grids
        cardinfo_layout.setSpacing(1)
        
        # margin around the widget
        cardinfo_layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(cardinfo_layout)

        # --- TITLE ---
        #  _________________________________________
        # | Icon | Title                            |
        # |______|__________________________________|
        #
        cardinfo_layout.addWidget(self.titles.getWidget(self, scale))
        cardinfo_layout.addWidget(QHLine())
        
        # --- ONLINE INFO ---"
        #  _________________________________________
        # | Year: Length: Country: Sound: Sutitle:  |
        # |_________________________________________|
        #
        cardinfo_layout.addWidget(self.general.getWidgetOneLine(self, scale))
        
        # --- GENERAL INFO ---
        #  ___________________________________________________________________________
        # | Director/Maker:                             |                             |
        # |                                             |                             |
        # | Writer/Author:                              |                             |
        # |                                             |                             |
        # | Actor/Performer/Lecturer/Contributor/Voice: |                             |
        # |                                             |                             |
        # | Genre :                                     |                             |
        # |                                             |                             |
        # | Theme:                                      |                             |
        # |_____________________________________________|_____________________________|
        # | Storyline/Topic/Lyrics/-:                   |                             |
        # |_____________________________________________|_____________________________|
        # | Tags:                                       |                             |
        # |_____________________________________________|_____________________________|
        #
        cardinfo_layout.addWidget(self.general.getWidget(self, scale))

        # --- MEDIA APPENDIX ---        
        cardinfo_layout.addWidget(self.getWidgetMediaAppendix(scale))
        
        # --- Stretch ---
#        cardinfo_layout.addStretch(1)
#        label = QLabel()
#        label.setMinimumHeight(0)
#        label.setFixedHeight(0)
#        cardinfo_layout.addWidget(label)        
        
        return widget

    def getWidgetMediaAppendix(self, sizeRate):
        """
            Media Appendix
        """
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        widget = QWidget()
        widget.setLayout(layout)
        
        if self.getMediaAppendixList():
            layout.addWidget(QHLine())

        for media_appendix in self.getMediaAppendixList():
            layout.addWidget(media_appendix.getWidget(sizeRate))
        
        return widget
    
    # --------------------------------------------
    # ----------------- STORYLINE ----------------
    # --------------------------------------------
    def addWidgetGeneralInfoStoryline(self, parent, sizeRate, grid_layout, row, title_id, value):
        raise NotImplementedError
        return row   

    # --------------------------------------------
    # ----------------- Rating -------------------
    # --------------------------------------------
    def getWidgetClassification(self, scale):
        """   __________
             | Rate     |
             |__________|
             | Favorite |            
             |__________|
             | New      |
             |__________|
        """
        return self.classification.getWidget(self, scale)
    
    # --------------------------------------------
    # --------------------------------------------
    # --------------- WIDGET -------------------
    # --------------------------------------------
    # --------------------------------------------
    def getWidget(self, scale):
        """  ___________________________________________
            |         |                        |        |
            |         |                        |        |
            |  Image  |  Card Information Text | Rating |
            |         |                        |        |
            |_________|________________________|________|
        """

        # layout of this widget => three columns
        grid_layout = QGridLayout()

        # space between the three grids
        grid_layout.setSpacing(10)
        
        # margin around the widget
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        # stretch out the middle part
        grid_layout.setColumnStretch(1, 1)

        widget = QWidget()
        widget.setStyleSheet('background: ' + self.getBackgroundColor())
        widget.setLayout(grid_layout)
        
        # --- Image ---
        grid_layout.addWidget(self.getWidgetImage(scale), 0, 0)
        
        # --- Card Information ---
        grid_layout.addWidget(self.getWidgetCardInformationText(scale), 0, 1)
        
        # --- Rating ---
        grid_layout.addWidget(self.getWidgetClassification(scale), 0, 2)
        
        self.widget = widget
        self.layout = grid_layout
        
        return widget
    
    def reGenerate(self, scale):

        layout = self.layout
        
        # delete all widgets
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().deleteLater()

        # --- Image ---
        layout.addWidget(self.getWidgetImage(scale), 0, 0)
        
        # --- Card Information ---
        layout.addWidget(self.getWidgetCardInformationText(scale), 0, 1)
        
        # --- Classification ---
        layout.addWidget(self.getWidgetClassification(scale), 0, 2)
        
        if self.isNeededTagField():
            self.classification.setFocusTagField(True)

    def setNeededTagField(self, value):
        self.neededTagField = value
        
    def isNeededTagField(self):
        return self.neededTagField
    
    def getMediaAppendixList(self):
        return self.mediaAppendixList

    def getQLabelToKeepImage(self):
        raise NotImplementedError
    
    def setNextLevelListener(self, nextLevelListener):
        raise NotImplementedError
    
    # TODO    
    def isSelected(self):
        """
            It indicates that the actual media (MediaCollector/MediaStorage) is selected to 
            be controlled by mouse.
            Practically it means that the media is a Card, and the Card is in the foreground
        """
        return True
    
    def getJson(self):
        json = {}
        
        json.update({JSON_SECTION_TITLES: self.titles.getJson()} if self.titles.getJson() else {})
        json.update({JSON_SECTION_GENERAL: self.general.getJson()} if self.general.getJson() else {})

        json.update({JSON_SECTION_STORYLINE: self.general.getStoryline().getJson()} if self.general.getStoryline().getJson() else {})
        json.update({JSON_SECTION_TOPIC: self.general.getTopic().getJson()} if self.general.getTopic().getJson() else {})
        json.update({JSON_SECTION_LYRICS: self.general.getLyrics().getJson()} if self.general.getLyrics().getJson() else {})

        json.update({JSON_SECTION_CLASSIFICATION: self.classification.getJson()} if self.classification.getJson() else {})
        json.update({JSON_SECTION_CONTROL: self.control.getJson()} if self.control.getJson() else {})
        
        json.update({JSON_NODE_APPENDIXES: [c.getJson() for c in self.mediaAppendixList]} if self.mediaAppendixList else {}) 
        
        return json
    
    