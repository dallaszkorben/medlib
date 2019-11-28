from medlib.mediamodel.paths_storage import PathsStorage

class PathsAppendix(PathsStorage):
    """
    This class represents the paths to the content elements
    """
    
    def __init__(self, name_folder, path_ini, path_jpeg, path_media):
        """
        This is the constructor of the ContainerPaths class
        ___________________________________________________
        input:
            name_folder        string        name of the folder of the MediaContainer
            path_ini           string        path to the ini file - for storing data
            path_jpeg          string        path to the jpeg file - for showing the image
            path_media         string        path to the media file - to play/show
        """
        super().__init__(name_folder, path_ini, path_jpeg, path_media)