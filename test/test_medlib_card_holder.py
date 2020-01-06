import sys

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QApplication

from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

from cardholder.cardholder import CardHolder
from cardholder.cardholder import Card

from medlib.input_output import collectCards
from PyQt5 import QtCore

class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'Card selector'
        self.left = 10
        self.top = 10
        self.width = 1200
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
        
        self.actual_card_holder = CardHolder(            
            self, 
            self.getNewCard,
            self.collectCards,
            self.goesHigher
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
        
        self.setFocusPolicy(Qt.NoFocus)

        self.show()

    def change_spinner(self):
        self.actual_card_holder.set_spinner(self.spinner_file_name)
        
    def fill_up(self):
        self.actual_card_holder.start_card_collection([])

    #
    # Input parameter for CardHolder
    #
    def collectCards(self, paths):
        """
        """
        collector = collectCards()
        collector.setNextLevelListener(self.goesDeeper)
     
        cdl = collector.getMediaCollectorList()
        
        return cdl

    #
    # Input parameter for CardHolder
    #
    def goesHigher(self, actual_collector):
        if actual_collector:
            parent_collector = actual_collector.getParentCollector()
            
            if parent_collector:
                mcl = parent_collector.getMediaCollectorList()
                msl = parent_collector.getMediaStorageList()
                self.actual_card_holder.refresh(mcl + msl)
        
    #
    # Input parameter for CardHolder
    #
    def getNewCard(self, card_data, local_index, index):
        """        
        """
        card = Card(self.actual_card_holder, card_data, local_index, index)
        
        card.set_border_selected_color(QColor(Qt.blue))
        #card.set_background_color(QColor(Qt.white))
        #card.set_border_radius( 15 )
        #card.set_border_width(18)
        card.setMaximumHeight(300)
        card.setMinimumHeight(300)
 
        panel = card.get_panel()
        layout = panel.get_layout()
        
        myPanel = card.card_data.getWidget(1)

        layout.addWidget(myPanel)
        
        return card
        
    #
    # Input parameter for MediaCollector
    #
    def goesDeeper(self, mediaCollector):        
        mcl = mediaCollector.getMediaCollectorList()
        msl = mediaCollector.getMediaStorageList()
        
        self.actual_card_holder.refresh(mcl + msl)

# !!!!!!!!!!!!!!!!!!!!!
#    def keyPressEvent(self, event):
#        if event.key() == QtCore.Qt.Key_Escape:
#            print( "Main window-Esc", event.key())
#        
#        return QWidget.keyPressEvent(self, event)
# !!!!!!!!!!!!!!!!!!!!!
    
    def get_y_coordinate_by_reverse_index(self, reverse_index):
        """        
        """        
#        return reverse_index * reverse_index * 16
        return reverse_index * 50
    
    def get_x_offset_by_index(self, index):
        """
        """
        return index * 4

class MyPanel(QWidget):
    
    def __init__(self, card):
        QWidget.__init__(self, card)
        
        self.card = card
        card.card_data.getWidget()
        
        self.setAttribute(Qt.WA_StyledBackground, True)

 
        
        

        
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
