from medlib.handle_property import _
from medlib.mediamodel.ini_storylines import IniStorylines

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
        
    def setDirectors(self, directors):
        self.directors = directors

    def setMakers(self, makers):
        self.makers = makers

    def setWriters(self, writers):
        self.writers = writers

    def setAuthors(self, authors):
        self.authors = authors

    def setActors(self, actors):
        self.actors = actors

    def setPerformers(self, performers):
        self.performers = performers

    def setLecturers(self, lecturer):
        self.lecturer = lecturer
        
    def setContributors(self, contributor):
        self.contributor = contributor
    
    def setVoices(self, voice):
        self.voice = voice
        
    def setLength(self, length):
        self.length = length
    
    def setSounds(self, sounds):
        self.sounds = sounds

    def setSubs(self, subs):
        self.subs = subs

    def setGenres(self, genres):
        self.genres = genres

    def setThemes(self, themes):
        self.themes = themes

    def setCountries(self, countries):
        self.countries = countries
        
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
        
    def getTranslatedGenreList(self, category=None):
        """
        Returns back the Genres list in the respective language.
        _________________________________________________________________________________________________
        input:
                category:    movie, music, show, presentation, alternative, miscellaneous, radioplay, audiobook 
        """
        pre = "genre" + ("_" + category if category is not None and category == "music" else "" ) + "_"
        genres = [ _(pre+g) for g in self.getGenres() ]
        
        return genres

    def getTranslatedThemeList(self, category=None):
        """
        Returns back the Theme list in the respective language.
        _________________________________________________________________________________________________
        input:
        """
        pre = "theme_"
        themes = [ _(pre+t) for t in self.getThemes() ]
        
        return themes

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

    