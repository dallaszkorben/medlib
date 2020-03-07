import os
import configparser
from pathlib import Path
from medlib import card_ini

#from akoteka.logger import logger

class Property(object):
 
    def __init__(self, file, writable=False, folder=None):
        self.writable = writable
        self.file = file
        self.folder = folder
        self.parser = configparser.RawConfigParser()

        # !!! make it CASE SENSITIVE !!! otherwise it duplicates the hit if there was a key with upper and lower cases. Now it throws an exception
        self.parser.optionxform = str

    def __write_file(self):

        if self.folder:
            Path(self.folder).mkdir(parents=True, exist_ok=True)

        with open(self.file, 'w', encoding='utf-8') as configfile:
            self.parser.write(configfile)


    def get(self, section, key, default_value, writable=None):

        # if not existing file and we want to create it
        if not os.path.exists(self.file) and self.should_write(writable) :
            #self.log_msg("MESSAGE: No file found FILE NAME: " + self.file + " OPERATION: get")

            self.parser[section]={key: default_value}
            self.__write_file()
        self.parser.read(self.file, encoding='utf-8')

        # try to read the key
        try:
            result=self.parser.get(section,key)

            # if it is EMPTY
            if not result:
                result = default_value

        # if does not exist the key
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            #self.log_msg("MESSAGE: " + str(e) + " FILE NAME: " + self.file + " OPERATION: get")

            # if it should be write
            if self.should_write(writable):
                self.update(section, key, default_value)
                result=self.parser.get(section,key)
            else:
                result = default_value

        return result

    def getBoolean(self, section, key, default_value, writable=None):

        # if not existing file and we want to create it
        if not os.path.exists(self.file) and self.should_write(writable) :
            self.parser[section]={key: default_value}
            self.__write_file()

        # read the file
        self.parser.read(self.file, encoding='utf-8')

        # try to read the key
        try:
            result=self.parser.getboolean(section, key)

        # if does not exist the key
        except (configparser.NoSectionError, configparser.NoOptionError):

            # if it should be write
            if self.should_write(writable):

                self.update(section, key, default_value)
                # It is strange how it works with get/getboolean
                # Sometimes it reads boolean sometimes it reads string
                # I could not find out what is the problem
                #result=self.parser.get(section,key)
            result=default_value

        return result

    def update(self, section, key, value, source=None):

        # if not existing file        
        if not os.path.exists(self.file):
            #self.log_msg("MESSAGE: No file found FILE NAME: " + self.file + " OPERATION: update SOURCE: " + source if source else "")
            self.parser[section]={key: value}

        # if the file exists
        else:

            # read the file
            self.parser.read(self.file, encoding='utf-8')

            # try to set the value
            try:
                # if no section -> NoSectionError | if no key -> Create it
                self.parser.set(section, key, value)

            # if there is no such section
            except configparser.NoSectionError as e:
                #self.log_msg("MESSAGE: " + str(e) + " FILE NAME: " + self.file + " OPERATION: update SOURCE: " + source)
                self.parser[section]={key: value}

        # update
        self.__write_file()
        
    def removeSection(self, section):
        self.parser.remove_section(section)
        self.__write_file()

    def removeOption(self, section, option):
        self.parser.read(self.file, encoding='utf-8')
        self.parser.remove_option(section, option)
        self.__write_file()
        
    def getOptions(self, section):
        try:
            return dict(self.parser.items(section))
        except configparser.NoSectionError as e:
            return None
    
    def should_write(self, writable):
        return ((writable is None and self.writable) or (writable))

# ====================
#
# Handle dictionary
#
# Singleton
#
# ====================
class Dict( Property ):
    
    DICT_FILE_PRE = "resources"
    DICT_FILE_EXT = "properties"
    DICT_FOLDER = "dict"
    DICT_SECTION = "dict"

    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls, lng):
        inst = cls.__new__(cls)
        cls.__init__(cls.__instance, lng)     
        return inst
        
    def __init__(self, lng):
        file = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.__class__.DICT_FOLDER, self.__class__.DICT_FILE_PRE + "_" + lng + "." + self.__class__.DICT_FILE_EXT)
        super().__init__( file )
    
    def _(self, key):
        return self.get(self.__class__.DICT_SECTION, key,  "[" + key + "]")

class Config:
    HOME = str(Path.home())
    CONFIG_FOLDER = '.medlib'
    
    @staticmethod 
    def get_path_to_config_folder():
        return os.path.join(Config.HOME, Config.CONFIG_FOLDER)


# =====================
#
# Handle config.ini
#
# =====================
class ConfigIni( Property ):
    INI_FILE_NAME="config.ini"

    # (section, key, default)
    DEFAULT_LANGUAGE = ("general", "language", "hu")
    DEFAULT_SCALE = ("general", "scale", 1)
    DEFAULT_SHOW_ORIGINAL_TITLE = ("general", "show-original-title", "n")
    DEFAULT_KEEP_HIERARCHY = ("general", "keep-hierarchy", "y")
    DEFAULT_USE_XDG = ("general", "use-xdg", "y")

    DEFAULT_MEDIA_PATH = ("media", "media-path", ".")    
    
#    DEFAULT_MEDIA_PLAYER_VIDEO = ("media", "player-video", "mplayer")
#    DEFAULT_MEDIA_PLAYER_VIDEO_PARAM = ("media", "player-video-param", "-zoom -fs -framedrop")
#    DEFAULT_MEDIA_PLAYER_VIDEO_EXT = ("media", "player-video-ext", "flv,divx,mkv,avi,mp4,webm")
#    DEFAULT_MEDIA_PLAYER_AUDIO = ("media", "player-audio", "rhythmbox")
#    DEFAULT_MEDIA_PLAYER_AUDIO_PARAM = ("media", "player-audio-param", "")
#    DEFAULT_MEDIA_PLAYER_AUDIO_EXT = ("media", "player-audio-ext", "mp3,ogg")
#
#    DEFAULT_MEDIA_PLAYER_ODT = ("media", "player-odt", "libreoffice")
#    DEFAULT_MEDIA_PLAYER_ODT_PARAM = ("media", "player-odt-param", "--writer --quickstart --nofirststartwizard --view")
#    DEFAULT_MEDIA_PLAYER_ODT_EXT = ("media", "player-odt-ext", "odt")
#
#    DEFAULT_MEDIA_PLAYER_PDF = ("media", "player-pdf", "okular")
#    DEFAULT_MEDIA_PLAYER_PDF_PARAM = ("media", "player-pdf-param", "--presentation --page 1 --unique")
#    DEFAULT_MEDIA_PLAYER_PDF_EXT = ("media", "player-pdf-ext", "pdf")
    
    __instance = None    

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        inst = cls.__new__(cls)
        cls.__init__(cls.__instance)
        return inst
        
    def __init__(self):
        folder = os.path.join(Config.HOME, Config.CONFIG_FOLDER)
        file = os.path.join(folder, ConfigIni.INI_FILE_NAME)
        super().__init__( file, True, folder )

    def getLanguage(self):
        return self.get(self.DEFAULT_LANGUAGE[0], self.DEFAULT_LANGUAGE[1], self.DEFAULT_LANGUAGE[2])

    def getScale(self):
        return self.get(self.DEFAULT_SCALE[0], self.DEFAULT_SCALE[1], self.DEFAULT_SCALE[2])

    def getShowOriginalTitle(self):
        return self.get(self.DEFAULT_SHOW_ORIGINAL_TITLE[0], self.DEFAULT_SHOW_ORIGINAL_TITLE[1], self.DEFAULT_SHOW_ORIGINAL_TITLE[2])

    def getKeepHierarchy(self):
        return self.get(self.DEFAULT_KEEP_HIERARCHY[0], self.DEFAULT_KEEP_HIERARCHY[1], self.DEFAULT_KEEP_HIERARCHY[2])

    def getUseXdg(self):
        return self.get(self.DEFAULT_USE_XDG[0], self.DEFAULT_USE_XDG[1], self.DEFAULT_USE_XDG[2])

    def getMediaPath(self):
        return self.get(self.DEFAULT_MEDIA_PATH[0], self.DEFAULT_MEDIA_PATH[1], self.DEFAULT_MEDIA_PATH[2])





#    def getMediaPlayerWithParameters(self, media, extension):
#        """
#            Returns a tuple with the player name and the necessary parameters
#            according to the 'media' and the file's extension
#            
#            This method assumes that config.ini file exist for the user
#            If it does not then the file will be created.
#            If the section or the key does not
#        """
#
#        default_player = self.get('player', media, None)
#        specific_player = self.get('player', media + "-" + extension, None)
#        
#        # if not the general neither the specific player does not exists
#        if specific_player is None and default_player is None:
#            return None
#                
#        if specific_player is not None:
#            result=specific_player.split(",")
#        else:
#            result=default_player.split(",")
#
#        return (result[0], result[1] if len(result) > 1 else None)
#            
#
#
#    def get_media_player_video(self):
#        return self.get(self.DEFAULT_MEDIA_PLAYER_VIDEO[0], self.DEFAULT_MEDIA_PLAYER_VIDEO[1], self.DEFAULT_MEDIA_PLAYER_VIDEO[2])
#
#    def get_media_player_video_param(self):
#        return self.get(self.DEFAULT_MEDIA_PLAYER_VIDEO_PARAM[0], self.DEFAULT_MEDIA_PLAYER_VIDEO_PARAM[1], self.DEFAULT_MEDIA_PLAYER_VIDEO_PARAM[2])
#
#    def get_media_player_video_ext(self):
#        return self.get(self.DEFAULT_MEDIA_PLAYER_VIDEO_EXT[0], self.DEFAULT_MEDIA_PLAYER_VIDEO_EXT[1], self.DEFAULT_MEDIA_PLAYER_VIDEO_EXT[2])
#
#    def get_media_player_audio(self):
#        return self.get(self.DEFAULT_MEDIA_PLAYER_AUDIO[0], self.DEFAULT_MEDIA_PLAYER_AUDIO[1], self.DEFAULT_MEDIA_PLAYER_AUDIO[2])
#
#    def get_media_player_audio_param(self):
#        return self.get(self.DEFAULT_MEDIA_PLAYER_AUDIO_PARAM[0], self.DEFAULT_MEDIA_PLAYER_AUDIO_PARAM[1], self.DEFAULT_MEDIA_PLAYER_AUDIO_PARAM[2])
#
#    def get_media_player_audio_ext(self):
#        return self.get(self.DEFAULT_MEDIA_PLAYER_AUDIO_EXT[0], self.DEFAULT_MEDIA_PLAYER_AUDIO_EXT[1], self.DEFAULT_MEDIA_PLAYER_AUDIO_EXT[2])
#
#
#    def get_media_player_odt(self):
#        return self.get(self.DEFAULT_MEDIA_PLAYER_ODT[0], self.DEFAULT_MEDIA_PLAYER_ODT[1], self.DEFAULT_MEDIA_PLAYER_ODT[2])
#
#    def get_media_player_odt_param(self):
#        return self.get(self.DEFAULT_MEDIA_PLAYER_ODT_PARAM[0], self.DEFAULT_MEDIA_PLAYER_ODT_PARAM[1], self.DEFAULT_MEDIA_PLAYER_ODT_PARAM[2])
#
#    def get_media_player_odt_ext(self):
#        return self.get(self.DEFAULT_MEDIA_PLAYER_ODT_EXT[0], self.DEFAULT_MEDIA_PLAYER_ODT_EXT[1], self.DEFAULT_MEDIA_PLAYER_ODT_EXT[2])
#
#    def get_media_player_pdf(self):
#        return self.get(self.DEFAULT_MEDIA_PLAYER_PDF[0], self.DEFAULT_MEDIA_PLAYER_PDF[1], self.DEFAULT_MEDIA_PLAYER_PDF[2])
#
#    def get_media_player_pdf_param(self):
#        return self.get(self.DEFAULT_MEDIA_PLAYER_PDF_PARAM[0], self.DEFAULT_MEDIA_PLAYER_PDF_PARAM[1], self.DEFAULT_MEDIA_PLAYER_PDF_PARAM[2])
#
#    def get_media_player_pdf_ext(self):
#        return self.get(self.DEFAULT_MEDIA_PLAYER_PDF_EXT[0], self.DEFAULT_MEDIA_PLAYER_PDF_EXT[1], self.DEFAULT_MEDIA_PLAYER_PDF_EXT[2])





    def setLanguage(self, lang):
        self.update(self.DEFAULT_LANGUAGE[0], self.DEFAULT_LANGUAGE[1], lang)

    def setScale(self, scale):
        self.update(self.DEFAULT_SCALE[0], self.DEFAULT_SCALE[1], scale)

    def setShowOriginal_title(self, show):
        self.update(self.DEFAULT_SHOW_ORIGINAL_TITLE[0], self.DEFAULT_SHOW_ORIGINAL_TITLE[1], show)

    def setKeepHierarchy(self, keep):
        self.update(self.DEFAULT_KEEP_HIERARCHY[0], self.DEFAULT_KEEP_HIERARCHY[1], keep)

    def setMediaPath(self, path):
        self.update(self.DEFAULT_MEDIA_PATH[0], self.DEFAULT_MEDIA_PATH[1], path)

    def setUseXdg(self, use_xdg):
        self.update(self.DEFAULT_USE_XDG[0], self.DEFAULT_USE_XDG[1], use_xdg)




#    def set_media_player_video(self, player):
#        self.update(self.DEFAULT_MEDIA_PLAYER_VIDEO[0], self.DEFAULT_MEDIA_PLAYER_VIDEO[1], player)
#
#    def set_media_player_video_param(self, param):
#        self.update(self.DEFAULT_MEDIA_PLAYER_VIDEO_PARAM[0], self.DEFAULT_MEDIA_PLAYER_VIDEO_PARAM[1], param)
#
#    def set_media_player_video_ext(self, param):
#        self.update(self.DEFAULT_MEDIA_PLAYER_VIDEO_EXT[0], self.DEFAULT_MEDIA_PLAYER_VIDEO_EXT[1], param)
#
#    def set_media_player_audio(self, player):
#        self.update(self.DEFAULT_MEDIA_PLAYER_AUDIO[0], self.DEFAULT_MEDIA_PLAYER_AUDIO[1], player)
#
#    def set_media_player_audio_param(self, param):
#        self.update(self.DEFAULT_MEDIA_PLAYER_AUDIO_PARAM[0], self.DEFAULT_MEDIA_PLAYER_AUDIO_PARAM[1], param)
#
#    def set_media_player_audio_ext(self, param):
#        self.update(self.DEFAULT_MEDIA_PLAYER_AUDIO_EXT[0], self.DEFAULT_MEDIA_PLAYER_AUDIO_EXT[1], param)

def updateCardIni(card_ini_path, section, key, value):
    card_ini = Property(card_ini_path, True)
    card_ini.update(section, key, value)

def getConfigIni():
    return ConfigIni.getInstance()

def reReadConfigIni():
    global config_ini
    global dic
    
    ci = getConfigIni()
    
    # Read config.ini    
    config_ini['language'] = ci.getLanguage()
    config_ini['scale'] = ci.getScale()
    config_ini['show_original_title'] = ci.getShowOriginalTitle()
    config_ini['keep_hierarchy'] = ci.getKeepHierarchy()
    config_ini['use_xdg'] = ci.getUseXdg()
    config_ini['media_path'] = ci.getMediaPath()
    
    options = ci.getOptions('player')
    for key in options:
        config_ini['player_' + key.replace("-","_")] = options[key]

    # Get the dictionary
    dic = Dict.getInstance( config_ini['language'] )

# --------------------------------------------------------
# --------------------------------------------------------
#
# Gives back the translation of the word
#
# word      word which should be translated
#
# --------------------------------------------------------
# --------------------------------------------------------
def _(word):
    return dic._(word)

# ----------------------------------------------------------------------------------------------------
#
# Below code runs when it imported or forced to re-run
#
# How to use dic:
#            - in the beginning of your code define: "from akoteka.handle_property import _"
#            - define the translations in the "akoteka.dict.resources_<lang>.properties file
#            - in the code where you need the translated word use: "_('word_to_translate')"
#
# How to use config_ini:
#            - your "config.ini" file is in "HOME/.akoteka" folder
#            - there are key-value pairs defined in the file
#            - in the beginning of your code: "from akoteka.handle_property import config_ini"
#            - you can refer to the contents like: "config_ini('language')"
#
# -----------------------------------------------------------------------------------------------------
config_ini = {}
reReadConfigIni()



