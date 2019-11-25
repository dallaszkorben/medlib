from medlib.handle_property import config_ini

class IniStorylines(object):
    """
    This class represents the [storyline] section in the card.ini file
    """
    
    def __init__(self, orig_storyline=None, storyline_list_by_language=None):
        """
        This is the constructor of the IniStoryline class
        ________________________________________________
        input:
            orig_storyline                string        The story line on the original language
            storyline_list_by_language    dictionary    {"hu":"A történet ...", "en":"The story ..."}
        """
        self.orig_storyline = orig_storyline if orig_storyline else ""
        self.storyline_list_by_language = storyline_list_by_language if storyline_list_by_language else {}
    
    def getOrigStoryline(self):
        return self.orig_storyline
        
    def getTranslatedStoryline(self):
        """
        Returns back the storyline in the respective language.
        If the storyline does not exists on the specific language, then the 'original' title will be returned
        _________________________________________________________________________________________________
        input:
        """
        storyline = self.storyline_list_by_language.get(config_ini['language'])
        if not storyline:
            storyline=self.getOrigStoryline()
        return storyline
    
