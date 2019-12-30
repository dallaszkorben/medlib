import os

import medlib

from medlib.constants import PANEL_FONT_TYPE
from medlib.constants import PANEL_FONT_SIZE
from medlib.constants import RATE_BACKGROUND_COLOR
from medlib.constants import RATING_ICON_FOLDER
from medlib.constants import RATING_ICON_PREFIX
from medlib.constants import RATING_ICON_FAVORITE_TAG   
from medlib.constants import RATING_ICON_SIZE
from medlib.constants import RATING_ICON_NEW_TAG
from medlib.constants import RATING_ICON_EXTENSION
from medlib.constants import ON
from medlib.constants import OFF

from medlib.card_ini import SECTION_CLASSIFICATION

from medlib.card_ini import KEY_CLASSIFICATION_RATE
from medlib.card_ini import KEY_CLASSIFICATION_TAG
from medlib.card_ini import KEY_CLASSIFICATION_NEW
from medlib.card_ini import KEY_CLASSIFICATION_FAVORITE

from medlib.handle_property import updateCardIni

from pkg_resources import resource_filename

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QAbstractSpinBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton

from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QCursor

from PyQt5.QtCore import Qt 
from PyQt5.QtCore import QSize

from PyQt5.Qt import QIcon

class IniClassification(object):
    """
    This class represents the [classification] section in the card.ini file
        -rate
        -favorite
        -new
        -tag
    """
    
    def __init__(self, rate=None, favorite=None, new=None):
        """
        This is the constructor of the IniClassification class
        ___________________________________________
        input:
            rate         integer       1-10
            favorite     boolean       True,False
            new          boolean       True,False
        """
        self.rate = rate if (rate is None or (rate >= 0 and rate <= 10)) else 1 if rate < 0 else 10
        self.favorite = favorite
        self.new = new
        
    def getRate(self):
        return self.rate
    
    def getFavorite(self):
        return self.favorite
    
    def getNew(self):
        return self.new
        
    def setRate(self, rate):
        self.rate = 10 if rate > 10 else 0 if rate < 0 else rate

    def setFavorite(self, favorite):
        self.favorite = favorite

    def setNew(self, new):
        self.new = new
        
    def getJson(self):        
        json = {}
        json.update({} if self.rate is None else {KEY_CLASSIFICATION_RATE: self.rate})
        json.update({} if self.favorite is None else {KEY_CLASSIFICATION_FAVORITE : "y" if self.favorite else "n"})
        json.update({} if self.new is None else {KEY_CLASSIFICATION_NEW: "y" if self.new else "n"})
        
        return json
    
    
    # --------------------------------------------
    # ----------------- Rating -------------------
    # --------------------------------------------
    def getWidget(self, media, scale):
        """   __________
             | Rate     |
             |__________|
             | Favorite |            
             |__________|
             | New      |
             |__________|
        """        
        # layout of this widget => three columns
        classification_layout = QVBoxLayout()
        classification_layout.setAlignment(Qt.AlignTop)
        
        # space between the three grids
        classification_layout.setSpacing(20 * scale)
        
        # margin around the widget
        classification_layout.setContentsMargins(0, 5, 5, 5)
        
        widget = QWidget()
        widget.setLayout(classification_layout)
        
        # --- RATE ---
        widgetRate = self.getWidgetClassificationInfoRate(media, scale)
        classification_layout.addWidget(widgetRate)
        
        # --- FAVORITE ---
        widgetFavorite=self.getWidgetClassificationInfoFavorite(media, scale)
        classification_layout.addWidget(widgetFavorite) 

        # --- NEW ---
        widgetNew=self.getWidgetClassificationInfoNew(media, scale)
        classification_layout.addWidget(widgetNew) 
        
        return widget

    # ---- #
    # Rate #
    # ---- #
    def getWidgetClassificationInfoRate( self, media, scale ):
        
        class MySpinBox(QSpinBox):
            
            def __init__(self, ini_classification, scale):
                super().__init__()
                self.ini_classification = ini_classification
        
                if self.ini_classification.getRate() is None:
                    self.hide()

                else:
                    self.setButtonSymbols(QAbstractSpinBox.NoButtons) #PlusMinus / NoButtons / UpDownArrows        
                    self.setMaximum(10)
                    self.setFocusPolicy(Qt.NoFocus)
                    self.lineEdit().setReadOnly(True)
                    self.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Normal))
                    self.lineEdit().setStyleSheet( "QLineEdit{color:black}")
                    self.setStyleSheet( "QSpinBox{background:'" + RATE_BACKGROUND_COLOR + "'}")
                    self.setValue(self.ini_classification.getRate())
                    
                    self.valueChanged.connect(self.classificationRateOnValueChanged)

            def stepBy(self, steps):
                """
                It needs to be override to make deselection after the step.
                If it is not there, the selection color (blue) will be appear on the field
                """
                super().stepBy(steps)
                self.lineEdit().deselect()

            # Mouse Hover in
            def enterEvent(self, event):
                self.update()
                QApplication.setOverrideCursor(Qt.PointingHandCursor)

                self.setButtonSymbols(QAbstractSpinBox.UpDownArrows) #PlusMinus / NoButtons / UpDownArrows        

#                self.card_panel.get_card_holder().setFocus()
                event.ignore()

            # Mouse Hover out
            def leaveEvent(self, event):
                self.update()
                QApplication.restoreOverrideCursor()

                self.setButtonSymbols(QAbstractSpinBox.NoButtons) #PlusMinus / NoButtons / UpDownArrows        
        
#                self.card_panel.get_card_holder().setFocus()
                event.ignore()

            def classificationRateOnValueChanged(self):
                 
                # change the value of the rate in the Object
                self.ini_classification.setRate(self.value())
                
                # change the value of the rate in the card.ini
                updateCardIni(media.getPathOfCard(), SECTION_CLASSIFICATION, KEY_CLASSIFICATION_RATE, self.value())
                
                # change the value of the rate in the json                
                medlib.input_output.saveJson(media.getRoot())
                
        widget = MySpinBox(self, scale)        
        return widget
        
    # -------- #
    # Favorite #
    # -------- #
    def getWidgetClassificationInfoFavorite(self, media, scale):
        class FavoriteButton(QPushButton):
            def __init__(self, ini_classification, scale):
                QPushButton.__init__(self)
                self.ini_classification = ini_classification
        
                if self.ini_classification.getFavorite() is None:
                    self.hide()
                else:
                    self.setCheckable(True)        
                    icon = QIcon()
                    icon.addPixmap(QPixmap( resource_filename(__name__, os.path.join(RATING_ICON_FOLDER, RATING_ICON_PREFIX + "-" + RATING_ICON_FAVORITE_TAG + "-" + ON + "." + RATING_ICON_EXTENSION)) ), QIcon.Normal, QIcon.On)
                    icon.addPixmap(QPixmap( resource_filename(__name__, os.path.join(RATING_ICON_FOLDER, RATING_ICON_PREFIX + "-" + RATING_ICON_FAVORITE_TAG + "-" + OFF + "." + RATING_ICON_EXTENSION)) ), QIcon.Normal, QIcon.Off)
                    self.setIcon(icon)
                    self.setIconSize(QSize(RATING_ICON_SIZE * scale, RATING_ICON_SIZE * scale))
                    self.setCursor(QCursor(Qt.PointingHandCursor))
                    self.setStyleSheet("background:transparent; border:none")
                    self.setChecked(self.ini_classification.getFavorite())
                    
                    self.clicked.connect(self.classificationFavoriteButtonOnClick)
                    
            def classificationFavoriteButtonOnClick(self):

                # change the status of the favorite in the Object
                self.ini_classification.setFavorite(self.isChecked())
                
                # change the status of the favorite in the card.ini
                updateCardIni(media.getPathOfCard(), SECTION_CLASSIFICATION, KEY_CLASSIFICATION_FAVORITE, 'y' if self.isChecked() else 'n')
        
                # change the value of the rate in the json
                medlib.input_output.saveJson(media.getRoot())

        button = FavoriteButton(self, scale)
        return button

    # --- #
    # New #
    # --- #
    def getWidgetClassificationInfoNew(self, media, scale):
        class NewButton(QPushButton):
            def __init__(self, ini_classification, scale):
                QPushButton.__init__(self)    
                self.ini_classification = ini_classification

                if self.ini_classification.getNew() is None:
                    self.hide()
                else:        
                    self.setCheckable(True)        
                    icon = QIcon()
                    icon.addPixmap(QPixmap(resource_filename(__name__, os.path.join(RATING_ICON_FOLDER, RATING_ICON_PREFIX + "-" + RATING_ICON_NEW_TAG + "-" + ON + "." + RATING_ICON_EXTENSION))), QIcon.Normal, QIcon.On)
                    icon.addPixmap(QPixmap(resource_filename(__name__, os.path.join(RATING_ICON_FOLDER, RATING_ICON_PREFIX + "-" + RATING_ICON_NEW_TAG + "-" + OFF + "." + RATING_ICON_EXTENSION))), QIcon.Normal, QIcon.Off)
                    self.setIcon(icon)
                    self.setIconSize(QSize(RATING_ICON_SIZE * scale, RATING_ICON_SIZE * scale))
                    self.setCursor(QCursor(Qt.PointingHandCursor))
                    self.setStyleSheet("background:transparent; border:none")
                    self.setChecked(ini_classification.getNew())
                    
                    self.clicked.connect(self.classificationNewButtonOnClick)
        
            def classificationNewButtonOnClick(self):
                
                # change the status of the favorite in the Object
                self.ini_classification.setNew(self.isChecked())
                
                # change the status of the favorite in the card.ini
                updateCardIni(media.getPathOfCard(), SECTION_CLASSIFICATION, KEY_CLASSIFICATION_NEW, 'y' if self.isChecked() else 'n')
        
                # change the value of the rate in the json
                medlib.input_output.saveJson(media.getRoot())
        
        button = NewButton(self, scale)
        return button
    
    
    
    
    