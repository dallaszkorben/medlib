import re

media_dict = {
    'video': {
        'ext': ('mkv', 'mp4', 'flv', 'divx', 'avi', 'webm'), 
        'category': ('movie', 'music', 'show', 'presentation', 'alternative', 'miscellaneous', 'elearning', 'family', 'appendix')},
    'audio': {
        'ext': ('mp3', 'ogg'), 
        'category': ('radioplay', 'music', 'show', 'presentation', 'audiobook', 'elearning', 'appendix')},
    'text': {
        'ext': ('doc', 'odt', 'pdf', 'epub', 'mobi', 'azw', 'azw3', 'iba', 'txt','rtf'), 
        'category': ('book', 'presentation', 'quiz', 'elearning', 'appendix')},
    'image': {
        'ext': ('jpg', 'jpeg', 'png'), 
        'category': ('elearning',)},
    'link' : {
        'ext': (), 
        'category': ('appendix','elearning')},
    '': {
        'ext': (), 
        'category': ()}
}

section_dict = {
    'titles': (),
    'storyline': (),
    'topic': (),
    'lyrics': (),               
    'general': (
        {'length': (True, 'setYear',)},
        {'year': (True, 'setYear',)},
        {'director': (True, 'setDirectors',)},
        {'maker': (True, 'setMakers',)},
        {'writer': (True, 'setWriters',)},
        {'author': (True, 'setAuthors',)},
        {'actor': (True, 'setActors',)},
        {'performer': (True, 'setPerformers',)},
        {'lecturer': (True, 'setLecturers',)},
        {'contributor': (True, 'setContributors',)},
        {'voice': (True, 'setVoices',)},
        {'genre': (True, 'setGenres',)},
        {'theme': (True, 'setThemes',)},
        {'sub': (True, 'setThemes',)},
        {'sound': (True, 'setThemes',)},
        {'country': (True, 'setThemes',)},
        {'season': (True, 'setSeason',)},
        {'episode': (True, 'setEpiside',)},
        {'album': (True, 'setAlbum',)},
        {'track': (True, 'setTrack',)},
        ),
    'classification': ('rate', 'tag', 'new','favorite'),    
    'control': ('orderby', 'media', 'category', 'iconkey'),    
    'media': ('link', 'file'),    
    'appendixes': (),    
    'links': (),
}



class CardIni(object):

    @staticmethod
    def getSectionList():
        return list(section_dict.keys()) 

    @staticmethod
    def getMediaList():
        return list(media_dict.keys())
    
    @staticmethod
    def getCategoryListByMedia(media):
        return media_dict[media]['category']

    @staticmethod
    def getExtensionListByMedia(media):
        return media_dict[media]['ext']

    @staticmethod
    def getMediaFilePatternByMedia(media):
        
        ptrn = '|'.join( media_dict[media]['ext'] )
        return re.compile( '^.+[.](' + ptrn + ')$' )

    @staticmethod
    def getOrderByList():
        return ('folder', 'title')

    @staticmethod
    def getKeyListBySection(section):        
        return section_dict[section]        
    
    @staticmethod
    def getSectionDict():
        return section_dict

CARD_INI_FILE_NAME = 'card.ini'
CARD_LIST_JSON_FILE_NAME = 'card.list.json'

SECTION_TITLES = 'titles'
SECTION_STORYLINE = 'storyline'
SECTION_TOPIC = 'topic'
SECTION_LYRICS = 'lyrics'
SECTION_GENERAL = 'general'
SECTION_CLASSIFICATION = 'classification'
SECTION_CONTROL = 'control'
SECTION_MEDIA = 'media'

KEY_CLASSIFICATION_RATE = 'rate'
KEY_CLASSIFICATION_TAG = 'tag'
KEY_CLASSIFICATION_NEW = 'new'
KEY_CLASSIFICATION_FAVORITE = 'favorite'

KEY_CONTROL_ORDERBY = 'orderby'
KEY_CONTROL_MEDIA = 'media'
KEY_CONTROL_CATEGORY = 'category'
KEY_CONTROL_ICONKEY = 'iconkey'

KEY_GENERAL_LENGTH = 'length'
KEY_GENERAL_YEAR = 'year'
KEY_GENERAL_DIRECTOR = 'director'
KEY_GENERAL_MAKER = 'maker'
KEY_GENERAL_WRITER = 'writer'
KEY_GENERAL_AUTHOR = 'author'
KEY_GENERAL_ACTOR = 'actor'
KEY_GENERAL_PERFORMER = 'performer'
KEY_GENERAL_LECTURER = 'lecturer'
KEY_GENERAL_CONTRIBUTOR = 'contributor'
KEY_GENERAL_VOICE = 'voice'
KEY_GENERAL_GENRE = 'genre'
KEY_GENERAL_THEME = 'theme'
KEY_GENERAL_SUB = 'sub'
KEY_GENERAL_SOUND = 'sound'
KEY_GENERAL_COUNTRY = 'country'
KEY_GENERAL_SEASON = 'season'
KEY_GENERAL_EPISODE = 'episode'
KEY_GENERAL_ALBUM = 'album'
KEY_GENERAL_TRACK = 'track'
KEY_GENERAL_INDEX = 'index'

# ---

JSON_SECTION_TITLES = SECTION_TITLES 
JSON_SECTION_STORYLINE = SECTION_STORYLINE 
JSON_SECTION_TOPIC = SECTION_TOPIC 
JSON_SECTION_LYRICS = SECTION_LYRICS 
JSON_SECTION_GENERAL = SECTION_GENERAL
JSON_SECTION_CLASSIFICATION = SECTION_CLASSIFICATION
JSON_SECTION_CONTROL = SECTION_CONTROL

JSON_NODE_COLLECTORS = 'collectors'
JSON_NODE_STORAGES = 'storages'
JSON_NODE_APPENDIXES = 'appendixes'

JSON_NODE_PATH_COLLECTOR = 'paths-collector'
JSON_NODE_PATH_STORAGE = 'paths-storage'
JSON_NODE_PATH_APPENDIX = 'paths-appendix'

JSON_KEY_COLLECTOR_NAME_OF_FOLDER = 'name-of-folder'
JSON_KEY_COLLECTOR_PATH_OF_CARD = 'path-of-card'
JSON_KEY_COLLECTOR_PATH_OF_IMAGE = 'path-of-image'
JSON_KEY_COLLECTOR_PATH_OF_ICON = 'path-of-icon'

JSON_KEY_STORAGE_NAME_OF_FOLDER = 'name-of-folder'
JSON_KEY_STORAGE_PATH_OF_CARD = 'path-of-card'
JSON_KEY_STORAGE_PATH_OF_IMAGE = 'path-of-image'
JSON_KEY_STORAGE_PATH_OF_MEDIA = 'path-of-media'
JSON_KEY_STORAGE_PATH_OF_ICON = 'path-of-icon'
JSON_KEY_STORAGE_MEDIA_EXTENSION = 'media-extension'

JSON_KEY_APPENDIX_NAME_OF_FOLDER = 'name-of-folder'
JSON_KEY_APPENDIX_PATH_OF_CARD = 'path-of-card'
JSON_KEY_APPENDIX_PATH_OF_IMAGE = 'path-of-image'
JSON_KEY_APPENDIX_PATH_OF_MEDIA = 'path-of-media'
JSON_KEY_APPENDIX_MEDIA_EXTENSION = 'media-extension'

JSON_KEY_CLASSIFICATION_RATE = KEY_CLASSIFICATION_RATE
JSON_KEY_CLASSIFICATION_TAG = KEY_CLASSIFICATION_TAG
JSON_KEY_CLASSIFICATION_NEW = KEY_CLASSIFICATION_NEW
JSON_KEY_CLASSIFICATION_FAVORITE = KEY_CLASSIFICATION_FAVORITE

JSON_KEY_CONTROL_ORDERBY = KEY_CONTROL_ORDERBY
JSON_KEY_CONTROL_MEDIA = KEY_CONTROL_MEDIA
JSON_KEY_CONTROL_CATEGORY = KEY_CONTROL_CATEGORY
JSON_KEY_CONTROL_ICONKEY = KEY_CONTROL_ICONKEY

JSON_KEY_GENERAL_LENGTH = KEY_GENERAL_LENGTH
JSON_KEY_GENERAL_YEAR = KEY_GENERAL_YEAR
JSON_KEY_GENERAL_DIRECTOR = KEY_GENERAL_DIRECTOR
JSON_KEY_GENERAL_MAKER = KEY_GENERAL_MAKER
JSON_KEY_GENERAL_WRITER = KEY_GENERAL_WRITER
JSON_KEY_GENERAL_AUTHOR = KEY_GENERAL_AUTHOR
JSON_KEY_GENERAL_ACTOR = KEY_GENERAL_ACTOR
JSON_KEY_GENERAL_PERFORMER = KEY_GENERAL_PERFORMER
JSON_KEY_GENERAL_LECTURER = KEY_GENERAL_LECTURER
JSON_KEY_GENERAL_CONTRIBUTOR = KEY_GENERAL_CONTRIBUTOR
JSON_KEY_GENERAL_VOICE = KEY_GENERAL_VOICE
JSON_KEY_GENERAL_GENRE = KEY_GENERAL_GENRE
JSON_KEY_GENERAL_THEME = KEY_GENERAL_THEME
JSON_KEY_GENERAL_SUB = KEY_GENERAL_SUB
JSON_KEY_GENERAL_SOUND = KEY_GENERAL_SOUND
JSON_KEY_GENERAL_COUNTRY = KEY_GENERAL_COUNTRY
JSON_KEY_GENERAL_SEASON = KEY_GENERAL_SEASON
JSON_KEY_GENERAL_EPISODE = KEY_GENERAL_EPISODE
JSON_KEY_GENERAL_ALBUM = KEY_GENERAL_ALBUM
JSON_KEY_GENERAL_TRACK = KEY_GENERAL_TRACK

