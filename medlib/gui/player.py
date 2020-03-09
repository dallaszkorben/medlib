import os
import platform
from subprocess import Popen

from medlib.handle_property import config_ini
from medlib.card_ini import CardIni
from PyQt5.QtCore import QThread, pyqtSignal
import signal
import psutil

class PlayerThread(QThread):
    
    startNextPlaying = pyqtSignal(int)
    stopPlaying = pyqtSignal()
    
    __instance = None
    __run = False
    __wait_for_stop = False
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
                    'media-path': - media_path: path to the media
                    'media-type': - media_type: type of the media (video, audio, text, image)
         """
        # If there was NO instance of class yet        
        if cls.__instance is None:
            
            # Create a new instance
            cls.__new__(cls)

        # If it is NOT running
        if not cls.__run:
            
            # Initiate the Object        
            cls.__init__(cls.__instance, list_of_media_to_play)

            # Start to run
            cls.__instance.start()
            
        return cls.__instance

    @classmethod
    def stop(cls):
        """
        Stops play list runnig
        """
        if PlayerThread.__pid:
            os.kill(PlayerThread.__pid, signal.SIGKILL)
        PlayerThread.__wait_for_stop = True
        
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance    

    def __init__(self, list_of_media_to_play):
        QThread.__init__(self)        
        self.list_of_media_to_play = list_of_media_to_play
         
    def run(self):

        PlayerThread.__run = True
        PlayerThread.__wait_for_stop = False

        for actual_media in self.list_of_media_to_play:
            media_index = actual_media['media-index']          
            media_path = actual_media['media-path']
            media_type = actual_media['media-type']            
            PlayerThread.__pid = None            
            
            # XDG handles the media
            # if xdg was used, I can not control the PID, so is is no possible to start the next media when the previous finished
            # for that the pid is None
            if config_ini["use_xdg"] == "y":

                if platform.system() == 'Darwin':                   # macOS
                    Popen(['open', media_path])
                elif platform.system() == 'Windows':                # Windows
                    os.startfile(media_path)
                elif platform.system() == 'Linux':                  # Linux:
                    Popen(['xdg-open', media_path])
                else:                                               # linux 
                    Popen(['xdg-open', media_path])
            
            # The media handled as it configured in config.ini
            else:        
                # try fetch extension of media_file to identify the media_player and media_param
                rematch = CardIni.getMediaFilePatternByMedia(media_type).match(media_path)      
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
                    try:
                        print(media_player, media_path, param_list)
                        process = Popen([media_player, media_path] + param_list)
                        PlayerThread.__pid = process.pid
                        print("pid:", PlayerThread.__pid)

                        # emit an media selection event
                        self.startNextPlaying.emit(media_index)       
                        
                        process.communicate()
                        
                        if PlayerThread.__wait_for_stop:
                            break
#                        print("visszatert")
#                           
#                        pid = process.pid
#
                    except FileNotFoundError as e:
                        print("File Not found:", e)
                else:
                    print("no player was found")            

        self.stopPlaying.emit()            
        PlayerThread.__run = False
