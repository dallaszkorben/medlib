from medlib.mediamodel.media_base import MediaBase

class MediaStorage(MediaBase):
    """
    This object represents the MediaStorage 
    This container can contain
    """
    
    def __init__(self, paths_content, titles, control, general=None, storylines=None,  rating=None):
        """
        This is the constructor of the MediaStorage
        ___________________________________________
        input:
                paths_content PathsContent      paths to the media content (card.ini, image.jpg, media)

                titles            IniTitles         represents the [titles] section
                control           IniControl        represents the [control] section
                general           IniGeneral        represents the [general] section
                storylines        IniStorylines     represents the [storyline] section
                rating        IniRating         represents the [rating] section
        """
        super().__init__(titles, control, general, storylines, rating)
        self.paths_content = paths_content    

    def getPathOfImage(self):
        return self.paths_content.getPathOfImage()

    def getHierarchyTitle(self, space):
        return space + "<S> " + self.getTranslatedTitle() + "\n"
     
    def setLanguage(self, language):
        """
        Sets the language, recursively, of the containers
        Sorts the order of the containers, recursively
        __________________________________________________
        input:
            language    string    like 'hu' or 'en' or ...
        """
        self.language = language
        for container in self.media_container_list:
            container.setLanguage(language)

        self.media_container_list.sort(key=lambda arg: arg.getTitle())
        
        