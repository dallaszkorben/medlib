class IniControl(object):
    """
    This class represents the [control] section in the card.ini file
        -orderby
        -category - (icon)
        -series
        -episode
        -(media)
    """
    
    def __init__(self, orderby, category, series=None, episode=None):
        """
        This is the constructor of the IniControl class
        ___________________________________________
        input:
            orderby         string        "folder","title","episode"
            category        string        "movie", "music", "show", "presentation", "alternative", "miscellaneous", "radioplay"
            series          integer       index of the series
            episode         integer       index of the episode
        """
        self.orderby = orderby
        self.category = category
        self.series = series
        self.episode = episode
        
    def getOrderBy(self):
        return self.orderby
    
    def getCategory(self):
        return self.category
    
    def getSeries(self):
        return self.series
    
    def getEpisode(self):
        return self.episode
  
    