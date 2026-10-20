# --- Объявление фонов и лого (с авто-растяжением на весь экран) ---
image bg black_corridor = Transform("images/backgrounds/black_corridor.png", xysize=(1920, 1080))
image bg home_corridor = Transform("images/backgrounds/home_corridor.png", xysize=(1920, 1080))

# Фон с ЗАКРЫТЫМ письмом (tabble с двумя b)
image bg table_closed = Transform("images/backgrounds/tabble_closed_letter.png", xysize=(1920, 1080))

# Фон с ОТКРЫТЫМ письмом
image bg table_open = Transform("images/backgrounds/table_open_letter.png", xysize=(1920, 1080))

image bg university_entrance = Transform("images/backgrounds/university_entrance.png", xysize=(1920, 1080))

# Логотип (если он слишком большой, можно уменьшить, например до 800x600)
image logo prologue = Transform("images/logo/prologue.png", xysize=(1200, 700))

# --- Объявление персонажей ---
define narr = Character(None, what_color="#ffffff")
default mc_name = "Алекс" 
define mc = Character("[mc_name]", color="#88ccff")
define mc_thought = Character("[mc_name]", what_color="#aaaaaa", what_italic=True, what_size=26)


label start:
    # 1. Старт с черного экрана
    scene black with None  
    
    # Музыка начинает играть очень плавно
    play music "audio/music/prologue.mp3" fadein 4.0
    
    # Принудительная пауза, чтобы игрок не проскипал красивый переход
    $ renpy.pause(1.0, hard=True)
    scene bg black_corridor with Dissolve(2.0)
    $ renpy.pause(1.5, hard=True)
    
    narr "Выпускаясь из школы, молодые люди часто сталкиваются с проблемой: “а что делать дальше?”"
    narr "Выбор, который повлияет на всю жизнь в последствии."
    narr "Сделаешь неверный выбор и будешь всю жизнь работать там, где тебе совсем не место…"
    narr "По крайней мере, так думают некоторые."
    narr "Но точно не ты."
    
    # Отключаем скип
    $ config.skipping = None
    
    # Запрос имени
    $ mc_name = renpy.input("Твое имя...", default="Грант", length=20).strip()
    if not mc_name:
        $ mc_name = "Грант"
        
    narr "[mc_name] не сильно заглядывает в будущее. Пусть все пойдет так, как нужно."
    
    # Переход в коридор дома
    scene bg home_corridor with Dissolve(1.5)
    $ renpy.pause(1.0, hard=True)
    mc "Зевок..."
    
    narr "[mc_name] подавал документы во множество вузов с надеждой на то, что сможет попасть хотя бы куда-нибудь. Нельзя сказать, что он совсем плохо учился, скорее… его это не интересовало. Родители то и дело пихали его в разные места, пытались хоть как-то пристроить в жизни, но все без толку. Пусть все идет своим чередом."
    
    # Переход к письмам
    scene bg table_closed with Dissolve(1.5)
    $ renpy.pause(1.0, hard=True)
    narr "Летние каникулы уже совсем почти закончились, близилось время, когда придется сделать важный выбор… куда же пойти?"
    narr "Среди кучи писем лежало одно сильно выделяющееся, с большой печатью и яркой надписью:"
    
    mc "FLAWED… не может быть. Нет, это ошибка какая-то, наверное перепутали адрес и отослали не туда…"
    
    narr "FLAWED - Основы гуманитарных наук, инженерного дела и дизайна. Звучит просто, но на деле вуз славиться своим уровнем образования, сильный преподавательский состав, идеальная для учеников программа и многое другое. Нет того, кто не мечтал бы попасть в FLAWED."
    
    # Открытое письмо
    scene bg table_open with Dissolve(1.5)
    $ renpy.pause(1.0, hard=True)
    mc_thought "Какого хуя. Тут мое имя… моя фамилия… Не могло же мне настолько сильно повезти…"
    
    narr "Не веря своему счастью, [mc_name] тут же решился поступать именно туда. Сама судьба откликнулась на его нерешительность."
    narr "Но будет ли это хорошим выбором?"
    
    # Логотип
    show logo prologue at truecenter with Dissolve(3.0)
    $ renpy.pause(3.0, hard=True) # Жесткая пауза, чтобы игрок посмотрел логотип
    
    hide logo prologue
    scene black with Dissolve(2.5)
    $ renpy.pause(2.0, hard=True)
    
    # Вход в вуз
    stop music fadeout 3.0
    scene bg university_entrance with Dissolve(3.0)
    $ renpy.pause(1.5, hard=True)
    play music "audio/music/letstarthere.mp3" fadein 3.0
    
    narr "Вот и наступил сентябрь. Начало учебы в самом разгаре."
    narr "Большинство студентов, как и [mc_name] начнут заселяться только сейчас, но есть и те, кто заселился еще летом…"

    return