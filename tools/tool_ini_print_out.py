import os
import re
from medlib.handle_property import Property
from medlib.card_ini import SECTION_TITLES, SECTION_STORYLINE, SECTION_GENERAL,\
    SECTION_CLASSIFICATION, SECTION_LYRICS, SECTION_CONTROL

HIGHLIGHT = '\033[31m'
COLORBACK = '\033[0;0m'
CARD_INI_FILE_NAME = 'card.ini'

def collectCards(actualDir, order):
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

        # Read the Card.ini file
        card_ini = Property(card_path, True)

        # --- CONTROL --- #
        category = card_ini.get(SECTION_CONTROL, "category", "", False)

        # --- TITLE --- #
        title_hu = card_ini.get(SECTION_TITLES, "hu", "", False)
        title_orig = card_ini.get(SECTION_TITLES, "orig", "", False)

        # --- YEAR --- #
        year = card_ini.get(SECTION_GENERAL, "year", "", False)

        if category == "movie":

            print("{0:4d}. {1} |{2}|".format(order, title_orig, year), end="")
            order = order + 1

            if title_orig != title_hu and title_hu:
                print("  [{0}]".format(title_hu), end="")

            print()

            #--- STORYLINE --- #
            # read 'rating' Section with all Options
            storyline_dict = card_ini.getOptions(SECTION_STORYLINE)

            # write the options into the new Section
            #if storyline_dict:
            #    for key, value in storyline_dict.items():
            #        card_ini.update(SECTION_LYRICS, key, value)
            #
            #    # delete old Section
            #    card_ini.removeSection(SECTION_STORYLINE)

            # --- MEDIA --- #

            #--- TOPIC --- #

            #--- LYRICS --- #

            #--- GENERAL --- #
            # actor = card_ini.get(SECTION_GENERAL, "actor", "", False)
            # card_ini.update(SECTION_GENERAL, "performer", actor)
            # card_ini.removeOption(SECTION_GENERAL, "actor")
        
            #--- CLSSIFICATION --- #
            # read 'rating' Section with all Options
            #rating_dict = card_ini.getOptions(SECTION_CLASSIFICATION)

    # ################################## #
    #                                    #
    # Go through all SUB-FOLDERS in the  #
    # folder and collect the files which #
    # matters                            #
    #                                    #
    # ################################## #    
    for name in dir_list:
        subfolder_path_os = os.path.join(actualDir, name)
        order = collectCards( subfolder_path_os, order )

    return order

def main(paths):

    #paths = "/media/akoel/Movies/Final/01.Movie/01.Films
    order = 1

    for path in paths:
        order = collectCards(path, order)


