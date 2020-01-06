import re

media_dict = {
    'video': {
        'ext': ('mkv', 'mp4', 'flv', 'divx', 'avi', 'webm'), 
        'category': ('movie', 'music', 'show', 'presentation', 'alternative', 'miscellaneous', 'appendix')},
    'audio': {
        'ext': ('mp3', 'ogg'), 
        'category': ('radioplay', 'music', 'show', 'presentation', 'audiobook', 'appendix')},
    'text': {
        'ext': ('doc', 'odt', 'pdf', 'epub', 'mobi', 'azw', 'azw3', 'iba', 'txt'), 
        'category': ('book', 'presentation', 'quiz', 'appendix')},
    'dia': {
        'ext': (), 
        'category': ()},
    'picture': {
        'ext': (), 
        'category': ()},
    'link' : {
        'ext': (), 
        'category': ('appendix',)},
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
        {'series': (True, 'setSeries',)},
        {'episode': (True, 'setEpiside',)},
        ),


    'classification': ('rate', 'tag', 'new','favorite'),
    
    'control': ('orderby', 'media', 'category'),
    
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

SECTION_TITLES = CardIni.getSectionList()[0]
SECTION_STORYLINE = CardIni.getSectionList()[1]
SECTION_TOPIC = CardIni.getSectionList()[2]
SECTION_LYRICS = CardIni.getSectionList()[3]
SECTION_GENERAL = CardIni.getSectionList()[4]
SECTION_CLASSIFICATION = CardIni.getSectionList()[5]
SECTION_CONTROL = CardIni.getSectionList()[6]
SECTION_MEDIA = CardIni.getSectionList()[7]

KEY_CLASSIFICATION_RATE = section_dict[SECTION_CLASSIFICATION][0]
KEY_CLASSIFICATION_TAG = section_dict[SECTION_CLASSIFICATION][1]
KEY_CLASSIFICATION_NEW = section_dict[SECTION_CLASSIFICATION][2]
KEY_CLASSIFICATION_FAVORITE = section_dict[SECTION_CLASSIFICATION][3]

KEY_CONTROL_ORDERBY = section_dict[SECTION_CONTROL][0]
KEY_CONTROL_MEDIA = section_dict[SECTION_CONTROL][1]
KEY_CONTROL_CATEGORY = section_dict[SECTION_CONTROL][2]

KEY_GENERAL_LENGTH = list(section_dict['general'][0].keys())[0]
KEY_GENERAL_YEAR = list(section_dict['general'][1].keys())[0]
KEY_GENERAL_DIRECTOR = list(section_dict['general'][2].keys())[0]
KEY_GENERAL_MAKER = list(section_dict['general'][3].keys())[0]
KEY_GENERAL_WRITER = list(section_dict['general'][4].keys())[0]
KEY_GENERAL_AUTHOR = list(section_dict['general'][5].keys())[0]
KEY_GENERAL_ACTOR = list(section_dict['general'][6].keys())[0]
KEY_GENERAL_PERFORMER = list(section_dict['general'][7].keys())[0]
KEY_GENERAL_LECTURER = list(section_dict['general'][8].keys())[0]
KEY_GENERAL_CONTRIBUTOR = list(section_dict['general'][9].keys())[0]
KEY_GENERAL_VOICE = list(section_dict['general'][10].keys())[0]
KEY_GENERAL_GENRE = list(section_dict['general'][11].keys())[0]
KEY_GENERAL_THEME = list(section_dict['general'][12].keys())[0]
KEY_GENERAL_SUB = list(section_dict['general'][13].keys())[0]
KEY_GENERAL_SOUND = list(section_dict['general'][14].keys())[0]
KEY_GENERAL_COUNTRY = list(section_dict['general'][15].keys())[0]
KEY_GENERAL_SERIES = list(section_dict['general'][16].keys())[0]
KEY_GENERAL_EPISODE = list(section_dict['general'][17].keys())[0]

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

JSON_KEY_STORAGE_NAME_OF_FOLDER = 'name-of-folder'
JSON_KEY_STORAGE_PATH_OF_CARD = 'path-of-card'
JSON_KEY_STORAGE_PATH_OF_IMAGE = 'path-of-image'
JSON_KEY_STORAGE_PATH_OF_MEDIA = 'path-of-media'

JSON_KEY_APPENDIX_NAME_OF_FOLDER = 'name-of-folder'
JSON_KEY_APPENDIX_PATH_OF_CARD = 'path-of-card'
JSON_KEY_APPENDIX_PATH_OF_IMAGE = 'path-of-image'
JSON_KEY_APPENDIX_PATH_OF_MEDIA = 'path-of-media'

JSON_KEY_CLASSIFICATION_RATE = KEY_CLASSIFICATION_RATE
JSON_KEY_CLASSIFICATION_TAG = KEY_CLASSIFICATION_TAG
JSON_KEY_CLASSIFICATION_NEW = KEY_CLASSIFICATION_NEW
JSON_KEY_CLASSIFICATION_FAVORITE = KEY_CLASSIFICATION_FAVORITE

JSON_KEY_CONTROL_ORDERBY = KEY_CONTROL_ORDERBY
JSON_KEY_CONTROL_MEDIA = KEY_CONTROL_MEDIA
JSON_KEY_CONTROL_CATEGORY = KEY_CONTROL_CATEGORY

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
JSON_KEY_GENERAL_SERIES = KEY_GENERAL_SERIES
JSON_KEY_GENERAL_EPISODE = KEY_GENERAL_EPISODE

