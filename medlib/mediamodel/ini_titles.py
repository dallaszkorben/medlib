from medlib.handle_property import config_ini

class IniTitles(object):
    """
    This class represents the [titles] section in the card.ini file
    """
    
    def __init__(self, orig_title, title_list_by_language=None):
        """
        This is the constructor of the IniTitles class
        ___________________________________________
        input:
            orig_title                string        "The title in the original language"
            title_list_by_language    dictionary    {"hu":"Magyar cim", "en":"English title"}
        """
        self.orig_title = orig_title
        self.title_list_by_language = title_list_by_language if title_list_by_language else []
    
    def getOrigTitle(self):
        return self.orig_title
        
    def getTranslatedTitle(self):
        """
        Returns back the title.
        If the title does not exists on the specific language, then the 'original' title will be returned
        _________________________________________________________________________________________________
        input:
        """
        title = self.title_list_by_language.get(config_ini['language'])
        if not title:
            title=self.getOrigTitle()
        return title
    
    def getJson(self):
        json = {}
        json.update({} if self.orig_title is None or not self.orig_title else {"orig": self.orig_title})
        
        json.update({key: value for key, value in self.title_list_by_language.items()})
       
        return json
