import pygame


IMAGES = {

    "WARNING": [
        {
            "type":"image",
            "id": "0",
            "path": "./assets/sprites/intro/game_made_by.png",
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
            "type":"image",
            "id": "0",
            "path": "./assets/sprites/CustomNight/CustomNightBackground.png",
            "alpha": 255,
            "x": 0,
            "y": 0,
            "trigger": False,
            "fullscreen": True,
            "subid": None
        },

        {
            "type":"image",
            "id": "CN",
            "path": "./assets/sprites/CustomNight/UI/Portraits/CustomIndicator.png",
            "alpha":255,
            "x":90,
            "y":200,
            "trigger":False,
            "fullscreen":False,
            "subid":None
        },

        {
            "type":"image",
            "id":"CN",
            "path":"./assets/sprites/CustomNight/UI/Portraits/Maurello_Portrait.png",
            "alpha":255,
            "x":100,
            "y":238,
            "trigger":False,
            "fullscreen":False,
            "subid":"MaurelloPortrait",
            "size":(125,125)
        },

        {
            "type":"image",
            "id":"CN",
            "path":"./assets/sprites/UI/left1.png",
            "alpha":255,
            "x":100,
            "y":368,
            "trigger":True,
            "fullscreen":False,
            "subid":"MaurelloMinusAi"
        },

        {
            "type":"image",
            "id":"CN",
            "path":"./assets/sprites/UI/right1.png",
            "alpha":255,
            "x":191,
            "y":368,
            "trigger":True,
            "fullscreen":False,
            "subid":"MaurelloAddAi"
        },

        # ...el resto exactamente igual...

        {
            "type":"image",
            "id":"GradientMask",
            "path":"./assets/sprites/CustomNight/BG_Fade.png",
            "alpha":255,
            "x":0,
            "y":0,
            "trigger":False,
            "fullscreen":True,
            "subid":None
        },

        {
            "type":"image",
            "id":"Config",
            "path":"./assets/sprites/CustomNight/UI/settings.png",
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
            "type":"image",
            "id":"1",
            "path":"./assets/sprites/BlipAnim/01.png",
            "alpha":255,
            "x":0,
            "y":0,
            "trigger":False,
            "fullscreen":False,
            "subid":None
        },

        {
            "type":"image",
            "id":"2",
            "path":"./assets/sprites/BlipAnim/05.png",
            "alpha":0,
            "x":0,
            "y":0,
            "trigger":False,
            "fullscreen":False,
            "subid":None
        },

        {
            "type":"image",
            "id":"3",
            "path":"./assets/sprites/BlipAnim/09.png",
            "alpha":0,
            "x":0,
            "y":0,
            "trigger":False,
            "fullscreen":False,
            "subid":None
        },

        {
            "type":"image",
            "id":"Controls",
            "path":"./assets/sprites/Alternative Controls.png",
            "alpha":0,
            "x":227,
            "y":0,
            "trigger":False,
            "fullscreen":False,
            "subid":None,
            "size":(827,620)
        }

    ],

    "INGAME_COMPACTOFFICE":[

        {
            "type":"image",
            "id":"background",
            "path":"./assets/sprites/CompactOffice/Office.png",
            "alpha":255,
            "x":0,
            "y":0,
            "trigger":False,
            "fullscreen":True,
            "subid":None
        },

        {   
            "type":"image",
            "id":"LeftDoor",
            "path":"./assets/sprites/Mechanics/Doors/ClosetDoor720.png",
            "alpha":0,
            "x":0,
            "y":0,
            "trigger":False,
            "fullscreen":False,
            "subid":"open"
        },

        {
            "type":"image",
            "id":"RightDoor",
            "path":"./assets/sprites/Mechanics/Doors/Door720p.png",
            "alpha":0,
            "x":1055,
            "y":0,
            "trigger":True,
            "fullscreen":False,
            "subid":"open"
        },

        {   
            "type":"image",
            "id":"LeftButtonbg",
            "path":"./assets/sprites/Mechanics/Buttons/exclusive-button.png",
            "alpha":255,
            "x":306,
            "y":236,
            "trigger":False,
            "fullscreen":False,
            "subid":None
        },

        {   
            "type":"image",
            "id":"LeftButton",
            "path":"./assets/sprites/Mechanics/Buttons/Doors-Button.png",
            "alpha":255,
            "x":322,
            "y":390,
            "trigger":True,
            "fullscreen":False,
            "subid":"off"
        },

        {
            "type":"image",
            "id":"RightButton",
            "path":"./assets/sprites/Mechanics/Buttons/Doors-Button.png",
            "alpha":255,
            "x":736,
            "y":390,
            "trigger":True,
            "fullscreen":False,
            "subid":"off"
        },

        {
            "type":"animation",
            "id":"Desk",
            "folder":"./assets/animations/DeskFan",
            "alpha":255,
            "trigger":False,
            "x":265,
            "y":340,
            "fullscreen":False,
            "subid":None,
            "fps": 20,
            "loop": True,
            "size":(750,384),
        },

        {
            "type":"image",
            "id":"CameraBar",
            "path":"./assets/sprites/Mechanics/Buttons/Monitor Button.png",
            "alpha":175,
            "x":500,
            "y":644,
            "trigger":True,
            "fullscreen":False,
            "subid":None
        },

        {
            "type":"image",
            "id":"MaskBar",
            "path":"./assets/sprites/Mechanics/Buttons/Mask Button.png",
            "alpha":175,
            "x":500,
            "y":20,
            "trigger":False,
            "fullscreen":False,
            "subid":None
        },

        {
            "type":"animation",
            "id":"Monitor",
            "folder":"./assets/animations/CameraPanel",
            "alpha":255,
            "trigger":False,
            "x":0,
            "y":0,
            "fullscreen":False,
            "subid":None,
            "fps": 60,
            "loop": False
        },

        {
            "type":"image",
            "id":"PowerContainer",
            "path":"./assets/sprites/Mechanics/PowerUsage/power_usage_container.png",
            "alpha":255,
            "x":38,
            "y":639,
            "trigger":False,
            "fullscreen":False,
            "subid":None
        },

        {
            "type":"image",
            "id":"PowerProgress",
            "path":"./assets/sprites/Mechanics/PowerUsage/power_usage_progression_1.png",
            "alpha":255,
            "x":38,
            "y":639,
            "trigger":False,
            "fullscreen":False,
            "subid":None
        },

        {
            "type":"image",
            "id":"fadein",
            "path":"./assets/sprites/onepixel.png",
            "alpha":255,
            "x":0,
            "y":0,
            "trigger":False,
            "fullscreen":True,
            "subid":None
        }

    ]


}