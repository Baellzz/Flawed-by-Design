# game/screens_custom.rpy
# Кастомное меню-доска для Flawed by Design

# Запуск музыки
init python:
    def ensure_menu_music():
        # Проверяем, играет ли ИМЕННО музыка меню
        if renpy.music.get_playing("music") != "audio/music/menu.mp3":
            renpy.music.play("audio/music/menu.mp3", channel="music", loop=True, fadein=1.5)

# --- Трансформации для кнопок ---

transform button_lively(base_angle=0, zoom=0.15):
    anchor (0.5, 0.5)
    rotate_pad False
    transform_anchor True
    zoom zoom
    
    # Базовое состояние (чтобы кнопки не телепортировались при загрузке меню)
    xoffset 0
    yoffset 0
    rotate base_angle
    
    on idle:
        ease 0.25 xoffset 0 yoffset 0 rotate base_angle
    on hover:
        # Убрали pause, чтобы анимация была плавной сразу
        ease 0.20 xoffset 12 yoffset 8 rotate (base_angle + 2)

transform button_jiggle(base_angle=0, zoom=0.15):
    anchor (0.5, 0.5)
    rotate_pad False
    transform_anchor True
    zoom zoom
    
    # Базовое состояние
    rotate base_angle
    
    on idle:
        rotate base_angle
    on hover:
        # Убрали pause
        block:
            linear 0.12 rotate (base_angle + 0.7)
            linear 0.12 rotate (base_angle - 0.7)
            repeat


screen main_menu():
    tag menu

    # ESC открывает настройки
    key "K_ESCAPE" action ShowMenu("preferences")

    # === МУЗЫКА МЕНЮ ===
    on "show" action Function(ensure_menu_music)
    on "replace" action Function(ensure_menu_music)
    on "hide" action Stop("music", fadeout=1.5)

    # === ФОН ===
    add "images/menu/menu_main/menu_background.png"

    # === ЛЕВАЯ КОЛОНКА ===

    imagebutton:
        idle "images/menu/menu_main/start.png"
        hover "images/menu/menu_main/start.png"
        action Start()
        xpos 390 ypos 236
        at button_lively(-3, zoom=0.13)

    imagebutton:
        idle "images/menu/menu_main/continue.png"
        hover "images/menu/menu_main/continue.png"
        action If(renpy.newest_slot() is not None, QuickLoad(), ShowMenu("load"))
        sensitive True
        xpos 380 ypos 349
        at button_lively(2, zoom=0.14)

    imagebutton:
        idle "images/menu/menu_main/load.png"
        hover "images/menu/menu_main/load.png"
        action ShowMenu("load")
        xpos 395 ypos 483
        at button_lively(-2, zoom=0.14)

    imagebutton:
        idle "images/menu/menu_main/options.png"
        hover "images/menu/menu_main/options.png"
        action ShowMenu("preferences")
        xpos 375 ypos 612
        at button_lively(3, zoom=0.14)

    imagebutton:
        idle "images/menu/menu_main/patreon.png"
        hover "images/menu/menu_main/patreon.png"
        action NullAction()
        xpos 385 ypos 790
        at button_jiggle(-3, zoom=0.15)

    # === ПРАВАЯ КОЛОНКА ===

    imagebutton:
        idle "images/menu/menu_main/gallery.png"
        hover "images/menu/menu_main/gallery.png"
        action ShowMenu("gallery")
        xpos 1331 ypos 575
        at button_jiggle(2, zoom=0.23)

    imagebutton:
        idle "images/menu/menu_main/discord.png"
        hover "images/menu/menu_main/discord.png"
        action NullAction()
        xpos 1360 ypos 810
        at button_jiggle(-2, zoom=0.16)