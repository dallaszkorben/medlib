import os
import re
from medlib.handle_property import Property
from medlib.card_ini import SECTION_TITLES, SECTION_STORYLINE, SECTION_GENERAL,\
    SECTION_CLASSIFICATION, SECTION_LYRICS, SECTION_CONTROL

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
        category = card_ini.get(SECTION_CONTROL, "category", "", False)

        # --- TITLE --- #
        print(".", end="")
        
        if category == "music":
        
            #--- STORYLINE --- #
            print(".", end="")        
            # read 'rating' Section with all Options
            storyline_dict = card_ini.getOptions(SECTION_STORYLINE)
        
            # write the options into the new Section
            if storyline_dict:
                for key, value in storyline_dict.items():
                    card_ini.update(SECTION_LYRICS, key, value)

                # delete old Section
                card_ini.removeSection(SECTION_STORYLINE)

            # --- MEDIA --- #
            print(".")
                                
            #--- TOPIC --- #
            print(".", end="")

            #--- LYRICS --- #
            print(".", end="")

            #--- GENERAL --- #
            print(".", end="")
            actor = card_ini.get(SECTION_GENERAL, "actor", "", False)
            card_ini.update(SECTION_GENERAL, "performer", actor)
            card_ini.removeOption(SECTION_GENERAL, "actor")
        
            #--- CLSSIFICATION --- #
            print(".", end="")
            # read 'rating' Section with all Options
            rating_dict = card_ini.getOptions(SECTION_CLASSIFICATION)

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

#    paths = "/media/akoel/Movies/Final/01.Video/02.Music"
#    fixCards(paths)

    print("END")


main()
