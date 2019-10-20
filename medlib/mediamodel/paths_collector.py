class PathsCollector(object):
    """
    This class represents the paths to the container elements
    """
    
    def __init__(self, name_folder, path_card, path_image):
        """
        This is the constructor of the ContainerPaths class
        ___________________________________________________
        input:
            name_folder        string        name of the folder of the MediaContainer
            path_card           string        path to the ini file - for storing data
            path_image          string        path to the jpeg file - for showing the image
        """
        self.name_folder = name_folder
        self.path_card = path_card
        self.path_image = path_image
        
    def getNameOfFolder(self):
        return self.name_folder
        
    def getPathOfCard(self):
        return self.path_card
    
    def getPathOfImage(self):
        return self.path_image 
