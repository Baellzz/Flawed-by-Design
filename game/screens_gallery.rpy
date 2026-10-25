# game/screens_gallery.rpy
# Кастомная галерея для Flawed by Design
#
# Разметка:
#   левая страница книги  — интерфейс (режим / страницы / назад);
#   правая страница книги — сетка 3x2 из полароидов.
#
# Все координаты и кропы подобраны под фон 1920x1080 из
# game/images/menu/gallery/. Если арт перерисуют — править только
# словари GALLERY_BUTTONS / GALLERY_FRAMES ниже.
#
# ВАЖНО: все размеры в screen language должны быть целыми числами.
# Дробный xysize ломает раскладку кнопок (особенно внутри hbox).

init python:
    GALLERY_DIR = "images/menu/gallery/"

    def find_art(path_base):
        for ext in [".png", ".jpg", ".jpeg", ".webp", ".gif"]:
            if renpy.loadable(path_base + ext):
                return path_base + ext
        return None

    class GalleryArt(object):
        def __init__(self, art_id, path_base, cat, title="", thumb_base=None,
                     unlocked_by_default=False):
            self.id = art_id
            self.img = find_art(path_base)
            self.thumb = find_art(thumb_base) if thumb_base else self.img
            self.cat = cat
            self.title = title
            self.unlocked_by_default = unlocked_by_default
            self.exists = self.img is not None

    GALLERY_ARTS = [
        GalleryArt("art_01", "images/scenes/art01", "sfw", "Жена Марата"),
        GalleryArt("art_02", "images/scenes/art02", "sfw", "Вайфу из Аркнайтс"),
        GalleryArt("art_03", "images/scenes/art03", "sfw", "Жена Такуми Мансуровича"),
        GalleryArt("art_04", "images/scenes/art04", "sfw", "Скибиди"),
        GalleryArt("art_05", "images/scenes/art05", "sfw", "Мой вторник"),
        GalleryArt("art_06", "images/scenes/art06", "sfw", "Причина почему я играю в хср"),
        GalleryArt("art_07", "images/scenes/art07", "sfw", ""),
        GalleryArt("art_08", "images/scenes/art08", "sfw", ""),
        GalleryArt("art_09", "images/scenes/art09", "sfw", ""),
        GalleryArt("art_10", "images/scenes/art10", "sfw", ""),
        GalleryArt("art_11", "images/scenes/art11", "sfw", ""),
        GalleryArt("art_12", "images/scenes/art12", "sfw", ""),
        GalleryArt("art_13", "images/scenes/art13", "sfw", ""),
        GalleryArt("art_14", "images/scenes/art14", "sfw", ""),
        GalleryArt("art_15", "images/scenes/art15", "sfw", ""),
        GalleryArt("art_16", "images/scenes/art16", "sfw", ""),
        GalleryArt("art_17", "images/scenes/art17", "sfw", ""),
        GalleryArt("art_18", "images/scenes/art18", "sfw", ""),
        GalleryArt("art_19", "images/scenes/art19", "sfw", ""),
        GalleryArt("art_20", "images/scenes/art20", "sfw", ""),
        GalleryArt("art_nsfw_01", "images/scenes/nsfw01", "nsfw", "Моя вайфу"),
        GalleryArt("art_nsfw_02", "images/scenes/nsfw02", "nsfw", ""),
        GalleryArt("art_nsfw_03", "images/scenes/nsfw03", "nsfw", ""),
        GalleryArt("art_nsfw_04", "images/scenes/nsfw04", "nsfw", ""),
    ]

    # Пока в сюжете нет вызовов gallery_unlock(), галерея была бы пустой.
    # Этот флаг открывает всё, что реально лежит в images/scenes/ — удобно
    # для сборки и проверки. Для релиза поставить False.
    GALLERY_UNLOCK_ALL = True

    GALLERY_PER_PAGE = 6
    GALLERY_PAGES = 4

    def gallery_unlock(art_id):
        if persistent.unlocked_arts is None:
            persistent.unlocked_arts = []
        if art_id not in persistent.unlocked_arts:
            persistent.unlocked_arts.append(art_id)

    def gallery_is_unlocked(art_id):
        if GALLERY_UNLOCK_ALL:
            return True
        return art_id in (persistent.unlocked_arts or [])

    def gallery_page(cat, page, per_page=GALLERY_PER_PAGE):
        """Шесть слотов страницы. Лишние слоты — None (пустые рамки)."""
        arts = [a for a in GALLERY_ARTS if a.cat == cat and a.exists]
        start = page * per_page
        chunk = arts[start:start + per_page]
        return chunk + [None] * (per_page - len(chunk))

    def gallery_short_title(title, limit=27):
        if not title:
            return ""
        if len(title) > limit:
            return title[:limit - 1].rstrip() + "…"
        return title

    # ------------------------------------------------------------------
    # Геометрия ассетов.
    #
    # Кнопки-надписи нарисованы с большими прозрачными полями, поэтому
    # каждую обрезаем по bbox непрозрачных пикселей и масштабируем по
    # высоте. Кропы: (x, y, width, height) в пикселях исходника.
    # ------------------------------------------------------------------
    GALLERY_BUTTONS = {
        "art":   ("images/menu/gallery/art_gallery.png",   (548,  96, 1166, 531)),
        "nsfw":  ("images/menu/gallery/nsfw_gallery.png",  (306,  57, 1649, 584)),
        "back":  ("images/menu/gallery/back_gallery.png",  (93,  211, 1422, 640)),
        "page1": ("images/menu/gallery/page1_gallery.png", (58,  186, 1460, 710)),
        "page2": ("images/menu/gallery/page2_gallery.png", (56,  205, 1467, 653)),
        "page3": ("images/menu/gallery/page3_gallery.png", (78,  200, 1420, 655)),
        "page4": ("images/menu/gallery/page4_gallery.png", (411, 100, 1384, 567)),
    }

    GALLERY_ICON_HEIGHTS = {
        "art": 30, "nsfw": 30, "back": 30,
        "page1": 42, "page2": 42, "page3": 42, "page4": 42,
    }

    # Фиолетовый оттенок как у надписи «Pages» на фоне.
    # ColorizeMatrix перекрашивает чёрный текст в фиолетовый,
    # оставляя белую обводку белой.
    GALLERY_TINT_SFW = ColorizeMatrix("#8B6F9F", "#ffffff")
    GALLERY_TINT_NSFW = ColorizeMatrix("#C9B3E0", "#ffffff")

    GALLERY_ICONS = {}
    GALLERY_ICONS_NSFW = {}
    GALLERY_ICON_W = {}
    for _key, (_path, _box) in GALLERY_BUTTONS.items():
        _z = float(GALLERY_ICON_HEIGHTS[_key]) / _box[3]
        GALLERY_ICONS[_key] = Transform(_path, crop=_box, zoom=_z,
                                       matrixcolor=GALLERY_TINT_SFW)
        GALLERY_ICONS_NSFW[_key] = Transform(_path, crop=_box, zoom=_z,
                                            matrixcolor=GALLERY_TINT_NSFW)
        # Только целые размеры — иначе кнопки «схлопываются».
        GALLERY_ICON_W[_key] = int(round(_box[2] * _z))

    # ------------------------------------------------------------------
    # Полароиды.
    #
    # active: (путь, bbox самой рамки, bbox прозрачного окна)
    # inactive: (путь, bbox рамки)
    #
    # Ширина полароида фиксирована (190 px), высота считается из рамки.
    # Окно позиционируется в тех же координатах, поэтому арт всегда
    # попадает ровно под прозрачное отверстие.
    # ------------------------------------------------------------------
    GALLERY_FRAME_W = 190

    GALLERY_FRAMES = {
        "sfw": {
            "active": (
                "images/menu/gallery/pollaroid_sfw_active.png",
                (165, 83, 926, 1093),
                (227, 151, 800, 812),
            ),
            "inactive": (
                "images/menu/gallery/pollaroid_sfw_nonactive.png",
                (205, 122, 851, 1000),
            ),
        },
        "nsfw": {
            "active": (
                "images/menu/gallery/pollaroid_nsfw_active.png",
                (111, 67, 1034, 1097),
                (191, 140, 874, 791),
            ),
            "inactive": (
                "images/menu/gallery/pollaroid_nsfw_nonactive.png",
                (109, 118, 1015, 1075),
            ),
        },
    }

    GALLERY_LAYOUT = {}
    for _cat, _data in GALLERY_FRAMES.items():
        _apath, _abox, _win = _data["active"]
        _ipath, _ibox = _data["inactive"]

        _scale = float(GALLERY_FRAME_W) / _abox[2]
        _iscale = float(GALLERY_FRAME_W) / _ibox[2]

        GALLERY_LAYOUT[_cat] = {
            "w": GALLERY_FRAME_W,
            "h": int(round(_abox[3] * _scale)),
            "frame": Transform(_apath, crop=_abox, zoom=_scale),
            "frame_inactive": Transform(_ipath, crop=_ibox, zoom=_iscale),
            "inactive_h": int(round(_ibox[3] * _iscale)),
            "win": (
                int(round((_win[0] - _abox[0]) * _scale)),
                int(round((_win[1] - _abox[1]) * _scale)),
                int(round(_win[2] * _scale)),
                int(round(_win[3] * _scale)),
            ),
        }

    # ------------------------------------------------------------------
    # Подгонка арта под окно рамки.
    #
    # fit "cover"/"contain" в screen language не обрезает картинку,
    # поэтому считаем crop/zoom сами. Так арт никогда не вылезает
    # за пределы полароида.
    # ------------------------------------------------------------------
    def gallery_fit_cover(path, w, h):
        iw, ih = renpy.image_size(path)
        scale = max(float(w) / iw, float(h) / ih)
        cw = max(1, int(round(w / scale)))
        ch = max(1, int(round(h / scale)))
        cx = max(0, (iw - cw) // 2)
        cy = max(0, (ih - ch) // 2)
        return Transform(path, crop=(cx, cy, cw, ch), zoom=scale)

    def gallery_fit_contain(path, w, h):
        iw, ih = renpy.image_size(path)
        scale = min(float(w) / iw, float(h) / ih)
        return Transform(path, zoom=scale)

    for _art in GALLERY_ARTS:
        if not _art.exists:
            continue
        _art.thumbs = {}
        for _cat, _lay in GALLERY_LAYOUT.items():
            _art.thumbs[_cat] = gallery_fit_cover(
                _art.thumb, _lay["win"][2], _lay["win"][3])
        _art.view = gallery_fit_contain(_art.img, 1500, 800)

    # ------------------------------------------------------------------
    # Сетка на правой странице (3 колонки x 2 ряда).
    # ------------------------------------------------------------------
    GALLERY_GRID_X = 1030
    GALLERY_GRID_Y = 220
    GALLERY_CELL_W = 220
    GALLERY_CELL_H = 300

    # Лёгкий «разброс», чтобы страница выглядела как живой альбом.
    GALLERY_ANGLES = (-1.2, 0.8, -0.6, 0.7, -1.0, 1.1)


default persistent.unlocked_arts = []
default persistent.nsfw_enabled = False


# ----------------------------------------------------------------------
# Анимации
# ----------------------------------------------------------------------

transform gallery_tab(active):
    # Текст без «физики»: только мягкое проявление при наведении.
    alpha (1.0 if active else 0.5)
    on idle:
        ease 0.15 alpha (1.0 if active else 0.5)
    on hover:
        ease 0.15 alpha 1.0


transform polaroid_hover(angle=0.0):
    # Деликатный hover: +5% и подъём на 5 px, 0.2 c.
    anchor (0.5, 0.5)
    rotate_pad False
    transform_anchor True
    rotate angle
    zoom 1.0
    yoffset 0
    on idle:
        ease 0.2 zoom 1.0 yoffset 0 rotate angle
    on hover:
        ease 0.2 zoom 1.05 yoffset -5 rotate angle


transform gallery_view_in:
    alpha 0.0
    zoom 0.985
    ease 0.22 alpha 1.0 zoom 1.0


# ----------------------------------------------------------------------
# Экран галереи
# ----------------------------------------------------------------------

screen gallery():
    tag menu

    # Если открыт просмотр — ESC закрывает только его.
    key "K_ESCAPE" action If(renpy.get_screen("gallery_view"),
                            Hide("gallery_view"),
                            Return())

    default cat = "sfw"
    default page = 0

    $ slots = gallery_page(cat, page)
    $ unlocked_here = [a for a in slots
                       if a is not None and gallery_is_unlocked(a.id)]
    $ icons = GALLERY_ICONS if cat == "sfw" else GALLERY_ICONS_NSFW

    # Фон: светлая книга для Art, тёмная — для NSFW.
    add (GALLERY_DIR + ("background_nsfw_gallery.png" if cat == "nsfw"
                        else "background_og_gallery.png")):
        xysize (1920, 1080)

    # ==================================================================
    # ЛЕВАЯ СТРАНИЦА
    # ==================================================================

    # --- Страницы (стопка под надписью «Pages») ---
    vbox:
        xpos 585
        ypos 400
        xanchor 0.5
        spacing 32

        for i in range(GALLERY_PAGES):
            button:
                xysize (120, 50)
                background None
                padding (0, 0)
                action [SetScreenVariable("page", i), With(Dissolve(0.12))]
                at gallery_tab(i == page)
                add icons["page%d" % (i + 1)]:
                    xalign 0.5
                    yalign 0.5

    # --- Режим галереи (под надписью «Gallery mode») ---
    hbox:
        xpos 585
        ypos 800
        xanchor 0.5
        spacing 10

        button:
            xysize (GALLERY_ICON_W["art"] + 16, 40)
            background None
            padding (0, 0)
            action [
                SetScreenVariable("cat", "sfw"),
                SetScreenVariable("page", 0),
                With(Dissolve(0.3)),
            ]
            at gallery_tab(cat == "sfw")
            add icons["art"]:
                xalign 0.5
                yalign 0.5

        button:
            xysize (GALLERY_ICON_W["nsfw"] + 16, 40)
            background None
            padding (0, 0)
            action [
                SetScreenVariable("cat", "nsfw"),
                SetScreenVariable("page", 0),
                With(Dissolve(0.3)),
            ]
            at gallery_tab(cat == "nsfw")
            add icons["nsfw"]:
                xalign 0.5
                yalign 0.5

    # --- Назад (на столе, слева внизу) ---
    button:
        xpos 60
        ypos 968
        xysize (GALLERY_ICON_W["back"] + 16, 40)
        background None
        padding (0, 0)
        action Return()
        add icons["back"]:
            xalign 0.5
            yalign 0.5

    # ==================================================================
    # ПРАВАЯ СТРАНИЦА — ПОЛАРОИДЫ
    # ==================================================================
    $ _lay = GALLERY_LAYOUT[cat]

    for i, art in enumerate(slots):
        $ _col = i % 3
        $ _row = i // 3
        $ _cx = GALLERY_GRID_X + _col * GALLERY_CELL_W + GALLERY_CELL_W // 2
        $ _cy = GALLERY_GRID_Y + _row * GALLERY_CELL_H + GALLERY_CELL_H // 2

        if art is not None and gallery_is_unlocked(art.id):
            button:
                xpos _cx
                ypos _cy
                xysize (GALLERY_FRAME_W, _lay["h"])
                background None
                padding (0, 0)
                action Show("gallery_view",
                            arts=unlocked_here,
                            index=unlocked_here.index(art))
                at polaroid_hover(GALLERY_ANGLES[i])

                # Сам арт — уже обрезан ровно под окно рамки.
                add art.thumbs[cat]:
                    xpos _lay["win"][0]
                    ypos _lay["win"][1]

                # Рамка полароида поверх арта.
                add _lay["frame"]

                if art.title:
                    text gallery_short_title(art.title, 24):
                        xalign 0.5
                        ypos _lay["win"][1] + _lay["win"][3] + 12
                        size 12
                        color ("#e8dcf0" if cat == "nsfw" else "#5b4a63")
                        xmaximum GALLERY_FRAME_W - 24
                        text_align 0.5

        else:
            # Закрытый арт или пустой слот — неактивная рамка.
            fixed:
                xpos _cx
                ypos _cy
                xanchor 0.5
                yanchor 0.5
                xysize (GALLERY_FRAME_W, _lay["h"])
                add _lay["frame_inactive"]:
                    xalign 0.5
                    yalign 0.5


# ----------------------------------------------------------------------
# Просмотр арта на весь экран
# ----------------------------------------------------------------------

screen gallery_view(arts, index):
    modal True
    zorder 100

    default idx = index

    $ art = arts[idx]
    $ total = len(arts)

    key "K_ESCAPE" action Hide("gallery_view")
    key "K_LEFT" action SetScreenVariable("idx", (idx - 1) % total)
    key "K_RIGHT" action SetScreenVariable("idx", (idx + 1) % total)

    # Клик по пустому месту закрывает просмотр.
    button:
        xysize (1920, 1080)
        background None
        padding (0, 0)
        action Hide("gallery_view")

    add "#0a0610ee"

    # Повторяем кнопку уже поверх затемнения.
    button:
        xysize (1920, 1080)
        background None
        padding (0, 0)
        action Hide("gallery_view")

    add art.view:
        xalign 0.5
        yalign 0.42
        at gallery_view_in

    # --- Подпись и счётчик ---
    fixed:
        xalign 0.5
        ypos 932
        xysize (1500, 78)

        add Solid("#120c18cc")

        if art.title:
            text gallery_short_title(art.title, 64):
                xpos 30
                yalign 0.5
                size 26
                color "#f0e6fa"

        text "%d / %d" % (idx + 1, total):
            xpos 1470
            yalign 0.5
            xanchor 1.0
            size 22
            color "#cbb6dd"

    # --- Стрелки перелистывания ---
    if total > 1:
        textbutton "<":
            xpos 46
            yalign 0.42
            background None
            padding (12, 12)
            action SetScreenVariable("idx", (idx - 1) % total)
            text_size 84
            text_color "#f4ecff"
            text_hover_color "#d8b8f0"
            text_outlines [(2, "#00000066", 0, 0)]

        textbutton ">":
            xpos 1874
            yalign 0.42
            xanchor 1.0
            background None
            padding (12, 12)
            action SetScreenVariable("idx", (idx + 1) % total)
            text_size 84
            text_color "#f4ecff"
            text_hover_color "#d8b8f0"
            text_outlines [(2, "#00000066", 0, 0)]

    text "ESC или клик — закрыть":
        xpos 1880
        ypos 30
        xanchor 1.0
        size 18
        color "#cbb6dd99"


