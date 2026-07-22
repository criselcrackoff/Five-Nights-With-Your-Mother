import pygame
comoffice = "./assets/sprites/CompactOffice/Office.png"
cam1 = "./assets/sprites/Mechanics/Cameras/Camera-bg/Hall.png"
cam2 = "./assets/sprites/Mechanics/Cameras/Camera-bg/Bedroom2.png"
cam3 = "./assets/sprites/Mechanics/Cameras/Camera-bg/Bedroom.png"
cam4 = "./assets/sprites/Mechanics/Cameras/Camera-bg/Livingroom.png"
cam5 = "./assets/sprites/Mechanics/Cameras/Camera-bg/Bathroom.png"
unavailable = "./assets/sprites/Mechanics/Cameras/Camera-bg/Disabled.png"
maurello_sprite1 = "./assets/sprites/Animatronics/Maurello/Maurello2.png"
maurello_sprite2 = "./assets/sprites/Animatronics/Maurello/Maurello-behind.png"
cam1off = "./assets/sprites/Mechanics/Cameras/Buttons/Cam-Button-H1.png"
cam1on = "./assets/sprites/Mechanics/Cameras/Buttons/Cam-Button-H1-Selected.png"
cam3off = "./assets/sprites/Mechanics/Cameras/Buttons/Cam-Button-A2.png"
cam3on = "./assets/sprites/Mechanics/Cameras/Buttons/Cam-Button-A2-Selected.png"
cam2off = "./assets/sprites/Mechanics/Cameras/Buttons/Cam-Button-A3.png"
cam2on = "./assets/sprites/Mechanics/Cameras/Buttons/Cam-Button-A3-Selected.png"
cam4off = "./assets/sprites/Mechanics/Cameras/Buttons/Cam-Button-A4.png"
cam4on = "./assets/sprites/Mechanics/Cameras/Buttons/Cam-Button-A4-Selected.png"
cam5off = "./assets/sprites/Mechanics/Cameras/Buttons/Cam-Button-A1.png"
cam5on = "./assets/sprites/Mechanics/Cameras/Buttons/Cam-Button-A1-Selected.png"

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
            "id":"maurellobg",
            "path":"./assets/sprites/CompactOffice/Office.png",
            "alpha":0,
            "x":0,
            "y":0,
            "trigger":False,
            "fullscreen":False,
            "subid":None
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
            "type":"animation",
            "id":"Mask",
            "folder":"./assets/animations/Mask",
            "alpha":255,
            "trigger":False,
            "x":0,
            "y":0,
            "fullscreen":True,
            "subid":None,
            "fps": 60,
            "loop": False
        },

        {
            "type":"animation",
            "id":"Map",
            "folder":"./assets/animations/Map",
            "alpha":0,
            "trigger":False,
            "x":950,
            "y":400,
            "fullscreen":False,
            "subid":None,
            "fps": 1,
            "loop": True
        },

        {
            "type":"image",
            "id":"Cambutton",
            "path":"./assets/sprites/Mechanics/Cameras/Buttons/Cam-Button-H1.png",
            "alpha":0,
            "x":1123,
            "y":618,
            "trigger":True,
            "fullscreen":False,
            "subid":"1",
            "size":(36,22)
        },

        {
            "type":"image",
            "id":"Cambutton",
            "path":"./assets/sprites/Mechanics/Cameras/Buttons/Cam-Button-A3.png",
            "alpha":0,
            "x":1175,
            "y":649,
            "trigger":True,
            "fullscreen":False,
            "subid":"2",
            "size":(36,22)
        },

        {
            "type":"image",
            "id":"Cambutton",
            "path":"./assets/sprites/Mechanics/Cameras/Buttons/Cam-Button-A2.png",
            "alpha":0,
            "x":1173,
            "y":597,
            "trigger":True,
            "fullscreen":False,
            "subid":"3",
            "size":(36,22)
        },

        {
            "type":"image",
            "id":"Cambutton",
            "path":"./assets/sprites/Mechanics/Cameras/Buttons/Cam-Button-A4.png",
            "alpha":0,
            "x":1071,
            "y":552,
            "trigger":True,
            "fullscreen":False,
            "subid":"4",
            "size":(36,22)
        },

        {
            "type":"image",
            "id":"Cambutton",
            "path":"./assets/sprites/Mechanics/Cameras/Buttons/Cam-Button-A1.png",
            "alpha":0,
            "x":1071,
            "y":481,
            "trigger":True,
            "fullscreen":False,
            "subid":"5",
            "size":(36,22)
        },

        {
            "type":"animation",
            "id":"blip",
            "folder":"./assets/animations/Blip",
            "alpha":0,
            "trigger":False,
            "x":0,
            "y":0,
            "fullscreen":True,
            "subid":None,
            "fps": 30,
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