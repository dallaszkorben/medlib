from medlib.constants import *

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

from PyQt5.QtCore import Qt , QSize

from PyQt5.Qt import QIcon

class IniRating(object):
    """
    This class represents the [rating] section in the card.ini file
        -rate
        -favorite
        -new
    """
    
    def __init__(self, rate=None, favorite=None, new=None):
        """
        This is the constructor of the IniRating class
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
        json.update({} if self.rate is None else {'rate': self.rate})
        json.update({} if self.favorite is None else {'favorite' : "y" if self.favorite else "n"})
        json.update({} if self.new is None else {'new': "y" if self.new else "n"})
        
        return json
    
    
    # --------------------------------------------
    # ----------------- Rating -------------------
    # --------------------------------------------
    def getWidget(self, scale):
        """   __________
             | Rate     |
             |__________|
             | Favorite |            
             |__________|
             | New      |
             |__________|
        """        
        # layout of this widget => three columns
        rating_layout = QVBoxLayout()
        rating_layout.setAlignment(Qt.AlignTop)
        
        # space between the three grids
        rating_layout.setSpacing(20 * scale)
        
        # margin around the widget
        rating_layout.setContentsMargins(0, 5, 5, 5)
        
        widget = QWidget()
        widget.setLayout(rating_layout)
        
        # --- RATE ---
        widgetRate = self.getWidgetRatingInfoRate(scale)
        rating_layout.addWidget(widgetRate)
        
        # --- FAVORITE ---
        widgetFavorite=self.getWidgetRatingInfoFavorite(scale)
        rating_layout.addWidget(widgetFavorite) 

        # --- NEW ---
        widgetNew=self.getWidgetRatingInfoNew(scale)
        rating_layout.addWidget(widgetNew) 
        
        return widget

    #             #
    # Rating Rate #
    #             #
    def getWidgetRatingInfoRate( self, scale ):
        
        class MySpinBox(QSpinBox):
            #def __init__(self, card_panel):
            def __init__(self, parent, scale):
                super().__init__()
                self.parent = parent
        
                if self.parent.getRate() is None:
                    self.hide()
                else:
                    self.setButtonSymbols(QAbstractSpinBox.NoButtons) #PlusMinus / NoButtons / UpDownArrows        
                    self.setMaximum(10)
                    self.setFocusPolicy(Qt.NoFocus)
                    self.lineEdit().setReadOnly(True)
                    self.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Normal))
                    self.lineEdit().setStyleSheet( "QLineEdit{color:black}")
                    self.setStyleSheet( "QSpinBox{background:'" + RATE_BACKGROUND_COLOR + "'}")
                    self.setValue(self.parent.getRate())

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

        widget = MySpinBox(self, scale)        
        return widget
        
    #                 #
    # Rating Favorite #
    #                 #
    def getWidgetRatingInfoFavorite(self, scale):
        class FavoriteButton(QPushButton):
            def __init__(self, parent, scale):
                QPushButton.__init__(self)
                self.parent = parent
        
                if self.parent.getFavorite() is None:
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
                    self.setChecked(self.parent.getFavorite())
                    self.clicked.connect(self.ratingFavoriteButtonOnClick)

            def ratingFavoriteButtonOnClick(self):
                self.parent.setFavorite(self.isChecked())        
        
        button = FavoriteButton(self, scale)
        return button

    #            #
    # Rating New #
    #            #
    def getWidgetRatingInfoNew(self, scale):
        class NewButton(QPushButton):
            def __init__(self, parent, scale):
                QPushButton.__init__(self)    
                self.parent = parent

                if self.parent.getNew() is None:
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
                    self.setChecked(parent.getNew())
                    self.clicked.connect(self.ratingNewButtonOnClick)
        
            def ratingNewButtonOnClick(self):
                self.parent.setNew(self.isChecked())
        
        button = NewButton(self, scale)
        return button
    
    
    
    
    