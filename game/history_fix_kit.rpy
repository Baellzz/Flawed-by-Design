# game/history_fix_kit.rpy
# ТЕСТОВЫЙ НАБОР для экрана логов (истории) Ren'Py 8.5.x
#
# Как пользоваться:
#   1. Положить файл в game/ (убедись, что старый screens_dialogue.rpy НЕ включён
#      одновременно с этим файлом: оба определяют экран custom_history).
#   2. Менять вариант переключателем hk_variant ниже (1..5).
#   3. В игре показывать экран как обычно: Show("custom_history") / show screen custom_history.
#   4. Результаты фиксировать в TEST_PLAN.md (таблица в конце).
#
# Варианты:
#   1 = контроль (твоя исходная реализация: vpgrid + YScrollValue)
#   2 = зонд: vpgrid + принудительная перестройка детей каждый тик (таймер)
#   3 = viewport-прищепка: внутренний скролл viewport заморожен, контент едет трансформом
#   4 = без viewport: скролл через crop трансформа
#   5 = пагинация (страницы, скролла нет)

define hk_variant = 1

init python:
    import math as _hk_math

    def hk_estimate_height(entries, width=1250, size=28):
        """Грубая оценка высоты колонки записей в пикселях (для вариантов 3-4)."""
        cpl = max(20, int(width / (size * 0.62)))
        total = 0
        for h in entries:
            lines = max(1, _hk_math.ceil(len(h.what or "") / float(cpl)))
            total += lines * int(size * 1.35) + 6
        return total + 24

    def hk_range(entries, view=800):
        return max(1, hk_estimate_height(entries) - view)

    def hk_clip(v, lo, hi):
        return max(lo, min(hi, v))

    def hk_bump(_x=None):
        store.hk_tick += 1

    def hk_goto_bottom():
        store.hk_pos = hk_range(_history_list)

    def hk_goto_last_page(per=16):
        n = len(_history_list)
        pages = max(1, -(-n // per))
        store.hk_page = pages - 1

default hk_pos = 0
default hk_tick = 0
default hk_page = 0

# --- Шейдер градиента (копия твоего, переименована, чтобы не конфликтовать) ---
init python:
    renpy.register_shader("hk.vertical.gradient", variables="""
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

transform hk_bottom_gradient:
    shader "hk.vertical.gradient"
    u_gradient_color_top (0.0, 0.0, 0.0, 0.0)
    u_gradient_color_bottom (0.0, 0.0, 0.0, 1.0)

transform hk_top_gradient:
    shader "hk.vertical.gradient"
    u_gradient_color_top (0.0, 0.0, 0.0, 1.0)
    u_gradient_color_bottom (0.0, 0.0, 0.0, 0.0)

transform hk_offset(pos):
    yoffset pos

transform hk_cropscroll(pos):
    crop (0, int(pos), 1580, 800)

# --- Общий каркас: полупрозрачная подложка + градиенты + закрытие ---
screen hk_frame():
    add Solid("#00000088")
    add Solid("#000000"):
        ypos 0
        xysize (1920, 250)
        at hk_top_gradient
    add Solid("#000000"):
        ypos 830
        xysize (1920, 250)
        at hk_bottom_gradient
    button:
        xfill True
        yfill True
        background None
        action NullAction()
    key "K_ESCAPE" action Hide("custom_history")

# --- Одна запись истории ---
screen hk_entry(h, is_current):
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
        text h.what:
            size 28
            color ("#ffb3c6" if is_current else "#ffffff")
            xmaximum 1250

# --- Диспетчер вариантов (внешнее имя не меняется) ---
screen custom_history():
    use expression ("custom_history_v%d" % hk_variant)

# ============================================================
# ВАРИАНТ 1. Контроль: исходный код (vpgrid + YScrollValue)
# ============================================================
screen custom_history_v1():
    modal True
    zorder 90
    predict False
    use hk_frame
    fixed:
        xpos 150
        ypos 120
        xsize 1600
        ysize 800
        vpgrid id "history_vp":
            cols 1
            xsize 1580
            ysize 800
            mousewheel True
            draggable True
            yinitial 1.0
            for h in _history_list:
                $ is_current = (h == _history_list[-1])
                use hk_entry(h, is_current)
        vbar value YScrollValue("history_vp") style "vscrollbar":
            xpos 1580
            ysize 800
            xsize 12
            unscrollable "hide"

# ============================================================
# ВАРИАНТ 2. Зонд: как контроль, но дети vpgrid перестраиваются
# каждый тик (таймер). Проверяем гипотезу «переиспользование
# текстуры детей viewport'а».
# ============================================================
screen custom_history_v2():
    modal True
    zorder 90
    predict False
    use hk_frame
    timer 0.06 repeat True action Function(hk_bump)
    fixed:
        xpos 150
        ypos 120
        xsize 1600
        ysize 800
        vpgrid id "history_vp":
            cols 1
            xsize 1580
            ysize 800
            mousewheel True
            draggable True
            yinitial 1.0
            null height (hk_tick % 2)
            for h in _history_list:
                $ is_current = (h == _history_list[-1])
                use hk_entry(h, is_current)
        vbar value YScrollValue("history_vp") style "vscrollbar":
            xpos 1580
            ysize 800
            xsize 12
            unscrollable "hide"

# ============================================================
# ВАРИАНТ 3. Viewport-прищепка: viewport только клипует,
# внутренний скролл выключен, контент сдвигаем трансформом.
# ============================================================
screen custom_history_v3():
    modal True
    zorder 90
    predict False
    use hk_frame
    on "show" action Function(hk_goto_bottom)
    $ rng = hk_range(_history_list)
    $ hk_pos = hk_clip(hk_pos, 0, rng)
    fixed:
        xpos 150
        ypos 120
        xsize 1600
        ysize 800
        viewport:
            xsize 1580
            ysize 800
            mousewheel False
            draggable False
            vbox:
                at hk_offset(-hk_pos)
                for h in _history_list:
                    $ is_current = (h == _history_list[-1])
                    use hk_entry(h, is_current)
        vbar value VariableValue("hk_pos", max=rng, step=12) style "vscrollbar":
            xpos 1580
            ysize 800
            xsize 12
        key "wheelup" action SetVariable("hk_pos", hk_clip(hk_pos - 120, 0, rng))
        key "wheeldown" action SetVariable("hk_pos", hk_clip(hk_pos + 120, 0, rng))

# ============================================================
# ВАРИАНТ 4. Без viewport: скролл кропом трансформа.
# ============================================================
screen custom_history_v4():
    modal True
    zorder 90
    predict False
    use hk_frame
    on "show" action Function(hk_goto_bottom)
    $ rng = hk_range(_history_list)
    $ hk_pos = hk_clip(hk_pos, 0, rng)
    fixed:
        xpos 150
        ypos 120
        xsize 1600
        ysize 800
        vbox:
            xsize 1580
            at hk_cropscroll(hk_pos)
            for h in _history_list:
                $ is_current = (h == _history_list[-1])
                use hk_entry(h, is_current)
        vbar value VariableValue("hk_pos", max=rng, step=12) style "vscrollbar":
            xpos 1580
            ysize 800
            xsize 12
        key "wheelup" action SetVariable("hk_pos", hk_clip(hk_pos - 120, 0, rng))
        key "wheeldown" action SetVariable("hk_pos", hk_clip(hk_pos + 120, 0, rng))

# ============================================================
# ВАРИАНТ 5. Пагинация: страницами, без скролла вообще.
# ============================================================
screen custom_history_v5():
    modal True
    zorder 90
    predict False
    use hk_frame
    on "show" action Function(hk_goto_last_page)
    $ per = 16
    $ total = len(_history_list)
    $ pages = max(1, -(-total // per))
    $ hk_page = hk_clip(hk_page, 0, pages - 1)
    $ start = hk_page * per
    fixed:
        xpos 150
        ypos 120
        xsize 1600
        ysize 800
        vbox:
            xsize 1580
            ysize 760
            for h in _history_list[start:start + per]:
                $ is_current = (h == _history_list[-1])
                use hk_entry(h, is_current)
        hbox:
            ypos 760
            xsize 1580
            spacing 20
            xalign 0.5
            textbutton "<":
                action SetVariable("hk_page", hk_clip(hk_page - 1, 0, pages - 1))
                text_size 32
                text_color "#ffffff"
                text_hover_color "#ffb3c6"
            text "%d / %d" % (hk_page + 1, pages):
                size 24
                color "#ffffff"
                yalign 0.5
            textbutton ">":
                action SetVariable("hk_page", hk_clip(hk_page + 1, 0, pages - 1))
                text_size 32
                text_color "#ffffff"
                text_hover_color "#ffb3c6"
        key "wheelup" action SetVariable("hk_page", hk_clip(hk_page - 1, 0, pages - 1))
        key "wheeldown" action SetVariable("hk_page", hk_clip(hk_page + 1, 0, pages - 1))
