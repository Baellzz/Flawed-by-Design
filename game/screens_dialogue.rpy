# game/screens_dialogue.rpy

default hide_ui = False
default show_log_overlay = False

style say_window:
    background None
    padding (0, 0)

init python:
    renpy.register_shader("vertical.gradient", variables="""
        uniform vec4 u_gradient_color_top;
        uniform vec4 u_gradient_color_bottom;
        uniform vec2 u_model_size;
        varying float v_gradient_done;
        attribute vec4 a_position;
    """,
    vertex_300="""
        v_gradient_done = a_position.y / u_model_size.y;
    """,
    fragment_300="""
        float gradient_done = v_gradient_done;
        gl_FragColor *= mix(u_gradient_color_top, u_gradient_color_bottom, gradient_done);
    """)

transform bottom_gradient:
    shader "vertical.gradient"
    u_gradient_color_top (0.0, 0.0, 0.0, 0.0)
    u_gradient_color_bottom (0.0, 0.0, 0.0, 1.0)

transform top_gradient:
    shader "vertical.gradient"
    u_gradient_color_top (0.0, 0.0, 0.0, 1.0)
    u_gradient_color_bottom (0.0, 0.0, 0.0, 0.0)


# --- 1. Экран диалога ---
screen say(who, what):
    if not hide_ui and not show_log_overlay:
        add Solid("#000000"):
            ypos 700
            xysize (1920, 300)
            at bottom_gradient
        add Solid("#000000"):
            ypos 1000
            xysize (1920, 80)

    window:
        id "window"
        background None
        xfill True
        ypos 900
        ysize 160
        padding (300, 20, 80, 20)

        at transform:
            alpha (0.0 if (hide_ui or show_log_overlay) else 1.0)

        if who is not None:
            hbox:
                spacing 40
                yalign 0.5
                text who id "who":
                    xsize 250
                    size 32
                    color "#ffffff"
                    yalign 0.0
                text what id "what":
                    size 28
                    color "#ffffff"
                    xmaximum 1300
                    yalign 0.0
        else:
            fixed:
                xfill True
                yfill True
                text what id "what":
                    align (0.5, 0.5)
                    text_align 0.5
                    size 28
                    color "#ffffff"
                    xmaximum 1300

    use quick_menu


# --- 2. Верхняя панель ---
screen quick_menu():
    zorder 100

    if not hide_ui:
        hbox:
            xpos 40
            ypos 30
            spacing 25

            textbutton "⚙":
                action ShowMenu()
                text_size 35
                text_color "#ffffff"
                text_hover_color "#ffb3c6"

            textbutton "👁":
                action SetVariable("hide_ui", True)
                text_size 35
                text_color "#ffffff"
                text_hover_color "#ffb3c6"

            textbutton "LOG":
                action If(renpy.get_screen("custom_history"), Hide("custom_history"), Show("custom_history"))
                text_size 24
                text_color ("#ffb3c6" if renpy.get_screen("custom_history") else "#ffffff")
                text_hover_color "#ffb3c6"

        hbox:
            xalign 0.98
            ypos 35
            spacing 25

            textbutton "AUTO":
                action Preference("auto-forward", "toggle")
                text_size 24
                text_color ("#ffb3c6" if preferences.afm_enable else "#ffffff")
                text_hover_color "#ffb3c6"

            textbutton "SKIP":
                action Skip() alternate Skip(fast=True, confirm=True)
                text_size 24
                text_color "#ffffff"
                text_hover_color "#ffb3c6"

    else:
        button:
            xfill True
            yfill True
            background None
            action SetVariable("hide_ui", False)

        key "K_SPACE" action SetVariable("hide_ui", False)
        key "K_RETURN" action SetVariable("hide_ui", False)


# --- 3. Кастомный экран логов ---
screen custom_history():
    modal True
    zorder 90
    predict False

    on "show" action SetVariable("show_log_overlay", True)
    on "hide" action SetVariable("show_log_overlay", False)
    on "replaced" action SetVariable("show_log_overlay", False)

    add Solid("#00000088")

    add Solid("#000000"):
        ypos 0
        xysize (1920, 250)
        at top_gradient
    add Solid("#000000"):
        ypos 830
        xysize (1920, 250)
        at bottom_gradient

    button:
        xfill True
        yfill True
        background None
        action Hide("custom_history")

    key "K_ESCAPE" action Hide("custom_history")

    # ИСПОЛЬЗУЕМ VIEWPORT ВМЕСТО VPGRID
    viewport id "history_vp":
        xpos 150
        ypos 120
        xsize 1580
        ysize 800
        mousewheel True
        draggable True
        # yinitial 1.0 # В viewport это не работает, мы прокрутим вниз через код ниже

        # ВНУТРИ ИСПОЛЬЗУЕМ VBOX
        vbox:
            spacing 40 # Отступ между репликами (можешь менять)

            for h in _history_list:
                $ is_current = (h == _history_list[-1])
                hbox:
                    spacing 20
                    xfill True

                    if h.who:
                        text h.who:
                            xsize 250
                            size 28
                            color ("#ffb3c6" if is_current else "#aaaaaa")
                    else:
                        null width 250

                    # У текста убираем xmaximum, чтобы он сам переносился,
                    # но задаем width для правильного расчета высоты
                    text h.what:
                        xsize 1250
                        size 28
                        color ("#ffb3c6" if is_current else "#ffffff")

    # Ползунок выносим рядом с viewport
    vbar value YScrollValue("history_vp") style "vscrollbar":
        xpos 1750
        ypos 120
        ysize 800
        xsize 12
        unscrollable "hide"


# --- 4. Кастомный экран ввода имени ---
screen input(prompt):
    style_prefix "input"

    add Solid("#000000"):
        ypos 700
        xysize (1920, 300)
        at bottom_gradient

    add Solid("#000000"):
        ypos 1000
        xysize (1920, 80)

    window:
        id "window"
        background None
        xfill True
        ypos 800
        ysize 200

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20

            text prompt:
                size 32
                color "#ffffff"
                xalign 0.5

            input id "input":
                size 36
                color "#ffb3c6"
                xalign 0.5