from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QApplication

from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPalette

from PyQt5.QtCore import Qt

from medlib.handle_property import _
from medlib.mediamodel.ini_storylines import IniStorylines
from medlib.mediamodel.extra import QHLine
from medlib.mediamodel.extra import FlowLayout

from medlib.constants import PANEL_FONT_TYPE
from medlib.constants import PANEL_FONT_SIZE

from builtins import object

from medlib.mediamodel.qlabel_to_link_on_cllick import QLabelToLinkOnClick

from medlib.card_ini import JSON_KEY_GENERAL_YEAR, JSON_KEY_GENERAL_PART,\
    JSON_KEY_GENERAL_DATE
from medlib.card_ini import JSON_KEY_GENERAL_BOOK
from medlib.card_ini import JSON_KEY_GENERAL_VOLUME
from medlib.card_ini import JSON_KEY_GENERAL_LENGTH
from medlib.card_ini import JSON_KEY_GENERAL_DIRECTOR
from medlib.card_ini import JSON_KEY_GENERAL_MAKER
from medlib.card_ini import JSON_KEY_GENERAL_WRITER
from medlib.card_ini import JSON_KEY_GENERAL_AUTHOR
from medlib.card_ini import JSON_KEY_GENERAL_ACTOR
from medlib.card_ini import JSON_KEY_GENERAL_PERFORMER
from medlib.card_ini import JSON_KEY_GENERAL_LECTURER
from medlib.card_ini import JSON_KEY_GENERAL_CONTRIBUTOR
from medlib.card_ini import JSON_KEY_GENERAL_INTERVIEWEE
from medlib.card_ini import JSON_KEY_GENERAL_INTERVIEWER
from medlib.card_ini import JSON_KEY_GENERAL_PRESENTER
from medlib.card_ini import JSON_KEY_GENERAL_ANCHOR
from medlib.card_ini import JSON_KEY_GENERAL_VOICE
from medlib.card_ini import JSON_KEY_GENERAL_SOUND
from medlib.card_ini import JSON_KEY_GENERAL_SUB
from medlib.card_ini import JSON_KEY_GENERAL_COUNTRY
from medlib.card_ini import JSON_KEY_GENERAL_GENRE
from medlib.card_ini import JSON_KEY_GENERAL_THEME
from medlib.card_ini import JSON_KEY_GENERAL_SEASON
from medlib.card_ini import JSON_KEY_GENERAL_EPISODE
from medlib.card_ini import JSON_KEY_GENERAL_ALBUM
from medlib.card_ini import JSON_KEY_GENERAL_TRACK
from medlib.card_ini import JSON_KEY_GENERAL_RECIPETYPE

import json

class IniGeneral(object):
    """
    This class represents the [general] section in the card.ini file

    """
    
    def __init__(self):
        """
        This is the constructor of the IniGeneral class
        _______________________________________________
        input:
            date             string             like "1987-12-21" or "2002/01/12" or "2020.11.06" 
            year             string             like "1987" or "1987-1988"
            
            directors        list of strings    ["Director 1", "Director 2"]
            makers           list of strings    ["Maker 1", "Maker 2"]            
            
            writers          list of strings    ["Writer 1", "Writer 2"]
            authors          list of strings    ["Author 1", "Author 2"]
            
            actors           list of strings    ["Actor 1", "Actor 2"]
            performers       list of strings    ["Performer 1", "Performer 2"]
            lecturer         list of strings    ["Lecturer 1", "Lecturer 2"]
            contributor      list of strings    ["Contributor 1", "Contributor 2"]
            interviewee      list of strings    ["Interviewee 1", "Interviewee 2"]
            interviewer      list of strings    ["Interviewer 1", "Interviewer 2"]
            anchor           list of strings    ["Anchor 1", "Anchor 2"]
            presenter        list of strings    ["Presenter 1", "Presenter 2"]

            voice            list of strings    ["Voice 1", "Voice 2"]
            
            length           string             "2:15"
            sounds           list of strings    ["en", "hu"]
            subs             list of strings    ["en", "hu"]
            genres           list of strings    ["drama", "action"]
            themes           list of strings    ["money", "greed"]
            recipeTypes      list of strings    ["chicken"]
            countries        list of strings    ["us", "ca"]
            
            storyline        storyLine
            topic            storyLine
            lyrics           storyLine
            
            season          integer       index of the season
            episode         integer       index of the episode
        """
        self.date = None
        self.year = None 
        self.directors = []
        self.makers = []
        self.writers = []
        self.authors = []
        self.actors = []
        self.performers = []
        self.lecturer = []
        self.contributor = []
        self.interviewee = []
        self.interviewer = []
        self.anchor = []
        self.voice = []
        self.presenter = []
        
        self.length = None
        self.sounds = []
        self.subs = []
        self.genres = []
        self.themes = []
        self.recipeTypes = []
        self.countries = []
        
        self.storyline = IniStorylines()
        self.topic = IniStorylines()
        self.lyrics = IniStorylines()
        self.ingredient = IniStorylines()
        self.method = IniStorylines()
        
        # Movie
        self.season = None        
        self.episode = None
        
        # Music
        self.album = None
        self.track = None

        # Book
        self.book = None
        self.volume = None
        
        self.part = None
    
    def __str__(self):
        return json.dumps(self.getJson(), indent=4, sort_keys=True)
#        return ("\n" + 
#            ("Storyline:   " + self.storyline.__str__() + "\n" if self.storyline.__str__() else "") +
#            ("Topic:       " + self.topic.__str__() + "\n" if self.topic.__str__() else "") +
#            ("Lyrics:      " + self.lyrics.__str__() + "\n" if self.lyrics.__str__() else "") +
#            "---\n" +
#            ("Year:        " + self.year + "\n" if self.year else "") +  
#            ("Director:    " + self.directors + "\n" if self.directors else "") +
#            ("Maker:       " + self.makers + "\n" if self.makers else "") +
#            ("Writer:      " + self.writers + "\n" if self.writers else "") +
#            ("Authoer:     " + self.authors + "\n" if self.authors else "") +
#            ("Actors:      " + self.actors + "\n" if self.actors else "") +
#            ("Performers:  " + self.performers + "\n" if self.performers else "") +
#            ("Lecturer:    " + self.lecturer + "\n" if self.lecturer else "") + 
#            ("Contributor: " + self.contributor + "\n" if self.contributor else "") +
#            ("Voice:       " + self.voice + "\n" if self.voice else "") +
#            "---\n" +
#            ("Length:      " + self.length + "\n" if self.length else "") +
#            ("Sound:       " + self.sounds + "\n" if self.sounds else "") +
#            ("Subtitles:   " + self.subs + "\n" if self.subs else "") +
#            ("Genre:       " + self.genres + "\n" if self.genres else "") +
#            ("Theme:       " + self.themes + "\n" if self.themes else "") +
#            ("Countries:   " + self.countries + "\n" if self.countries else "")
#        )
        
    def setDate(self, date):
        self.date = date
        
    def setYear(self, year):
        self.year = year
        
    def setDirectors(self, directorList):
        self.directors = directorList

    def setMakers(self, makers):
        self.makers = makers

    def setWriters(self, writerList):
        self.writers = writerList

    def setAuthors(self, authorList):
        self.authors = authorList

    def setActors(self, actorList):
        self.actors = actorList

    def setPerformers(self, performerList):
        self.performers = performerList

    def setLecturers(self, lecturerList):
        self.lecturer = lecturerList
        
    def setContributors(self, contributorList):
        self.contributor = contributorList
        
    def setInterviewees(self, intervieweeList):
        self.interviewee = intervieweeList        

    def setInterviewers(self, interviewerList):
        self.interviewer = interviewerList        

    def setAnchors(self, anchorList):
        self.anchor = anchorList

    def setPresenters(self, presenterList):
        self.presenter = presenterList

    
    def setVoices(self, voiceList):
        self.voice = voiceList
        
    def setLength(self, length):
        self.length = length
    
    def setSounds(self, soundList):
        self.sounds = soundList

    def setSubs(self, subList):
        self.subs = subList

    def setGenres(self, genreList):
        self.genres = genreList

    def setRecipeTypes(self, recipeTypeList):
        self.recipeTypes = recipeTypeList
        
    def setThemes(self, themeList):
        self.themes = themeList

    def setCountries(self, countrieList):
        self.countries = countrieList
        
    def setStoryline(self, storyline):
        self.storyline = storyline
 
    def setTopic(self, topic):
        self.topic = topic

    def setLyrics(self, lyrics):
        self.lyrics = lyrics
        
    def setIngredient(self, ingredient):
        self.ingredient = ingredient

    def setMethod(self, method):
        self.method = method
                
    def setSeason(self, season):
        self.season = season

    def setEpisode(self, episode):
        self.episode = episode

    def setAlbum(self, album):
        self.album = album
        
    def setTrack(self, track):
        self.track = track

    def setBook(self, book):
        self.book = book

    def setVolume(self, volume):
        self.volume = volume

    def setPart(self, part):
        self.part = part

    # ---

    def getTranslatedRecipeTypeList(self, category, rawRecipeTypeList=None):
        """
        Returns back the RecipeType list in the respective language.
        _________________________________________________________________________________________________
        input:
                category:    movie, music, show, presentation, alternative, miscellaneous, radioplay, audiobook
        output:
                [(translated, raw), (translated, raw), ... ]
        """
        pre = "recipetype_"        
        recipetypes = [ (_(pre+g), g) for g in self.getRecipeTypes() ]
        
        return recipetypes
       
    # ---
    
    def getTranslatedGenreList(self, category, rawGenreList=None):
        """
        Returns back the Genres list in the respective language.
        _________________________________________________________________________________________________
        input:
                category:    movie, music, show, presentation, alternative, miscellaneous, radioplay, audiobook
        output:
                [(translated, raw), (translated, raw), ... ]
        """
#        pre = "genre" + ("_" + category if category is not None and category == "music" else "" ) + "_"
        pre = "genre_"        
        genres = [ (_(pre+g), g) for g in self.getGenres() ]
        
        return genres

    # ---
    
    def getTranslatedThemeList(self, category=None):
        """
        Returns back the Theme list in the respective language.
        _________________________________________________________________________________________________
        input:
        """
        pre = "theme_"
        themes = [ (_(pre+t), t) for t in self.getThemes() ]
        
        return themes

    # ---
    
    def getTranslatedSoundStringList(self, category=None):
        """
        Returns back the Sounds list in the respective language.
        _________________________________________________________________________________________________
        input:
        """
        sound_list = ", ".join( [ _("lang_" + s) for s in self.getSounds()])        

        return sound_list
    
    def getDate(self):
        return self.date
        
    def getYear(self):
        return self.year
    
    def getDirectors(self):
        return self.directors

    def getMakers(self):
        return self.makers
    
    def getWriters(self):
        return self.writers

    def getAuthors(self):
        return self.authors
    
    def getActors(self):
        return self.actors

    def getPerformers(self):
        return self.performers
        
    def getLecturers(self):
        return self.lecturer
    
    def getContributors(self):
        return self.contributor

    def getInterviewees(self):
        return self.interviewee

    def getInterviewers(self):
        return self.interviewer

    def getAnchors(self):
        return self.anchor

    def getPresenters(self):
        return self.presenter

    
    def getVoices(self):
        return self.voice        

    def getLength(self):
        return self.length
    
    def getSounds(self):
        return self.sounds
    
    def getSubs(self):
        return self.subs
    
    def getGenres(self):
        return self.genres
    
    def getRecipeTypes(self):
        return self.recipeTypes
    
    def getThemes(self):
        return self.themes
    
    def getCountries(self):
        return self.countries
    
    def getStoryline(self):
        return self.storyline

    def getTopic(self):
        return self.topic
    
    def getLyrics(self):
        return self.lyrics
    
    def getIngredient(self):
        return self.ingredient

    def getMethod(self):
        return self.method
    
    def getSeason(self):
        return self.season
    
    def getEpisode(self):
        return self.episode
    
    def getAlbum(self):
        return self.album
    
    def getTrack(self):
        return self.track

    def getBook(self):
        return self.book

    def getVolume(self):
        return self.volume

    def getPart(self):
        return self.part

    def getJson(self):        
        json = {}
        json.update({} if self.date is None or not self.date else {JSON_KEY_GENERAL_DATE: self.date})
        json.update({} if self.year is None or not self.year else {JSON_KEY_GENERAL_YEAR: self.year})
        json.update({} if self.length is None or not self.length else {JSON_KEY_GENERAL_LENGTH: self.length})
        
        json.update({} if self.directors is None or not self.directors else {JSON_KEY_GENERAL_DIRECTOR: self.directors})
        json.update({} if self.makers is None or not self.makers else {JSON_KEY_GENERAL_MAKER: self.makers})
        json.update({} if self.writers is None or not self.writers else {JSON_KEY_GENERAL_WRITER: self.writers})
        json.update({} if self.authors is None or not self.authors else {JSON_KEY_GENERAL_AUTHOR: self.authors})
        json.update({} if self.actors is None or not self.actors else {JSON_KEY_GENERAL_ACTOR: self.actors})
        json.update({} if self.performers is None or not self.performers else {JSON_KEY_GENERAL_PERFORMER: self.performers})
        json.update({} if self.lecturer is None or not self.lecturer else {JSON_KEY_GENERAL_LECTURER: self.lecturer})
        json.update({} if self.contributor is None or not self.contributor else {JSON_KEY_GENERAL_CONTRIBUTOR: self.contributor})
        json.update({} if self.interviewee is None or not self.interviewee else {JSON_KEY_GENERAL_INTERVIEWEE: self.interviewee})
        json.update({} if self.interviewer is None or not self.interviewer else {JSON_KEY_GENERAL_INTERVIEWER: self.interviewer})
        json.update({} if self.anchor is None or not self.anchor else {JSON_KEY_GENERAL_ANCHOR: self.anchor})
        json.update({} if self.presenter is None or not self.presenter else {JSON_KEY_GENERAL_PRESENTER: self.presenter})
        json.update({} if self.voice is None or not self.voice else {JSON_KEY_GENERAL_VOICE: self.voice})
        
        json.update({} if self.sounds is None or not self.sounds else {JSON_KEY_GENERAL_SOUND: self.sounds})
        json.update({} if self.subs is None or not self.subs else {JSON_KEY_GENERAL_SUB: self.subs})
        json.update({} if self.countries is None or not self.countries else {JSON_KEY_GENERAL_COUNTRY: self.countries})
        
        json.update({} if self.genres is None or not self.genres else {JSON_KEY_GENERAL_GENRE: self.genres})
        json.update({} if self.themes is None or not self.themes else {JSON_KEY_GENERAL_THEME: self.themes})
        json.update({} if self.recipeTypes is None or not self.recipeTypes else {JSON_KEY_GENERAL_RECIPETYPE: self.recipeTypes})
        
        json.update({} if self.season is None or not self.season else {JSON_KEY_GENERAL_SEASON: self.season})
        json.update({} if self.episode is None or not self.episode else {JSON_KEY_GENERAL_EPISODE: self.episode})        
        json.update({} if self.album is None or not self.album else {JSON_KEY_GENERAL_ALBUM: self.album})
        json.update({} if self.track is None or not self.track else {JSON_KEY_GENERAL_TRACK: self.track})
        json.update({} if self.book is None or not self.book else {JSON_KEY_GENERAL_BOOK: self.book})
        json.update({} if self.volume  is None or not self.volume else {JSON_KEY_GENERAL_VOLUME: self.volume})
        json.update({} if self.part  is None or not self.part else {JSON_KEY_GENERAL_PART: self.part})
        
        return json
    
    def getWidgetOneLine(self, media, scale):
        layout = QGridLayout()
        
        layout.setSpacing(1)
        
        layout.setContentsMargins(0, 0, 0, 0)

        widget = QWidget()
        #widget.setStyleSheet('background: ' + self.getBackgroundColor())
        widget.setLayout(layout)

        layout.addWidget(self.getWidgetOneLineInfoYear(media, scale), 0, 0)

        layout.addWidget(self.getWidgetOneLineInfoLength(media, scale), 0, 1)
        
        layout.addWidget(self.getWidgetOneLineInfoCountries(media, scale), 0, 2)
        
        layout.addWidget(self.getWidgetOneLineInfoSounds(media, scale), 0, 3)
        
        layout.addWidget(self.getWidgetOneLineInfoSubs(media, scale), 0, 4)
        
        if layout.sizeHint().height() > 0:
            layout.addWidget(QHLine(), 1, 0, 1, 5)

        return widget
    
    def getWidgetOneLineInfoSubs(self, media, scale):
        sub_list = ", ".join( [ _("lang_" + c) for c in self.getSubs()])
        
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)        
        layout.setSpacing(1)        
        layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(layout)
        
        if sub_list:

            key_label = QLabel( _('title_sub')  + ": ")
            key_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Normal))
            layout.addWidget(key_label)
        
            value_label = QLabel(sub_list)
            value_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Bold))
            layout.addWidget(value_label)
        return widget
    
    def getWidgetOneLineInfoYear(self, media, scale):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)        
        layout.setSpacing(1)        
        layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(layout)
        
        if self.getDate():

            key_label = QLabel(_('title_date')  + ": ")
            key_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Normal))
            layout.addWidget(key_label)
        
            value_label = QLabel(self.getDate())
            value_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Bold))
            layout.addWidget(value_label)
            
        elif self.getYear():

            key_label = QLabel(_('title_year')  + ": ")
            key_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Normal))
            layout.addWidget(key_label)
        
            value_label = QLabel(self.getYear())
            value_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Bold))
            layout.addWidget(value_label)
        
        return widget
        
    def getWidgetOneLineInfoLength(self, media, scale):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)        
        layout.setSpacing(1)        
        layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(layout)
        
        if self.getLength():

            key_label = QLabel(_('title_length')  + ": ")
            key_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Normal))
            layout.addWidget(key_label)
        
            value_label = QLabel(self.getLength())
            value_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Bold))
            layout.addWidget(value_label)
        
        return widget    
        
    def getWidgetOneLineInfoCountries(self, media, scale):
        country_list = ", ".join( [ _("country_" + c) for c in self.getCountries()])
        
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)        
        layout.setSpacing(1)        
        layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(layout)
        
        if country_list:

            key_label = QLabel(_('title_country')  + ": ")
            key_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Normal))
            layout.addWidget(key_label)
        
            value_label = QLabel(country_list)
            value_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Bold))
            layout.addWidget(value_label)
        
        return widget
        
    def getWidgetOneLineInfoSounds(self, media, scale):
        sound_list = self.getTranslatedSoundStringList()
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)        
        layout.setSpacing(1)        
        layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(layout)
        
        if sound_list:

            key_label = QLabel( _('title_sound')  + ": ")
            key_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Normal))
            layout.addWidget(key_label)
        
            value_label = QLabel(sound_list)
            value_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Bold))
            layout.addWidget(value_label)
        return widget

    # --------------------------------------------
    # ------------GENERAL INFORMATION ------------
    # --------------------------------------------
    
    def getWidget(self, mainWidget, media, scale):
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
            | Tags:                                       |                             |
            |_____________________________________________|_____________________________|            
        """                
        class GeneralWidget(QWidget):
            def __init__(self, mainWidget, media, scale):
                QWidget.__init__(self)
            
                self.mainWidget = mainWidget
                self.scale = scale
                self.media = media
                
                self.row = 0                
                self.tag_widget = None
                self.hasGeneral = False

                self.grid_layout = QGridLayout()
        
                # space between the three grids
                self.grid_layout.setSpacing(1)
        
                # margin around the widget
                self.grid_layout.setContentsMargins(0, 0, 0, 0)

                # stretch out the 2nd column
                self.grid_layout.setColumnStretch(1, 1)
        
                # space between the three grids
                self.grid_layout.setSpacing(1)

                self.setLayout(self.grid_layout)

            def addQlinkSimpleWidget(self, media, scale, title_id, value_method):
                value = value_method()

                if value:
                    self.hasGeneral = True
        
                    widget_key = QLabel(_(title_id) + ":", )
                    widget_key.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Bold))
                    widget_key.setAlignment(Qt.AlignTop)
        
                    layout = FlowLayout()
                    layout.setAlignment(Qt.AlignLeft)        
                    layout.setSpacing(1)        
                    layout.setContentsMargins(0, 0, 0, 0)

                    widget_value = QWidget()
                    widget_value.setLayout( layout )
                    widget_value.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Normal))        
                    first = True
                    for d in value:
                        if not first:
                            comma_label = QLabel(", ")
                            comma_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Normal))
                            layout.addWidget(comma_label)
                        label = IniGeneral.QLinkLabelToSearch(media, scale, d, d, title_id)
                        layout.addWidget(label)
                        first = False

                    self.grid_layout.addWidget(widget_key, self.row, 0)
                    self.grid_layout.addWidget(widget_value, self.row, 1)
                    self.row = self.row + 1

            def addQlinkTranslatedWidget(self, media, scale, title_id, element_list):
       
                if element_list:
                    self.hasGeneral = True
                    
                    widget_key = QLabel(_(title_id) + ":", )
                    widget_key.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Bold))
        
                    layout_genres = QHBoxLayout()
                    layout_genres.setAlignment(Qt.AlignLeft)
                    layout_genres.setSpacing(1)        
                    layout_genres.setContentsMargins(0, 0, 0, 0)

                    widget_value = QWidget()
                    widget_value.setLayout( layout_genres )
                    widget_value.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Normal))
                    first = True
            
                    for d, e in element_list:
                        if not first:
                            comma_label = QLabel(", ")
                            comma_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Normal))
                            layout_genres.addWidget( comma_label )
                        label = IniGeneral.QLinkLabelToSearch(media, scale, d, e, title_id)                
                        layout_genres.addWidget(label)
                        first = False
        
                    self.grid_layout.addWidget(widget_key, self.row, 0)
                    self.grid_layout.addWidget(widget_value, self.row, 1)
                    self.row = self.row + 1

            def addStorylineWidget(self, storyline_widget, title_id):
                if storyline_widget:
                    
                    if self.hasGeneral:
                        self.grid_layout.addWidget(QHLine(), self.row, 0, 1, 2)
                        self.row = self.row + 1

                    widget_key = QLabel(_(title_id) + ":", )
                    widget_key.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Bold))
                    widget_key.setAlignment(Qt.AlignTop)
            
                    self.grid_layout.addWidget( widget_key, self.row, 0)            
                    self.grid_layout.addWidget( storyline_widget, self.row, 1)        
                    self.row = self.row + 1                    
                    
            def addTagWidget(self, tag_widget, title_id):
                if tag_widget:
                    
                    self.tag_widget = tag_widget
                    
                    self.grid_layout.addWidget(QHLine(), self.row, 0, 1, 2)
                    self.row = self.row + 1
                    
                    widget_key = QLabel(_(title_id) + ":", )
                    widget_key.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Bold))
                    widget_key.setAlignment(Qt.AlignTop)

                    
                    self.grid_layout.addWidget(widget_key, self.row, 0)
                    self.grid_layout.addWidget(tag_widget, self.row, 1)
                    self.row = self.row + 1

            def setFocusTagField(self, value):
                if self.tag_widget:
                    self.tag_widget.setFocusTagField(value)

#       ---------------- GeneralWidget -----------------------

        widget = GeneralWidget(mainWidget, media, scale)
 
        # ---
        # --- DIRECTORS ---
        widget.addQlinkSimpleWidget(media, scale, 'title_director', media.general.getDirectors)

        # --- MAKER ---       
        widget.addQlinkSimpleWidget(media, scale, 'title_maker', media.general.getMakers)

        # ---
        # --- WRITERS ---
        widget.addQlinkSimpleWidget(media, scale, 'title_writer', media.general.getWriters)

        # --- AUTHORS ---
        widget.addQlinkSimpleWidget(media, scale, 'title_author', media.general.getAuthors)

        # ---
        # --- ACTORS ---       
        widget.addQlinkSimpleWidget(media, scale, 'title_actor', media.general.getActors)

        # --- PERFORMER ---       
        widget.addQlinkSimpleWidget(media, scale, 'title_performer', media.general.getPerformers)

        # --- LECTURER ---       
        widget.addQlinkSimpleWidget(media, scale, 'title_lecturer', media.general.getLecturers)

        # --- CONTRIBUTOR ---       
        widget.addQlinkSimpleWidget(media, scale, 'title_contributor', media.general.getContributors)

        # --- INTERVIEWEE ---       
        widget.addQlinkSimpleWidget(media, scale, 'title_interviewee', media.general.getInterviewees)

        # --- INTERVIEWER ---       
        widget.addQlinkSimpleWidget(media, scale, 'title_interviewer', media.general.getInterviewers)

        # --- ANCHOR ---       
        widget.addQlinkSimpleWidget(media, scale, 'title_anchor', media.general.getAnchors)

        # --- PRESENTER ---       
        widget.addQlinkSimpleWidget(media, scale, 'title_presenter', media.general.getPresenters)

        # --- VOICE ---       
        widget.addQlinkSimpleWidget(media, scale, 'title_voice', media.general.getVoices)

        # ---
        # --- GENRE ---       
        widget.addQlinkTranslatedWidget(media, scale, 'title_genre', media.getTranslatedGenreList())

        # ---
        # --- THEME ---
        widget.addQlinkTranslatedWidget(media, scale, 'title_theme', media.getTranslatedThemeList())    

        # ---
        # --- RECIPETYPE ---
        widget.addQlinkTranslatedWidget(media, scale, 'title_recipetype', media.getTranslatedRecipeTypeList())    

        # ---
        # --- STORILINES ---
        storyline_widget = media.getWidgetGeneralInfoStoryLine(widget, scale, media.getTranslatedStoryline(self.getStoryline()))
        widget.addStorylineWidget(storyline_widget, 'title_storyline')

        # --- TOPIC ---
        storyline_widget = media.getWidgetGeneralInfoStoryLine(widget, scale, media.getTranslatedStoryline(self.getTopic()))
        widget.addStorylineWidget(storyline_widget, 'title_topic')
        
        # --- LYRICS ---
        storyline_widget = media.getWidgetGeneralInfoStoryLine(widget, scale, media.getTranslatedStoryline(self.getLyrics()))
        widget.addStorylineWidget(storyline_widget, 'title_lyrics')

        # --- INGREDIENT ---
        storyline_widget = media.getWidgetGeneralInfoStoryLine(widget, scale, media.getTranslatedStoryline(self.getIngredient()))
        widget.addStorylineWidget(storyline_widget, 'title_ingredient')

        # --- METHOD ---
        storyline_widget = media.getWidgetGeneralInfoStoryLine(widget, scale, media.getTranslatedStoryline(self.getMethod()))
        widget.addStorylineWidget(storyline_widget, 'title_method')

        # --- TAG ---
        self.tag_widget = media.classification.getWidgetTagListButtons(mainWidget, media, scale, 'title_tag', media.classification.getTagList)
        widget.addTagWidget(self.tag_widget, 'title_tag')
        
        return widget

    class QLinkLabelToSearch( QLabelToLinkOnClick ):
        """
        Link Widget to search Genre/Theme/Director/Maker/Writer/Actor/Performer/Lecturer/Contributor/Voice/Interviewer/Interviewee/Anchor/Presenter
        """
        def __init__(self, media, scale, translatedText, rawText, title_id):
            super().__init__(media, translatedText, media.isInFocus)
            self.media = media
            self.rawText = rawText
            self.title_id = title_id
            self.scale = scale
            self.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Normal))

        def toDoOnClick(self):
            modifiers = QApplication.keyboardModifiers()
            if modifiers == Qt.ShiftModifier:
                withShift = True
            else:
                withShift = False

            self.media.search( withShift, self.rawText, self.title_id)                
            
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
 




        