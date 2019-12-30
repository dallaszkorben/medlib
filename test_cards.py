import sys
import os

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication

from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QUrl

from PyQt5.QtWebEngineWidgets import QWebEngineView

from pkg_resources import resource_string, resource_filename

from cardholder.cardholder import CardHolder
from cardholder.cardholder import Card

from medlib.mediamodel.ini_titles import IniTitles
from medlib.mediamodel.ini_storylines import IniStorylines
from medlib.mediamodel.ini_control import IniControl
from medlib.mediamodel.ini_rating import IniClassification
from medlib.mediamodel.ini_general import IniGeneral

from medlib.mediamodel.media_collector import MediaCollector
from medlib.mediamodel.media_storage import MediaStorage

from medlib.mediamodel.paths_collector import PathsCollector
from medlib.mediamodel.paths_storage import PathsStorage
from PyQt5.QtWebEngine import QtWebEngine
from PyQt5 import QtWebEngineWidgets


class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'Card selector'
        self.left = 10
        self.top = 10
        self.width = 420
        self.height = 300
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height) 
        self.setStyleSheet('background: white')
 
        self.scroll_layout = QVBoxLayout(self)
        self.scroll_layout.setContentsMargins(15, 15, 15, 15)
        self.scroll_layout.setSpacing(0)
        self.setLayout(self.scroll_layout)
        
        self.buildUpMediaModel()
        
        self.actual_card_holder = CardHolder(            
            self, 
            [],
            "Kezdocim",            
            self.getNewCard,
            self.collectCards
        )
        
        self.actual_card_holder.set_background_color(QColor(Qt.yellow))
        self.actual_card_holder.set_border_width(10)
        self.actual_card_holder.set_max_overlapped_cards(5)
        self.actual_card_holder.set_y_coordinate_by_reverse_index_method(self.get_y_coordinate_by_reverse_index)
        self.actual_card_holder.set_x_offset_by_index_method(self.get_x_offset_by_index)
        self.scroll_layout.addWidget(self.actual_card_holder)
        
        next_button = QPushButton("next",self)
        next_button.clicked.connect(self.actual_card_holder.button_animated_move_to_next)        
        next_button.setFocusPolicy(Qt.NoFocus)
        
        previous_button = QPushButton("prev",self)
        previous_button.clicked.connect(self.actual_card_holder.button_animated_move_to_previous)
        previous_button.setFocusPolicy(Qt.NoFocus)

        fill_up_button = QPushButton("fill up",self)
        fill_up_button.clicked.connect(self.fill_up)
        fill_up_button.setFocusPolicy(Qt.NoFocus)

        self.scroll_layout.addStretch(1)
        self.scroll_layout.addWidget(previous_button)
        self.scroll_layout.addWidget(next_button)
        self.scroll_layout.addWidget(fill_up_button)
        
        self.actual_card_holder.setFocus()



        

        self.show()
        
    def buildUpMediaModel(self):
        path_collector_A = PathsCollector('A_folder_name', "/path/to/ini", "/media/akoel/Movies/Final/01.Video/01.Movie/01.Films/01.Uncategorized/A.Profi-1981/image.jpeg")
        titles_A = IniTitles("Eredeti cim", {"hu":"Magyar cim", "en":"English title", "se":" "})
        control_A =IniControl("title", "video", "movie")
        storylines_A = IniStorylines("A tortenet ...", {"en":"the story is ..", "hu":"a történet ..."})    
        self.collector_A = MediaCollector(path_collector_A, titles_A, control_A, None, storylines_A)

        path_collector_B = PathsCollector('C_folder_name', "/path/to/ini", "/path/to/jpeg")
        titles_B = IniTitles("B Eredeti cim", {"hu":"oMagyar cim", "en":"D English title", "se":"B"})
        control_B =IniControl("title", "video", "movie")
        storylines_B = IniStorylines("A tortenet ...", {"en":"the story is ..", "hu":"a történet \n tobb soros\n leiras a filmrol\n hogy lehessen tesztelnei milyen hosszu uzeneteket\n tud kezelni"})    
        self.collector_B = MediaCollector(path_collector_B, titles_B, control_B, None, storylines_B)

        path_collector_C = PathsCollector('D_folder_name', "/path/to/ini", "/path/to/jpeg")
        titles_C =  IniTitles("C Eredeti cim", {"hu":"ö Magyar cim", "en":"A English title", "se":"C"})
        control_C =IniControl("title", "video", "movie")
        storylines_C = IniStorylines("A tortenet ...", {"en":"the story is ..", "hu":"a történet ..."})    
        self.collector_C = MediaCollector(path_collector_C, titles_C, control_C, None, storylines_C)

        path_collector_D = PathsCollector('A_folder_name', "/path/to/ini", "/path/to/jpeg")
        titles_D =  IniTitles("D Eredeti cim", {"hu":"á Magyar cim", "en":"B English title", "se":"D"})
        control_D =IniControl("title", "video", "movie")
        storylines_D = IniStorylines("A tortenet ...", {"en":"the story is ..", "hu":"a történet ..."})
        self.collector_D = MediaCollector(path_collector_D, titles_D, control_D, None, storylines_D)

# ---

        path_collector_BA = PathsCollector('A_folder_name', "/path/to/ini", "/path/to/jpeg")
        titles_BA =  IniTitles("A Konténer", {"hu":"A Konténer", "en":"A Container", "se":"D"})
        control_BA =IniControl("title", "video", "movie")
        storylines_BA = IniStorylines("A gyujtő ...", {"en":"the container is ..", "hu":"A Gyüjtő ..."})
        collector_BA = MediaCollector(path_collector_BA, titles_BA, control_BA, None, storylines_BA)
        self.collector_B.addMediaCollector(collector_BA)

        path_collector_BB = PathsCollector('A_folder_name', "/path/to/ini", "/path/to/jpeg")
        titles_BB =  IniTitles("K Konténer", {"hu":"K Konténer", "en":"K Container", "se":"D"})
        control_BB =IniControl("title", "video", "movie")
        storylines_BB =IniStorylines("A gyujtő ...", {"en":"the container is ..", "hu":"A Gyüjtő ..."})
        collector_BB = MediaCollector(path_collector_BB, titles_BB, control_BB, None, storylines_BB)
        self.collector_B.addMediaCollector(collector_BB)

        path_storage_BC = PathsStorage('C_folder_name', "/path/to/ini", "/media/akoel/Movies/Final/01.Video/01.Movie/01.Films/01.Uncategorized/A.Profi-1981/image.jpeg", "/path/to/media")
        titles_BC = IniTitles("B Mozi cime", {"hu":"B Mozi cim", "en":"D Movie title", "se":"B"})
        control_BC =IniControl("title", "video", "movie")
        storylines_BC =IniStorylines("Ez a default: \nA Moz\ni tor\ntenet ...\n Ez egy\ntobb \nsoros\nUzenet\n Mert p\nont ezt \nakarom \n tesz\nte\nlni", {"en":"the movie's story is .." })
        #general_BC = IniGeneral("2012-2013", ["Dir 1", "Dir 2"], ["Writ 1", "Writ 2"], ["Act 1", "Act 2"], "2:12", ["en", "hu"], ["en", "hu"], ["action", "crime"], ["money", "greed"], ["us", "ca"])
        general_BC = IniGeneral("2012-2013", ["Dir 1", "Dir 2"], ["Writ 1", "Writ 2"], ["Act 1", "Act 2"], "2:12", [], [], ["action", "crime"], ["money", "greed"], ['us', 'ca'])
        rating_BC = IniClassification(10, True, True) 
        self.storage_BC = MediaStorage(path_storage_BC, titles_BC, control_BC, general_BC, storylines_BC, rating_BC)
        self.collector_B.addMediaStorage(self.storage_BC)

        path_storage_BD = PathsStorage('C_folder_name', "/path/to/ini", "/media/akoel/Movies/Final/01.Video/01.Movie/01.Films/01.Uncategorized/A.Profi-1981/image.jpeg", "/path/to/media")
        titles_BD = IniTitles("C Default Mozi cime", {"en":"A Movie title", "se":"B"})
        control_BD =IniControl("title", "video", "movie")
        storylines_BD =IniStorylines("Ez a \ndefault: \nA Mozi \ntorte\nnet ...\n Ez egy tobb soros\nUzenet\n Mert po\nnt ezt a\nkarom \n tesztelni", {"en":"the movie's story is .." })
        general_BD = IniGeneral("2012-2013", ["Dir 1", "Dir 2"], ["Writ 1", "Writ 2"], ["Act 1", "Act 2", "Act 3", "Act 4", "Act 5", "Act 6", "Act 7", "Act 8", "Act 9", "Act 10", "Act 11", "Act 12", "Act 13", "Act 14"], "2:12", ["en", "hu"], ["en", "hu"], ["action", "crime"], ["money", "greed"], ["us", "ca"])
        rating_BD = IniClassification(10, True, True) 
        storage_BD = MediaStorage(path_storage_BD, titles_BD, control_BD, general_BD, storylines_BD, rating_BD)
        self.collector_B.addMediaStorage(storage_BD)

# ---

        self.collector_A.addMediaCollector(self.collector_D)
        self.collector_A.addMediaCollector(self.collector_B)
        self.collector_A.addMediaCollector(self.collector_C)
        
    

    def change_spinner(self):
        self.actual_card_holder.set_spinner(self.spinner_file_name)

        
    def fill_up(self):
        self.actual_card_holder.start_card_collection([])
        
    def collectCards(self, paths):
        """
        """
        cdl = []        
        cdl.append(self.collector_A)
        cdl.append(self.collector_B)
        cdl.append(self.collector_C)
        cdl.append(self.storage_BC)
        return cdl
        
    def getNewCard(self, card_data, local_index, index):
        """
        
        """
        card = Card(self.actual_card_holder, card_data, local_index, index)
        
        card.set_border_selected_color(QColor(Qt.blue))
        #card.set_background_color(QColor(Qt.white))
        #card.set_border_radius( 15 )
        #card.set_border_width(18)
        card.setMaximumHeight(265)
        card.setMinimumHeight(265)
        
 
        panel = card.get_panel()
        layout = panel.get_layout()
        
        # Construct the Card
#        label=QLabel(card_data + "\n\n\n\n\n\n\n\n\n\nHello")
#        layout.addWidget(label)
        #layout.addWidget(QPushButton("hello"))

        
        myPanel = MyPanel(card)        
        layout.addWidget(myPanel)
        
        return card
    
    def get_y_coordinate_by_reverse_index(self, reverse_index):
        """
        
        """        
        return reverse_index * reverse_index * 16
    
    def get_x_offset_by_index(self, index):
        """
        """
        return index * 4

class MyPanel(QWidget):
    
    def __init__(self, card):
        QWidget.__init__(self, card)
        
        self.card = card
        #self.setAttribute(Qt.WA_StyledBackground, True)
        #self.setStyleSheet('background-color: red' )
        
        
        
        settings = QtWebEngineWidgets.QWebEngineSettings.globalSettings()
        for attr in (QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, QtWebEngineWidgets.QWebEngineSettings.ScreenCaptureEnabled,):
            settings.setAttribute(attr, True)
 
        
        
        
        
        self.browser = QWebEngineView()
        self.browser.setHtml( card.card_data.getHtml(), QUrl("file://"))
        self.browser.loadFinished.connect(self.onLoadFinished)
        
    def onLoadFinished(self, ok):
        if ok:
            pass                              
        
            self.self_layout = QVBoxLayout()
            self.self_layout.setSpacing(0)
            self.setLayout(self.self_layout)
        
            self.self_layout.addWidget(self.browser)
        
        
    def mousePressEvent(self, event):
        #if event.button() == Qt.LeftButton:
        #    print(self.card.card_data, self.card.local_index, self.card.status)
        event.ignore()

    def mouseMoveEvent(self, event):
        event.ignore()
        
  
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    #ex.start_card_holder()
    sys.exit(app.exec_())
