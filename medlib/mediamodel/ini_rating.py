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