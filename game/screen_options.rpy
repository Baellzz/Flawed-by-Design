# game/screen_options.rpy
# Кастомный экран настроек для Flawed by Design

# === Трансформации ===
transform text_btn_effect:
    on idle:
        zoom 1.0
        matrixcolor TintMatrix("#ffffff")
    on hover:
        linear 0.1 zoom 1.05 matrixcolor TintMatrix("#ffb3c6")

transform text_color_effect:
    on idle:
        matrixcolor TintMatrix("#ffffff")
    on hover:
        linear 0.1 matrixcolor TintMatrix("#ffb3c6")

# === Стили ===
style custom_slider is slider:
    left_bar Frame("images/menu/Options/slider_fill.png", 20, 0)
    right_bar Frame("images/menu/Options/slider_bar.png", 20, 0)
    thumb "images/menu/Options/slider_knob_idle.png"
    thumb_offset 25
    xysize (500, 50)

style invisible_button is button:
    background None
    padding (0, 0)


screen preferences():
    tag menu
    
    key "K_ESCAPE" action Return()
    
    # Переменные для наведения на слайдеры
    default ts_hover = False
    default mv_hover = False
    default sv_hover = False

    add "images/menu/Options/background_options.png":
        xysize (1920, 1080)

    imagebutton:
        idle "images/menu/gallery/back_gallery.png"
        hover "images/menu/gallery/back_gallery.png"
        action Return()
        xpos 100
        ypos 950
        xysize (180, 60)

    # ==========================================
    # ЛЕВАЯ КОЛОНКА
    # ==========================================

    fixed:
        xpos 120
        ypos 440

        button:
            style "invisible_button"
            action Preference("display", "window")
            at text_btn_effect 
            xpos 0
            ypos 0
            add "images/menu/Options/window.png":
                xysize (310, 90)
        
        button:
            style "invisible_button"
            action Preference("display", "fullscreen")
            at text_btn_effect 
            xpos 0
            ypos 120 
            add "images/menu/Options/fullscreen.png":
                xysize (310, 90)

    # --- Скорость текста ---
    vbox:
        xpos 235
        ypos 890
        
        # add "images/menu/Options/text_speed.png":
        #    ypos -90
        #    xysize (300, 60)
        #    at (text_color_effect if ts_hover else None)

        bar value Preference("text speed") style "custom_slider":
            hovered SetScreenVariable("ts_hover", True)
            unhovered SetScreenVariable("ts_hover", False)


    # ==========================================
    # ПРАВАЯ КОЛОНКА
    # ==========================================

    vbox:
        xpos 1170
        ypos 200
        
        # add "images/menu/Options/music_volume.png":
        #    ypos -80
        #    at (text_color_effect if mv_hover else None)

        bar value Preference("music volume") style "custom_slider":
            hovered SetScreenVariable("mv_hover", True)
            unhovered SetScreenVariable("mv_hover", False)

    vbox:
        xpos 1170
        ypos 460
        
        # add "images/menu/Options/sounds_volume.png":
        #    ypos -80
        #    at (text_color_effect if sv_hover else None)

        bar value Preference("sound volume") style "custom_slider":
            hovered SetScreenVariable("sv_hover", True)
            unhovered SetScreenVariable("sv_hover", False)

    # --- Настройки пропуска (Skip) ---
    vbox:
        xpos 1160 
        ypos 710  
        spacing 33

        # 1. Unseen text
        button:
            xysize (450, 60)
            background None
            hover_background Solid("#ffffff30") 
            action Preference("skip", "toggle")
            hbox:
                spacing 15
                yalign 0.5
                add ("images/menu/Options/checkbox_on.png" if preferences.skip_unseen else "images/menu/Options/checkbox_off.png"):
                    xysize (45, 45)
                    yalign 0.5
                add "images/menu/Options/unseen_text.png":
                    yalign 0.5
                    yoffset -6 
                    xysize (380, 60)
                    at text_color_effect

        # 2. After choices
        button:
            xysize (450, 60)
            background None
            hover_background Solid("#ffffff30") 
            action Preference("after choices", "toggle") 
            hbox:
                spacing 15
                yalign 0.5
                add ("images/menu/Options/checkbox_on.png" if preferences.skip_after_choices else "images/menu/Options/checkbox_off.png"):
                    xysize (45, 45)
                    yalign 0.5
                add "images/menu/Options/after_choices.png":
                    yalign 0.5
                    yoffset -6
                    xysize (380, 60)
                    at text_color_effect

        # 3. Transitions
        button:
            xysize (450, 60)
            background None
            hover_background Solid("#ffffff30") 
            action Preference("transitions", "toggle")
            hbox:
                spacing 15
                yalign 0.5
                add ("images/menu/Options/checkbox_on.png" if preferences.transitions else "images/menu/Options/checkbox_off.png"):
                    xysize (45, 45)
                    yalign 0.5
                add "images/menu/Options/transitions.png":
                    yalign 0.5
                    yoffset -6
                    xysize (380, 60)
                    at text_color_effect