import sys
import os
import importlib
from pkg_resources import resource_string
from pkg_resources import resource_filename

from functools import cmp_to_key
import locale

from medlib.mediamodel.extra import clearLayout, FlowLayout
from medlib.setup.setup import getSetupIni

from cardholder.cardholder import CardHolder
from cardholder.cardholder import Card

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QDesktopWidget

from PyQt5.QtCore import QObject
from PyQt5.QtCore import Qt

from medlib.constants import MAIN_BACKGROUND_COLOR, LINK_TILE_FONT_SIZE
from medlib.constants import CARD_BORDER_FOCUSED_BACKGROUND_COLOR
from medlib.constants import CARD_BORDER_NORMAL_BACKGROUND_COLOR
from medlib.constants import COLLECTOR_BACKGROUND_COLOR
from medlib.constants import STORAGE_BACKGROUND_COLOR
from medlib.constants import WIDTH_WINDOW
from medlib.constants import HEIGHT_WINDOW
from medlib.constants import LINK_TILE_FONT_TYPE

from medlib.constants import CARDHOLDER_BACKGROUND_COLOR
from medlib.constants import RADIUS_CARDHOLDER
from medlib.constants import IMG_WINDOW
    
from PyQt5.QtGui import QColor, QFontMetrics
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPainter

from medlib.input_output import collectCards
from medlib.mediamodel.media_base import FOLDER_TYPE_STORAGE
from PyQt5 import QtCore

class MedlibGui(QWidget):#, QObject):
    
    def __init__(self):
        QWidget.__init__(self)
#        QObject.__init__(self)
       
        self.mediaCollector = None
       
        # It is important not to use the 'setStylesheet' because on that case
        # the rounded corner will fail to be painted               
        p = self.palette()
        color = QColor(0, 0, 0)
        color.setNamedColor(MAIN_BACKGROUND_COLOR)
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)
       
        # most outer container, just right in the Main Window
        box_layout = QVBoxLayout(self)
        self.setLayout(box_layout)
        
        # controls the distance between the MainWindow and the added container: scrollContent
        box_layout.setContentsMargins(10, 10, 10, 10)
        box_layout.setSpacing(5)
    
        # control panel
#        self.control_panel = ControlPanel(self)
#        self.control_panel.set_back_button_method(self.restore_previous_holder)
#        box_layout.addWidget( self.control_panel)
    
        # -------------------------------
        # Title
        # -------------------------------
        self.hierarchy_title = HierarchyTitle(self, self)
        self.hierarchy_title.setBackgroundColor(QColor(CARDHOLDER_BACKGROUND_COLOR))
        self.hierarchy_title.setBorderRadius(RADIUS_CARDHOLDER)

        self.back_button_listener = None

        # ------------------        
        # --- CardHolder ---
        # ------------------                
        self.card_holder = CardHolder(            
            self, 
            self.getNewCard,
            self.collectCards,
            self.refreshCollectedCardsListener,
            None,               #self.selectCard,
            None,               #self.goesHigher
        )
    
        self.card_holder.setBackgroundColor(QColor(CARDHOLDER_BACKGROUND_COLOR))
        self.card_holder.setBorderWidth(10)
        self.card_holder.set_max_overlapped_cards(5)
        self.card_holder.set_y_coordinate_by_reverse_index_method(self.get_y_coordinate_by_reverse_index)
        self.card_holder.set_x_offset_by_index_method(self.get_x_offset_by_index)

        box_layout.addWidget(self.hierarchy_title)
        box_layout.addWidget(self.card_holder)
        box_layout.addStretch(1)

        self.startCardHolder()                

        # --- Window ---
        sp=getSetupIni()
        self.setWindowTitle(sp['name'] + '-' + sp['version'])
        self.setWindowIcon(QIcon(resource_filename(__name__,os.path.join("images", IMG_WINDOW)))) 
        #self.setGeometry(300, 300, 300, 200)
        self.resize(WIDTH_WINDOW, HEIGHT_WINDOW )
        self.center()
        self.show()
        
    def center(self):
        """Aligns the window to middle on the screen"""
        fg=self.frameGeometry()
        cp=QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        self.move(fg.topLeft())

    def startCardHolder(self):
        """
        Start Card Holder        
        """
        self.card_holder.startCardCollection([])        
       
    def get_y_coordinate_by_reverse_index(self, reverse_index):
        """        
        """        
#        return reverse_index * reverse_index * 16
        return reverse_index * 50
    
    def get_x_offset_by_index(self, index):
        """
        """
        return index * 4
    
    def refreshCollectedCardsListener(self, mediaCollector):
        
        self.mediaCollector = mediaCollector
        
        # Show the History Link Title
        if mediaCollector:
            self.hierarchy_title.setTitle(mediaCollector)   
    
    #
    # Input parameter for CardHolder
    #
    def collectCards(self, paths):
        collector = collectCards()
        collector.setNextLevelListener(self.goesDeeper)     
        cdl = collector.getMediaCollectorList()        
        return cdl
        
    #
    # Input parameter for CardHolder
    #
    def getNewCard(self, card_data, local_index, index):
        """        
        """
        card = Card(self.card_holder, card_data, local_index, index)
        
        if card_data.getFolderType() == FOLDER_TYPE_STORAGE:
            card.setBackgroundColor(QColor(STORAGE_BACKGROUND_COLOR))
        else:
            card.setBackgroundColor(QColor(COLLECTOR_BACKGROUND_COLOR))
        
        card.setBorderNormalColor(QColor(CARD_BORDER_NORMAL_BACKGROUND_COLOR))
        card.setBorderFocusedColor(QColor(CARD_BORDER_FOCUSED_BACKGROUND_COLOR))

        card.setBorderRadius(10)
        card.setBorderWidth(8)
        
        card.setMaximumHeight(300)
        card.setMinimumHeight(300)

        card.setNotFocused()
 
        panel = card.getPanel()
        layout = panel.getLayout()
        
        myPanel = card.card_data.getWidget(1)

        layout.addWidget(myPanel)
        
        return card
        
    #
    # Input parameter for MediaCollector
    #
    def goesDeeper(self, mediaCollector):               
        mcl = mediaCollector.getMediaCollectorList()
        msl = mediaCollector.getMediaStorageList()
        sum_list = mcl + msl
        if sum_list:
            self.card_holder.refresh(sum_list)    
  
    def to_integer(self, value):         
        hours, minutes = map(int, (['0']+value.split(':'))[-2:])
        return hours * 60 + minutes
  
    def resizeEvent(self, event):
        """
        When the window resized, then the Hierarchy Title will be re-arranged.
        Without this, the Hierarchy Title will be static, not reflecting on the width
        """
        if self.mediaCollector:
            
            # refresh the Hierarchy Title
            self.hierarchy_title.setTitle(self.mediaCollector) 
            
        self.card_holder.alignSpinner(self.geometry().width(), self.geometry().height())
  
  
  
  
  
  
  
 
  

class LinkLabel(QLabel):
    def __init__(self, gui, label, card_list, index):
        QLabel.__init__(self, label)
        self.gui = gui
        self.label = label
        self.card_list = card_list
        self.index = index
        self.setFont(QFont( LINK_TILE_FONT_TYPE, LINK_TILE_FONT_SIZE, weight=QFont.Bold if index is not None else QFont.Normal))

    # Mouse Hover in
    def enterEvent(self, event):
        if self.index is not None:
            QApplication.setOverrideCursor(Qt.PointingHandCursor)
        event.ignore()

    # Mouse Hover out
    def leaveEvent(self, event):
        if self.index is not None:
            QApplication.restoreOverrideCursor()
        event.ignore()

    # Mouse Press
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton: # and self.index:
            QApplication.restoreOverrideCursor()

            # Generate new Hierarchy Title        
            self.gui.card_holder.refresh(self.card_list, self.index) 
            
        event.ignore()
    

# =========================================
# 
# This Class represents the title
#
# =========================================
#
class HierarchyTitle(QWidget):
    DEFAULT_BACKGROUND_COLOR = Qt.lightGray
    DEFAULT_BORDER_RADIUS = 10
    
    def __init__(self, parent, panel):
        QWidget.__init__(self, parent)

        self.parent = parent
        self.panel = panel
        
        self.self_layout = QHBoxLayout(self)
        self.self_layout.setContentsMargins(5, 5, 5, 5)
        self.self_layout.setSpacing(0)
        self.setLayout(self.self_layout)        
        self.text = QWidget(self)

        # calculate text height        
        self.text.setFont(QFont( LINK_TILE_FONT_TYPE, LINK_TILE_FONT_SIZE, weight=QFont.Normal )) 
        self.fm = QFontMetrics(self.text.font())
        self.text.setMinimumHeight(self.fm.height())
        
        self.self_layout.addWidget(self.text)

        #self.text_layout = FlowLayout(self.text)
        self.text_layout = QVBoxLayout(self.text)
        self.text_layout.setContentsMargins(0, 0, 0, 0)
        self.text_layout.setSpacing(0)

        self.text.setLayout(self.text_layout)        
        
        self.setBackgroundColor(QColor(HierarchyTitle.DEFAULT_BACKGROUND_COLOR), False)
        self.setBorderRadius(HierarchyTitle.DEFAULT_BORDER_RADIUS, False)
        
    def minimumSizeHint(self):
        return QtCore.QSize(150, self.fm.height())
    
    def setTitle(self, collector):
        clearLayout(self.text_layout)
     
        title_list = []
        collector.getTranslatedTitleList(title_list)

        one_line_container, one_line_container_layout = self.get_one_line_container()
                
        text_width = 0
        for title in reversed(title_list[1:]):
#        for title in reversed(title_list):
            
            # Generate text
            label = LinkLabel(self.parent, title["title"], title["card-list"], title["index"])            
            text_width = text_width + self.get_width_in_pixels(label)
            if text_width > self.text.size().width():
                self.text_layout.addWidget(one_line_container)
                
                one_line_container, one_line_container_layout = self.get_one_line_container()
                text_width = self.get_width_in_pixels(label)                
                
            one_line_container_layout.addWidget(label)

            # Generate separator
            label = QLabel(">")
            label.setFont(QFont( LINK_TILE_FONT_TYPE, LINK_TILE_FONT_SIZE, weight=QFont.Bold ))

            text_width = text_width + self.get_width_in_pixels(label)
            if text_width > self.text.size().width():
                self.text_layout.addWidget(one_line_container)
                
                one_line_container, one_line_container_layout = self.get_one_line_container()
                text_width = self.get_width_in_pixels(label)                

            one_line_container_layout.addWidget(label)
       
       
        label = LinkLabel(self.parent, title_list[0]["title"], title_list[0]["card-list"], title_list[0]["index"])       
        text_width = text_width + self.get_width_in_pixels(label)
        if text_width > self.text.size().width():
            self.text_layout.addWidget(one_line_container)
                
            one_line_container, one_line_container_layout = self.get_one_line_container()
            text_width = self.get_width_in_pixels(label)                

        one_line_container_layout.addWidget(label)

        self.text_layout.addWidget(one_line_container)

        self.text_layout.setAlignment(Qt.AlignHCenter)
        

    def get_one_line_container(self):
        one_line_container = QWidget(self)
        one_line_container_layout = QHBoxLayout(one_line_container)
        one_line_container_layout.setContentsMargins(0, 0, 0, 0)
        one_line_container_layout.setSpacing(0)
        one_line_container.setLayout(one_line_container_layout)
        one_line_container_layout.setAlignment(Qt.AlignHCenter)
        return one_line_container, one_line_container_layout





    def create_one_line_container(self):
        self.one_line_container = QWidget(self)
        self.one_line_container_layout = QHBoxLayout(self.one_line_container)
        self.one_line_container_layout.setContentsMargins(0, 0, 0, 0)
        self.one_line_container_layout.setSpacing(0)
        self.one_line_container.setLayout(self.one_line_container_layout)
        self.one_line_container_layout.setAlignment(Qt.AlignHCenter)

    def add_to_one_line_container(self, cw):
        self.one_line_container_layout.addWidget(cw)
        
    def push_new_line_container(self):
        self.text_layout.addWidget(self.one_line_container)
        
    def get_width_in_pixels(self, cw):
        initialRect = cw.fontMetrics().boundingRect(cw.text());
        improvedRect = cw.fontMetrics().boundingRect(initialRect, 0, cw.text());   
        return improvedRect.width()        
        
    def setBackgroundColor(self, color, update=False):
        self.background_color = color
        self.text.setStyleSheet('background: ' + color.name()) 
        if update:
            self.update()
            
    def setBorderRadius(self, radius, update=True):
        self.border_radius = radius
        if update:
            self.update()            
        
    def paintEvent(self, event):
        s = self.size()
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        qp.setBrush( self.background_color )

        qp.drawRoundedRect(0, 0, s.width(), s.height(), self.border_radius, self.border_radius)
        qp.end()      

        
def main():    
    app = QApplication(sys.argv)
    ex = MedlibGui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    