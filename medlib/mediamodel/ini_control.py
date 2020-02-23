from medlib.card_ini import JSON_KEY_CONTROL_MEDIA
from medlib.card_ini import JSON_KEY_CONTROL_ORDERBY
from medlib.card_ini import JSON_KEY_CONTROL_CATEGORY

import json

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
    
    def __str__(self):
        return json.dumps(self.getJson(), indent=4, sort_keys=True)
#        return "\norderby:  " + self.getOrderBy() + "\n" + "media:    " + self.getMedia() + "\n" + "category: " + self.getCategory() + "\n"
        
    def getOrderBy(self):
        return self.orderby

    def getMedia(self):
        return self.media
    
    def getCategory(self):
        return self.category

    def getJson(self):        
        json = {}
        json.update({} if self.orderby is None or not self.orderby else {JSON_KEY_CONTROL_ORDERBY: self.orderby})
        json.update({} if self.media is None or not self.media else {JSON_KEY_CONTROL_MEDIA: self.media})
        json.update({} if self.category is None or not self.category else {JSON_KEY_CONTROL_CATEGORY:self.category})
        
        return json
    
    