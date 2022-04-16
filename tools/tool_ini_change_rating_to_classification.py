import os
import re
from medlib.handle_property import Property
from medlib.card_ini import SECTION_TITLES, SECTION_STORYLINE, SECTION_GENERAL,\
    SECTION_CLASSIFICATION

HIGHLIGHT = '\033[31m'
COLORBACK = '\033[0;0m'
CARD_INI_FILE_NAME = 'card.ini'

def fixCards(actualDir):
    """
        Recursive analysis on the the file system for the mediaCollectors
        _________________________________________________________________
        input:
                actualDir             The actual directory where the analysis is in process
                parentMediaCollector  The actual parentMediaCollector
    """

    # Collect files and and dirs in the current directory
    file_list = [f for f in os.listdir(actualDir) if os.path.isfile(os.path.join(actualDir, f))] if os.path.exists(actualDir) else []
    dir_list = [d for d in os.listdir(actualDir) if os.path.isdir(os.path.join(actualDir, d))] if os.path.exists(actualDir) else []
    
    # ####################################
    #
    # Go through all FILES in the folder
    # and collect the files which matters
    #
    # ####################################    
    card_path = None
    for file_name in file_list:
        
        # find the Card
        if file_name == CARD_INI_FILE_NAME:
            card_path = os.path.join(actualDir, file_name)
            

    # If there is Card.ini (could be MediaCollector/MediaStorage
    if card_path:
        
        print(card_path + ": ", end="")
        
        # Read the Card.ini file
        card_ini = Property(card_path, True)
        
        # --- CONTROL --- #
        print(".", end="")

        # --- TITLE --- #
        print(".", end="")
        title_orig = card_ini.get(SECTION_TITLES, "title_orig", "", False)
        card_ini.update(SECTION_TITLES, "orig", title_orig)
        card_ini.removeOption(SECTION_TITLES, "title_orig")
        
        titles_dict = card_ini.getOptions(SECTION_TITLES)
        if titles_dict:
            for key, value in titles_dict.items():
                hit = re.compile( '^title_(.{2})$' ).match(key)
                if hit is not None:
                    card_ini.update(SECTION_TITLES, hit.group(1), value)
                    card_ini.removeOption(SECTION_TITLES, "title_" + hit.group(1))
            
        #--- STORYLINE --- #
        print(".", end="")
        storyline_orig = card_ini.get(SECTION_STORYLINE, "storyline_orig", "", False)
        card_ini.update(SECTION_STORYLINE, "orig", storyline_orig)
        card_ini.removeOption(SECTION_STORYLINE, "storyline_orig")
        
        storyline_dict = card_ini.getOptions(SECTION_STORYLINE)
        if storyline_dict:
            for key, value in storyline_dict.items():
                hit_lang = re.compile( '^storyline_(.{2})$' ).match(key)                
                if hit_lang is not None:
                    card_ini.update(SECTION_STORYLINE, hit_lang.group(1), value)
                    card_ini.removeOption(SECTION_STORYLINE, "storyline_" + hit_lang.group(1))
                    
        #--- TOPIC --- #
        print(".", end="")

        #--- LYRICS --- #
        print(".", end="")

        #--- GENERAL --- #
        print(".", end="")

        general_dict = card_ini.getOptions(SECTION_GENERAL)
        
        #--- RATE --- #
        print(".", end="")
        # read 'rating' Section with all Options
        rating_dict = card_ini.getOptions("rating")
        
        # write the options into the new Section
        if rating_dict:
            for key, value in rating_dict.items():
                hit = re.compile( '^(favorite|new|rate)$' ).match(key)
                if hit is not None:
                    card_ini.update(SECTION_CLASSIFICATION, hit.group(1), value)

            # delete old Section
            card_ini.removeSection("rating")

        # --- MEDIA --- #
        print(".")

    # ################################## #
    #                                    #
    # Go through all SUB-FOLDERS in the  #
    # folder and collect the files which #
    # matters                            #
    #                                    #
    # ################################## #    
    for name in dir_list:
        subfolder_path_os = os.path.join(actualDir, name)
        fixCards( subfolder_path_os )        
 
    return
  
  
  


def main():
#    paths = "/home/akoel/tmp/media"
#    fixCards(paths)

#    paths = "/media/akoel/Movies/Final"
#    fixCards(paths)

    print("END")


main()
