import subprocess
import platform

from medlib.constants import *
from medlib.handle_property import _

from medlib.mediamodel.media_base import MediaBase 
from medlib.mediamodel.media_base import FOLDER_TYPE_STORAGE

from medlib.mediamodel.paths_storage import PathsStorage

from medlib.mediamodel.qlabel_to_link_on_cllick import QLabelToLinkOnClick
from PyQt5.QtGui import QKeyEvent
from PyQt5 import QtCore
from PyQt5.QtCore import QEvent

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

            def toDoOnClick(self):
                """
                When the user Left-Mouse-Click on the Image
                
                Delegate the Click on the Image as a SPACE key press to up. 
                This event can be caught it in the higher level Widget as a SPACE key press
                (for example in CardHolder)

                I could have made a direct selection in the media_collector/media_storage
                using the toDoOnClick() method, but I do not do this because in that case 
                I could not have the index of the selected Card  
                """
#        event = QKeyEvent(QEvent.KeyPress, QtCore.Qt.Key_Space, Qt.NoModifier, str(self.media.getCard().getIndexInDataList()))
                event = QKeyEvent(QEvent.KeyPress, QtCore.Qt.Key_Space, Qt.NoModifier, str(self.media.getIndex()))
                QtCore.QCoreApplication.postEvent(self, event)
 
            def toDoSelection(self):
                """
                In the CardHolder the Space/Enter triggers
                Plays the media regarding on the configuration in the OS
                """

                if platform.system() == 'Darwin':                   # macOS
                    subprocess.call(('open', self.pathOfMedia))
                elif platform.system() == 'Windows':                # Windows
                    os.startfile(self.pathOfMedia)
                elif platform.system() == 'Linux':                  # Linux:
                    subprocess.call(('xdg-open', self.pathOfMedia))
                else:                                               # linux 
                    subprocess.call(('xdg-open', self.pathOfMedia))
        
        return QLabelWithLinkToMedia(self, self.isInFocus, self.getPathOfMedia())

    def setNextLevelListener(self, nextLevelListener):
        pass    
            
    def getJson(self):
        json = super().getJson();
        
        json['paths-storage'] = self.pathsStorage.getJson()
                
        return json

        