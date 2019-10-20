from medlib.mediamodel.media_base import MediaBase

class MediaCollector(MediaBase):
    """
    This object represents the MediaCollector
    This container can contain more MediaContainers and/or
    one MediaContent
    """
    def __init__(self, paths_collector, titles, control, general=None, storylines=None,  rating=None):  
        """
        This is the constructor of the MediaCollector
        ________________________________________
        input:
                paths_collector   PathsCollector    paths to the collector elements (card.ini, image.jpg ...)
        
                titles            IniTitles         represents the [titles] section
                control           IniControl        represents the [control] section
                general           IniGeneral        represents the [general] section
                storylines        IniStorylines     represents the [storyline] section
                rating        IniRating         represents the [rating] section
        """
        super().__init__(titles, control, general, storylines, rating)
        self.paths_collector = paths_collector
        self.media_collector_list = []
        self.media_storage_list = []
  
    def getPathOfImage(self):
        return self.paths_collector.getPathOfImage()
        
    def addMediaCollector(self, media_collector):
        """
        Adds a new MediaCollector to this MediaCollector
        It is ordered accordingly the language by the control.orderby
        _____________________________________________________________
        input:
                media_collector    MediaCollector    the MediaCollector to add
        """
        # Add the MediaCollector
        self.media_collector_list.append(media_collector)
        
        # Sort the list
        self.sortMediaCollector()
        
    def addMediaStorage(self, media_storage):
        """
        Adds a new MediaStorage to this MediaCollector
        It is ordered accordingly the language by the control.orderby
        _____________________________________________________________
        input:
                media_storage    MediaStorage    the MediaStorage to add
        """
        # Add the MediaStorage
        self.media_storage_list.append(media_storage)
        
        # Sort the list
        self.sortMediaStorage()
    
    def getPathsCollector(self):
        return self.paths_collector
        
    def getMediaStorageList(self):
        return self.media_storage_list
    
    def getMediaCollectorList(self):
        return self.media_collector_list    
    
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

        self.sortMediaCollector()
        self.sortMediaContent()        
        
    def sortMediaCollector(self):
        """
        Sort the MediaCollectors regarding to the control.orderby
           = title
           = folder
           = series
        """
#        self.media_container_list.sort(key=lambda arg: arg.getTitle() if arg.control.getOrderBy() == 'title' else arg.container_paths.getNameOfFolder() if arg.control.getOrderBy() == 'folder' else arg.container_paths.getNameOfFolder())
        self.media_collector_list.sort(key=lambda arg: MediaBase.sort_key(arg))
        
    def sortMediaStorage(self):
        """
        Sort the MediaStorage regarding to the control.orderby
           = title
           = folder
           = series
        """
        #self.media_content_list.sort(key=lambda arg: arg.getTitle() if arg.control.getOrderBy() == 'title' else arg.container_paths.getNameOfFolder() if arg.control.getOrderBy() == 'folder' else arg.container_paths.getNameOfFolder())
        self.media_storage_list.sort(key=lambda arg: MediaBase.sort_key(arg))

                
    def getHierarchyTitle(self, space):
        out = space + "<C> " + self.getTranslatedTitle() + "\n"        
        
        for collector in self.media_collector_list:
            out += collector.getHierarchyTitle(space + "   ")
            
        for storage in self.media_storage_list:
            out += storage.getHierarchyTitle(space + "   ")        
        return out  
   
        