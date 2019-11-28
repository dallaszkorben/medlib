from medlib.mediamodel.paths_collector import PathsCollector

class PathsStorage(PathsCollector):
    """
    This class represents the paths to the content elements
    """
    
    def __init__(self, nameFolder, pathIni, pathJpeg, pathMedia):
        """
        This is the constructor of the ContainerPaths class
        ___________________________________________________
        input:
            nameFolder        string        name of the folder of the MediaContainer
            pathIni           string        path to the ini file - for storing data
            pathJpeg          string        path to the jpeg file - for showing the image
            pathMedia         string        path to the media file - to play/show
        """
        super().__init__(nameFolder, pathIni, pathJpeg)
        self.pathMedia = pathMedia
        
    def getPathOfMedia(self):
        return self.pathMedia

    