import json
import os
import copy


SAVE_PATH = "./save/save.json"


DEFAULT_SAVE = {
    "version": "1.0.3.5",

    "progress": {
        "stars": 0,
        "highscore": 0
    },

    "challenges": {
        "challenge_1": False,
        "challenge_2": False,
        "challenge_3": False
    },

    "settings": {
        "fullscreen": False,
        "width": 1280,
        "height": 720
    },

    "statistics": {
        "play_time": 0,
        "total_deaths": 0,
        "total_wins": 0
    },

    "animatronics": {
        "Maurello": {
            "ai": 5,
            "ignoremask": True,
            "jumpscare": [
                "./assets/sfx/Furry.mp3",
                "./assets/animations/Jumpscares/Maurello"
            ],
            "path": [
                {
                    "cam": 3,
                    "spritepath": "./assets/sprites/Animatronics/Maurello/Maurello2.png",
                    "size": (400, 556),
                    "x": 910,
                    "y": 147
                },
                {
                    "cam": 1,
                    "spritepath": "./assets/sprites/Animatronics/Maurello/Maurello-behind.png",
                    "size": (500, 695),
                    "x": 393,
                    "y": 339
                },
                {
                    "cam": 4,
                    "spritepath": "./assets/sprites/Animatronics/Maurello/Maurello4.png",
                    "size": (300, 617),
                    "x": 741,
                    "y": 245
                },
                {
                    "cam": 5,
                    "spritepath": "./assets/sprites/Animatronics/Maurello/Maurello3.png",
                    "size": (600, 834),
                    "x": 599,
                    "y": 226
                },
                {
                    "cam": 4,
                    "spritepath": "./assets/sprites/Animatronics/Maurello/Maurello4.png",
                    "size": (300, 617),
                    "x": 741,
                    "y": 245
                },
                {
                    "cam": 1,
                    "spritepath": "./assets/sprites/Animatronics/Maurello/Maurello-behind.png",
                    "size": (500, 695),
                    "x": 393,
                    "y": 339
                },
                {
                    "cam": 2,
                    "spritepath": "./assets/sprites/Animatronics/Maurello/Maurello5.png",
                    "size": (1400, 1945),
                    "x": -73,
                    "y": 189
                },
                {
                    "cam": "door_right"
		        },
		        {
                    "cam": "office"
		        }
            ]
        },

        "Furry": {
            "ai": 5,
            "ignoremask": True,
            "jumpscare": [
                "./assets/sfx/Furry.mp3"
            ],
            "path": [
                {
                    "cam": 1,
                    "spritepath": "./assets/sprites/Animatronics/Furry/furry_hallway.png",
                    "size": [
                        90,
                        184
                    ],
                    "x": 755,
                    "y": 479
                },
                {
                    "cam": 2,
                    "spritepath": "./assets/sprites/Animatronics/Furry/furry_bedroom.png",
                    "size": [
                        233,
                        237
                    ],
                    "x": 656,
                    "y": 30
                },
                {
                    "cam": 3,
                    "spritepath": "./assets/sprites/Animatronics/Furry/furry_peeking.png",
                    "size": [
                        590,
                        720
                    ],
                    "x": 0,
                    "y": 0
                },
                {
                    "cam": 6,
                    "spritepath": "./assets/sprites/Animatronics/Furry/furry_backyard.png",
                    "size": [
                        242,
                        268
                    ],
                    "x": 207,
                    "y": 299
                },
                {
                    "cam": 11,
                    "spritepath": "./assets/sprites/Animatronics/Furry/furry_insidevent_1.png",
                    "size": [
                        1280,
                        720
                    ],
                    "x": 0,
                    "y": 0
                },
                {
                    "cam": 5,
                    "spritepath": "./assets/sprites/Animatronics/Furry/furry_bath.png",
                    "size": [
                        196,
                        324
                    ],
                    "x": 195,
                    "y": 141
                },
                {
                    "cam": 4,
                    "spritepath": "./assets/sprites/Animatronics/Furry/furry_living.png",
                    "size": [
                        189,
                        223
                    ],
                    "x": 412,
                    "y": 497
                }
            ]
        }
    }
}


SAVE = {}


# =========================================================
# MERGE NORMAL
# =========================================================

def merge_save(save, default):
    """
    Merge normal del save.

    Los datos que ya existen en el save del usuario
    tienen prioridad.

    Solamente se agregan datos nuevos que no existían.
    """

    if not isinstance(save, dict):
        return save

    if not isinstance(default, dict):
        return save

    for key, default_value in default.items():

        # -------------------------------------------------
        # El dato no existe
        # -------------------------------------------------

        if key not in save:

            save[key] = copy.deepcopy(
                default_value
            )

        # -------------------------------------------------
        # Ambos son diccionarios
        # -------------------------------------------------

        elif (
            isinstance(save[key], dict)
            and isinstance(default_value, dict)
        ):

            merge_save(
                save[key],
                default_value
            )

    return save


# =========================================================
# MERGE DE ANIMATRÓNICOS
# =========================================================

def merge_animatronics(save):
    """
    Sincroniza completamente la categoría
    de animatrónicos con DEFAULT_SAVE.

    A diferencia del merge normal, aquí NO se
    conservan los valores antiguos.

    Los animatrónicos son datos internos del juego,
    por lo que DEFAULT_SAVE siempre tiene prioridad.
    """

    save["animatronics"] = copy.deepcopy(
        DEFAULT_SAVE["animatronics"]
    )

    return save


# =========================================================
# CREAR / MIGRAR SAVE
# =========================================================

def create_save():

    os.makedirs(
        os.path.dirname(SAVE_PATH),
        exist_ok=True
    )

    # =====================================================
    # NO EXISTE SAVE
    # =====================================================

    if not os.path.exists(SAVE_PATH):

        with open(
            SAVE_PATH,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                DEFAULT_SAVE,
                f,
                indent=4
            )

        print(
            f"[SAVE] Created new save "
            f"({DEFAULT_SAVE['version']})."
        )

        return


    # =====================================================
    # LEER SAVE EXISTENTE
    # =====================================================

    try:

        with open(
            SAVE_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            old_save = json.load(f)

    except (json.JSONDecodeError, OSError) as error:

        print(
            f"[SAVE] Could not read save: {error}"
        )

        return


    # =====================================================
    # VALIDAR
    # =====================================================

    if not isinstance(old_save, dict):

        print(
            "[SAVE] Invalid save format."
        )

        return


    # =====================================================
    # GUARDAR INFORMACIÓN ORIGINAL
    # =====================================================

    old_version = old_save.get(
        "version",
        "unknown"
    )

    original_save = copy.deepcopy(
        old_save
    )


    # =====================================================
    # MERGE NORMAL
    # =====================================================

    merge_save(
        old_save,
        DEFAULT_SAVE
    )


    # =====================================================
    # SINCRONIZAR ANIMATRÓNICOS
    # =====================================================

    merge_animatronics(
        old_save
    )


    # =====================================================
    # ACTUALIZAR VERSIÓN
    # =====================================================

    old_save["version"] = DEFAULT_SAVE["version"]


    # =====================================================
    # COMPROBAR CAMBIOS
    # =====================================================

    if old_save != original_save:

        with open(
            SAVE_PATH,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                old_save,
                f,
                indent=4
            )

        print(
            f"[SAVE] Migrated "
            f"{old_version} -> "
            f"{DEFAULT_SAVE['version']}"
        )

    else:

        print(
            f"[SAVE] Save already up to date "
            f"({old_version})."
        )


# =========================================================
# CARGAR SAVE
# =========================================================

def load_save():

    global SAVE

    create_save()

    try:

        with open(
            SAVE_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            SAVE = json.load(f)

    except (json.JSONDecodeError, OSError) as error:

        print(
            f"[SAVE] Could not load save: {error}"
        )

        SAVE = copy.deepcopy(
            DEFAULT_SAVE
        )

    return SAVE


# =========================================================
# GUARDAR PARTIDA
# =========================================================

def save_game(data):

    os.makedirs(
        os.path.dirname(SAVE_PATH),
        exist_ok=True
    )

    with open(
        SAVE_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )


# =========================================================
# OBTENER DATO
# =========================================================

def get_fromSave(path):

    data = SAVE

    for key in path.split("."):

        data = data[key]

    return data


# =========================================================
# MODIFICAR DATO
# =========================================================

def set_fromSave(path, value):

    data = SAVE

    keys = path.split(".")

    for key in keys[:-1]:

        data = data[key]

    data[keys[-1]] = value