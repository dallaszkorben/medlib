import locale
import os

from pkg_resources import resource_filename

from medlib.constants import *
from medlib.handle_property import _
from builtins import object

from medlib.mediamodel.ini_general import IniGeneral
from medlib.mediamodel.ini_storylines import IniStorylines
from medlib.mediamodel.ini_rating import IniRating
from medlib.mediamodel.extra import QHLine

from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QFont


from PyQt5.QtGui import QPixmap

class MediaBase(object):
    """
    This object represents the MediaBase
    """

   
    @staticmethod
    def sort_key(arg):
        """
        """
        return locale.strxfrm(arg.getTranslatedTitle()) if arg.control.getOrderBy() == 'title' else arg.container_paths.getNameOfFolder() if arg.control.getOrderBy() == 'folder' else arg.container_paths.getNameOfFolder() 
    
    def __init__(self, titles, control, general=None, storylines=None,  rating=None):
        """
        This is the constructor of the MediaCollector
        ________________________________________
        input:
                titles            IniTitles         represents the [titles] section
                control           IniControl        represents the [control] section
                general           IniGeneral        represents the [general] section
                storylines        IniStorylines     represents the [storyline] section
                rating            IniRating         represents the [rating] section
        """
        super().__init__()
        self.titles = titles
        self.control = control
        self.general = general if general else IniGeneral()
        self.storylines = storylines if storylines else IniStorylines()
        self.rating = rating if rating else IniRating()
    
    def getPathOfImage(self):
        raise NotImplementedError

    def getBackgroundColor(self):
        raise NotImplementedError
    
    def getFolderType(self):
        raise NotImplementedError
            
    def getTranslatedTitle(self):
        return self.titles.getTranslatedTitle()
    
    def getTranslatedStoryline(self):
        return self.storylines.getTranslatedStoryline()
   
    def getTitles(self):
        """
        Returns back the [titles] section.
        _________________________________________________________________________________________________
        input:
        output:
                titles       IniTitles
        """
        return self.titles
    
    def getControl(self):
        """
        Returns back the [control] section.
        _________________________________________________________________________________________________
        input:
        output:
                control       IniControl
        """
        return self.control
    
    def getGeneral(self):
        """
        Returns back the [general] section.
        _________________________________________________________________________________________________
        input:
        output:
                general       IniGeneral
        """
        return self.general

    def getStorylines(self):
        """
        Returns back the [storylines] section.
        _________________________________________________________________________________________________
        input:
        output:
                storylines       IniStoryline
        """
        return self.storylines

    def getRating(self):
        """
        Returns back the [rating] section.
        _________________________________________________________________________________________________
        input:
        output:
                general       IniRating
        """
        return self.rating
    
   
    
       
 
         
    # --------------------------------------------
    # ----------- MultiLineInfo -----------------
    # --------------------------------------------
    def getHtmlMultiLineInfo(self):
        out = ""
        out += self.getHtmlMultilineInfoDirectors()
        out += self.getHtmlMultilineInfoWriters()
        out += self.getHtmlMultilineInfoActors()
        out += self.getHtmlMultilineInfoGenres()
        out += self.getHtmlMultilineInfoThemes()
     
#        self.occupied['divs'] = self.occupied['divs'] + 1 if out else 0        
     
        return "<table  id='multiline-table' >" + out + "</table><hr>" if out else ""
     
    def getHtmlMultilineInfoDirectors(self):
        dir_list = ", ".join( "<a href='' style='text-decoration:none;'>" + d + "</a>" for d in self.general.getDirectors())
        out = "<tr><td valign='top'> <b>" + _('title_director') + ":</b> </td> <td>" + dir_list + "</td></tr>"  if  dir_list else ""
        
#        self.occupied['rows'] = self.occupied['rows'] + 1 if dir_list else 0        
        return out
         
    def getHtmlMultilineInfoWriters(self):
        writer_list = ", ".join(d for d in self.general.getWriters())
        out = "<tr><td valign='top'> <b>" + _('title_writer') + ":</b> </td> <td>" + writer_list + "</td></tr>"  if  writer_list else ""

#        self.occupied['rows'] = self.occupied['rows'] + 1 if writer_list else 0        
        return out
         
    def getHtmlMultilineInfoActors(self):
        actor_list = ", ".join(d for d in self.general.getActors())
        out = "<tr><td valign='top'> <b>" + _('title_actor') + ":</b> </td> <td>" + actor_list + "</td></tr>"  if  actor_list else ""

#        self.occupied['rows'] = self.occupied['rows'] + 1 if actor_list else 0        
        return out
     
    def getHtmlMultilineInfoGenres(self):
        genre_list = ", ".join( [ _("genre_" + c) for c in self.general.getGenres()])   
        out = "<tr><td valign='top'> <b>" + _('title_genre') + ":</b> </td> <td>" + genre_list + "</td></tr>"  if  genre_list else ""
        
#        self.occupied['rows'] = self.occupied['rows'] + 1 if genre_list else 0        
        return out
     
    
    def getHtmlMultilineInfoThemes(self):
        theme_list = ", ".join( [ _("theme_" + c) for c in self.general.getThemes()])   
        out = "<tr><td valign='top'> <b>" + _('title_theme') + ":</b> </td> <td>" + theme_list + "</td></tr>"  if  theme_list else ""
        
#        self.occupied['rows'] = self.occupied['rows'] + 1 if theme_list else 0        
        return out     
  
    # -------------------------------------------
    # --------------- Storyline -----------------
    # --------------------------------------------
    def getHtmlStoryline(self):
        out = "<table id='storyline-table' width='100%' >"
        out +=   "<tr height='100%'>"
        out +=      "<td valign='top'>"
        out +=          "<b>" + _('title_storyline') + ":</b>"
        out +=      "</td>"
        out +=      "<td width='100%' valign='top'>"
        out +=          "<textarea id='storyline-textarea' readonly>"
        out +=               self.storylines.getTranslatedStoryline().replace('\n', '&#13;&#10;')
        out +=          "</textarea>"        
        out +=      "</td>"
        out +=   "</tr>"
        out +="</table>"        
        return out

    # --------------------------------------------
    # --------------- Rating ---------------------
    # --------------------------------------------
    def getHtmlRating(self):
        iconFavoriteFileName = RATING_ICON_PREFIX + "-" + RATING_ICON_FAVORITE_TAG + "-" + ("on" if self.getRating().getFavorite() else "off") + "." + RATING_ICON_EXTENSION        
        pathToFavorite = resource_filename(__name__, os.path.join(RATING_ICON_FOLDER, iconFavoriteFileName))
        
        iconNewFileName = RATING_ICON_PREFIX + "-" + RATING_ICON_NEW_TAG + "-" + ("on" if self.getRating().getNew() else "off") + "." + RATING_ICON_EXTENSION        
        pathToNew = resource_filename(__name__, os.path.join(RATING_ICON_FOLDER, iconNewFileName))
        
        out = "<table id='rating-table' height='100%'>"
        out +=   "<tr height='20%'>"
        out +=      "<td>"
        out +=          "<input id='rate-input' type='number'  min='0' max='10' oninput='if(parseInt(this.value)>10){ this.value =10; }else if(this.value.length<1){this.value=0}' value='" + str(self.getRating().getRate()) + "'/>"
        out +=      "</td>"
        out +=   "</tr>"
        out +=   "<tr height='20%'>"
        out +=      "<td align='center'>"
        out +=          "<a href=''>"
        out +=              "<img id='favorite-img' src='file://" + pathToFavorite + "'>"
        out +=          "</a>"                
        out +=      "</td>"
        out +=   "</tr>"
        out +=   "<tr height='20%'>"
        out +=      "<td align='center'>"
        out +=          "<a href=''>"
        out +=              "<img id='favorite-img' src='file://" + pathToNew + "'>"
        out +=          "</a>"               
        out +=      "</td>"
        out +=   "</tr>"
        out +=   "<tr height='40%'>"
        out +=      "<td>"
        out +=      "</td>"
        out +=   "</tr>"        
        out +="</table>"   

        
        return out

        
        
        
        
        
    # --------------------------------------------
    # --------------- Image ---------------------
    # --------------------------------------------
    def getWidgetImage(self, sizeRate):
        
        # layout of this widget => three columns
        image_layout = QHBoxLayout()
        
        # space between the three grids
        image_layout.setSpacing(1)
        
        # margin around the widget
        image_layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QLabel()
        widget.setStyleSheet('background: black')
        widget.setLayout(image_layout)

        pixmap = QPixmap( self.getPathOfImage( ) )

        # if card image was not found
        if pixmap.isNull():            
            # then a blanc image appears
            smaller_pixmap = QPixmap(PANEL_HEIGHT * sizeRate, PANEL_HEIGHT * sizeRate)
            smaller_pixmap.fill(QColor('gray'))
        elif pixmap.width() >= pixmap.height():
            smaller_pixmap = pixmap.scaledToWidth(PANEL_HEIGHT * sizeRate)
        else:
            smaller_pixmap = pixmap.scaledToHeight(PANEL_HEIGHT * sizeRate)
   
        widget.setPixmap(smaller_pixmap)
        
        return widget         
        
    # --------------------------------------------
    # ------------- Middle - Text part -----------
    # --------------------------------------------
    def getWidgetMiddleText(self, sizeRate):
        
        # layout of this widget => three columns
        middle_layout = QVBoxLayout()
        middle_layout.setAlignment(Qt.AlignTop)
        
        # space between the three grids
        middle_layout.setSpacing(1)
        
        # margin around the widget
        middle_layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(middle_layout)

        middle_layout.addWidget(self.getWidgetTitle(sizeRate))
        middle_layout.addWidget(QHLine())
        middle_layout.addWidget(self.getWidgetOneLineInfo(sizeRate))
        middle_layout.addWidget(QLabel("general"))
        return widget         

    # --------------------------------------------
    # ---------------- Title ---------------------
    # --------------------------------------------
    def getWidgetTitle(self, sizeRate):
        title_layout = QHBoxLayout()
        title_layout.setAlignment(Qt.AlignLeft)
        
        # space between the three grids
        title_layout.setSpacing(1)
        
        # margin around the widget
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(title_layout)

        #
        # Icon
        #
        iconFileName = TITLE_ICON_PREFIX + "-" + self.getFolderType() + "-" + self.control.getMedia() + "-" + self.control.getCategory() + "." + TITLE_ICON_EXTENSION
        pathToFile = resource_filename(__name__, os.path.join(TITLE_ICON_FOLDER, iconFileName))       
        pixmap = QPixmap( pathToFile )

        if pixmap.isNull():            
            smaller_pixmap = QPixmap(TITLE_ICON_HEIGHT * sizeRate, TITLE_ICON_HEIGHT * sizeRate)
            smaller_pixmap.fill(QColor(self.getBackgroundColor()))
        else:
            smaller_pixmap = pixmap.scaledToWidth(TITLE_ICON_HEIGHT * sizeRate)
   
        iconWidget = QLabel()
        iconWidget.setPixmap(smaller_pixmap)

        title_layout.addWidget(iconWidget)

        #
        # Title
        #
        titleWidget = QLabel(self.titles.getTranslatedTitle())
        titleWidget.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate * 1.8, weight=QFont.Bold))

        title_layout.addWidget(titleWidget)
        return widget                 
        
        
    # --------------------------------------------
    # ----------- OneLineInfo -----------------
    # --------------------------------------------
    def getWidgetOneLineInfo(self, sizeRate):
                
        layout = QGridLayout()
        
        layout.setSpacing(1)
        
        layout.setContentsMargins(0, 0, 0, 0)

        widget = QWidget()
        #widget.setStyleSheet('background: ' + self.getBackgroundColor())
        widget.setLayout(layout)
        widget.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Normal))

        layout.addWidget(self.getWidgetOneLineInfoYear(sizeRate), 0, 0)

        layout.addWidget(self.getWidgetOneLineInfoLength(sizeRate), 0, 1)
        
        layout.addWidget(self.getWidgetOneLineInfoCountries(sizeRate), 0, 2)
        
        layout.addWidget(self.getWidgetOneLineInfoSounds(sizeRate), 0, 3)
        
        layout.addWidget(self.getHtmlOneLineInfoSubs(sizeRate), 0, 4)
        
        if layout.sizeHint().height() > 0:
            layout.addWidget(QHLine(), 1, 0, 1, 5)

        return widget
    
    def getWidgetOneLineInfoYear(self, sizeRate):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)        
        layout.setSpacing(1)        
        layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(layout)
        
        if self.general.getYear():

            key_label = QLabel(_('title_year')  + ": ")
            layout.addWidget(key_label)
        
            value_label = QLabel(self.general.getYear())
            value_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Bold))
            layout.addWidget(value_label)
        
        return widget
        
    def getWidgetOneLineInfoLength(self, sizeRate):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)        
        layout.setSpacing(1)        
        layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(layout)
        
        if self.general.getLength():

            key_label = QLabel(_('title_length')  + ": ")
            layout.addWidget(key_label)
        
            value_label = QLabel(self.general.getLength())
            value_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Bold))
            layout.addWidget(value_label)
        
        return widget
    
        
    def getWidgetOneLineInfoCountries(self, sizeRate):
        country_list = ", ".join( [ _("country_" + c) for c in self.general.getCountries()])
        
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)        
        layout.setSpacing(1)        
        layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(layout)
        
        if country_list:

            key_label = QLabel(_('title_country')  + ": ")
            layout.addWidget(key_label)
        
            value_label = QLabel(country_list)
            value_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Bold))
            layout.addWidget(value_label)
        
        return widget
        
    def getWidgetOneLineInfoSounds(self, sizeRate):
        sound_list = ", ".join( [ _("lang_" + c) for c in self.general.getSounds()])        
        
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)        
        layout.setSpacing(1)        
        layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(layout)
        
        if sound_list:

            key_label = QLabel( _('title_sound')  + ": ")
            layout.addWidget(key_label)
        
            value_label = QLabel(sound_list)
            value_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Bold))
            layout.addWidget(value_label)
        
        return widget
        
    def getHtmlOneLineInfoSubs(self, sizeRate):
        sub_list = ", ".join( [ _("lang_" + c) for c in self.general.getSubs()])
        
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)        
        layout.setSpacing(1)        
        layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(layout)
        
        if sub_list:

            key_label = QLabel( _('title_sub')  + ": ")
            layout.addWidget(key_label)
        
            value_label = QLabel(sub_list)
            value_label.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * sizeRate, weight=QFont.Bold))
            layout.addWidget(value_label)
        
        return widget
 
        
    # --------------------------------------------
    # --------------------------------------------
    # --------------- WIDGET -------------------
    # --------------------------------------------
    # --------------------------------------------
    def getWidget(self, sizeRate):

        # layout of this widget => three columns
        grid_layout = QGridLayout()
        
        # space between the three grids
        grid_layout.setSpacing(1)
        
        # margin around the widget
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        # stretch out the middle part
        grid_layout.setColumnStretch(1, 1)

        widget = QWidget()
        widget.setStyleSheet('background: ' + self.getBackgroundColor())
        widget.setLayout(grid_layout)
        
        label_vege = QLabel("vege")
        label_vege.setStyleSheet('background:yellow')                
        
        grid_layout.addWidget(self.getWidgetImage(sizeRate), 0, 0)
        grid_layout.addWidget(self.getWidgetMiddleText(sizeRate), 0, 1)
        grid_layout.addWidget(label_vege, 0, 2)
        
        return widget