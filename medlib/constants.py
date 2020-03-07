import os
from pathlib import Path
from PyQt5.QtCore import Qt

IMG_WINDOW = "medlib.png"
WIDTH_WINDOW = 1400
HEIGHT_WINDOW = 700

LINK_TILE_FONT_SIZE = 25
LINK_TILE_FONT_TYPE = "Comic Sans MS"

PANEL_HEIGHT  = 300
PANEL_FONT_SIZE = 10
PANEL_FONT_TYPE = "Comic Sans MS"

CARD_IMAGE_DEFAULT_FOLDER = "images"
CARD_IMAGE_DEFAULT_NAME = "default"
CARD_IMAGE_DEFAULT_EXTENSION = "jpg"

TITLE_ICON_FOLDER = "images"
TITLE_ICON_PREFIX = "media"
TITLE_ICON_EXTENSION = 'png'
TITLE_ICON_HEIGHT = 35

CLASSIFICATION_ICON_FOLDER = "images"
CLASSIFICATION_ICON_PREFIX = "rating" 
CLASSIFICATION_ICON_EXTENSION = "png"
CLASSIFICATION_ICON_FAVORITE_TAG = 'favorite'
CLASSIFICATION_ICON_NEW = 'new'
CLASSIFICATION_ICON_TAG_ADD = 'tag-add'
CLASSIFICATION_ICON_TAG_DELETE = 'tag-delete'
CLASSIFICATION_ICON_SIZE = 25

CLASSIFICATION_TAG_FIELD_BACKGROUND_COLOR = "#f7bb07"
CLASSIFICATION_RATE_FIELD_BACKGROUND_COLOR = "#f7bb07"

STORAGE_BACKGROUND_COLOR = "#b3d4c9"
COLLECTOR_BACKGROUND_COLOR = "#71a49b"

ON = "on"
OFF = "off"

FOLDER_CONFIG = '.medlib'
PATH_HOME = str(Path.home())
PATH_FOLDER_CONFIG = os.path.join(PATH_HOME, FOLDER_CONFIG)

MAIN_BACKGROUND_COLOR = "#73948d"
CARDHOLDER_BACKGROUND_COLOR = "#3f6b61"
CARD_BORDER_NORMAL_BACKGROUND_COLOR = "#0e997a"
CARD_BORDER_FOCUSED_BACKGROUND_COLOR = "#00ff00"

RADIUS_CARDHOLDER = 10

CONTROL_BACKGROUND_COLOR = Qt.lightGray
CONTROL_IMG_SIZE = 32
CONTROL_IMG_FOLDER = "images"
CONTROL_IMG_EXTENTION = "png"
CONTROL_IMG_BACK_BUTTON = "back-button"
CONTROL_IMG_HIERARCHY_BUTTON = "hierarchy-button"
CONTROL_IMG_PLAY_BUTTON = "play-button"
CONTROL_IMG_STOP_BUTTON = "stop-button"
