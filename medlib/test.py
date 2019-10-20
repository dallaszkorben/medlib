from medlib.mediamodel.ini_titles import IniTitles
from medlib.mediamodel.ini_storylines import IniStorylines
from medlib.mediamodel.ini_control import IniControl
from medlib.mediamodel.ini_rating import IniRating
from medlib.mediamodel.ini_general import IniGeneral

from medlib.mediamodel.media_collector import MediaCollector
from medlib.mediamodel.media_storage import MediaStorage

from medlib.mediamodel.paths_collector import PathsCollector
from medlib.mediamodel.paths_storage import PathsStorage

def main():

    global dic
    path_collector_A = PathsCollector('A_folder_name', "/path/to/ini", "/path/to/jpeg")
    titles_A = IniTitles("Eredeti cim", {"hu":"Magyar cim", "en":"English title", "se":" "})
    control_A =IniControl("title", "movie")
    storylines_A = IniStorylines("A tortenet ...", {"en":"the story is ..", "hu":"a történet ..."})    
    collector_A = MediaCollector(path_collector_A, titles_A, control_A, None, storylines_A)

    path_collector_B = PathsCollector('C_folder_name', "/path/to/ini", "/path/to/jpeg")
    titles_B = IniTitles("B Eredeti cim", {"hu":"oMagyar cim", "en":"D English title", "se":"B"})
    control_B =IniControl("title", "movie")
    storylines_B = IniStorylines("A tortenet ...", {"en":"the story is ..", "hu":"a történet \n tobb soros\n leiras a filmrol\n hogy lehessen tesztelnei milyen hosszu uzeneteket\n tud kezelni"})    
    collector_B = MediaCollector(path_collector_B, titles_B, control_B, None, storylines_B)

    path_collector_C = PathsCollector('D_folder_name', "/path/to/ini", "/path/to/jpeg")
    titles_C =  IniTitles("C Eredeti cim", {"hu":"ö Magyar cim", "en":"A English title", "se":"C"})
    control_C =IniControl("title", "movie")
    storylines_C = IniStorylines("A tortenet ...", {"en":"the story is ..", "hu":"a történet ..."})    
    collector_C = MediaCollector(path_collector_C, titles_C, control_C, None, storylines_C)

    path_collector_D = PathsCollector('A_folder_name', "/path/to/ini", "/path/to/jpeg")
    titles_D =  IniTitles("D Eredeti cim", {"hu":"á Magyar cim", "en":"B English title", "se":"D"})
    control_D =IniControl("title", "movie")
    storylines_D = IniStorylines("A tortenet ...", {"en":"the story is ..", "hu":"a történet ..."})
    collector_D = MediaCollector(path_collector_D, titles_D, control_D, None, storylines_D)

# ---

    path_collector_BA = PathsCollector('A_folder_name', "/path/to/ini", "/path/to/jpeg")
    titles_BA =  IniTitles("A Konténer", {"hu":"A Konténer", "en":"A Container", "se":"D"})
    control_BA =IniControl("title", "movie")
    storylines_BA = IniStorylines("A gyujtő ...", {"en":"the container is ..", "hu":"A Gyüjtő ..."})
    collector_BA = MediaCollector(path_collector_BA, titles_BA, control_BA, None, storylines_BA)
    collector_B.addMediaCollector(collector_BA)

    path_collector_BB = PathsCollector('A_folder_name', "/path/to/ini", "/path/to/jpeg")
    titles_BB =  IniTitles("K Konténer", {"hu":"K Konténer", "en":"K Container", "se":"D"})
    control_BB =IniControl("title", "movie")
    storylines_BB =IniStorylines("A gyujtő ...", {"en":"the container is ..", "hu":"A Gyüjtő ..."})
    collector_BB = MediaCollector(path_collector_BB, titles_BB, control_BB, None, storylines_BB)
    collector_B.addMediaCollector(collector_BB)

    path_storage_BC = PathsStorage('C_folder_name', "/path/to/ini", "/media/akoel/Movies/Final/01.Video/01.Movie/01.Films/01.Uncategorized/A.Profi-1981/image.jpeg", "/path/to/media")
    titles_BC = IniTitles("B Mozi cime", {"hu":"B Mozi cim", "en":"D Movie title", "se":"B"})
    control_BC =IniControl("title", "movie")
    storylines_BC =IniStorylines("A Mozi tortenet ...", {"en":"the movie's story is ..", "hu":"a Mozi történet ..."})
    general_BC = IniGeneral("2012-2013", ["Dir 1", "Dir 2"], ["Writ 1", "Writ 2"], ["Act 1", "Act 2"], "2:12", ["en", "hu"], ["en", "hu"], ["action", "crime"], ["money", "greed"], ["us", "ca"])
    rating_BC = IniRating(10, True, True) 
    storage_BC = MediaStorage(path_storage_BC, titles_BC, control_BC, general_BC, storylines_BC, rating_BC)
    collector_B.addMediaStorage(storage_BC)

    path_storage_BD = PathsStorage('C_folder_name', "/path/to/ini", "/media/akoel/Movies/Final/01.Video/01.Movie/01.Films/01.Uncategorized/A.Profi-1981/image.jpeg", "/path/to/media")
    titles_BD = IniTitles("C Default Mozi cime", {"en":"A Movie title", "se":"B"})
    control_BD =IniControl("title", "movie")
    storylines_BD =IniStorylines("Ez a default: \nA Mozi tortenet ...\n Ez egy tobb soros\nUzenet\n Mert pont ezt akarom \n tesztelni", {"en":"the movie's story is .." })
    general_BD = IniGeneral("2012-2013", ["Dir 1", "Dir 2"], ["Writ 1", "Writ 2"], ["Act 1", "Act 2", "Act 3", "Act 4", "Act 5", "Act 6", "Act 7", "Act 8", "Act 9", "Act 10", "Act 11", "Act 12", "Act 13", "Act 14"], "2:12", ["en", "hu"], ["en", "hu"], ["action", "crime"], ["money", "greed"], ["us", "ca"])
    rating_BD = IniRating(10, True, True) 
    storage_BD = MediaStorage(path_storage_BD, titles_BD, control_BD, general_BD, storylines_BD, rating_BD)
    collector_B.addMediaStorage(storage_BD)

# ---

    collector_A.addMediaCollector(collector_D)
    collector_A.addMediaCollector(collector_B)
    collector_A.addMediaCollector(collector_C)
#    collector_A.setLanguage("hu")

#Collector_A
#├── Collector_D
#├── Collector_C
#└── Collector_B
#            ├── Collector_BA
#            ├── Collector_BB
#            ├── Storage_BC
#            └── Storage_BD

#for mc in collector_A.getMediaContainerList():
#    print(mc.getTitle())
    print(collector_A.getHierarchyTitle(""))

    #print(BB_content.getHtml())
    print(storage_BC.getHtml())

