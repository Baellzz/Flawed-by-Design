# game/screens_gallery.rpy
# Кастомная галерея для Flawed by Design

init python:
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

    def gallery_filtered(cat):
        unlocked = persistent.unlocked_arts or []
        return [a for a in GALLERY_ARTS
                if (a.id in unlocked or a.unlocked_by_default)
                and (cat == "all" or a.cat == cat)
                and a.exists]

    def gallery_unlock(art_id):
        if persistent.unlocked_arts is None:
            persistent.unlocked_arts = []
        if art_id not in persistent.unlocked_arts:
            persistent.unlocked_arts.append(art_id)

    def gallery_is_unlocked(art_id):
        return art_id in (persistent.unlocked_arts or [])

    # === Физика покачивания для каждого полароида ===
    class PolaroidPhysics(object):
        """Пружина с затуханием. У каждого полароида — свой экземпляр,
        поэтому при наведении на один остальные не реагируют."""
        def __init__(self):
            self.angle = 0.0       # текущий угол
            self.velocity = 0.0    # скорость изменения угла
            self.target = 0.0      # целевой угол (7° при hover, 0° в покое)
            self.last_st = -1.0    # для расчёта dt
            self.started = False

        def step(self, trans, st, at):
            if not self.started:
                self.last_st = st
                self.started = True
            dt = st - self.last_st
            self.last_st = st
            # Защита от первого кадра и от больших dt после пауз
            if dt <= 0 or dt > 0.1:
                dt = 1.0 / 60.0

            stiffness = 150.0
            damping = 12.0
            force = (self.target - self.angle) * stiffness - self.velocity * damping
            self.velocity += force * dt
            self.angle += self.velocity * dt

            # Ограничение угла, чтобы картинка не выходила за края полароида
            if self.angle > 8.0:
                self.angle = 8.0
                self.velocity = 0.0
            elif self.angle < -8.0:
                self.angle = -8.0
                self.velocity = 0.0

            trans.rotate = self.angle
            trans.rotate_pad = False
            trans.transform_anchor = True
            return 0  # пересчитать на следующем кадре

    _physics_cache = {}

    def get_sway(art_id):
        """Transform с уникальным для этого полароида объектом физики."""
        if art_id not in _physics_cache:
            _physics_cache[art_id] = PolaroidPhysics()
        return Transform(function=_physics_cache[art_id].step)

    def sway_hover(art_id):
        """Активировать покачивание у полароида с данным id."""
        if art_id not in _physics_cache:
            _physics_cache[art_id] = PolaroidPhysics()
        _physics_cache[art_id].target = 7.0

    def sway_idle(art_id):
        """Вернуть полароид с данным id в покой."""
        if art_id in _physics_cache:
            _physics_cache[art_id].target = 0.0

default persistent.unlocked_arts = []
default persistent.nsfw_enabled = False


# === Трансформации (осталось только для кнопок страниц) ===

transform faded_page:
    alpha 0.55
    on hover:
        linear 0.15 alpha 1.0
    on idle:
        linear 0.15 alpha 0.55

transform back_btn_size:
    xysize (180, 60)


screen gallery():
    tag menu

    key "K_ESCAPE" action Return()

    default cat = "sfw"
    default page = 0
    $ PER_PAGE = 4
    $ TOTAL_PAGES = 5

    add "images/menu/gallery/background_gallery.png"

    # === ФИЛЬТРЫ ===
    hbox:
        xpos 1250
        ypos 60
        spacing 30
        textbutton "Обычные":
            action [
                SetScreenVariable("cat", "sfw"),
                SetScreenVariable("page", 0),
                With(dissolve)
            ]
            text_size 22
            text_color ("#ff88aa" if cat == "sfw" else "#ffffffcc")
            text_outlines [(2, "#00000080", 0, 0)]
        textbutton "NSFW":
            action [
                SetScreenVariable("cat", "nsfw"),
                SetScreenVariable("page", 0),
                With(dissolve)
            ]
            text_size 22
            text_color ("#ff88aa" if cat == "nsfw" else "#ffffffcc")
            text_outlines [(2, "#00000080", 0, 0)]

    python:
        _arts_all = gallery_filtered(cat)
        _start = page * PER_PAGE
        _page_arts = list(_arts_all[_start:_start + PER_PAGE])
        while len(_page_arts) < PER_PAGE:
            _page_arts.append(None)

    # === КНОПКИ СТРАНИЦ ===
    vbox:
        xpos 100
        ypos 300
        spacing 20
        for p in range(TOTAL_PAGES):
            button:
                xysize (130, 45)
                background None
                action SetScreenVariable("page", p)
                at (None if p == page else faded_page)
                add ("images/menu/gallery/page%d_gallery.png" % (p + 1)):
                    xysize (130, 45)

    # === СЕТКА ПОЛАРОИДОВ ===
    for i in range(PER_PAGE):
        $ art = _page_arts[i]
        $ px = 570 if (i % 2 == 0) else 1000
        $ py = 100 if (i < 2) else 540

        if art is not None:
            button:
                xpos px
                ypos py
                xysize (440, 460)
                background None
                action Show("gallery_view", art=art)
                hovered Function(sway_hover, art.id)
                unhovered Function(sway_idle, art.id)
                at get_sway(art.id)

                add art.thumb:
                    xalign 0.5
                    yalign 0.5
                    fit "fill"
                    xysize (335, 395)

                add "images/menu/gallery/polaroid_gallery_active.png":
                    xalign 0.5
                    yalign 0.5
                    xysize (340, 400)

                if art.title:
                    text art.title:
                        xalign 0.5
                        ypos 372
                        size 22
                        color "#3a2a1a"
                        hover_color "#8a3a3a"
        else:
            button:
                xpos px
                ypos py
                xysize (440, 460)
                background None

                add "images/menu/gallery/polaroid_gallery.png":
                    xalign 0.5
                    yalign 0.5
                    xysize (340, 400)
                    alpha 0.3

    # === КНОПКА НАЗАД ===
    imagebutton:
        idle "images/menu/gallery/back_gallery.png"
        hover "images/menu/gallery/back_gallery.png"
        action Return()
        xpos 130
        ypos 930
        at back_btn_size


# === Просмотр арта ===
screen gallery_view(art):
    modal True
    zorder 100

    key "K_ESCAPE" action Hide("gallery_view")

    add "#000000cc"

    add art.img:
        xalign 0.5
        yalign 0.5
        fit "contain"
        xysize (1600, 900)

    text art.title:
        xalign 0.5
        ypos 30
        size 38
        color "#ffffff"
        outlines [(2, "#00000080", 0, 0)]

    imagebutton:
        idle "images/menu/gallery/back_gallery.png"
        hover "images/menu/gallery/back_gallery.png"
        action Hide("gallery_view")
        xalign 0.5
        ypos 990
        at back_btn_size