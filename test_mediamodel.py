from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout

import sys

from medlib.mediamodel.ini_titles import IniTitles
from medlib.mediamodel.ini_storylines import IniStorylines
from medlib.mediamodel.ini_control import IniControl
from medlib.mediamodel.ini_rating import IniRating
from medlib.mediamodel.ini_general import IniGeneral

from medlib.mediamodel.media_collector import MediaCollector
from medlib.mediamodel.media_storage import MediaStorage

from medlib.mediamodel.paths_collector import PathsCollector
from medlib.mediamodel.paths_storage import PathsStorage

class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'Card test'
        self.left = 10
        self.top = 10
        self.width = 820
        self.height = 250
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height) 
        self.setStyleSheet('background: white')
                
        self.setLayout(layout)
        
        
        #global dic
        path_collector_A = PathsCollector('A_folder_name', "/path/to/ini", "/path/to/jpeg")
        titles_A = IniTitles("Eredeti cim", {"hu":"Magyar cim", "en":"English title", "se":" "})
        control_A =IniControl("title", "video", "movie")
        storylines_A = IniStorylines("A tortenet ...", {"en":"the story is ..", "hu":"a történet ..."})    
        collector_A = MediaCollector(path_collector_A, titles_A, control_A, None, storylines_A)

        path_collector_B = PathsCollector('C_folder_name', "/path/to/ini", "/path/to/jpeg")
        titles_B = IniTitles("B Eredeti cim", {"hu":"oMagyar cim", "en":"D English title", "se":"B"})
        control_B =IniControl("title", "video", "movie")
        storylines_B = IniStorylines("A tortenet ...", {"en":"the story is ..", "hu":"a történet \n tobb soros\n leiras a filmrol\n hogy lehessen tesztelnei milyen hosszu uzeneteket\n tud kezelni"})    
        collector_B = MediaCollector(path_collector_B, titles_B, control_B, None, storylines_B)

        path_collector_C = PathsCollector('D_folder_name', "/path/to/ini", "/path/to/jpeg")
        titles_C =  IniTitles("C Eredeti cim", {"hu":"ö Magyar cim", "en":"A English title", "se":"C"})
        control_C =IniControl("title", "video", "movie")
        storylines_C = IniStorylines("A tortenet ...", {"en":"the story is ..", "hu":"a történet ..."})    
        collector_C = MediaCollector(path_collector_C, titles_C, control_C, None, storylines_C)

        path_collector_D = PathsCollector('A_folder_name', "/path/to/ini", "/path/to/jpeg")
        titles_D =  IniTitles("D Eredeti cim", {"hu":"á Magyar cim", "en":"B English title", "se":"D"})
        control_D =IniControl("title", "video", "movie")
        storylines_D = IniStorylines("A tortenet ...", {"en":"the story is ..", "hu":"a történet ..."})
        collector_D = MediaCollector(path_collector_D, titles_D, control_D, None, storylines_D)


        path_collector_BA = PathsCollector('A_folder_name', "/path/to/ini", "/path/to/jpeg")
        titles_BA =  IniTitles("A Konténer", {"hu":"A Konténer", "en":"A Container", "se":"D"})
        control_BA =IniControl("title", "video", "movie")
        storylines_BA = IniStorylines("A gyujtő ...", {"en":"the container is ..", "hu":"A Gyüjtő ..."})
        collector_BA = MediaCollector(path_collector_BA, titles_BA, control_BA, None, storylines_BA)
        collector_B.addMediaCollector(collector_BA)

        path_collector_BB = PathsCollector('A_folder_name', "/path/to/ini", "/path/to/jpeg")
        titles_BB =  IniTitles("K Konténer", {"hu":"K Konténer", "en":"K Container", "se":"D"})
        control_BB = IniControl("title", "video", "movie")
        storylines_BB = IniStorylines("A gyujtő ...", {"en":"the container is ..", "hu":"A Gyüjtő ..."})
        collector_BB = MediaCollector(path_collector_BB, titles_BB, control_BB, None, storylines_BB)
        collector_B.addMediaCollector(collector_BB)

# ---

        path_storage_BC = PathsStorage('C_folder_name', "/path/to/ini", "/media/akoel/Movies/Final/01.Video/01.Movie/01.Films/01.Uncategorized/A.Profi-1981/image.jpeg", "/path/to/media")
        titles_BC = IniTitles("B Mozi cime", {"hu":"B Mozi cim", "en":"D Movie title", "hu":"Magyar cim"})
        control_BC = IniControl("title", "video", "movie")
        storylines_BC = IniStorylines("Ez a \ndefault tortenet", {"en": "English story\nSecond line\nThird line\nFourth line", "hu": "Magyar tortenet" })
        general_BC = IniGeneral()
        general_BC.setYear( "2012-2013")
        general_BC.setDirectors(["Director 1", "Director 2", "Director 3", "Director 4", "Director 5", "Director 6", "Director 7", "Director 8"])
        #general_BC.setMakers(["Maker 1", "Maker 2", "Maker 3"])
        general_BC.setWriters(["Writ 1", "Writ 2"])
        #general_BC.setAuthors(["Author 1", "Author 2"]) 
        general_BC.setActors(["Actor 1", "Actor 2", "Actor 3", "Actor 4", "Actor 5", "Actor 6", "Actor 7", "Actor 8", "Actor 9", "Actor 10", "Actor 11", "Actor 12", "Actor 13", "Actor 14"])
        #general_BC.setPerformers(["Performer 1", "Performer 2"])
        #general_BC.setLecturers(["Lecturer 1", "Lecturer 2"])
        #general_BC.setContributors(["Contributor 1", "Contributor 2"])
        #general_BC.setVoices(["Voice 1", "Voice 2"])
        general_BC.setLength( "2:12" )
        general_BC.setSounds(["en", "hu", "sv"])
        general_BC.setSubs(["en", "hu", "de", "it", "pl"])
        general_BC.setGenres(["action", "crime"])
        general_BC.setThemes(["money", "greed"])
        general_BC.setStoryline(storylines_BC)
        rating_BC = IniRating(10, True, True) 
        storage_BC = MediaStorage(path_storage_BC, titles_BC, control_BC, general_BC, rating_BC)
        collector_B.addMediaStorage(storage_BC)

# ---

        path_storage_BD = PathsStorage('C_folder_name', "/path/to/ini", "/media/akoel/Movies/Final/01.Video/01.Movie/01.Films/01.Uncategorized/A.Profi-1981/image.jpeg", "/path/to/media")
        titles_BD = IniTitles("C Default Mozi cime", {"en":"A Movie title", "se":"B"})
        control_BD = IniControl("title", "video", "movie")
        storylines_BD = IniStorylines("Ez a \ndefault: \nA Mozi \ntorte\nnet ...\n Ez egy tobb soros\nUzenet\n Mert po\nnt ezt a\nkarom \n tesztelni", {"en":"the movie's story is .." })
       
        general_BD = IniGeneral()
        general_BD.setYear( "2012-2013")
        general_BD.setDirectors(["Dir 1", "Dir 2"])
        #general_BD.setMakers(["Maker 1", "Maker 2", "Maker 3"])
        general_BD.setWriters(["Writ 1", "Writ 2"])
        #general_BD.setAuthors(["Author 1", "Author 2"])
        general_BD.setActors(["Actor 1", "Actor 2", "Actor 3", "Actor 4", "Actor 5", "Actor 6", "Actor 7", "Actor 8", "Actor 9", "Actor 10", "Actor 11", "Actor 12", "Actor 13", "Actor 14"])
        #general_BD.setPerformers(["Performer 1", "Performer 2"])
        #general_BD.setLecturers(["Lecturer 1", "Lecturer 2"])
        #general_BD.setContributors(["Contributor 1", "Contributor 2"])
        #general_BD.setVoices(["Voice 1", "Voice 2"])
        #general_BD.setLength( "2:12" )
        #general_BD.setSounds(["en", "hu", "sv"])
        general_BD.setSubs(["en", "hu", "de", "it", "pl"])
        general_BD.setGenres(["action", "crime"])
        general_BD.setThemes(["money", "greed"])
        general_BD.setStoryline(storylines_BD)
        rating_BD = IniRating(10, True, True) 
        storage_BD = MediaStorage(path_storage_BD, titles_BD, control_BD, general_BD, rating_BD)
        collector_B.addMediaStorage(storage_BD)

# ---

        collector_A.addMediaCollector(collector_D)
        collector_A.addMediaCollector(collector_B)
        collector_A.addMediaCollector(collector_C)
        
        widget = storage_BC.getWidget(1)
        layout.addWidget(widget)
        self.show()
        
        
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
#    print(collector_A.getHierarchyTitle(""))

    #print(BB_content.getHtml())
#    print(storage_BC.getHtml())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    #ex.start_card_holder()
    sys.exit(app.exec_())
