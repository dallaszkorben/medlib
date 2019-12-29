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

class CardIni(object):

    @staticmethod
    def getSectionList():
        return ('titles', 'storyline', 'general', 'rating', 'links', 'control')

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
        category = {
            'titles': ('movie', 'music', 'show', 'presentation', 'alternative', 'miscellaneous'),
            'storyline': (),
            
            'general': ({'year': (True, 'setYear',)},
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
                        {'storyline', (False, 'setStoryline',)},
                        {'topic', (True, 'setTopic',)},
                        {'lyrics', (True, 'setLyrics',)},
                        {'series', (True, 'setSeries',)},
                        {'episode', (True, 'setEpiside',)},
                        ),



            'rating': ('new','favorite','rate'),
            'links': (),
            'control': ('orderby', 'media', 'category')
        }
        return category[section]
    


