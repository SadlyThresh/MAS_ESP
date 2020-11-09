



init -100 python:

    for archive in ['audio','images','scripts','fonts']:
        if not archive in config.archives:
            
            renpy.error("Los archivos de DDLC no fueron encontrados en la carpeta /game. Verifica la instalación e intenta nuevamente.")





init python:
    menu_trans_time = 1

    splash_message_default = _("Este juego es un trabajo fan no oficial, desafiliado al Team Salvato.")
    splash_messages = [
    _("Por favor apoya el Doki Doki Literature Club & Team Salvato."),
    _("Tú eres mi sol,\nMi único sol"),
    _("Te extrañé."),
    _("Juega conmigo"),
    _("Es sólo un juego, en su mayoría."),
    _("¿Este juego no es adecuado para niños\nni para aquellos que se perturban fácilmente?"),
    _("sdfasdklfgsdfgsgoinrfoenlvbd"),
    _("nulo"),
    _("He llevado a los niños al infierno"),
    _("PM murió por esto."),
    _("Sólo fue parcialmente tu culpa."),
    _("Este juego no es adecuado para niños\nni para aquellos que se desmembran fácilmente.")

    ]

image splash_warning = ParameterizedText(style="splash_text", xalign=0.5, yalign=0.5)


image menu_logo:
    "mod_assets/menu_new.png"
    subpixel True
    xcenter 240
    ycenter 120
    zoom 0.60
    menu_logo_move



image menu_bg:
    topleft
    "gui/menu_bg.png"
    menu_bg_move

image game_menu_bg:
    topleft
    "gui/menu_bg.png"
    menu_bg_loop

image menu_fade:
    "white"
    menu_fadeout

image menu_art_m:
    subpixel True
    "gui/menu_art_m.png"
    xcenter 1000
    ycenter 640
    zoom 1.00
    menu_art_move(1.00, 1000, 1.00)

image menu_art_m_ghost:
    subpixel True
    "gui/menu_art_m_ghost.png"
    xcenter 1000
    ycenter 640
    zoom 1.00
    menu_art_move(1.00, 1000, 1.00)

image menu_nav:
    "gui/overlay/main_menu.png"
    menu_nav_move

image menu_particles:
    2.481
    xpos 224
    ypos 104
    ParticleBurst("gui/menu_particle.png", explodeTime=0, numParticles=20, particleTime=2.0, particleXSpeed=6, particleYSpeed=4).sm
    particle_fadeout

transform particle_fadeout:
    easeout 1.5 alpha 0

transform menu_bg_move:
    subpixel True
    topleft
    parallel:
        xoffset 0 yoffset 0
        linear 3.0 xoffset -100 yoffset -100
        repeat
    parallel:
        ypos 0
        time 0.65
        ease_cubic 2.5 ypos -500

transform menu_bg_loop:
    subpixel True
    topleft
    parallel:
        xoffset 0 yoffset 0
        linear 3.0 xoffset -100 yoffset -100
        repeat

transform menu_logo_move:
    subpixel True
    yoffset -300
    time 1.925
    easein_bounce 1.5 yoffset 0

transform menu_nav_move:
    subpixel True
    xoffset -500
    time 1.5
    easein_quint 1 xoffset 0

transform menu_fadeout:
    easeout 0.75 alpha 0
    time 2.481
    alpha 0.4
    linear 0.5 alpha 0

transform menu_art_move(z, x, z2):
    subpixel True
    yoffset 0 + (1200 * z)
    xoffset (740 - x) * z * 0.5
    zoom z2 * 0.75
    time 1.0
    parallel:
        ease 1.75 yoffset 0
    parallel:
        pause 0.75
        ease 1.5 zoom z2 xoffset 0

image intro:
    truecenter
    "white"
    0.5
    "bg/splash.png" with Dissolve(0.5, alpha=True)
    2.5
    "white" with Dissolve(0.5, alpha=True)
    0.5

image warning:
    truecenter
    "white"
    "splash_warning" with Dissolve(0.5, alpha=True)
    2.5
    "white" with Dissolve(0.5, alpha=True)
    0.5

image tos = "bg/warning.png"
image tos2 = "bg/warning2.png"


label splashscreen:
    python:
        _mas_AffStartup()

        persistent.sessions['current_session_start']=datetime.datetime.now()
        persistent.sessions['total_sessions'] = persistent.sessions['total_sessions']+ 1
        store.mas_calendar.loadCalendarDatabase()


        store.mas_sprites.adjust_zoom()

    if mas_corrupted_per and (mas_no_backups_found or mas_backup_copy_failed):


        call mas_backups_you_have_corrupted_persistent from _call_mas_backups_you_have_corrupted_persistent

    scene white


    default persistent.first_run = False
    $ persistent.tried_skip = False
    if not persistent.first_run:
        $ quick_menu = False
        pause 0.5
        scene tos
        with Dissolve(1.0)
        pause 1.0
        "[config.name] es un mod fan de Doki Doki Literature Club que no está afiliado a Team Salvato."
        "Está diseñado para ser jugado sólo después de que el juego oficial haya sido culminado, contiene spoilers del juego oficial."
        "Los archivos de juego de DDLC son necesarios para jugar este mod y se consiguen gratis en http://ddlc.moe o en Steam."
        menu:
            "Al jugar [config.name] usted está de acuerdo en que ha completado Doki Doki Literature Club y acepta cualquier spoiler que contenga."
            "Acepto.":
                pass
        scene tos2
        with Dissolve(1.5)
        pause 1.0

        scene white
        with Dissolve(1.5)


        if not persistent.has_merged:
            call import_ddlc_persistent from _call_import_ddlc_persistent

        $ persistent.first_run = True



    python:
        basedir = config.basedir.replace("\\", "/")


        with open(basedir + "/game/masrun", "w") as versfile:
            versfile.write(config.name + "|" + config.version + "\n")






    if persistent.autoload and not _restart:
        jump autoload

    $ mas_enable_quit()


    $ config.allow_skipping = False


    show white
    $ persistent.ghost_menu = False
    $ splash_message = splash_message_default
    $ config.main_menu_music = audio.t1
    $ renpy.music.play(config.main_menu_music)
    show intro with Dissolve(0.5, alpha=True)
    pause 2.5
    hide intro with Dissolve(0.5, alpha=True)

    if renpy.random.randint(0, 3) == 0:
        $ splash_message = renpy.random.choice(splash_messages)
    show splash_warning "[splash_message]" with Dissolve(0.5, alpha=True)
    pause 2.0
    hide splash_warning with Dissolve(0.5, alpha=True)
    $ config.allow_skipping = False

    python:
        if persistent._mas_auto_mode_enabled:
            mas_darkMode(mas_current_background.isFltDay())
        else:
            mas_darkMode(not persistent._mas_dark_mode_enabled)
    return

label warningscreen:
    hide intro
    show warning
    pause 3.0

label after_load:
    $ config.allow_skipping = False
    $ _dismiss_pause = config.developer
    $ persistent.ghost_menu = False
    $ style.say_dialogue = style.normal

    if anticheat != persistent.anticheat:
        stop music
        scene black
        "El archivo de guardado no pudo ser cargado."
        "¿Intentas hacer trampas?"

        $ renpy.utter_restart()
    return


label autoload:
    python:

        if "_old_game_menu_screen" in globals():
            _game_menu_screen = _old_game_menu_screen
            del _old_game_menu_screen
        if "_old_history" in globals():
            _history = _old_history
            del _old_history
        renpy.block_rollback()


        renpy.context()._menu = False
        renpy.context()._main_menu = False
        main_menu = False
        _in_replay = None


    $ config.keymap["debug_voicing"] = list()
    $ config.keymap["choose_renderer"] = list()


    $ renpy.pop_call()


    if persistent._mas_chess_mangle_all:
        jump mas_chess_go_ham_and_delete_everything









    $ store.mas_dockstat.setMoniSize(persistent.sessions["total_playtime"])


    $ mas_runDelayedActions(MAS_FC_START)



    jump ch30_autoload

label before_main_menu:
    $ config.main_menu_music = audio.t1
    return

label quit:
    python:
        store.mas_calendar.saveCalendarDatabase(CustomEncoder)
        persistent.sessions['last_session_end']=datetime.datetime.now()
        today_time = (
            persistent.sessions["last_session_end"]
            - persistent.sessions["current_session_start"]
        )
        new_time = today_time + persistent.sessions["total_playtime"]


        if datetime.timedelta(0) < new_time <= mas_maxPlaytime():
            persistent.sessions['total_playtime'] = new_time


        store.mas_dockstat.setMoniSize(persistent.sessions["total_playtime"])


        store.mas_selspr.save_selectables()


        monika_chr.save()


        store.mas_weather.saveMWData()


        store.mas_background.saveMBGData()


        store.mas_island_event.removeImages()


        store.mas_o31_event.removeImages()


        mas_runDelayedActions(MAS_FC_END)
        store.mas_delact.saveDelayedActionMap()

        _mas_AffSave()


        if not persistent._mas_dockstat_going_to_leave:
            store.mas_utils.trydel(mas_docking_station._trackPackage("monika"))


        store.mas_sprites._clear_caches()


        store.mas_xp.grant()

    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
