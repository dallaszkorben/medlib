import locale
import os

from pkg_resources import resource_filename

from medlib.constants import *
from medlib.handle_property import _
from builtins import object

from medlib.mediamodel.ini_general import IniGeneral
from medlib.mediamodel.ini_storylines import IniStorylines
from medlib.mediamodel.ini_rating import IniRating
from medlib.mediamodel.extra import QHLine, FlowLayout

from PyQt5.QtWidgets import QGridLayout, QSpinBox
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QAbstractSpinBox
from PyQt5.QtWidgets import QApplication

from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPixmap

from PyQt5.QtCore import Qt 

class MediaBase(object):
    """
    This object represents the MediaBase
    """
   
    @staticmethod
    def sort_key(arg):
        """
        """
        return locale.strxfrm(arg.getTranslatedTitle()) if arg.control.getOrderBy() == 'title' else arg.container_paths.getNameOfFolder() if arg.control.getOrderBy() == 'folder' else arg.container_paths.getNameOfFolder() 
    
    def __init__(self, titles, control, general=None, storylines=None,  rating=None):
        """
        This is the constructor of the MediaCollector
        ________________________________________
        input:
                titles            IniTitles         represents the [titles] section
                control           IniControl        represents the [control] section
                general           IniGeneral        represents the [general] section
                storylines        IniStorylines     represents the [storyline] section
                rating            IniRating         represents the [rating] section
        """
        super().__init__()
        self.titles = titles
        self.control = control
        self.general = general if general else IniGeneral()
        self.storylines = storylines if storylines else IniStorylines()
        self.rating = rating if rating else IniRating()
    
    def getPathOfImage(self):
        raise NotImplementedError

    def getBackgroundColor(self):
        raise NotImplementedError
    
    def getFolderType(self):
        raise NotImplementedError
            
    def getTranslatedTitle(self):
        return self.titles.getTranslatedTitle()
    
    def getTranslatedStoryline(self):
        return self.storylines.getTranslatedStoryline()
   
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

    def getStorylines(self):
        """
        Returns back the [storylines] section.
        _________________________________________________________________________________________________
        input:
        output:
                storylines       IniStoryline
        """
        return self.storylines

    def getRating(self):
        """
        Returns back the [rating] section.
        _________________________________________________________________________________________________
        input:
        output:
                general       IniRating
        """
        return self.rating
        
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
        
        widget = QLabel()
        widget.setStyleSheet('background: black')
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
   
        widget.setPixmap(smaller_pixmap)
        
        return widget         
        
    # --------------------------------------------
    # ------------- Middle - Text part -----------
    # --------------------------------------------
    def getWidgetCardInformationText(self, sizeRate):
        
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
        
        return widget

    # --------------------------------------------
    # ---------------- Title ---------------------
    # --------------------------------------------
    def getWidgetTitle(self, sizeRate):
        title_layout = QHBoxLayout()
        title_layout.setAlignment(Qt.AlignLeft)
        
        # space between the three grids
        title_layout.setSpacing(1)
        
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
        titleWidget = QLabel(self.titles.getTranslatedTitle())
        titleWidget.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate * 1.8, weight=QFont.Bold))

        title_layout.addWidget(titleWidget)
        return widget                 
        
        
    # --------------------------------------------
    # ----------- OneLineInfo -----------------
    # --------------------------------------------
    def getWidgetOneLineInfo(self, sizeRate):
                
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
        sound_list = ", ".join( [ _("lang_" + c) for c in self.general.getSounds()])        
        
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
 
        # --- DIRECTORS ---       
        row = self.addWidgetGeneralInfoDirectors(sizeRate, grid_layout, row)

        # --- WRITERS ---       
        row = self.addWidgetGeneralInfoWriters(sizeRate, grid_layout, row)

        # --- ACTORS ---       
        row = self.addWidgetGeneralInfoActors(sizeRate, grid_layout, row)

        # --- GEMRE ---       
        row = self.addWidgetGeneralInfoGenres(sizeRate, grid_layout, row)

        # --- THEME ---       
        row = self.addWidgetGeneralInfoThemes(sizeRate, grid_layout, row)
        
        # --- STORILINES ---
        row = self.addWidgetGeneralInfoStoryline(widget, sizeRate, grid_layout, row)
                
        return widget

    # #########
    # Directors 
    # #########
    def addWidgetGeneralInfoDirectors(self, sizeRate, grid_layout, row):
       
        widget_key = QLabel(_('title_director') + ":", )
        widget_key.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Bold))
        
        layout_directors = QHBoxLayout()
        layout_directors.setAlignment(Qt.AlignLeft)        
        layout_directors.setSpacing(1)        
        layout_directors.setContentsMargins(0, 0, 0, 0)

        widget_value = QWidget()
        widget_value.setLayout( layout_directors )
        widget_value.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Normal))
        first = True
        for d in self.general.getDirectors():
            if not first:
                layout_directors.addWidget( QLabel(", ") )
            label = QLabel(d)
            layout_directors.addWidget(label)
            first = False

        if self.general.getDirectors():
            grid_layout.addWidget(widget_key, row, 0)
            grid_layout.addWidget(widget_value, row, 1)
            row = row + 1
            
        return row   

    # #########
    # Writers 
    # #########
    def addWidgetGeneralInfoWriters(self, sizeRate, grid_layout, row):
       
        widget_key = QLabel(_('title_writer') + ":", )
        widget_key.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Bold))
        
        layout_directors = QHBoxLayout()
        layout_directors.setAlignment(Qt.AlignLeft)        
        layout_directors.setSpacing(1)        
        layout_directors.setContentsMargins(0, 0, 0, 0)

        widget_value = QWidget()
        widget_value.setLayout( layout_directors )
        widget_value.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Normal))
        first = True
        for d in self.general.getWriters():
            if not first:
                layout_directors.addWidget( QLabel(", ") )
            label = QLabel(d)
            layout_directors.addWidget(label)
            first = False
        
        if self.general.getWriters():
            grid_layout.addWidget(widget_key, row, 0)
            grid_layout.addWidget(widget_value, row, 1)
            row = row + 1
            
        return row

    # #########
    # Actors 
    # #########
    def addWidgetGeneralInfoActors(self, sizeRate, grid_layout, row):
       
        widget_key = QLabel(_('title_actor') + ":", )
        widget_key.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Bold))
        widget_key.setAlignment(Qt.AlignTop)
        
        layout_actors = FlowLayout()
        layout_actors.setAlignment(Qt.AlignLeft)        
        layout_actors.setSpacing(1)        
        layout_actors.setContentsMargins(0, 0, 0, 0)

        widget_value = QWidget()
        widget_value.setLayout( layout_actors )
        widget_value.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Normal))
        first = True
        for d in self.general.getActors():
            if not first:
                layout_actors.addWidget( QLabel(", ") )
            label = QLabel(d)
            layout_actors.addWidget(label)
            first = False
        
        if self.general.getActors():
            grid_layout.addWidget(widget_key, row, 0)
            grid_layout.addWidget(widget_value, row, 1)
            row = row + 1
            
        return row

    # #########
    # Genre 
    # #########
    def addWidgetGeneralInfoGenres(self, sizeRate, grid_layout, row):
       
        widget_key = QLabel(_('title_genre') + ":", )
        widget_key.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Bold))
        
        layout_genres = QHBoxLayout()
        layout_genres.setAlignment(Qt.AlignLeft)        
        layout_genres.setSpacing(1)        
        layout_genres.setContentsMargins(0, 0, 0, 0)

        widget_value = QWidget()
        widget_value.setLayout( layout_genres )
        widget_value.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Normal))
        first = True
        for d in self.general.getGenres():
            if not first:
                layout_genres.addWidget( QLabel(", ") )
            label = QLabel(d)
            layout_genres.addWidget(label)
            first = False
        
        if self.general.getGenres():
            grid_layout.addWidget(widget_key, row, 0)
            grid_layout.addWidget(widget_value, row, 1)
            row = row + 1
            
        return row

    # #########
    # Theme 
    # #########
    def addWidgetGeneralInfoThemes(self, sizeRate, grid_layout, row):
       
        widget_key = QLabel(_('title_theme') + ":", )
        widget_key.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Bold))
        
        layout_themes = QHBoxLayout()
        layout_themes.setAlignment(Qt.AlignLeft)        
        layout_themes.setSpacing(1)        
        layout_themes.setContentsMargins(0, 0, 0, 0)

        widget_value = QWidget()
        widget_value.setLayout( layout_themes )
        widget_value.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Normal))
        first = True
        for d in self.general.getThemes():
            if not first:
                layout_themes.addWidget( QLabel(", ") )
            label = QLabel(d)
            layout_themes.addWidget(label)
            first = False
        
        if self.general.getThemes():
            grid_layout.addWidget(widget_key, row, 0)
            grid_layout.addWidget(widget_value, row, 1)
            row = row + 1
            
        return row
    
    # #########
    # Storiline
    # #########
    def addWidgetGeneralInfoStoryline(self, parent, sizeRate, grid_layout, row):
       
        widget_key = QLabel(_('title_storyline') + ":", )
        widget_key.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Bold))
        widget_key.setAlignment(Qt.AlignTop)

        widget_value = QPlainTextEdit(parent)
        widget_value.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Normal))
        widget_value.insertPlainText(self.getTranslatedStoryline())
        widget_value.setReadOnly(True)
        widget_value.setMinimumHeight( PANEL_FONT_SIZE * sizeRate )
        
        if self.getTranslatedStoryline():
            grid_layout.addWidget( widget_key, row, 0)
            grid_layout.addWidget( widget_value, row, 1)        
            row = row + 1
            
        return row   

    # --------------------------------------------
    # ----------------- Rating -------------------
    # --------------------------------------------
    def getWidgetRatingInfo(self, sizeRate):
        
        # layout of this widget => three columns
        rating_layout = QVBoxLayout()
        rating_layout.setAlignment(Qt.AlignTop)
        
        # space between the three grids
        rating_layout.setSpacing(1)
        
        # margin around the widget
        rating_layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(rating_layout)
        
        # --- RATE ---
        rating_layout.addWidget(self.getWidgetRatingInfoRate(sizeRate))
        
        # --- FAVORITE ---
        rating_layout.addWidget(self.getWidgetRatingInfoFavorite(sizeRate)) 

        # --- NEW ---
        rating_layout.addWidget(self.getWidgetRatingInfoNew(sizeRate)) 
        
        return widget

    def getWidgetRatingInfoRate( self, sizeRate ):
        
        class MySpinBox(QSpinBox):
            #def __init__(self, card_panel):
            def __init__(self):
                super().__init__()
        
                #self.card_panel = card_panel
        
                self.setButtonSymbols(QAbstractSpinBox.NoButtons) #PlusMinus / NoButtons / UpDownArrows        
                self.setMaximum(10)
                self.setFocusPolicy(Qt.NoFocus)
                self.lineEdit().setReadOnly(True)
                self.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Normal))
                self.lineEdit().setStyleSheet( "QLineEdit{color:black}")
                self.setStyleSheet( "QSpinBox{background:'" + RATE_BACKGROUND_COLOR + "'}")

            def stepBy(self, steps):
                """
                It needs to be override to make deselection after the step.
                If it it not there, the selection color (blue) will be appear on the field
                """
                super().stepBy(steps)
                self.lineEdit().deselect()

            # Mouse Hover in
            def enterEvent(self, event):
                self.update()
                QApplication.setOverrideCursor(Qt.PointingHandCursor)

                self.setButtonSymbols(QAbstractSpinBox.PlusMinus) #PlusMinus / NoButtons / UpDownArrows        

#                self.card_panel.get_card_holder().setFocus()
                event.ignore()

            # Mouse Hover out
            def leaveEvent(self, event):
                self.update()
                QApplication.restoreOverrideCursor()

                self.setButtonSymbols(QAbstractSpinBox.NoButtons) #PlusMinus / NoButtons / UpDownArrows        
        
#                self.card_panel.get_card_holder().setFocus()
                event.ignore()

        widget = MySpinBox()        
        return widget
        
    def getWidgetRatingInfoFavorite(self, sizeRate):
        iconFileName = RATING_ICON_PREFIX + "-" + RATING_ICON_FAVORITE_TAG + "-" + ON + "." + RATING_ICON_EXTENSION
        pathToFile = resource_filename(__name__, os.path.join(RATING_ICON_FOLDER, iconFileName))       
        pixmap_on = QPixmap( pathToFile )

        iconWidget = QLabel()
        iconWidget.setPixmap(pixmap_on)
        return iconWidget

    def getWidgetRatingInfoNew(self, sizeRate):
        iconFileName = RATING_ICON_PREFIX + "-" + RATING_ICON_NEW_TAG + "-" + ON + "." + RATING_ICON_EXTENSION
        pathToFile = resource_filename(__name__, os.path.join(RATING_ICON_FOLDER, iconFileName))       
        pixmap_on = QPixmap( pathToFile )

        iconWidget = QLabel()
        iconWidget.setPixmap(pixmap_on)
        return iconWidget

        
    # --------------------------------------------
    # --------------------------------------------
    # --------------- WIDGET -------------------
    # --------------------------------------------
    # --------------------------------------------
    def getWidget(self, sizeRate):

        # layout of this widget => three columns
        grid_layout = QGridLayout()

        # space between the three grids
        grid_layout.setSpacing(1)
        
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
    