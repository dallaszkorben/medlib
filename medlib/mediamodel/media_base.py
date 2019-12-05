import locale
import os

from pkg_resources import resource_filename

from medlib.constants import *
from medlib.handle_property import _
from builtins import object

from medlib.mediamodel.ini_general import IniGeneral
from medlib.mediamodel.ini_rating import IniRating
from medlib.mediamodel.ini_titles import IniTitles
from medlib.mediamodel.ini_control import IniControl

from medlib.mediamodel.media_appendix import MediaAppendix

from medlib.mediamodel.extra import QHLine, FlowLayout

from medlib.mediamodel.qlabel_to_link_on_cllick import QLabelToLinkOnClick

from PyQt5.QtWidgets import QGridLayout, QSpinBox
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QAbstractSpinBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton

from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QTextCursor
from PyQt5.QtGui import QCursor

from PyQt5.QtCore import Qt , QSize

from PyQt5.Qt import QIcon

class MediaBase(object):
    """
    This object represents the MediaBase
    """
   
    @staticmethod
    def sort_key(arg):
        """
        """
        return locale.strxfrm(arg.getTranslatedTitle()) if arg.control.getOrderBy() == 'title' else arg.getNameOfFolder() if arg.control.getOrderBy() == 'folder' else arg.getNameOfFolder() 
    
    def __init__(self, titles, control, general=None, rating=None):
        """
        This is the constructor of the MediaCollector
        ________________________________________
        input:
                titles             IniTitles         represents the [titles] section
                control            IniControl        represents the [control] section
                general            IniGeneral        represents the [general] section
                rating             IniRating         represents the [rating] section
        """
        super().__init__()
        
        NoneType = type(None)
        assert issubclass(titles.__class__, IniTitles)
        assert issubclass(control.__class__, IniControl)
        assert issubclass(general.__class__, (IniGeneral, NoneType)), general.__class__
        assert issubclass(rating.__class__, (IniRating, NoneType)), rating.__class__
        
        self.parentCollector = None
        self.mediaAppendixList = []
        self.titles = titles
        self.control = control
        self.general = general if general else IniGeneral()
        self.rating = rating if rating else IniRating()
        
        self.searchFunction = None

    def setSearchFunction(self, searchFunction ):
        """
            searchFunction( forWho, byWhat )    - A search function when you click on a link on the card.
                                                  For example on a Director or Actor ...
                                                  It has two parameters:
                                                  -forWho is the text you clicked on
                                                  -byWhat is the title_id of the group. for example for the
                                                   directors: title_director or actors: title_actor ...
        """
        self.searchFunction = searchFunction

    def getParentCollector(self):
        return self.parentCollector
        
    def setParentCollector(self, parentCollector):
        self.parentCollector = parentCollector
        
    def getNameOfFolder(self):
        raise NotImplementedError
        
    def getPathOfImage(self):
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

    def getRating(self):
        """
        Returns back the [rating] section.
        _________________________________________________________________________________________________
        input:
        output:
                general       IniRating
        """
        return self.rating

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
    def getWidgetImage(self, sizeRate):

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
            # then a blanc image appears
            smaller_pixmap = QPixmap(PANEL_HEIGHT * sizeRate, PANEL_HEIGHT * sizeRate)
            smaller_pixmap.fill(QColor('gray'))
        elif pixmap.width() >= pixmap.height():
            smaller_pixmap = pixmap.scaledToWidth(PANEL_HEIGHT * sizeRate)
        else:
            smaller_pixmap = pixmap.scaledToHeight(PANEL_HEIGHT * sizeRate)

        widget.setMinimumWidth(PANEL_HEIGHT * sizeRate)
        widget.setPixmap(smaller_pixmap)
        
        return widget         
        
    # --------------------------------------------
    # ------------- Middle - Text part -----------
    # --------------------------------------------
    def getWidgetCardInformationText(self, sizeRate):
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
        cardinfo_layout.addWidget(self.getWidgetTitle(sizeRate))
        cardinfo_layout.addWidget(QHLine())
        
        # --- ONLINE INFO ---"
        cardinfo_layout.addWidget(self.getWidgetOneLineInfo(sizeRate))
        
        # --- GENERAL INFO ---
        cardinfo_layout.addWidget(self.getWidgetGeneralInfo(sizeRate))

        # --- MEDIA APPENDIX ---        
        cardinfo_layout.addWidget(self.getWidgetMediaAppendix(sizeRate))
        
        # --- Stretch ---
        cardinfo_layout.addStretch(1)
        label = QLabel()
        label.setMinimumHeight(0)
        label.setFixedHeight(0)
        cardinfo_layout.addWidget(label)        
        
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
    # ---------------- Title ---------------------
    # --------------------------------------------
    def getWidgetTitle(self, sizeRate):
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
        iconFileName = TITLE_ICON_PREFIX + "-" + self.getFolderType() + "-" + self.control.getMedia() + "-" + self.control.getCategory() + "." + TITLE_ICON_EXTENSION
        pathToFile = resource_filename(__name__, os.path.join(TITLE_ICON_FOLDER, iconFileName))       
        pixmap = QPixmap( pathToFile )

        if pixmap.isNull():            
            smaller_pixmap = QPixmap(TITLE_ICON_HEIGHT * sizeRate, TITLE_ICON_HEIGHT * sizeRate)
            smaller_pixmap.fill(QColor(self.getBackgroundColor()))
        else:
            smaller_pixmap = pixmap.scaledToWidth(TITLE_ICON_HEIGHT * sizeRate)
   
        iconWidget = QLabel()
        iconWidget.setPixmap(smaller_pixmap)

        title_layout.addWidget(iconWidget)

        #
        # Title
        #
        
        series = self.general.getSeries()
        episode = self.general.getEpisode()
        titleWidget = QLabel(
            ("S" + series + "E" + episode + "-" if episode is not None and series is not None else "") + 
            self.titles.getTranslatedTitle() + 
            ("-"+_("title_part").format(episode) if episode is not None and series is None else "") )
        titleWidget.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate * 1.8, weight=QFont.Bold))

        title_layout.addWidget(titleWidget)
        return widget
        
    # --------------------------------------------
    # ----------- OneLineInfo -----------------
    # --------------------------------------------
    def getWidgetOneLineInfo(self, sizeRate):
        """  _________________________________________
            | Year: Length: Country: Sound: Sutitle:  |
            |_________________________________________|
        """                
        layout = QGridLayout()
        
        layout.setSpacing(1)
        
        layout.setContentsMargins(0, 0, 0, 0)

        widget = QWidget()
        #widget.setStyleSheet('background: ' + self.getBackgroundColor())
        widget.setLayout(layout)
        widget.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Normal))

        layout.addWidget(self.getWidgetOneLineInfoYear(sizeRate), 0, 0)

        layout.addWidget(self.getWidgetOneLineInfoLength(sizeRate), 0, 1)
        
        layout.addWidget(self.getWidgetOneLineInfoCountries(sizeRate), 0, 2)
        
        layout.addWidget(self.getWidgetOneLineInfoSounds(sizeRate), 0, 3)
        
        layout.addWidget(self.getHtmlOneLineInfoSubs(sizeRate), 0, 4)
        
        if layout.sizeHint().height() > 0:
            layout.addWidget(QHLine(), 1, 0, 1, 5)

        return widget
    
    def getWidgetOneLineInfoYear(self, sizeRate):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)        
        layout.setSpacing(1)        
        layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(layout)
        
        if self.general.getYear():

            key_label = QLabel(_('title_year')  + ": ")
            layout.addWidget(key_label)
        
            value_label = QLabel(self.general.getYear())
            value_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Bold))
            layout.addWidget(value_label)
        
        return widget
        
    def getWidgetOneLineInfoLength(self, sizeRate):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)        
        layout.setSpacing(1)        
        layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(layout)
        
        if self.general.getLength():

            key_label = QLabel(_('title_length')  + ": ")
            layout.addWidget(key_label)
        
            value_label = QLabel(self.general.getLength())
            value_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Bold))
            layout.addWidget(value_label)
        
        return widget
    
        
    def getWidgetOneLineInfoCountries(self, sizeRate):
        country_list = ", ".join( [ _("country_" + c) for c in self.general.getCountries()])
        
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)        
        layout.setSpacing(1)        
        layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(layout)
        
        if country_list:

            key_label = QLabel(_('title_country')  + ": ")
            layout.addWidget(key_label)
        
            value_label = QLabel(country_list)
            value_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Bold))
            layout.addWidget(value_label)
        
        return widget
        
    def getWidgetOneLineInfoSounds(self, sizeRate):
        sound_list = self.general.getTranslatedSoundStringList()
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)        
        layout.setSpacing(1)        
        layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(layout)
        
        if sound_list:

            key_label = QLabel( _('title_sound')  + ": ")
            layout.addWidget(key_label)
        
            value_label = QLabel(sound_list)
            value_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Bold))
            layout.addWidget(value_label)
        return widget
        
    def getHtmlOneLineInfoSubs(self, sizeRate):
        sub_list = ", ".join( [ _("lang_" + c) for c in self.general.getSubs()])
        
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)        
        layout.setSpacing(1)        
        layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(layout)
        
        if sub_list:

            key_label = QLabel( _('title_sub')  + ": ")
            layout.addWidget(key_label)
        
            value_label = QLabel(sub_list)
            value_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Bold))
            layout.addWidget(value_label)
        return widget
 
    # --------------------------------------------
    # ------------GENERAL INFORMATION ------------
    # --------------------------------------------
    def getWidgetGeneralInfo(self, sizeRate):
        """  ___________________________________________________________________________
            | Director/Maker:                             |                             |
            |                                             |                             |
            | Writer/Author:                              |                             |
            |                                             |                             |
            | Actor/Performer/Lecturer/Contributor/Voice: |                             |
            |                                             |                             |
            | Genre :                                     |                             |
            |                                             |                             |
            | Theme:                                      |                             |
            |_____________________________________________|_____________________________|
            | Storyline/Topic/Lyrics/-:                   |                             |
            |_____________________________________________|_____________________________|
        """                

        grid_layout = QGridLayout()
        widget = QWidget()
        widget.setLayout(grid_layout)
        row = 0;
        
        # space between the three grids
        grid_layout.setSpacing(1)
        
        # margin around the widget
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # stretch out the 2nd column
        grid_layout.setColumnStretch(1, 1)

        #
        # TODO if by control.media / control.category 
        #
 
        # ---
        # --- DIRECTORS ---
        row = self.addWidgetGeneralInfoLinkList(sizeRate, grid_layout, row, 'title_director', self.general.getDirectors)

        # --- MAKER ---       
        row = self.addWidgetGeneralInfoLinkList(sizeRate, grid_layout, row, 'title_maker', self.general.getMakers)

        # ---
        # --- WRITERS ---
        row = self.addWidgetGeneralInfoLinkList(sizeRate, grid_layout, row, 'title_writer', self.general.getWriters)

        # --- AUTHORS ---
        row = self.addWidgetGeneralInfoLinkList(sizeRate, grid_layout, row, 'title_author', self.general.getAuthors)

        # ---
        # --- ACTORS ---       
        row = self.addWidgetGeneralInfoLinkList(sizeRate, grid_layout, row, 'title_actor', self.general.getActors)

        # --- PERFORMER ---       
        row = self.addWidgetGeneralInfoLinkList(sizeRate, grid_layout, row, 'title_performer', self.general.getPerformers)

        # --- LECTURER ---       
        row = self.addWidgetGeneralInfoLinkList(sizeRate, grid_layout, row, 'title_lecturer', self.general.getLecturers)

        # --- CONTRIBUTOR ---       
        row = self.addWidgetGeneralInfoLinkList(sizeRate, grid_layout, row, 'title_contributor', self.general.getContributors)

        # --- VOICE ---       
        row = self.addWidgetGeneralInfoLinkList(sizeRate, grid_layout, row, 'title_voice', self.general.getVoices)

        # ---
        # --- GEMRE ---       
        row = self.addWidgetGeneralInfoStringList(sizeRate, grid_layout, row, 'title_genre', self.getTranslatedGenreList)

        # ---
        # --- THEME ---       
        row = self.addWidgetGeneralInfoStringList(sizeRate, grid_layout, row, 'title_theme', self.getTranslatedThemeList)
        
        # ---
        # --- STORILINES ---
        row = self.addWidgetGeneralInfoStoryline(widget, sizeRate, grid_layout, row, 'title_storyline', self.getTranslatedStoryline(self.general.getStoryline()))

        # --- TOPIC ---
        row = self.addWidgetGeneralInfoStoryline(widget, sizeRate, grid_layout, row, 'title_topic', self.getTranslatedStoryline(self.general.getTopic()))

        # --- LYRICS ---
        row = self.addWidgetGeneralInfoStoryline(widget, sizeRate, grid_layout, row, 'title_lyrics', self.getTranslatedStoryline(self.general.getLyrics()))
                
        return widget

    # #####################################################################################
    # Link List - Director/Maker/Writer/Author/Actor/Performer/Lecturer/Contributor/Voice #
    # #####################################################################################
    def addWidgetGeneralInfoLinkList(self, sizeRate, grid_layout, row, title_id, value_method):
        value = value_method()

        if value:
        
            widget_key = QLabel(_(title_id) + ":", )
            widget_key.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Bold))
            widget_key.setAlignment(Qt.AlignTop)
        
            layout = FlowLayout()
            layout.setAlignment(Qt.AlignLeft)        
            layout.setSpacing(1)        
            layout.setContentsMargins(0, 0, 0, 0)

            widget_value = QWidget()
            widget_value.setLayout( layout )
            widget_value.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Normal))        
            first = True
            for d in value:
                if not first:
                    layout.addWidget( QLabel(", ") )
                label = MediaBase.QLabelWithLinkToSearch(self.isSelected, d, title_id, sizeRate)
                layout.addWidget(label)
                first = False

            grid_layout.addWidget(widget_key, row, 0)
            grid_layout.addWidget(widget_value, row, 1)
            row = row + 1
            
        return row   

    class QLabelWithLinkToSearch( QLabelToLinkOnClick ):

        def __init__(self, funcIsSelected, text, title_id, sizeRate):
            super().__init__(text, funcIsSelected)
            self.text = text
            self.title_id = title_id
            self.sizeRate = sizeRate
            self.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Normal))

        def toDoOnClick(self):
            if self.searchFunction is not None:
                self.searchFunction( self.text, self.title_id)
            print("Search for " + self.text + " by " + self.title_id)
            
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
   

    # ###########################
    # String List - Genre/Theme #
    # ###########################
    def addWidgetGeneralInfoStringList(self, sizeRate, grid_layout, row, title_id, value_method):
       
        element_list = value_method()
        
        if element_list:
            widget_key = QLabel(_(title_id) + ":", )
            widget_key.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Bold))
        
            layout_genres = QHBoxLayout()
            layout_genres.setAlignment(Qt.AlignLeft)
            layout_genres.setSpacing(1)        
            layout_genres.setContentsMargins(0, 0, 0, 0)

            widget_value = QWidget()
            widget_value.setLayout( layout_genres )
            widget_value.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Normal))
            first = True
            for d in element_list:
                if not first:
                    layout_genres.addWidget( QLabel(", ") )
                label = QLabel(d)
                layout_genres.addWidget(label)
                first = False
        
            grid_layout.addWidget(widget_key, row, 0)
            grid_layout.addWidget(widget_value, row, 1)
            row = row + 1
            
        return row
     
    # #########
    # Storyline
    # #########
    def addWidgetGeneralInfoStoryline(self, parent, sizeRate, grid_layout, row, title_id, value):
        raise NotImplementedError
        return row   

    # --------------------------------------------
    # ----------------- Rating -------------------
    # --------------------------------------------
    def getWidgetRatingInfo(self, sizeRate):
        """   __________
             | Rate     |
             |__________|
             | Favorite |            
             |__________|
             | New      |
             |__________|
        """        
        # layout of this widget => three columns
        rating_layout = QVBoxLayout()
        rating_layout.setAlignment(Qt.AlignTop)
        
        # space between the three grids
        rating_layout.setSpacing(20 * sizeRate)
        
        # margin around the widget
        rating_layout.setContentsMargins(0, 5, 5, 5)
        
        widget = QWidget()
        widget.setLayout(rating_layout)
        
        # --- RATE ---
        rating_layout.addWidget(self.getWidgetRatingInfoRate(sizeRate))
        
        # --- FAVORITE ---
        rating_layout.addWidget(self.getWidgetRatingInfoFavorite(sizeRate)) 

        # --- NEW ---
        rating_layout.addWidget(self.getWidgetRatingInfoNew(sizeRate)) 
        
        return widget

    #             #
    # Rating Rate #
    #             #
    def getWidgetRatingInfoRate( self, sizeRate ):
        
        class MySpinBox(QSpinBox):
            #def __init__(self, card_panel):
            def __init__(self, parent, sizeRate):
                super().__init__()
                self.parent = parent
        
                if self.parent.rating.getRate() is None:
                    self.hide()
                else:
                    self.setButtonSymbols(QAbstractSpinBox.NoButtons) #PlusMinus / NoButtons / UpDownArrows        
                    self.setMaximum(10)
                    self.setFocusPolicy(Qt.NoFocus)
                    self.lineEdit().setReadOnly(True)
                    self.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Normal))
                    self.lineEdit().setStyleSheet( "QLineEdit{color:black}")
                    self.setStyleSheet( "QSpinBox{background:'" + RATE_BACKGROUND_COLOR + "'}")
                    self.setValue(self.parent.rating.getRate())

            def stepBy(self, steps):
                """
                It needs to be override to make deselection after the step.
                If it is not there, the selection color (blue) will be appear on the field
                """
                super().stepBy(steps)
                self.lineEdit().deselect()

            # Mouse Hover in
            def enterEvent(self, event):
                self.update()
                QApplication.setOverrideCursor(Qt.PointingHandCursor)

                self.setButtonSymbols(QAbstractSpinBox.UpDownArrows) #PlusMinus / NoButtons / UpDownArrows        

#                self.card_panel.get_card_holder().setFocus()
                event.ignore()

            # Mouse Hover out
            def leaveEvent(self, event):
                self.update()
                QApplication.restoreOverrideCursor()

                self.setButtonSymbols(QAbstractSpinBox.NoButtons) #PlusMinus / NoButtons / UpDownArrows        
        
#                self.card_panel.get_card_holder().setFocus()
                event.ignore()

        widget = MySpinBox(self, sizeRate)        
        return widget
        
    #                 #
    # Rating Favorite #
    #                 #
    def getWidgetRatingInfoFavorite(self, sizeRate):
        class FavoriteButton(QPushButton):
            def __init__(self, parent, sizeRate):
                QPushButton.__init__(self)
                self.parent = parent
        
                if self.parent.rating.getFavorite() is None:
                    self.hide()
                else:
                    self.setCheckable(True)        
                    icon = QIcon()
                    icon.addPixmap(QPixmap( resource_filename(__name__, os.path.join(RATING_ICON_FOLDER, RATING_ICON_PREFIX + "-" + RATING_ICON_FAVORITE_TAG + "-" + ON + "." + RATING_ICON_EXTENSION)) ), QIcon.Normal, QIcon.On)
                    icon.addPixmap(QPixmap( resource_filename(__name__, os.path.join(RATING_ICON_FOLDER, RATING_ICON_PREFIX + "-" + RATING_ICON_FAVORITE_TAG + "-" + OFF + "." + RATING_ICON_EXTENSION)) ), QIcon.Normal, QIcon.Off)
                    self.setIcon(icon)
                    self.setIconSize(QSize(RATING_ICON_SIZE * sizeRate, RATING_ICON_SIZE * sizeRate))
                    self.setCursor(QCursor(Qt.PointingHandCursor))
                    self.setStyleSheet("background:transparent; border:none")
                    self.setChecked(self.parent.rating.getFavorite())
                    self.clicked.connect(self.ratingFavoriteButtonOnClick)

            def ratingFavoriteButtonOnClick(self):
                self.parent.rating.setFavorite(self.isChecked())        
        
        button = FavoriteButton(self, sizeRate)
        return button

    #            #
    # Rating New #
    #            #
    def getWidgetRatingInfoNew(self, sizeRate):
        class NewButton(QPushButton):
            def __init__(self, parent, sizeRate):
                QPushButton.__init__(self)    
                self.parent = parent

                if self.parent.rating.getNew() is None:
                    self.hide()
                else:        
                    self.setCheckable(True)        
                    icon = QIcon()
                    icon.addPixmap(QPixmap(resource_filename(__name__, os.path.join(RATING_ICON_FOLDER, RATING_ICON_PREFIX + "-" + RATING_ICON_NEW_TAG + "-" + ON + "." + RATING_ICON_EXTENSION))), QIcon.Normal, QIcon.On)
                    icon.addPixmap(QPixmap(resource_filename(__name__, os.path.join(RATING_ICON_FOLDER, RATING_ICON_PREFIX + "-" + RATING_ICON_NEW_TAG + "-" + OFF + "." + RATING_ICON_EXTENSION))), QIcon.Normal, QIcon.Off)
                    self.setIcon(icon)
                    self.setIconSize(QSize(RATING_ICON_SIZE * sizeRate, RATING_ICON_SIZE * sizeRate))
                    self.setCursor(QCursor(Qt.PointingHandCursor))
                    self.setStyleSheet("background:transparent; border:none")
                    self.setChecked(parent.rating.getNew())
                    self.clicked.connect(self.ratingNewButtonOnClick)
        
            def ratingNewButtonOnClick(self):
                self.parent.rating.setNew(self.isChecked())
        
        button = NewButton(self, sizeRate)
        return button
    
    # --------------------------------------------
    # --------------------------------------------
    # --------------- WIDGET -------------------
    # --------------------------------------------
    # --------------------------------------------
    def getWidget(self, sizeRate):
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
        grid_layout.addWidget(self.getWidgetImage(sizeRate), 0, 0)
        
        # --- Card Information ---
        grid_layout.addWidget(self.getWidgetCardInformationText(sizeRate), 0, 1)
        
        # --- Rating ---
        grid_layout.addWidget(self.getWidgetRatingInfo(sizeRate), 0, 2)
        
        return widget
    
    def getMediaAppendixList(self):
        return self.mediaAppendixList

    def getQLabelToKeepImage(self):
        raise NotImplementedError
    
    # TODO    
    def isSelected(self):
        """
            It indicates that the actual media (MediaCollector/MediaStorage) is selected to 
            be controlled by mouse.
            Practically it means that the media is a Card, and the Card is in the foreground
        """
        return True   
    
    