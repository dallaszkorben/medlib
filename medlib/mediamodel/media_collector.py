from medlib.mediamodel.media_base import MediaBase
from medlib.mediamodel.media_storage import MediaStorage
from medlib.mediamodel.paths_collector import PathsCollector

from medlib.mediamodel.qlabel_to_link_on_cllick import QLabelToLinkOnClick
from medlib.constants import COLLECTOR_BACKGROUND_COLOR

class MediaCollector(MediaBase):
    """
    This object represents the MediaCollector
    This container can contain more MediaContainers and/or
    one MediaContent
    """
    def __init__(self, pathsCollector, titles, control, general=None, classification=None):  
        """
        This is the constructor of the MediaCollector
        ________________________________________
        input:
                pathsCollector    PathsCollector    paths to the collector elements (card.ini, image.jpg ...)
        
                titles            IniTitles         represents the [titles] section
                control           IniControl        represents the [control] section
                general           IniGeneral        represents the [general] section
                classification    IniClassification represents the [classification] section
        """
        super().__init__(titles, control, general, classification)
        
#        NoneType = type(None)
#        assert issubclass(parentCollector.__class__, (MediaCollector, NoneType)), general.__class__
        assert issubclass(pathsCollector.__class__, PathsCollector)
        
        self.pathsCollector = pathsCollector
        self.media_collector_list = []
        self.media_storage_list = []
        
        self.nextLevelListener = None
#        self.previousLevelListener = None

#    def doSelection(self):
#        if self.hasNextLevelListener():
#            self.media.getNextLevelListener()(self.media)
#        elif self.getRoot().hasNextLevelListener():
#            self.media.getRoot().getNextLevelListener()(self.media)
#        else:
#            mcl = self.getMediaCollectorList()
#            msl = self.getMediaStorageList()
#            sum_list = mcl + msl
#            if sum_list:
#                self.card_holder.refresh(sum_list)

    def getNameOfFolder(self):
        return self.pathsCollector.getNameOfFolder()
    
    def getPathOfImage(self):
        return self.pathsCollector.getPathOfImage()
    
    def getPathOfCard(self):
        return self.pathsCollector.getPathOfCard()
    
    def getBackgroundColor(self):
        return COLLECTOR_BACKGROUND_COLOR
        
    def getFolderType(self):
        return "collector" 
        
    def addMediaCollector(self, mediaCollector):
        """
        Adds a new MediaCollector to this MediaCollector
        It is ordered accordingly the language by the control.orderby
        _____________________________________________________________
        input:
                mediaCollector    MediaCollector    the MediaCollector to add
        """
        
        assert issubclass(mediaCollector.__class__, MediaCollector)
        
        mediaCollector.setParentCollector(self)
        
        # Add the MediaCollector
        self.media_collector_list.append(mediaCollector)
        
        # Sort the list
        self.sortMediaCollector()
        
    def addMediaStorage(self, mediaStorage):
        """
        Adds a new MediaStorage to this MediaCollector
        It is ordered accordingly the language by the control.orderby
        _____________________________________________________________
        input:
                mediaStorage    MediaStorage    the MediaStorage to add
        """
        
        assert issubclass(mediaStorage.__class__, MediaStorage) 

        mediaStorage.setParentCollector(self)

        # Add the MediaStorage
        self.media_storage_list.append(mediaStorage)
        
        # Sort the list
        self.sortMediaStorage()
    
    def getPathsCollector(self):
        return self.pathsCollector
        
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
        self.media_collector_list.sort(key=lambda arg: MediaCollector.sort_key(arg))
        
    def sortMediaStorage(self):
        """
        Sort the MediaStorage regarding to the control.orderby
           = title
           = folder
           = series
        """
        self.media_storage_list.sort(key=lambda arg: MediaStorage.sort_key(arg))

                
    def getHierarchyTitle(self, space):
        out = space + "<C> " + self.getTranslatedTitle() + "\n"        
        
        for collector in self.media_collector_list:
            out += collector.getHierarchyTitle(space + "   ")
            
        for storage in self.media_storage_list:
            out += storage.getHierarchyTitle(space + "   ")        
        return out

    def hasNextLevelListener(self):
        if self.nextLevelListener:
            return True
        else:
            return False
        
    def getNextLevelListener(self):
        return self.nextLevelListener
    
    def setNextLevelListener(self, nextLevelListener):
        """
            From outside, it is needed to provide a METHOD as the nextLevelListener parameter, 
            which will handle the selection of the actual MediaCollector - goes one level deeper 
            ________________________________________
            input:
                    nextLevelListener    Function    handles the selection of this mediaCollector

        """
        self.nextLevelListener = nextLevelListener

#    def setPreviousLevelListener(self, previousLevelListener):
#        """
#            From outside, it is needed to provide a METHOD as the previousLevelListener parameter, 
#            which will handle the Escape on the actual MediaCollector - goes one level higher 
#            ________________________________________
#            input:
#                    previousLevelListener    Function    handles the Escape
#
#        """
#        self.previousLevelListener = previousLevelListener
        
    def getQLabelToHoldImage(self):
        """
            Gives back a class extending QLabel which will keep the image.
            This class has to implement the 'toDoOnClick' method which
            handles the selection of this MediaCollector
        """
        class QLabelWithLinkToNextLevel( QLabelToLinkOnClick ):
            def __init__(self, collector):
                super().__init__(collector, None, collector.isSelected)

            def toDoSelection(self):
#                self.media.doSelection()
                if self.media.hasNextLevelListener():
                    self.media.getNextLevelListener()(self.media)
                elif self.media.getRoot().hasNextLevelListener():
                    self.media.getRoot().getNextLevelListener()(self.media)
        
        return QLabelWithLinkToNextLevel(self)



    def getJson(self):
        json = super().getJson();
        
        json['paths-collector'] = self.getPathsCollector().getJson()
                
        json['collectors'] = [c.getJson() for c in self.media_collector_list]
        json['storages'] = [c.getJson() for c in self.media_storage_list]
        return json
        