## Основное ####################################################################
define config.name = _("Flawed by Design")
define gui.show_name = True
define config.version = "1.0"
define gui.about = _p("")
define build.name = "FlawedbyDesign"

## Звуки и музыка ##############################################################
define config.has_sound = True
define config.has_music = True
define config.has_voice = True

## Переходы ####################################################################
default preferences.transitions = True
define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.intra_transition = dissolve
define config.after_load_transition = None
define config.end_game_transition = None

## Управление окнами ###########################################################
define config.window = "auto"
define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)

## Стандартные настройки #######################################################
define config.default_text_cps = 40
default preferences.afm_time = 3
default preferences.afm_after_click = True

## Директория сохранений #######################################################
define config.save_directory = "School_V1-1790528331"

## Иконка ######################################################################
define config.window_icon = "gui/window_icon.png"

## Настройка Дистрибутива ######################################################
init python:
    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)
    build.documentation('*.html')
    build.documentation('*.txt')

## Настройки отображения и аудио ###############################################
define config.default_fullscreen = True
define config.gl_resize = False
define config.gl_clear_color = "#000000"
define config.gl2 = True

default preferences.gl_powersave = False
default preferences.audio_when_unfocused = True
default preferences.audio_when_minimized = True

## Включаем пропуск невиданного текста для работы SKIP
default preferences.skip_unseen = True

## Принудительно меняем шрифт для диалогов, имен и всего интерфейса
define gui.text_font = "fonts/manga.ttf"
define gui.name_text_font = "fonts/manga.ttf"
define gui.interface_text_font = "fonts/manga.ttf"