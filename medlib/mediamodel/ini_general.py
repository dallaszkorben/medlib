from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout

from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPalette

from PyQt5.QtCore import Qt

from medlib.handle_property import _
from medlib.mediamodel.ini_storylines import IniStorylines
from medlib.mediamodel.extra import QHLine
from medlib.mediamodel.extra import FlowLayout

from medlib.constants import *
from medlib.handle_property import _
from builtins import object

from medlib.mediamodel.qlabel_to_link_on_cllick import QLabelToLinkOnClick

class IniGeneral(object):
    """
    This class represents the [general] section in the card.ini file

    """
    
    def __init__(self):
        """
        This is the constructor of the IniGeneral class
        _______________________________________________
        input:
            year             string             like "1987" or "1987-1988"
            
            directors        list of strings    ["Director 1", "Director 2"]
            makers           list of strings    ["Maker 1", "Maker 2"]            
            
            writers          list of strings    ["Writer 1", "Writer 2"]
            authors          list of strings    ["Author 1", "Author 2"]
            
            actors           list of strings    ["Actor 1", "Actor 2"]
            performers       list of strings    ["Performer 1", "Performer 2"]
            lecturer         list of strings    ["Lecturer 1", "Lecturer 2"]
            contributor      list of strings    ["Contributor 1", "Contributor 2"]
            voice            list of strings    ["Voice 1", "Voice 2"]
            
            length           string             "2:15"
            sounds           list of strings    ["en", "hu"]
            subs             list of strings    ["en", "hu"]
            genres           list of strings    ["drama", "action"]
            themes           list of strings    ["money", "greed"]
            countries        list of strings    ["us", "ca"]
            
            storyline        storyLine
            topic            storyLine
            lyrics           storyLine
            
            series          integer       index of the series
            episode         integer       index of the episode
        """
        self.year = None 
        self.directors = []
        self.makers = []
        self.writers = []
        self.authors = []
        self.actors = []
        self.performers = []
        self.lecturer = []
        self.contributor = []
        self.voice = []
        
        self.length = None
        self.sounds = []
        self.subs = []
        self.genres = []
        self.themes = []
        self.countries = []
        
        self.storyline = IniStorylines()
        self.topic = IniStorylines()
        self.lyrics = IniStorylines()
        
        self.series = None
        self.episode = None
    
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
        
    def setSeries(self, series):
        self.series = series

    def setEpisode(self, episode):
        self.episode = episode
   
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
        pre = "genre" + ("_" + category if category is not None and category == "music" else "" ) + "_"
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
    
    def getSeries(self):
        return self.series
    
    def getEpisode(self):
        return self.episode

    def getJson(self):        
        json = {}
        json.update({} if self.year is None or not self.year else {'year': self.year})
        json.update({} if self.length is None or not self.length else {'length': self.length})
        
        json.update({} if self.directors is None or not self.directors else {'director': self.directors})
        json.update({} if self.makers is None or not self.makers else {'maker': self.makers})
        json.update({} if self.writers is None or not self.writers else {'writer': self.writers})
        json.update({} if self.authors is None or not self.authors else {'author': self.authors})
        json.update({} if self.actors is None or not self.actors else {'actor': self.actors})
        json.update({} if self.performers is None or not self.performers else {'performer': self.performers})
        json.update({} if self.lecturer is None or not self.lecturer else {'lecturer': self.lecturer})
        json.update({} if self.contributor is None or not self.contributor else {'contributor': self.contributor})
        json.update({} if self.voice is None or not self.voice else {'voice': self.voice})
        
        json.update({} if self.sounds is None or not self.sounds else {'sound': self.sounds})
        json.update({} if self.subs is None or not self.subs else {'sub': self.subs})
        json.update({} if self.countries is None or not self.countries else {'country': self.countries})
        
        json.update({} if self.genres is None or not self.genres else {'genre': self.genres})
        json.update({} if self.themes is None or not self.themes else {'theme': self.themes})
        
        json.update({} if self.series is None or not self.series else {'series': self.series})
        json.update({} if self.episode is None or not self.episode else {'episode': self.episode})        
        
        return json
    
    def getWidgetOneLine(self, parent, scale):
        layout = QGridLayout()
        
        layout.setSpacing(1)
        
        layout.setContentsMargins(0, 0, 0, 0)

        widget = QWidget()
        #widget.setStyleSheet('background: ' + self.getBackgroundColor())
        widget.setLayout(layout)
        widget.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Normal))

        layout.addWidget(self.getWidgetOneLineInfoYear(self, scale), 0, 0)

        layout.addWidget(self.getWidgetOneLineInfoLength(self, scale), 0, 1)
        
        layout.addWidget(self.getWidgetOneLineInfoCountries(self, scale), 0, 2)
        
        layout.addWidget(self.getWidgetOneLineInfoSounds(self, scale), 0, 3)
        
        layout.addWidget(self.getWidgetOneLineInfoSubs(self, scale), 0, 4)
        
        if layout.sizeHint().height() > 0:
            layout.addWidget(QHLine(), 1, 0, 1, 5)

        return widget
    
    def getWidgetOneLineInfoSubs(self, parent, scale):
        sub_list = ", ".join( [ _("lang_" + c) for c in self.getSubs()])
        
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
            value_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Bold))
            layout.addWidget(value_label)
        return widget
    
    def getWidgetOneLineInfoYear(self, parent, scale):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)        
        layout.setSpacing(1)        
        layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(layout)
        
        if self.getYear():

            key_label = QLabel(_('title_year')  + ": ")
            layout.addWidget(key_label)
        
            value_label = QLabel(self.getYear())
            value_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Bold))
            layout.addWidget(value_label)
        
        return widget
        
    def getWidgetOneLineInfoLength(self, parent, scale):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)        
        layout.setSpacing(1)        
        layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(layout)
        
        if self.getLength():

            key_label = QLabel(_('title_length')  + ": ")
            layout.addWidget(key_label)
        
            value_label = QLabel(self.getLength())
            value_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Bold))
            layout.addWidget(value_label)
        
        return widget
    
        
    def getWidgetOneLineInfoCountries(self, parent, scale):
        country_list = ", ".join( [ _("country_" + c) for c in self.getCountries()])
        
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
            value_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Bold))
            layout.addWidget(value_label)
        
        return widget
        
    def getWidgetOneLineInfoSounds(self, parent, scale):
        sound_list = self.getTranslatedSoundStringList()
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
            value_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Bold))
            layout.addWidget(value_label)
        return widget



    # --------------------------------------------
    # ------------GENERAL INFORMATION ------------
    # --------------------------------------------
    def getWidget(self, parent, scale):
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
        row = self.addNameListToQLinkLabel(parent, scale, grid_layout, row, 'title_director', parent.general.getDirectors)

        # --- MAKER ---       
        row = self.addNameListToQLinkLabel(parent, scale, grid_layout, row, 'title_maker', parent.general.getMakers)

        # ---
        # --- WRITERS ---
        row = self.addNameListToQLinkLabel(parent, scale, grid_layout, row, 'title_writer', parent.general.getWriters)

        # --- AUTHORS ---
        row = self.addNameListToQLinkLabel(parent, scale, grid_layout, row, 'title_author', parent.general.getAuthors)

        # ---
        # --- ACTORS ---       
        row = self.addNameListToQLinkLabel(parent, scale, grid_layout, row, 'title_actor', parent.general.getActors)

        # --- PERFORMER ---       
        row = self.addNameListToQLinkLabel(parent, scale, grid_layout, row, 'title_performer', parent.general.getPerformers)

        # --- LECTURER ---       
        row = self.addNameListToQLinkLabel(parent, scale, grid_layout, row, 'title_lecturer', parent.general.getLecturers)

        # --- CONTRIBUTOR ---       
        row = self.addNameListToQLinkLabel(parent, scale, grid_layout, row, 'title_contributor', parent.general.getContributors)

        # --- VOICE ---       
        row = self.addNameListToQLinkLabel(parent, scale, grid_layout, row, 'title_voice', parent.general.getVoices)

        # ---
        # --- GEMRE ---       
        row = self.addTranslatedListToQLinkLabel(parent, scale, grid_layout, row, 'title_genre', parent.getTranslatedGenreList())
#        row = self.addTranslatedListToQLinkLabel(scale, grid_layout, row, 'title_genre', self.general.getGenres)

        # ---
        # --- THEME ---       
        row = self.addTranslatedListToQLinkLabel(parent, scale, grid_layout, row, 'title_theme', parent.getTranslatedThemeList())
        
        # ---
        # --- STORILINES ---
        row = parent.addWidgetGeneralInfoStoryline(widget, scale, grid_layout, row, 'title_storyline', parent.getTranslatedStoryline(self.getStoryline()))

        # --- TOPIC ---
        row = parent.addWidgetGeneralInfoStoryline(widget, scale, grid_layout, row, 'title_topic', parent.getTranslatedStoryline(self.getTopic()))

        # --- LYRICS ---
        row = parent.addWidgetGeneralInfoStoryline(widget, scale, grid_layout, row, 'title_lyrics', parent.getTranslatedStoryline(self.getLyrics()))
                
        return widget

    # #####################################################################################
    # Link List - Director/Maker/Writer/Author/Actor/Performer/Lecturer/Contributor/Voice #
    # #####################################################################################
    def addNameListToQLinkLabel(self, parent, scale, grid_layout, row, title_id, value_method):
        value = value_method()

        if value:
        
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
                    layout.addWidget( QLabel(", ") )
                label = IniGeneral.QLinkLabelToSearch(parent, d, d, title_id, scale)
                layout.addWidget(label)
                first = False

            grid_layout.addWidget(widget_key, row, 0)
            grid_layout.addWidget(widget_value, row, 1)
            row = row + 1
            
        return row   

    # ###########################
    # String List - Genre/Theme #
    # ###########################
    def addTranslatedListToQLinkLabel(self, parent, scale, grid_layout, row, title_id, element_list):
       
        if element_list:
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
                    layout_genres.addWidget( QLabel(", ") )
                label = IniGeneral.QLinkLabelToSearch(parent, d, e, title_id, scale)                
                layout_genres.addWidget(label)
                first = False
        
            grid_layout.addWidget(widget_key, row, 0)
            grid_layout.addWidget(widget_value, row, 1)
            row = row + 1
            
        return row
     
    class QLinkLabelToSearch( QLabelToLinkOnClick ):

        def __init__(self, media, translatedText, rawText, title_id, sizeRate):
            super().__init__(translatedText, media.isSelected)
            self.media = media
            self.rawText = rawText
            self.title_id = title_id
            self.scale = sizeRate
            self.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Normal))

        def toDoOnClick(self):
            if self.media.searchFunction is not None:
                self.media.searchFunction( self.rawText, self.title_id)
            print("Search for " + self.rawText + " by " + self.title_id)
            
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
 




        