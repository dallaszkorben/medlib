import os
import platform
import time
from subprocess import Popen

from medlib.handle_property import config_ini, Config
from medlib.card_ini import CardIni
from PyQt5.QtCore import QThread, pyqtSignal
import signal
import psutil
import logging
from medlib.handle_property import config_ini

class PlayerThread(QThread):

#    brakPreviousPlaying = pyqtSignal()
    startNextPlaying = pyqtSignal(int)
    stopPlayingAll = pyqtSignal()
    
    __instance = None
    __run = False
    __stop_continously_play = False
    __pid = None
    
    @classmethod
    def play(cls, list_of_media_to_play):
        """
        Starts to play the play list provided in the parameter
        This method can be invoked from 
            MediaAppendix.QLinkLabelToAppendixMedia or 
            MediaStorage.QLabelWithLinkToMedia or
            ControlButtonHolder 
            
        @control_buttons_holder ControlButtonsHolder object where the "play continously" mode was invoked from ControlButtonHolder 
                    if it is not set, it means that the media was invoked separately (MediaStorage/MediaAppendix).
        @list_of_media_to_play list List of the media to play. The elements are dict
                    'media-path': (list)  - media_path: path to the media
                    'media-type': (string - media_type: type of the media (video, audio, text, image)
         """

        logging.info("Play started")
        
        # It stop anyway
        cls.stop()

        # Set the playing list
        inst = cls.getInstance()
        inst.list_of_media_to_play = list_of_media_to_play

        # Waits until the thread stops. Max 5 sec
        limit = 10
        while cls.__run and limit >= 0:
            time.sleep(0.5)
            limit -= 1
            logging.debug("  Waiting if an existing thread is still running")

        # It starts
        inst.start()
        
    @classmethod
    def getInstance(cls):
        inst = cls.__new__(cls)
#        cls.__init__(inst)     
        return inst        
        
    @classmethod
    def stop(cls):
        """
        Stops play list running
        """
        logging.debug("  >Stop playing list")
        if PlayerThread.__pid:
            try:
                os.kill(PlayerThread.__pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            PlayerThread.__pid = None
        PlayerThread.__stop_continously_play = True
    
    @classmethod
    def isPlaying(cls):
        return cls.__run    
        
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__init__(cls.__instance)
        return cls.__instance
    
#    def __init__(self):
#        QThread.__init__(self)        
         
    def run(self):

        PlayerThread.__run = True
        PlayerThread.__stop_continously_play = False

        logging.info("  Play in loop started")
        for actual_media in self.list_of_media_to_play:
            media_index = actual_media['media-index']          
            media_path = actual_media['media-path']
            media_type = actual_media['media-type']            
            PlayerThread.__pid = None            
            
            # XDG handles the media
            # if xdg was used, I can not control the PID, so is is no possible to start the next media when the previous finished
            # for that the pid is None
            if config_ini["use_xdg"] == "y" and media_path:

                if platform.system() == 'Darwin':                   # macOS
                    Popen(['open', media_path])
                elif platform.system() == 'Windows':                # Windows
                    os.startfile(media_path)
                elif platform.system() == 'Linux':                  # Linux:
                    Popen(['xdg-open', media_path])
                else:                                               # linux 
                    Popen(['xdg-open', media_path])
            
            # The media handled as it configured in config.ini
            elif media_path:        
                # try fetch extension of media_file to identify the media_player and media_param
                rematch = CardIni.getMediaFilePatternByMedia(media_type).match(media_path[0])      
                if rematch:
                    extension = rematch.groups()[0]
                else:
                    extension = ""
            
                # try to find the configuration of media_player and media_param by "media/extension"
                try:
                    media_player = config_ini["player_" + media_type + "_" + extension + "_player"]
                    media_param = config_ini["player_" + media_type + "_" + extension + "_param"]
                # if not, then try to find the configuration only for "media"
                except KeyError:
                    try:
                        media_player = config_ini["player_" + media_type + "_player"]
                        media_param = config_ini["player_" + media_type + "_param"] 
                    except KeyError:
                        media_player = None
                        media_param = ""
                if media_player:
                    param_list = media_param.replace(" ", ",").split(",") if media_param else []
                    
                    #print(type(media_path), media_path)
                    
                    #path_list = media_path.replace(" ", ",").split(",") if media_path else []
                    #path_list = [media_path] if media_path else []
                    path_list = media_path
                    try:                        
                        
#                        print("=============")
#                        print("media_param: ", media_param)
#                        print("media_path:  ", media_path)
#                        print("-------------")
#                        print("param_list:  ", param_list)
#                        print("path_list:   ", path_list)
#                        print("Popoen:      ", [media_player] + param_list + path_list)
#                        print()

                        logging.debug("    " + media_player + " " + media_param + " " + ",".join(media_path))
                        process = Popen([media_player] + param_list + path_list )
                        
                        PlayerThread.__pid = process.pid
                        logging.debug("    pid: " + str(PlayerThread.__pid))

                        # emit an media selection event
                        self.startNextPlaying.emit(media_index)       

                        # Start to play the media                        
                        process.communicate()

                        # if you want to stop continously playing you break the loop
                        if PlayerThread.__stop_continously_play:
                            logging.debug("    Break loop")
                            break

                    except FileNotFoundError as e:
                        logging.error("    File Not found to play: " + media_path)
                else:
                    logging.error("    No Player was found: " + media_player)

        logging.info("Play stopped + emit stopPlayingAll")
        PlayerThread.__run = False
        self.stopPlayingAll.emit()
