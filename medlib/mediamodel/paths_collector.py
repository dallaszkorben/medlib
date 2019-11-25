class PathsCollector(object):
    """
    This class represents the paths to the container elements
    """
    
    def __init__(self, nameFolder, pathCard, pathImage):
        """
        This is the constructor of the ContainerPaths class
        ___________________________________________________
        input:
            nameFolder        string        name of the folder of the MediaContainer
            pathCard          string        path to the ini file - for storing data
            pathImage         string        path to the jpeg file - for showing the image
        """
        self.nameFolder = nameFolder
        self.pathCard = pathCard
        self.pathImage = pathImage
        
    def getNameOfFolder(self):
        return self.nameFolder
        
    def getPathOfCard(self):
        return self.pathCard
    
    def getPathOfImage(self):
        return self.pathImage 
