import subprocess
import platform

from medlib.constants import *
from medlib.handle_property import _

from medlib.mediamodel.media_base import MediaBase 
from medlib.mediamodel.media_base import FOLDER_TYPE_STORAGE

from medlib.mediamodel.paths_storage import PathsStorage

from medlib.mediamodel.qlabel_to_link_on_cllick import QLabelToLinkOnClick

class MediaStorage(MediaBase):
    """
    This object represents the MediaStorage 
    This container can contain
    """
    
    def __init__(self, pathsStorage, titles, control, general=None,  classification=None):
        """
        This is the constructor of the MediaStorage
        ___________________________________________
        input:
                pathsStorage    PathsStorage      paths to the media content (card.ini, image.jpg, media)

                titles          IniTitles         represents the [titles] section
                control         IniControl        represents the [control] section
                general         IniGeneral        represents the [general] section
                classification          IniRating         represents the [classification] section
        """
        super().__init__(titles, control, general, classification)
        
        assert issubclass(pathsStorage.__class__, PathsStorage)
        
        self.pathsStorage = pathsStorage
        self.media_appendix_list = []

    def getNameOfFolder(self):
        return self.pathsStorage.getNameOfFolder()
    
    def getPathOfImage(self):
        return self.pathsStorage.getPathOfImage()

    def getPathOfMedia(self):
        return self.pathsStorage.getPathOfMedia()
    
    def getPathOfCard(self):
        return self.pathsStorage.getPathOfCard()

    def getBackgroundColor(self):
        return STORAGE_BACKGROUND_COLOR

    def getFolderType(self):
        return FOLDER_TYPE_STORAGE 
    
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

    def getQLabelToHoldImage(self):
        class QLabelWithLinkToMedia( QLabelToLinkOnClick ):

            def __init__(self, media, funcIsSelected, pathOfMedia):
                super().__init__(media, None, funcIsSelected)
                self.pathOfMedia = pathOfMedia

            def toDoSelection(self):
        
                if platform.system() == 'Darwin':                   # macOS
                    subprocess.call(('open', self.pathOfMedia))
                elif platform.system() == 'Windows':                # Windows
                    os.startfile(filepath)
                elif platform.system() == 'Linux':                  # Linux:
                    subprocess.call(('xdg-open', self.pathOfMedia))
                else:                                               # linux 
                    subprocess.call(('xdg-open', self.pathOfMedia))

        
        return QLabelWithLinkToMedia(self, self.isSelected, self.getPathOfMedia())

    def setNextLevelListener(self, nextLevelListener):
        pass
    
            
    def getJson(self):
        json = super().getJson();
        
        json['paths-storage'] = self.pathsStorage.getJson()
                
        return json

        