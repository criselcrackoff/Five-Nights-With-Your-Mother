import pygame

IMAGES = {

    "WARNING": [
        {
            "id": "0",
            "path": "./sprites/intro/game_made_by.png",
            "alpha": 0,
            "x": 0,
            "y": 0,
            "trigger": False,
            "fullscreen": True,
            "subid": None
        }
    ],

    "CUSTOM_NIGHT": [

        {
            "id": "0",
            "path": "./sprites/CustomNight/CustomNightBackground.png",
            "alpha": 255,
            "x": 0,
            "y": 0,
            "trigger": False,
            "fullscreen": True,
            "subid": None
        },

        {
            "id": "CN",
            "path": "./sprites/CustomNight/UI/Portraits/CustomIndicator.png",
            "alpha":255,
            "x":90,
            "y":200,
            "trigger":False,
            "fullscreen":False,
            "subid":None
        },

        {
            "id":"CN",
            "path":"./sprites/CustomNight/UI/Portraits/Maurello_Portrait.png",
            "alpha":255,
            "x":100,
            "y":238,
            "trigger":False,
            "fullscreen":False,
            "subid":"MaurelloPortrait",
            "size":(125,125)
        },

        {
            "id":"CN",
            "path":"./sprites/UI/left1.png",
            "alpha":255,
            "x":100,
            "y":368,
            "trigger":True,
            "fullscreen":False,
            "subid":"MaurelloMinusAi"
        },

        {
            "id":"CN",
            "path":"./sprites/UI/right1.png",
            "alpha":255,
            "x":191,
            "y":368,
            "trigger":True,
            "fullscreen":False,
            "subid":"MaurelloAddAi"
        },

        # ...el resto exactamente igual...

        {
            "id":"GradientMask",
            "path":"./sprites/CustomNight/BG_Fade.png",
            "alpha":255,
            "x":0,
            "y":0,
            "trigger":False,
            "fullscreen":True,
            "subid":None
        },

        {
            "id":"Config",
            "path":"./sprites/CustomNight/UI/settings.png",
            "alpha":255,
            "x":-1060,
            "y":0,
            "trigger":False,
            "fullscreen":False,
            "subid":None
        }

    ],

    "LOAD_NIGHT":[

        {
            "id":"1",
            "path":"./sprites/BlipAnim/01.png",
            "alpha":255,
            "x":0,
            "y":0,
            "trigger":False,
            "fullscreen":False,
            "subid":None
        },

        {
            "id":"2",
            "path":"./sprites/BlipAnim/05.png",
            "alpha":0,
            "x":0,
            "y":0,
            "trigger":False,
            "fullscreen":False,
            "subid":None
        },

        {
            "id":"3",
            "path":"./sprites/BlipAnim/09.png",
            "alpha":0,
            "x":0,
            "y":0,
            "trigger":False,
            "fullscreen":False,
            "subid":None
        },

        {
            "id":"Controls",
            "path":"./sprites/Alternative Controls.png",
            "alpha":0,
            "x":227,
            "y":0,
            "trigger":False,
            "fullscreen":False,
            "subid":None,
            "size":(827,620)
        }

    ],

    "INGAME":[

        {
            "id":"office",
            "path":"./sprites/CompactOffice/Office.png",
            "alpha":255,
            "x":0,
            "y":0,
            "trigger":False,
            "fullscreen":True,
            "subid":None
        },

        {
            "id":"CameraBar",
            "path":"./sprites/Mechanics/Buttons/Monitor Button.png",
            "alpha":175,
            "x":500,
            "y":644,
            "trigger":False,
            "fullscreen":False,
            "subid":None
        },

        {
            "id":"MaskBar",
            "path":"./sprites/Mechanics/Buttons/Mask Button.png",
            "alpha":175,
            "x":500,
            "y":20,
            "trigger":False,
            "fullscreen":False,
            "subid":None
        },

        {
            "id":"fadein",
            "path":"./sprites/onepixel.png",
            "alpha":255,
            "x":0,
            "y":0,
            "trigger":False,
            "fullscreen":True,
            "subid":None
        }

    ]

}