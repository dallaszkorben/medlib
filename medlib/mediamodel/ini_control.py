class IniControl(object):
    """
    This class represents the [control] section in the card.ini file
        -orderby
        -media - (icon)
        -category
        -series
        -episode
        -(media)
    """
    
    def __init__(self, orderby, media, category, series=None, episode=None):
        """
        This is the constructor of the IniControl class
        ___________________________________________
        input:
            orderby         string        "folder","title","episode"
            media           string        "video", "audio", "ebook", "picture", "doc"
            category        string        "movie", "music", "show", "presentation", "alternative", "miscellaneous", "radioplay"
            series          integer       index of the series
            episode         integer       index of the episode
        """
        self.orderby = orderby
        self.media = media
        self.category = category
        self.series = series
        self.episode = episode
        
    def getOrderBy(self):
        return self.orderby

    def getMedia(self):
        return self.media
    
    def getCategory(self):
        return self.category
    
    def getSeries(self):
        return self.series
    
    def getEpisode(self):
        return self.episode
  
    