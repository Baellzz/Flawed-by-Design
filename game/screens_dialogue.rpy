# game/screens_dialogue.rpy
# Кастомный интерфейс диалогов в стиле Arknights

# Переменные для управления интерфейсом
default hide_ui = False
default show_log_overlay = False

# Явно указываем, что стандартное окно диалогов не имеет фона
style say_window:
    background None
    padding (0, 0)

# --- РЕГИСТРАЦИЯ ШЕЙДЕРА ГРАДИЕНТА (Оставляем для диалогов, но убираем из логов) ---
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

# --- ТРАНСФОРМАЦИИ ДЛЯ ГРАДИЕНТОВ ---
transform bottom_gradient:
    shader "vertical.gradient"
    u_gradient_color_top (0.0, 0.0, 0.0, 0.0)
    u_gradient_color_bottom (0.0, 0.0, 0.0, 1.0)

transform top_gradient:
    shader "vertical.gradient"
    u_gradient_color_top (0.0, 0.0, 0.0, 1.0)
    u_gradient_color_bottom (0.0, 0.0, 0.0, 0.0)

# --- СТИЛЬ СКРОЛЛБАРА ---
style vscrollbar:
    xsize 12
    base_bar Solid("#ffffff30")
    thumb Solid("#cccccc")

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

    if show_log_overlay:
        use custom_history

    if not hide_ui:
        hbox:
            xpos 40
            ypos 30
            spacing 25
            textbutton "⚙" action ShowMenu() text_size 35 text_color "#ffffff" text_hover_color "#ffb3c6"
            textbutton "LOG" action ToggleVariable("show_log_overlay") text_size 24 text_color ("#ffb3c6" if show_log_overlay else "#ffffff") text_hover_color "#ffb3c6"
            textbutton "👁" action SetVariable("hide_ui", True) text_size 35 text_color "#ffffff" text_hover_color "#ffb3c6"

        hbox:
            xalign 0.98
            ypos 35
            spacing 25
            textbutton "AUTO" action Preference("auto-forward", "toggle") text_size 24 text_color ("#ffb3c6" if preferences.afm_enable else "#ffffff") text_hover_color "#ffb3c6"
            textbutton "SKIP" action Skip() alternate Skip(fast=True, confirm=True) text_size 24 text_color "#ffffff" text_hover_color "#ffb3c6"

    else:
        button:
            xfill True
            yfill True
            background None
            action SetVariable("hide_ui", False)
        key "K_SPACE" action SetVariable("hide_ui", False)
        key "K_RETURN" action SetVariable("hide_ui", False)



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