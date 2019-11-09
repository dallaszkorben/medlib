from medlib.handle_property import _

class IniGeneral(object):
    """
    This class represents the [general] section in the card.ini file

    """
    
    def __init__(self, year=None, directors=None, writers=None, actors=None, length=None, sounds=None, subs=None, genres=None, themes=None, countries=None):
        """
        This is the constructor of the IniGeneral class
        _______________________________________________
        input:
            year         string             like "1987" or "1987-1988"
            directors    list of strings    ["Director 1", "Director 2"]
            writers      list of strings    ["Writer 1", "Writer 2"]
            actors       list of strings    ["Actor 1", "Actor 2"]
            length       string             "2:15"
            sounds       list of strings    ["en", "hu"]
            subs         list of strings    ["en", "hu"]
            genres       list of strings    ["drama", "action"]
            themes       list of strings    ["money", "greed"]
            countries    list of strings    ["us", "ca"]
        """
        self.year = year 
        self.directors = directors if directors else []
        self.writers = writers if writers else []
        self.actors = actors if actors else []
        self.length = length
        self.sounds = sounds  if sounds else []
        self.subs = subs if subs else []
        self.genres = genres if genres else []
        self.themes = themes if themes else []
        self.countries = countries if countries else []
        
    def getTranslatedGenres(self, category=None):
        """
        Returns back the Genres list in the respective language.
        _________________________________________________________________________________________________
        input:
                category:    movie, music, show, presentation, alternative, miscellaneous, radioplay, audiobook 
        """
        pre = "genre" + ("_" + category if category is not None and category == "music" else "" ) + "_"
        genres = [ _(pre+g) for g in self.getGenres() ]
        
        return genres

        
    def getYear(self):
        return self.year
    
    def getDirectors(self):
        return self.directors
    
    def getWriters(self):
        return self.writers
    
    def getActors(self):
        return self.actors
    
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
    
    
    