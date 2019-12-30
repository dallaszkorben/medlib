import re

media_dict = {
    'video': {
        'ext': ('mkv', 'mp4', 'flv', 'divx', 'avi' 'webm'), 
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
    'titles': ('movie', 'music', 'show', 'presentation', 'alternative', 'miscellaneous'),
    'storyline': (),
    'topic': (),
    'lyrics': (),
               
    'general': (
        {'year': (True, 'setYear',)},
        {'director', (True, 'setDirectors',)},
        {'maker', (True, 'setMakers',)},
        {'writer', (True, 'setWriters',)},
        {'author', (True, 'setAuthors',)},
        {'actor', (True, 'setActors',)},
        {'performer', (True, 'setPerformers',)},
        {'lecturer', (True, 'setLecturers',)},
        {'contributor', (True, 'setContributors',)},
        {'voice', (True, 'setVoices',)},
        {'genre', (True, 'setGenres',)},
        {'theme', (True, 'setThemes',)},
#        {'storyline', (False, 'setStoryline',)},
#        {'topic', (True, 'setTopic',)},
#        {'lyrics', (True, 'setLyrics',)},
        {'series', (True, 'setSeries',)},
        {'episode', (True, 'setEpiside',)},
        ),


    'classification': ('rate', 'tag', 'new','favorite'),
    'control': ('orderby', 'media', 'category'),
    'links': (),

}

class CardIni(object):

    @staticmethod
    def getSectionList():
        return list(section_dict.keys()) 
        #return ('titles', 'storyline', 'general', 'classification', 'links', 'control')

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
    def getKeyList(section):        
        return section_dict[section]
    
    @staticmethod
    def getSectionDict():
        return section_dict

SECTION_TITLES = CardIni.getSectionList()[0]
SECTION_STORYLINE = CardIni.getSectionList()[1]
SECTION_TOPIC = CardIni.getSectionList()[2]
SECTION_LYRICS = CardIni.getSectionList()[3]
SECTION_GENERAL = CardIni.getSectionList()[4]
SECTION_CLASSIFICATION = CardIni.getSectionList()[5]
SECTION_CONTROL = CardIni.getSectionList()[6]

KEY_CLASSIFICATION_RATE = section_dict[SECTION_CLASSIFICATION][0]
KEY_CLASSIFICATION_TAG = section_dict[SECTION_CLASSIFICATION][1]
KEY_CLASSIFICATION_NEW = section_dict[SECTION_CLASSIFICATION][2]
KEY_CLASSIFICATION_FAVORITE = section_dict[SECTION_CLASSIFICATION][3]
