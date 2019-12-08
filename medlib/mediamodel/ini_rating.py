class IniRating(object):
    """
    This class represents the [rating] section in the card.ini file
        -rate
        -favorite
        -new
    """
    
    def __init__(self, rate=None, favorite=None, new=None):
        """
        This is the constructor of the IniRating class
        ___________________________________________
        input:
            rate         integer       1-10
            favorite     boolean       True,False
            new          boolean       True,False
        """
        self.rate = rate if (rate is None or (rate >= 0 and rate <= 10)) else 1 if rate < 0 else 10
        self.favorite = favorite
        self.new = new
        
    def getRate(self):
        return self.rate
    
    def getFavorite(self):
        return self.favorite
    
    def getNew(self):
        return self.new
        
    def setRate(self, rate):
        self.rate = 10 if rate > 10 else 0 if rate < 0 else rate

    def setFavorite(self, favorite):
        self.favorite = favorite

    def setNew(self, new):
        self.new = new
        
    def getJson(self):        
        json = {}
        json.update({} if self.rate is None else {'rate': self.rate})
        json.update({} if self.favorite is None else {'favorite' : "y" if self.favorite else "n"})
        json.update({} if self.new is None else {'new': "y" if self.new else "n"})
        
        return json