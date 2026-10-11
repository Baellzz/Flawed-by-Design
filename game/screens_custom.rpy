# game/screens_custom.rpy
# Кастомное меню-доска для School_V1

# --- Трансформации для "живых" кнопок ---

transform button_lively(base_angle=0, zoom=0.15):
    anchor (0.5, 0.5)
    rotate_pad True
    transform_anchor True
    zoom zoom
    on idle:
        ease 0.25 xoffset 0 yoffset 0 rotate base_angle
    on hover:
        ease 0.20 xoffset 12 yoffset 8 rotate (base_angle + 2)

transform button_jiggle(base_angle=0, zoom=0.15):
    anchor (0.5, 0.5)
    rotate_pad True
    transform_anchor True
    zoom zoom
    on idle:
        rotate base_angle
    on hover:
        block:
            linear 0.12 rotate (base_angle + 0.7)
            linear 0.12 rotate (base_angle - 0.7)
            repeat


screen main_menu():
    tag menu

    # ESC открывает настройки
    key "K_ESCAPE" action ShowMenu("preferences")

    # === МУЗЫКА МЕНЮ ===
    on "show" action Play("music", "audio/music/menu.mp3", loop=True, fadein=1.0)
    on "hide" action Stop("music", fadeout=1.5)

    # === ФОН ===
    add "images/menu_background.png"

    # === ЛЕВАЯ КОЛОНКА ===

    imagebutton:
        idle "images/start.png"
        hover "images/start.png"
        action Start()
        xpos 390 ypos 236
        at button_lively(-3, zoom=0.13)

    imagebutton:
        idle "images/continue.png"
        hover "images/continue.png"
        action If(renpy.newest_slot() is not None, QuickLoad(), ShowMenu("load"))
        sensitive True
        xpos 380 ypos 349
        at button_lively(2, zoom=0.14)

    imagebutton:
        idle "images/load.png"
        hover "images/load.png"
        action ShowMenu("load")
        xpos 395 ypos 483
        at button_lively(-2, zoom=0.14)

    imagebutton:
        idle "images/options.png"
        hover "images/options.png"
        action ShowMenu("preferences")
        xpos 375 ypos 612
        at button_lively(3, zoom=0.14)

    imagebutton:
        idle "images/patreon.png"
        hover "images/patreon.png"
        action NullAction()
        xpos 385 ypos 790
        at button_jiggle(-3, zoom=0.15)

    # === ПРАВАЯ КОЛОНКА ===

    imagebutton:
        idle "images/gallery.png"
        hover "images/gallery.png"
        action ShowMenu("gallery")
        xpos 1331 ypos 575
        at button_jiggle(2, zoom=0.23)

    imagebutton:
        idle "images/discord.png"
        hover "images/discord.png"
        action NullAction()
        xpos 1360 ypos 810
        at button_jiggle(-2, zoom=0.16)


# Заглушка экрана галереи
screen gallery():
    tag menu

    add "#1a1a1a"

    text "ГАЛЕРЕЯ" xalign 0.5 ypos 50 size 48 color "#ffffff"
    text "Тут будут картинки, открытые по ходу игры." xalign 0.5 ypos 120 size 20 color "#ffffff80"

    grid 3 2:
        xalign 0.5
        ypos 200
        spacing 20

        for i in range(6):
            frame:
                xsize 200 ysize 200
                background "#ffffff15"
                text "[i+1]" xalign 0.5 yalign 0.5 color "#ffffff40" size 40

    textbutton "Назад":
        action Return()
        xalign 0.5
        ypos 650
        text_size 30
        text_color "#ffffff"