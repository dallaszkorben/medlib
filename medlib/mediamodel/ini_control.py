class IniControl(object):
    """
    This class represents the [control] section in the card.ini file
        -orderby
        -media - (icon)
        -category
    """
    
    def __init__(self, orderby, media, category):
        """
        This is the constructor of the IniControl class
        ___________________________________________
        input:
            orderby         string        "folder","title","episode"
            media           string        "video", "audio", "ebook", "picture", "doc"
            category        string        "movie", "music", "show", "presentation", "alternative", "miscellaneous", "radioplay"            
        """
        self.orderby = orderby
        self.media = media
        self.category = category        
        
    def getOrderBy(self):
        return self.orderby

    def getMedia(self):
        return self.media
    
    def getCategory(self):
        return self.category

    def getJson(self):        
        json = {}
        json.update({} if self.media is None or not self.media else {'media': self.media})
        json.update({} if self.orderby is None or not self.orderby else {'orderby': self.orderby})
        json.update({} if self.category is None or not self.category else {'category':self.category})
        
        return json
    
    