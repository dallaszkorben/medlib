import os

import medlib

from medlib.handle_property import _

from medlib.constants import PANEL_FONT_TYPE
from medlib.constants import PANEL_FONT_SIZE

from medlib.constants import CLASSIFICATION_TAG_FIELD_BACKGROUND_COLOR
from medlib.constants import CLASSIFICATION_RATE_FIELD_BACKGROUND_COLOR

from medlib.constants import CLASSIFICATION_ICON_TAG_ADD
from medlib.constants import CLASSIFICATION_ICON_TAG_DELETE
from medlib.constants import CLASSIFICATION_ICON_FOLDER
from medlib.constants import CLASSIFICATION_ICON_PREFIX
from medlib.constants import CLASSIFICATION_ICON_FAVORITE_TAG   
from medlib.constants import CLASSIFICATION_ICON_SIZE
from medlib.constants import CLASSIFICATION_ICON_NEW
from medlib.constants import CLASSIFICATION_ICON_EXTENSION
from medlib.constants import ON
from medlib.constants import OFF

from medlib.card_ini import KEY_CLASSIFICATION_RATE
from medlib.card_ini import KEY_CLASSIFICATION_TAG
from medlib.card_ini import KEY_CLASSIFICATION_NEW
from medlib.card_ini import KEY_CLASSIFICATION_FAVORITE

from medlib.card_ini import SECTION_CLASSIFICATION

from medlib.card_ini import JSON_KEY_CLASSIFICATION_RATE
from medlib.card_ini import JSON_KEY_CLASSIFICATION_TAG
from medlib.card_ini import JSON_KEY_CLASSIFICATION_NEW
from medlib.card_ini import JSON_KEY_CLASSIFICATION_FAVORITE

from medlib.mediamodel.extra import FlowLayout
from medlib.mediamodel.extra import QHLine

from medlib.handle_property import updateCardIni

from pkg_resources import resource_filename

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QAbstractSpinBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton

from PyQt5.QtGui import QFont
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QIcon

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QSize

class IniClassification(object):
    """
    This class represents the [classification] section in the card.ini file
        -rate
        -favorite
        -new
        -tag
    """
    
    def __init__(self, rate=None, tag_list=[], favorite=None, new=None):
        """
        This is the constructor of the IniClassification class
        ___________________________________________
        input:
            rate        integer     1-10
            tag_list    list        list of tags
            favorite    boolean     True,False
            new         boolean     True,False
        """
        self.rate = rate if (rate is None or (rate >= 0 and rate <= 10)) else 1 if rate < 0 else 10
        self.tag_list = tag_list if tag_list else []
        self.favorite = favorite
        self.new = new
        
        self.tag_field_widget = None
        
    def getRate(self):
        return self.rate
    
    def getTagList(self):
        return self.tag_list
    
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
        
    def setTagList(self, tag_list):
        self.tag_list = tag_list
        
    def getJson(self):        
        json = {}
        json.update({} if self.rate is None else {JSON_KEY_CLASSIFICATION_RATE: self.rate})
        json.update({} if self.tag_list is None or not self.tag_list else {JSON_KEY_CLASSIFICATION_TAG: self.tag_list})
        json.update({} if self.favorite is None else {JSON_KEY_CLASSIFICATION_FAVORITE : "y" if self.favorite else "n"})
        json.update({} if self.new is None else {JSON_KEY_CLASSIFICATION_NEW: "y" if self.new else "n"})
        
        return json    
    
    # --------------------------------------------
    # ------------- Classification ---------------
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
        widgetFavorite = self.getWidgetClassificationInfoFavorite(media, scale)
        classification_layout.addWidget(widgetFavorite) 

        # --- NEW ---
        widgetNew = self.getWidgetClassificationInfoNew(media, scale)
        classification_layout.addWidget(widgetNew) 
        
        # --- ADD ---
        widgetAdd = self.getWidgetAdd(media, scale)
        classification_layout.addWidget(widgetAdd)
        
        return widget

    def setFocusTagField(self, value):
        if self.tag_field_widget:
            self.tag_field_widget.setFocus()
        
    # ---------- #
    # Rate field #
    # ---------- #
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
                    self.setStyleSheet( "QSpinBox{background:'" + CLASSIFICATION_RATE_FIELD_BACKGROUND_COLOR + "'}")
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
        
    # --------------- #
    # Favorite button #
    # --------------- #
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
                    icon.addPixmap(QPixmap( resource_filename(__name__, os.path.join(CLASSIFICATION_ICON_FOLDER, CLASSIFICATION_ICON_PREFIX + "-" + CLASSIFICATION_ICON_FAVORITE_TAG + "-" + ON + "." + CLASSIFICATION_ICON_EXTENSION)) ), QIcon.Normal, QIcon.On)
                    icon.addPixmap(QPixmap( resource_filename(__name__, os.path.join(CLASSIFICATION_ICON_FOLDER, CLASSIFICATION_ICON_PREFIX + "-" + CLASSIFICATION_ICON_FAVORITE_TAG + "-" + OFF + "." + CLASSIFICATION_ICON_EXTENSION)) ), QIcon.Normal, QIcon.Off)
                    self.setIcon(icon)
                    self.setIconSize(QSize(CLASSIFICATION_ICON_SIZE * scale, CLASSIFICATION_ICON_SIZE * scale))
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

    # ---------- #
    # New button #
    # ---------- #
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
                    icon.addPixmap(QPixmap(resource_filename(__name__, os.path.join(CLASSIFICATION_ICON_FOLDER, CLASSIFICATION_ICON_PREFIX + "-" + CLASSIFICATION_ICON_NEW + "-" + ON + "." + CLASSIFICATION_ICON_EXTENSION))), QIcon.Normal, QIcon.On)
                    icon.addPixmap(QPixmap(resource_filename(__name__, os.path.join(CLASSIFICATION_ICON_FOLDER, CLASSIFICATION_ICON_PREFIX + "-" + CLASSIFICATION_ICON_NEW + "-" + OFF + "." + CLASSIFICATION_ICON_EXTENSION))), QIcon.Normal, QIcon.Off)
                    self.setIcon(icon)
                    self.setIconSize(QSize(CLASSIFICATION_ICON_SIZE * scale, CLASSIFICATION_ICON_SIZE * scale))
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

    # ---------- #
    # ADD button #
    # ---------- #
    def getWidgetAdd(self, media, scale):
        class AddButton(QPushButton):
   
            class AddLabel(QLabel):            
                clicked=pyqtSignal()
            
                def __init__(self, parent=None):
                    QLabel.__init__(self, parent)

                def mousePressEvent(self, event):
                    self.clicked.emit()
                
                def enterEvent(self, event):
                    self.update()
                    QApplication.setOverrideCursor(Qt.PointingHandCursor)        
                    event.ignore()
        
                def leaveEvent(self, event):
                    self.update()
                    QApplication.restoreOverrideCursor()        
                    event.ignore()
            
            def __init__(self, ini_classification, scale):
                QPushButton.__init__(self)    
                self.ini_classification = ini_classification

                icon = QIcon()
                icon.addPixmap(QPixmap(resource_filename(__name__, os.path.join(CLASSIFICATION_ICON_FOLDER, CLASSIFICATION_ICON_TAG_ADD + "." + CLASSIFICATION_ICON_EXTENSION))), QIcon.Normal, QIcon.On)

                self.setIcon(icon)
                self.setIconSize(QSize(CLASSIFICATION_ICON_SIZE * scale, CLASSIFICATION_ICON_SIZE * scale))
                
                self.setCursor(QCursor(Qt.PointingHandCursor))

                self.setStyleSheet("background:transparent; border:none")
                    
                self.clicked.connect(self.on_click)

            # You clicked on the Add (green cross) button
            def on_click(self):
 
                # Indicates that the TAG FIELD needs to be shown
                media.setNeededTagField(True)
                
                # Re-paint the widget (with the TAG FIELD)
                media.reGenerate(scale)              
#                pass
                # change the status of the favorite in the Object
#                self.ini_classification.setNew(self.isChecked())
                
                # change the status of the favorite in the card.ini
#                updateCardIni(media.getPathOfCard(), SECTION_CLASSIFICATION, KEY_CLASSIFICATION_NEW, 'y' if self.isChecked() else 'n')
        
                # change the value of the rate in the json
#                medlib.input_output.saveJson(media.getRoot())
        
        button = AddButton(self, scale)
        return button






    def addTagListButtons(self, media, scale, grid_layout, row, title_id, value_method):
        """
        Adds the tags as buttons        
        """
        
        tag_list = value_method()

        #
        # TAG button
        #
        class TagButtonForSearch(QPushButton):
            """
            It represents the tag button
            The button has a "delete" icon on the right side.
            If you click on the delete icon, the tag will be removed
            """
            class DeleteLabel(QLabel):            
                clicked=pyqtSignal()
            
                def __init__(self, parent=None):
                    QLabel.__init__(self, parent)

                def mousePressEvent(self, event):
                    self.clicked.emit()
                
                def enterEvent(self, event):
                    self.update()
                    QApplication.setOverrideCursor(Qt.PointingHandCursor)        
                    event.ignore()
        
                def leaveEvent(self, event):
                    self.update()
                    QApplication.restoreOverrideCursor()        
                    event.ignore()
                
            def __init__(self, media, scale, translatedText, rawText, title_id):
            
                super().__init__(translatedText + "     ")
                self.media = media
                self.rawText = rawText
                self.title_id = title_id

                iconBorder = 2 * scale

                # Set size of button
                self.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Bold)) 
                fm = QFontMetrics(self.font())

                # Icon
                pathToDeleteIcon = resource_filename(__name__, os.path.join(CLASSIFICATION_ICON_FOLDER, CLASSIFICATION_ICON_TAG_DELETE + "." + CLASSIFICATION_ICON_EXTENSION))
                
                label_icon = self.DeleteLabel()
                label_icon.setAttribute(QtCore.Qt.WA_TranslucentBackground)
                label_icon.setPixmap(QIcon(pathToDeleteIcon).pixmap(QSize(fm.height() - iconBorder * 2, fm.height() - iconBorder * 2)))

                layout = QHBoxLayout(self)
                layout.setContentsMargins(0, 0, iconBorder, 0)
                layout.addWidget(label_icon, alignment=QtCore.Qt.AlignRight)

                # calculate text width
                self.setFixedWidth(fm.width(self.text()) + 10)
                self.setFixedHeight(fm.height())

                label_icon.clicked.connect(self.on_delete)            
                self.clicked.connect(self.on_click)

            def on_delete(self):

                # remove the tag from the tag list
                tag_list.remove(self.rawText)
                
                media.setNeededTagField(False)
            
                # change the tag list in the Object
                media.classification.setTagList(tag_list)
            
                # change the status of the favorite in the card.ini
                updateCardIni(media.getPathOfCard(), SECTION_CLASSIFICATION, KEY_CLASSIFICATION_TAG, ','.join(tag_list))
        
                # change the value of the rate in the json
                medlib.input_output.saveJson(media.getRoot())

                # Re-print the widgets
                media.reGenerate(scale)
            
            def on_click(self):
                modifiers = QApplication.keyboardModifiers()
                if modifiers == Qt.ShiftModifier:
                    withShift = True
                else:
                    withShift = False
                self.media.search( withShift, self.rawText, self.title_id)

        #
        # TAG FIELD
        #
        class TagField(QLineEdit):
            """
            It represents the TAG field
            """
            def __init__(self, media, scale): #, translatedText, rawText, title_id):
            
                super().__init__()
                self.media = media

                # Set size of button
                self.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Bold)) 
                self.setStyleSheet( "color:black; background:'" + CLASSIFICATION_TAG_FIELD_BACKGROUND_COLOR + "'")
                fm = QFontMetrics(self.font())

                # calculate text width
                self.setFixedWidth(fm.width("WWWWWWW") + 10)
                self.setFixedHeight(fm.height())

                self.returnPressed.connect(self.pressedEnterEvent)

            # press ENTER on the TAG FIELD
            def pressedEnterEvent(self):

                text = self.text().strip()
                
                if text and text not in tag_list:

                    # add the tag to the tag list
                    tag_list.append(text)
            
                    # change the tag list in the Object
                    media.classification.setTagList(tag_list)
            
                    # change the status of the favorite in the card.ini
                    updateCardIni(media.getPathOfCard(), SECTION_CLASSIFICATION, KEY_CLASSIFICATION_TAG, ','.join(tag_list))
        
                    # change the value of the rate in the json
                    medlib.input_output.saveJson(media.getRoot())

                # No need TAG FIELD anymore
                media.setNeededTagField(False)

                # Re-print the widgets
                media.reGenerate(scale)                
                
            def focusOutEvent(self, event):

                # No need TAG FIELD anymore
                media.setNeededTagField(False)
                
                # Re-paint the widget (without the TAG FIELD)
                media.reGenerate(scale)              




        
        
        # --- horizontal line at the beginning
        grid_layout.addWidget(QHLine(), row, 0, 1, 2)
        row = row + 1
            
        widget_key = QLabel(_(title_id) + ":", )
        widget_key.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Bold))
        widget_key.setAlignment(Qt.AlignTop)
        
        layout = FlowLayout()
        layout.setAlignment(Qt.AlignLeft)        
        layout.setSpacing(1)        
        layout.setContentsMargins(0, 0, 0, 0)

        widget_value = QWidget()
        widget_value.setLayout( layout )
        widget_value.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Normal))        

        needWidget = False
        
        # Add TAG buttons
        for tag in tag_list:            
            label = TagButtonForSearch(media, scale, tag, tag, title_id)
            layout.addWidget(label)
            needWidget = True
                
        # Add TAG field
        if media.isNeededTagField():
            field = TagField(media, scale)
            layout.addWidget(field)
                
            self.tag_field_widget = field
            
            needWidget = True

        else:
            self.tag_field_widget = None
            
        # if there was TAGs and/or TAG FIELD    
        if needWidget:
                               
            grid_layout.addWidget(widget_key, row, 0)
            grid_layout.addWidget(widget_value, row, 1)
            row = row + 1
            
        return row   

        
    
    