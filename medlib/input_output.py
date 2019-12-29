import os
import re
import json
import configparser

from medlib.mediamodel.media_collector import MediaCollector
from medlib.mediamodel.media_storage import MediaStorage
from medlib.mediamodel.media_appendix import MediaAppendix
from medlib.mediamodel.paths_collector import PathsCollector
from medlib.mediamodel.paths_storage import PathsStorage
from medlib.mediamodel.paths_appendix import PathsAppendix
from medlib.mediamodel.ini_titles import IniTitles 
from medlib.mediamodel.ini_control import IniControl
from medlib.mediamodel.ini_storylines import IniStorylines
from medlib.mediamodel.ini_general import IniGeneral
from medlib.mediamodel.ini_rating import IniRating

from medlib.constants import PATH_FOLDER_CONFIG

from medlib.card_ini import CardIni
from medlib.handle_property import config_ini 

from medlib.mediamodel import ini_storylines

def getPatternImage():
    return re.compile( '^image[.](jp(eg|g)|png)$' )

def getPatternRate():
    return re.compile('^([1][0])|([0-9])$')

def getPatternYear():
    return re.compile('^((19|[2-9][0-9])\d{2})(-((19|[2-9][0-9])\d{2}))?$')

def getPatternNumber():
    return re.compile('^([0-9]+)$')

def getPatternLength():
    return re.compile('^\d{1,3}[:]\d{1,2}$')

def collectCards():
    """
        Reads the Cards. First try to read from the json file.
        If there is no json file then it reads it from the file system and
        then save it to the json file 
    """
    
    media_path = config_ini['media_path']
    
    jsonForm = CardListJson.getInstance().read()

    if not jsonForm:            
        mainCollector = collectCardsFromFileSystem(media_path)
        #jsonForm = mainCollector.getJson()
        #CardListJson.getInstance().write(jsonForm)
        saveJson(mainCollector)
    else: 
        mainCollector = collectCardsFromJson(jsonForm)

    return mainCollector

def saveJson(mediaCollector):
    jsonForm = mediaCollector.getJson()
    CardListJson.getInstance().write(jsonForm)

def collectCardsFromFileSystem(actualDir, parentMediaCollector = None):
    """
        Recursive analysis on the the file system for the mediaCollectors
        _________________________________________________________________
        input:
                actualDir             The actual directory where the analysis is in process
                parentMediaCollector  The actual parentMediaCollector
    """
    NoneType = type(None)
    assert issubclass(parentMediaCollector.__class__, (MediaCollector, MediaStorage, NoneType))

    recentMedia = parentMediaCollector
        
    # Collect files and and dirs in the current directory
    file_list = [f for f in os.listdir(actualDir) if os.path.isfile(os.path.join(actualDir, f))] if os.path.exists(actualDir) else []
    dir_list = [d for d in os.listdir(actualDir) if os.path.isdir(os.path.join(actualDir, d))] if os.path.exists(actualDir) else []

    card_path = None
    media_path = None
    image_path = None
    media_name = None
    
    # ####################################
    #
    # Go through all FILES in the folder
    # and collect the files which matters
    #
    # ####################################    
    for file_name in file_list:
        
        # find the Card
        if file_name == "card.ini":
            card_path = os.path.join(actualDir, file_name)
            
        # find the Image
        if getPatternImage().match( file_name ):
            image_path = os.path.join(actualDir, file_name)

#        # find the Media (video or audio or odt or pdf)
#        if getPatternAudio().match(file_name) or getPatternVideo().match(file_name) or getPatternOdt().match(file_name) or getPatternPdf().match(file_name):
#            media_path = os.path.join(actualDir, file_name)
#            media_name = file_name

    # If there is Card.ini (could be MediaCollector/MediaStorage
    if card_path:
        
        # Read the Card.ini file
        parser = configparser.RawConfigParser()
        parser.read(card_path, encoding='utf-8')
        
        # --- CONTROL --- #
        try:
            con_orderby = parser.get("control", "orderby")
            con_orderby = con_orderby if con_orderby in CardIni.getOrderByList() else ""
        except (configparser.NoSectionError, configparser.NoOptionError):
            con_orderby = ""        

        try:
            con_media = parser.get("control", "media")
            con_media = con_media if con_media in CardIni.getMediaList() else ""
        except (configparser.NoSectionError, configparser.NoOptionError):
            con_media = ""
        
        try:
            con_category = parser.get("control", "category")            
            con_category = con_category if con_category in CardIni.getCategoryListByMedia(con_media) else ""
        except (configparser.NoSectionError, configparser.NoOptionError):
            con_category = ""
                    
        control = IniControl(con_orderby, con_media, con_category) 
 
        for file_name in file_list:
             
            # find the Media (video or audio or odt or pdf)
            if CardIni.getMediaFilePatternByMedia(con_media).match(file_name):                
                media_path = os.path.join(actualDir, file_name)
                media_name = file_name
         
        # --- TITLE --- #
        try:
            titles_dict=dict(parser.items("titles"))
        except (configparser.NoSectionError, configparser.NoOptionError):
#            titles_dict={"title_orig": ""}       
            titles_dict={"orig": ""}            
        
        try:
#            title_orig=parser.get("titles", "title_orig")
            title_orig=parser.get("titles", "orig")
        except (configparser.NoSectionError, configparser.NoOptionError):
            title_orig=""        
        
        titles_lang_dict = {}
        for key, value in titles_dict.items():
#            hit = re.compile( '^title_(.{2})$' ).match(key)
            hit = re.compile( '^(.{2})$' ).match(key)
            if hit is not None:
                titles_lang_dict[hit.group(1)] = value
            
        titles = IniTitles(title_orig, titles_lang_dict)

        #--- STORYLINE --- #
        try:
            storyline_dict=dict(parser.items("storyline"))
        except (configparser.NoSectionError, configparser.NoOptionError):
            storyline_dict=None       
      
        if storyline_dict:
            storyline_lang_dict = {}
            storyline_orig=""            
            for key, value in storyline_dict.items():
#                hit_lang = re.compile( '^storyline_(.{2})$' ).match(key)                
                hit_lang = re.compile( '^(.{2})$' ).match(key)                
                if hit_lang is not None:
                    storyline_lang_dict[hit_lang.group(1)] = value
#                elif key == "storyline_orig":
                elif key == "orig":
                    storyline_orig = value
                    
            storyline = IniStorylines(storyline_orig, storyline_lang_dict)
        else:
            storyline = None
                
        #--- TOPIC --- #
        try:
            topic_dict=dict(parser.items("topic"))
        except (configparser.NoSectionError, configparser.NoOptionError):
            topic_dict=None       
        
        if topic_dict:
            topic_lang_dict = {}
            topic_orig=""            
            for key, value in topic_dict.items():
#                hit_lang = re.compile( '^topic_(.{2})$' ).match(key)
                hit_lang = re.compile( '^(.{2})$' ).match(key)                
                if hit_lang is not None:
                    topic_lang_dict[hit_lang.group(1)] = value
                elif key == "orig":
                    topic_orig = value
            
            topic = IniStorylines(topic_orig, topic_lang_dict)
        else:
            topic = None

        #--- LYRICS --- #
        try:
            lyrics_dict=dict(parser.items("lyrics"))
        except (configparser.NoSectionError, configparser.NoOptionError):
            lyrics_dict=None       
        
        if lyrics_dict:
            lyrics_lang_dict = {}
            lyrics_orig = ""            
            for key, value in lyrics_dict.items():
#                hit_lang = re.compile( '^lyrics_(.{2})$' ).match(key)                
                hit_lang = re.compile( '^(.{2})$' ).match(key)                
                if hit_lang is not None:
                    lyrics_lang_dict[hit_lang.group(1)] = value
                elif key == "orig":
                    lyrics_orig = value
            
            lyrics = IniStorylines(lyrics_orig, lyrics_lang_dict)
        else:
            lyrics = None        
       
        #--- GENERAL --- #
        try:
            general_dict=dict(parser.items("general"))
        except (configparser.NoSectionError, configparser.NoOptionError):
            if lyrics or topic or storyline:
                general_dict = {}
            else:
                general_dict=None       
        
        general = None
        if general_dict is not None:
            general = IniGeneral()    
            for key, value in general_dict.items():
                 
                # - length - #
                if key == "length" and getPatternLength().match( value ):
                    general.setLength(value)

                # - year - #
                if key == "year" and getPatternYear().match( value ):
                    general.setYear(value)

                # - director - #
                elif key == "director" and len(value) > 0:
                    directors = value.split(",")
                    director_list = []            
                    for director in directors:
                        director_list.append(director.strip())
                    general.setDirectors(director_list)
                
                # - maker - #
                elif key == "maker" and len(value) > 0:
                    makers = value.split(",")
                    maker_list = []            
                    for maker in makers:
                        maker_list.append(maker.strip())
                    general.setMakers(maker_list)

                # - writer - #
                elif key == "writer" and len(value) > 0:
                    writers = value.split(",")
                    writer_list = []            
                    for writer in writers:
                        writer_list.append(writer.strip())
                    general.setWriters(writer_list)
                
                # - author - #
                elif key == "author" and len(value) > 0:
                    authors = value.split(",")
                    author_list = []            
                    for author in authors:
                        author_list.append(author.strip())
                    general.setAuthor(author_list)

                # - actor - #
                elif key == "actor" and len(value) > 0:
                    actors = value.split(",")
                    actor_list = []            
                    for actor in actors:
                        actor_list.append(actor.strip())
                    general.setActors(actor_list)
                
                # - performer - #
                elif key == "performer" and len(value) > 0:
                    performers = value.split(",")
                    performer_list = []            
                    for performer in performers:
                        performer_list.append(performer.strip())
                    general.setPerformers(performer_list)
                
                # - lecturer - #
                elif key == "lecturer" and len(value) > 0:
                    lecturers = value.split(",")
                    lecturer_list = []            
                    for lecturer in lecturers:
                        lecturer_list.append(lecturer.strip())
                    general.setLecturers(lecturer_list)
                
                # - contributor - #
                elif key == "contributor" and len(value) > 0:
                    contributors = value.split(",")
                    contributor_list = []            
                    for contributor in contributors:
                        contributor_list.append(contributor.strip())
                    general.setContributors(contributor_list)
                
                # - voice - #
                elif key == "voice" and len(value) > 0:
                    voices = value.split(",")
                    voice_list = []            
                    for voice in voices:
                        voice_list.append(voice.strip())
                    general.setVoices(voice_list)
                
                # - genre - #
                elif key == "genre" and len(value) > 0:
                    genres = value.split(",")
                    genre_list = []            
                    for genre in genres:
                        genre_list.append(genre.strip())
                    general.setGenres(genre_list)
                
                # - theme - #
                elif key == "theme" and len(value) > 0:
                    themes = value.split(",")
                    theme_list = []            
                    for theme in themes:
                        theme_list.append(theme.strip())
                    general.setThemes(theme_list)
                
                # - subtitle - #
                elif key == "sub" and len(value) > 0:
                    subs = value.split(",")
                    sub_list = []            
                    for sub in subs:
                        sub_list.append(sub.strip())
                    general.setSubs(sub_list)

                # - sound - #
                elif key == "sound" and len(value) > 0:
                    sounds = value.split(",")
                    sound_list = []            
                    for sound in sounds:
                        sound_list.append(sound.strip())
                    general.setSounds(sound_list)

                # - country - #
                elif key == "country" and len(value) > 0:
                    countrys = value.split(",")
                    country_list = []            
                    for country in countrys:
                        country_list.append(country.strip())
                    general.setCountries(country_list)
                    
                # - series - #
                elif key == "series" and getPatternNumber().match( value ):
                    general.setSeries(value)
                
                # - episode - #
                elif key == "episode" and getPatternNumber().match( value ):
                    general.setEpisode(value)
            
            if storyline:
                general.setStoryline(storyline);
            elif topic:
                general.setTopic(topic)
            if lyrics:
                general.setLyrics(lyrics)
        
        #--- RATING --- #
        try:
            rating_dict=dict(parser.items("rating"))
        except (configparser.NoSectionError, configparser.NoOptionError):
            rating_dict=None       
        
        rating = None
        if rating_dict:
            rat_rate = 0
            rat_favorite = False
            rat_new = False
       
            for key, value in rating_dict.items():
                if key == "rate" and getPatternRate().match(value):
                    rat_rate = int(value)
                elif key == "favorite" and (value == 'y' or value == 'n'):
                    rat_favorite = True if value == 'y' else False
                elif key == "new" and (value == 'y' or value == 'n'):
                    rat_new = True if value == 'y' else False
                   
            rating = IniRating(rat_rate, rat_favorite, rat_new) 

        # --- MEDIA --- #
        try:
            media_path = parser.get("media", "link")
        except (configparser.NoSectionError, configparser.NoOptionError):
            pass


        # -------------------- MediaCollector/MediaStorage/MediaAppendix construction ------------
        #                                                    V
        #  ┌────────────────┐                         ┌────────────────┐
        #  │     NONE       │                         │     FOLDER     │
        #  └───────┬────────┘                         └───────┬────────┘  
        #          │           ┌────────────────┐             │           ┌────────────────┐
        #          ├───────────┤ MediaCollector |             ├───────────┤ MediaCollector |
        #          │           └────────────────┘             │           └────────────────┘
        #          │                                          │
        #          │           ┌────────────────┐             │           ┌────────────────┐
        #          └───────────┤    FOLDER      |             ├───────────┤ MediaAppendix  | 
        #                      └────────────────┘             |           └────────────────┘
        #                                                     │
        #                                                     │           ┌────────────────┐ 
        #                                                     └───────────┤    FOLDER      |   
        #                                                                 └────────────────┘
        #         
        #  ┌────────────────┐                         ┌────────────────┐
        #  │ MediaCollector │                         │  MediaStorage  │
        #  └───────┬────────┘                         └───────┬────────┘  
        #          │           ┌────────────────┐             │           ┌────────────────┐
        #          ├───────────┤ MediaCollector |             ├───────────┤ MediaAppendix  |
        #          │           └────────────────┘             │           └────────────────┘
        #          │                                          │
        #          │           ┌────────────────┐             │           ┌────────────────┐
        #          ├───────────┤  MediaStorage  |             └───────────┤     FOLDER     | 
        #          │           └────────────────┘                         └────────────────┘
        #          │
        #          │           ┌────────────────┐ 
        #          └───────────┤    FOLDER      |   
        #                      └────────────────┘ 
        #        
        
        # If MediaCollector - under MediaCollector or Root
        #      
        if card_path and not media_path and dir_list and issubclass(parentMediaCollector.__class__, (MediaCollector, NoneType)):
            pathCollector = PathsCollector(os.path.dirname(card_path), card_path, image_path)            
            recentMedia = MediaCollector(pathCollector, titles, control, general, rating)
            
            # If it has parent -> add it to parent, otherwise it will be the parent
            if parentMediaCollector:
                parentMediaCollector.addMediaCollector(recentMedia)
            else:
                parentMediaCollector = recentMedia

        #
        # If MediaStorage - Under MediaCollector
        #
        elif card_path and media_path and issubclass(parentMediaCollector.__class__, MediaCollector):
            pathStorage = PathsStorage(os.path.dirname(card_path), card_path, image_path, media_path)            
            recentMedia = MediaStorage(pathStorage, titles, control, general, rating)
            parentMediaCollector.addMediaStorage(recentMedia)

        #
        # If MediaAppendix - MediaStorage
        #
        elif card_path and media_path and issubclass(parentMediaCollector.__class__, MediaStorage) and con_category == 'appendix':
            pathAppendix = PathsAppendix(os.path.dirname(card_path), card_path, image_path, media_path)
            recentMedia = MediaAppendix(pathAppendix, titles)
            parentMediaCollector.addMediaAppendix(recentMedia)

    # ################################## #
    #                                    #
    # Go through all SUB-FOLDERS in the  #
    # folder and collect the files which #
    # matters                            #
    #                                    #
    # ################################## #    
    for name in dir_list:
        subfolder_path_os = os.path.join(actualDir, name)
        collectCardsFromFileSystem( subfolder_path_os, recentMedia )        

    # If no media found at all #
    if parentMediaCollector is None:
        parentMediaCollector = MediaCollector(PathsCollector("", "", ""), IniTitles("", {'orig':''}), IniControl("", "", ""), None, None)

    # and finaly returns
    return parentMediaCollector
  
  
def collectCardsFromJson(jsonForm, parentMediaCollector = None):
    """
        Recursively go through the jsonForm and fill up the MediaCollector
        _________________________________________________________________
        input:
                jsonForm            media cards collected in json form to
                                    make MediaCollector
        output:
                MediaCollector
    """
    NoneType = type(None)
    assert issubclass(parentMediaCollector.__class__, (MediaCollector, MediaStorage, NoneType))

    nextParent = parentMediaCollector
    
    # --- TITLE --- #
    titles = jsonForm.get('titles')
    ini_titles = None
    if titles:        
        titles_dict = {}
        titles_orig = None
        for key, value in titles.items():
            hit = re.compile( '^(.{2})$' ).match(key)
            if hit is not None:
                titles_dict[key] = value
            elif key == 'orig':
                titles_orig = value
        ini_titles = IniTitles(titles_orig, titles_dict)
        
    #--- STORYLINE --- #
    storyline = jsonForm.get('storyline')
    ini_storyline = None
    if storyline:
        storyline_dict = {}
        storyline_orig = None
        for key, value in storyline.items():
            hit = re.compile( '^(.{2})$' ).match(key)                
            if hit is not None:
                storyline_dict[key] = value
            elif key == 'orig':
                storyline_orig = value
        ini_storyline = IniStorylines(storyline_orig, storyline_dict)                
                
    #--- TOPIC --- #
    topic = jsonForm.get('topic')
    ini_topic = None
    if topic:
        topic_dict = {}
        topic_orig = None
        for key, value in topic.items():
            hit = re.compile( '^(.{2})$' ).match(key)                
            if hit is not None:
                topic_dict[key] = value
            elif key == 'orig':
                topic_orig = value
        ini_topic = IniStorylines(topic_orig, topic_dict)                
            
    #--- LYRICS --- #
    lyrics = jsonForm.get('lyrics')
    ini_lyrics = None
    if lyrics:
        lyrics_dict = {}
        lyrics_orig = None
        for key, value in lyrics.items():
            hit = re.compile( '^(.{2})$' ).match(key)                
            if hit is not None:
                lyrics_dict[key] = value
            elif key == 'orig':
                lyrics_orig = value
        ini_topic = IniStorylines(topic_orig, lyrics_dict)

    ini_general = IniGeneral()            
    if ini_lyrics or ini_storylines or ini_topic:
        if ini_storyline:
            ini_general.setStoryline(ini_storyline);
        if ini_topic:
            ini_general.setTopic(ini_topic)
        if ini_lyrics:
            ini_general.setLyrics(ini_lyrics)
#    else:
#        ini_general = None
        
    #--- GENERAL --- #
    general = jsonForm.get('general')
    if general:
        year = general.get('year')
        length = general.get('length')
        director = general.get('director')
        maker = general.get('maker')
        author = general.get('author')
        actor = general.get('actor')
        performer = general.get('performer')
        lecturer = general.get('lecturer')
        contributor = general.get('contributor')
        voice = general.get('voice')
        genre = general.get('genre')
        theme = general.get('theme')
        sub = general.get('sub')
        sound = general.get('sound')
        country = general.get('country')
        series = general.get('series')
        episode = general.get('episode')

#        if year or length or director or maker or author or actor or performer or lecturer or contributor or voice or genre or theme or sub or sound or country or series or episode:
#            ini_general = IniGeneral()
            
        if year:
            ini_general.setYear(year)
        if length:
            ini_general.setLength(length)
        if director:
            ini_general.setDirectors(director)
        if maker:
            ini_general.setMakers(maker)
        if author:
            ini_general.setAuthors(author)
        if actor:
            ini_general.setActors(actor)
        if performer:
            ini_general.setPerformers(performer)
        if lecturer:
            ini_general.setLecturers(lecturer)
        if contributor:
            ini_general.setContributors(contributor)
        if voice:
            ini_general.setVoices(voice)
        if genre:
            ini_general.setGenres(genre)
        if theme:
            ini_general.setThemes(theme)
        if sub:
            ini_general.setSubs(sub)
        if sound:
            ini_general.setSounds(sound)
        if country:
            ini_general.setCountries(country)
        if series:
            ini_general.setSeries(series)
        if episode:
            ini_general.setEpisode(episode)

    #--- RATING --- #
    rating = jsonForm.get('rating')
    ini_rating = None
    if rating:

        rat_rate = rating.get('rate')
        rat_favorite = rating.get('favorite')
        rat_new = rating.get('new')        
        
        rat_rate = rat_rate if getPatternRate().match(str(rat_rate)) else 0            
        rat_favorite = True if rat_favorite == 'y' else False        
        rat_new = True if rat_new == 'y' else False      
                   
        ini_rating = IniRating(rat_rate, rat_favorite, rat_new) 

    # --- CONTROL --- #
    control = jsonForm.get('control')
    #ini_control = None
    con_orderby = ""
    con_media = ""
    con_category = ""
    if control:
        con_orderby = control.get('orderby')
        con_media = control.get('media')
        con_category = control.get('category')
    ini_control = IniControl(con_orderby, con_media, con_category) 
 
    # --- MEDIA --- #
    
        
    # --- MEDIA-COLLECTOR --- #        
    path_collector = jsonForm.get('paths-collector')
    
    # --- MEDIA-STORAGE --- #        
    path_storage = jsonForm.get('paths-storage')
    
    # --- MEDIA-APPENDIX --- #
    path_appendix = jsonForm.get('paths-appendix')
    
    #
    # If MediaCollector - under MediaCollector or Root
    #
    if path_collector:
        name_of_folder = path_collector.get('name-of-folder')
        path_of_card = path_collector.get('path-of-card')
        path_of_image = path_collector.get('path-of-image')
        
        ini_path_collector = PathsCollector(name_of_folder, path_of_card, path_of_image)
        nextParent = MediaCollector(ini_path_collector, ini_titles, ini_control, ini_general, ini_rating)
    
        if parentMediaCollector:
            parentMediaCollector.addMediaCollector(nextParent)
        else:
            parentMediaCollector = nextParent
            
    #
    # If MediaStorage - Under MediaCollector
    #
    elif path_storage:
        name_of_folder = path_storage.get('name-of-folder')
        path_of_card = path_storage.get('path-of-card')
        path_of_image = path_storage.get('path-of-image')
        path_of_media = path_storage.get('path-of-media')
    
        ini_path_storage = PathsStorage(name_of_folder, path_of_card, path_of_image, path_of_media)
        nextParent = MediaStorage(ini_path_storage, ini_titles, ini_control, ini_general, ini_rating)
        parentMediaCollector.addMediaStorage(nextParent)
        
    #
    # If MediaAppendix - MediaStorage
    #
    elif path_appendix:
        name_of_folder = path_appendix.get('name-of-folder')
        path_of_card = path_appendix.get('path-of-card')
        path_of_image = path_appendix.get('path-of-image')
        path_of_media = path_appendix.get('path-of-media')
        
        ini_path_appendix = PathsAppendix(name_of_folder, path_of_card, path_of_image, path_of_media)
        nextParent = MediaAppendix(ini_path_appendix, ini_titles)
        parentMediaCollector.addMediaAppendix(nextParent)

    # ################################## #
    #                                    #
    # Go through all SUB-FOLDERS in the  #
    # folder and collect the files which #
    # matters                            #
    #                                    #
    # ################################## #    
    
    # --- COLLECTORS --- #        
    collectors_list = jsonForm.get('collectors')    
    for childJson in collectors_list if collectors_list else {}:
        collectCardsFromJson( childJson, nextParent )        
 
    # --- STORAGES --- #        
    storages_list = jsonForm.get('storages')
    for childJson in storages_list if storages_list else {}:
        collectCardsFromJson( childJson, nextParent )
        
    # --- APPENDIXES --- #        
    appendixes_list = jsonForm.get('appendixes')
    for childJson in appendixes_list if appendixes_list else []:
        collectCardsFromJson( childJson, nextParent )    

    return parentMediaCollector






# =====================
#
# Handle card.list.json
#
# =====================
class CardListJson():
    FILE_NAME = 'card.list.json'

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
        self.file = os.path.join(PATH_FOLDER_CONFIG, CardListJson.FILE_NAME)
        
    def write(self, jsonContent):
        with open(self.file, 'w') as outfile:
            json.dump(jsonContent, outfile)

    def read(self):
#        path=config_ini['media_path']
                
        content = self.inner_read()
        return content
#        if content['path'] == path:
#            return content['cards']
#        else:
#            return None
        
    def inner_read(self):
        try:
            with open(self.file) as infile:
                data = json.load(infile)
        except:
            data = {}
        return data
      

