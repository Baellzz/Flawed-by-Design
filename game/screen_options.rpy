# game/screen_options.rpy
# Экран настроек для Flawed by Design

# === Трансформация для кнопок ===
transform btn_hover_effect:
    on idle:
        matrixcolor TintMatrix("#ffffff")
    on hover:
        linear 0.1 matrixcolor TintMatrix("#ffb3c6")

# === Стили ===
style custom_slider is slider:
    left_bar Frame("images/menu/options/slider_fill.png", 20, 0)
    right_bar Frame("images/menu/options/slider_bar.png", 20, 0)
    thumb "images/menu/options/slider_knob_idle.png"
    thumb_offset 25
    xysize (450, 40)

style invisible_button is button:
    background None
    padding (0, 0)


screen preferences():
    tag menu

    key "K_ESCAPE" action Return()

    add "images/menu/options/background.png":
        xysize (1920, 1080)

    # --- Кнопка Назад (Текстовая) ---
    textbutton "Back":
        action Return()
        xpos 100
        ypos 930
        text_size 36
        text_color "#ffffff"
        text_hover_color "#ffb3c6"
        text_outlines [(3, "#00000080", 0, 0)]

    # ==========================================
    # ЛЕВАЯ КОЛОНКА
    # ==========================================

    vbox:
        xpos 260
        ypos 420
        spacing 15

        button:
            style "invisible_button"
            action Preference("display", "window")
            at btn_hover_effect
            add "images/menu/options/window.png":
                xysize (220, 60)

        button:
            style "invisible_button"
            action Preference("display", "fullscreen")
            at btn_hover_effect
            add "images/menu/options/fullscreen.png":
                xysize (220, 60)

    vbox:
        xpos 310
        ypos 720
        bar value Preference("text speed") style "custom_slider"


    # ==========================================
    # ПРАВАЯ КОЛОНКА
    # ==========================================

    vbox:
        xpos 955
        ypos 430
        bar value Preference("music volume") style "custom_slider"

    vbox:
        xpos 955
        ypos 600
        bar value Preference("sound volume") style "custom_slider"

    hbox:
        xpos 960
        ypos 755
        spacing 30

        button:
            style "invisible_button"
            action Language("english")
            at btn_hover_effect
            add "images/menu/options/eng.png":
                xysize (150, 60)

        button:
            style "invisible_button"
            action Language("russian")
            at btn_hover_effect
            add "images/menu/options/rus.png":
                xysize (150, 60)