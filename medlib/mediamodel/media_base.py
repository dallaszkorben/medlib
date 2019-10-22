import locale
import os

from pkg_resources import resource_filename

from medlib.constants import *
from medlib.handle_property import _
from builtins import object

from medlib.mediamodel.ini_general import IniGeneral
from medlib.mediamodel.ini_storylines import IniStorylines
from medlib.mediamodel.ini_rating import IniRating

class MediaBase(object):
    """
    This object represents the MediaBase
    """
    PANEL_HEIGHT  = "230"
    PANEL_WIDTH = "500"
    FONT_SIZE = "14"
   
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
                rating        IniRating         represents the [rating] section
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
    # --------------- Image ---------------------
    # --------------------------------------------
    def getHtmlImage(self):
        out = "<img id='main-image' src='file://" + self.getPathOfImage() + "' alt='Needs a default image' width='100%'>"
        return out
        
    # --------------------------------------------
    # ---------------- Title ---------------------
    # --------------------------------------------
    def getHtmlTitle(self):
        iconFileName = TITLE_ICON_PREFIX + "-" + self.getFolderType() + "-" + self.control.getMedia() + "-" + self.control.getCategory() + "." + TITLE_ICON_EXTENSION
        pathToFile = resource_filename(__name__, os.path.join(TITLE_ICON_FOLDER, iconFileName))
        out = "<img height='" + TITLE_ICON_HEIGHT + "' src='file://" + pathToFile + "'> <b>" + self.titles.getTranslatedTitle() + "</b>"
        out += "<hr>"
        return out
    
    # --------------------------------------------
    # ----------- OneLineInfo -----------------
    # --------------------------------------------
    def getHtmlOneLineInfo(self):
        out = ""
        
        out += "<td>" + self.getHtmlOneLineInfoYear() + "</td>" if  self.getHtmlOneLineInfoYear() else ""
        out +="<td>" +  self.getHtmlOneLineInfoLength() + "</td>" if self.getHtmlOneLineInfoLength() else  ""
        out +="<td>" +  self.getHtmlOneLineInfoCountries() + "</td>" if self.getHtmlOneLineInfoCountries() else  ""
        out +="<td>" +  self.getHtmlOneLineInfoSounds() + "</td>" if self.getHtmlOneLineInfoSounds() else  ""
        out +="<td>" +  self.getHtmlOneLineInfoSubs() + "</td>" if self.getHtmlOneLineInfoSubs() else  ""
        
        out = "<table id='content-oneline' width='100%'><tr>" + out + "</tr></table><hr>" if out else ""
        return out
    
    def getHtmlOneLineInfoYear(self):
        return "<b>" + _('title_year')  + ":</b> " + self.general.getYear() if self.general.getYear() else ""
        
    def getHtmlOneLineInfoLength(self):
        return "<b>" + _('title_length')  + ":</b> " + self.general.getLength() if self.general.getLength() else ""
        
    def getHtmlOneLineInfoCountries(self):        
        country_list = ", ".join( [ _("country_" + c) for c in self.general.getCountries()])        
        return "<b>" + _('title_country')  + ":</b> " + country_list if country_list else ""
        
    def getHtmlOneLineInfoSounds(self):
        sound_list = ", ".join( [ _("lang_" + c) for c in self.general.getSounds()])        
        return "<b>" + _('title_sound')  + ":</b> " + sound_list if sound_list else ""
        
    def getHtmlOneLineInfoSubs(self):
        sub_list = ", ".join( [ _("lang_" + c) for c in self.general.getSounds()])        
        return "<b>" + _('title_sub')  + ":</b> " + sub_list if sub_list else ""
        
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
        return "<table  id='content-multiline' >" + out + "</table><hr>" if out else ""
     
    def getHtmlMultilineInfoDirectors(self):
        dir_list = ", ".join(d for d in self.general.getDirectors())
        return "<tr><td valign='top'> <b>" + _('title_director') + ":</b> </td> <td>" + dir_list + "</td></tr>"  if  dir_list else ""
         
    def getHtmlMultilineInfoWriters(self):
        writer_list = ", ".join(d for d in self.general.getWriters())
        return "<tr><td valign='top'> <b>" + _('title_writer') + ":</b> </td> <td>" + writer_list + "</td></tr>"  if  writer_list else ""
         
    def getHtmlMultilineInfoActors(self):
        actor_list = ", ".join(d for d in self.general.getActors())
        return "<tr><td valign='top'> <b>" + _('title_actor') + ":</b> </td> <td>" + actor_list + "</td></tr>"  if  actor_list else ""
     
    def getHtmlMultilineInfoGenres(self):
        genre_list = ", ".join( [ _("genre_" + c) for c in self.general.getGenres()])   
        return "<tr><td valign='top'> <b>" + _('title_genre') + ":</b> </td> <td>" + genre_list + "</td></tr>"  if  genre_list else ""
    
    def getHtmlMultilineInfoThemes(self):
        theme_list = ", ".join( [ _("theme_" + c) for c in self.general.getThemes()])   
        return "<tr><td valign='top'> <b>" + _('title_theme') + ":</b> </td> <td>" + theme_list + "</td></tr>"  if  theme_list else ""
  
    # -------------------------------------------
    # --------------- Storyline -----------------
    # --------------------------------------------
    def getHtmlStoryline(self):
        out = "<table id='content-storyline' width='100%' ><tr><td valign='top'><b>" + _('title_storyline') + ":</b></td><td width='100%' height='100%' valign='top'><div  style='max-height:" + self.__class__.FONT_SIZE + "pt;overflow-y: hidden;'>" + self.storylines.getTranslatedStoryline().replace('\n', '<br>') + "</div></td></tr></table>"
        
        return out
    
    # --------------------------------------------
    # --------------------------------------------
    # --------------- HTML ---------------------
    # --------------------------------------------
    # --------------------------------------------
    def getHtml(self):
        out = "" #<!DOCTYPE html>"
        out += "<html>"
        out += "<head><style>"
        out += "body{"
        out +=     "margin: 0;"        
        out +=     "background-color:" + self.getBackgroundColor() + ";}" 
        out += "table {"
        out +=     "font-size:" + self.__class__.FONT_SIZE + "px;" 
        out +=     "font-family: Comic Sans MS, cursive, sans-serif;}"
        out += "table, th, td{"
        out +=     "margin: 0;" 
        out +=     "padding: 0;" 
        out +=     "border: 1px solid black;}"
        out += "#main-image-td{"
        out +=     "background-color:#000000;}"
        out += "#main-image{"
        out +=      "display: block;"
        out +=      "max-height:" + self.__class__.PANEL_HEIGHT + "px;"
        out +=      "max-width:" + self.__class__.PANEL_HEIGHT + "px;"
        out +=     "background-color:#000000;}"
        out += "#main-title{"
        out +=     "font-size:2.5em;}" 
        out += "hr{"
        out +=     "margin: 0;" 
        out +=     "padding: 0;}"
        out += "</style>"
        
        out += "<script>"
        out += "function changeImageSize(){"
        out +=      "var frame = document.getElementById('main-image-td');"
        out +=      "var image = document.getElementById('main-image');"
        out +=      "var imgRealWidth = image.naturalWidth;"
        out +=      "var imgRealHeight = image.naturalHeight;"
        out +=      "if( imgRealWidth > imgRealHeight){"
        out +=          "image.style.width = frame.clientWidth;"
        out +=          "image.style.height = null;"
        out +=      "}else{"
        out +=          "image.style.height = frame.clientHeight;"
        out +=          "image.style.width = null;"
        out +=      "}"
        out += "}"

        out += "</script>"
        
        out += "</head>"        
        out += "<body onload='changeImageSize()'>"
        out +=   "<table id='main-table' width='100%' height='" + self.__class__.PANEL_HEIGHT + "px'>"
        out +=     "<tr>"

        # Image
        out +=       "<td id='main-image-td' width='"+ self.__class__.PANEL_HEIGHT + "px' height='" + self.__class__.PANEL_HEIGHT + "px' valign='middle' align='middle'>"
        out +=      self.getHtmlImage()
        out +=       "</td>"
        
        # Content
        out +=       "<td valign='top'>"
        out +=         "<table id='content-table' width='100%' height='100%'>"        
        
        # --- Title ---
        out +=           "<tr>"
        out +=             "<td id='main-title'>"
        out +=               self.getHtmlTitle()
        out +=             "</td>"
        out +=           "</tr>"
        
        # --- One-line Info: Year, Length, Country, Sound, Subtitle ---
        out +=           "<tr>"
        out +=             "<td>"
        out +=               self.getHtmlOneLineInfo()
        out +=             "</td>"
        out +=           "</tr>"

        # --- Multi-line Info: Writers, Directors, Actors Genre, Theme ---
        out +=           "<tr>"
        out +=             "<td>"
        out +=               self.getHtmlMultiLineInfo()
        out +=             "</td>"
        out +=           "</tr>"

        # --- Storyline---
        out +=           "<tr height='100%'>"
        out +=             "<td valign='top'>"
        out +=               self.getHtmlStoryline()
        out +=             "</td>"
        out +=           "</tr>"


        out +=         "</table>"        
        out +=       "</td>"
        
        # Rating
        
        out +=     "</tr>"        
        out +=   "</table>"
        out += "</body>"
        out += "</html>"
        return out
        