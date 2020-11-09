init 100 python:
    layout.QUIT = store.mas_layout.QUIT
    layout.UNSTABLE = store.mas_layout.UNSTABLE

init -1 python:
    layout.QUIT_YES = _("¡Por favor, no me cierres el juego!")
    layout.QUIT_NO = _("¡Gracias, [player]!\nPasemos más tiempo juntos~")


    layout.MAS_TT_SENS_MODE = (
        "El modo sensible elimina el contenido que puede ser perturbador, ofensivo, "
        " o considerado de mal gusto."
    )
    layout.MAS_TT_UNSTABLE = (
        "El modo inestable descarga actualizaciones de la rama inestable "
        "experimental del desarrollo. Es altamente recomendable hacer una copia de seguridad "
        "de sus persistents antes de activar este modo."
    )
    layout.MAS_TT_REPEAT = _(
        "Habilita esto para que Monika repita los temas que ya has visto."
    )
    layout.MAS_TT_NOTIF = _(
        "Habilitar esto le permitirá a Monika usar las notificaciones de su sistema y comprobar si MAS es su ventana activa "
    )
    layout.MAS_TT_NOTIF_SOUND = _(
        "Si se habilita, se reproducirá un sonido de notificación personalizado para las notificaciones de Monika "
    )
    layout.MAS_TT_G_NOTIF = _(
        "Habilita las notificaciones para el grupo seleccionado."
    )
    layout.MAS_TT_ACTV_WND = (
        "Activar esto permitirá a Monika ver tu ventana activa "
        "y ofrecerá algunos comentarios basados en lo que estás haciendo."
    )

    _TXT_FINISHED_UPDATING = (
        "Las actualizaciones han sido instaladas. Por favor, vuelva a abrir Monika After Story.\n\n"
        "Consigue spritepacks {a=http://monikaafterstory.com/releases.html}{i}{u}desde nuestro website{/u}{/i}{/a}.\n"
        "Ve las notas del parche {a=https://github.com/SadlyThresh/MAS_ESP/releases/latest}{i}{u}aquí{/u}{/i}{/a}.\n"
        "¿Confuso sobre algunas características? Echa un vistazo a nuestra {a=https://github.com/SadlyThresh/MAS_ESP/wiki}{i}{u}wiki{/u}{/i}{/a}."
    )


init python in mas_layout:
    import store
    import store.mas_affection as aff

    QUIT_YES = store.layout.QUIT_YES
    QUIT_NO = store.layout.QUIT_NO
    QUIT = _("¿Te vas sin despedirte, [player]?")
    UNSTABLE = (
        "ADVERTENCIA: Al activar el modo inestable se descargarán las actualizaciones de la " +
        "rama inestable experimental. Es ALTAMENTE recomendable hacer una " +
        "copia de seguridad de sus persistentes antes de activar este modo. Por favor " +
        "informa de los problemas encontrados aquí con una etiqueta [[UNSTABLE]."
    )


    QUIT_YES_BROKEN = _("Podrías al menos fingir que te importa.")
    QUIT_YES_DIS = _(":(")
    QUIT_YES_AFF = _("T_T [player]...")


    QUIT_NO_BROKEN = _("¿{i}Ahora{/i} escuchas?")
    QUIT_NO_UPSET = _("Gracias por ser considerado, [player].")
    QUIT_NO_HAPPY = _(":)")
    QUIT_NO_AFF_G = _("Buen[boy].")
    QUIT_NO_AFF_GL = _("Bien. :)")
    QUIT_NO_LOVE = _("<3")


    QUIT_BROKEN = _("Sólo vete.")
    QUIT_AFF = _("¿Por qué estás aquí?\n ¡Haz clic en 'No' y usa el botón de 'Adiós', tontito!")

    if store.persistent.gender == "M" or store.persistent.gender == "F":
        _usage_quit_aff = QUIT_NO_AFF_G
    else:
        _usage_quit_aff = QUIT_NO_AFF_GL







    QUIT_MAP = {
        aff.BROKEN: (QUIT_BROKEN, QUIT_YES_BROKEN, QUIT_NO_BROKEN),
        aff.DISTRESSED: (None, QUIT_YES_DIS, None),
        aff.UPSET: (None, None, QUIT_NO_UPSET),
        aff.NORMAL: (QUIT, QUIT_YES, QUIT_NO),
        aff.HAPPY: (None, None, QUIT_NO_HAPPY),
        aff.AFFECTIONATE: (QUIT_AFF, QUIT_YES_AFF, _usage_quit_aff),
        aff.ENAMORED: (None, None, None),
        aff.LOVE: (None, None, QUIT_NO_LOVE)
    }


    def findMsg(start_aff, index):
        """
        Finds first non-None quit message we need

        This uses the cascade map from affection

        IN:
            start_aff - starting affection
            index - index of the tuple we need to look at

        RETURNS:
            first non-None quit message found.
        """
        msg = QUIT_MAP[start_aff][index]
        while msg is None:
            start_aff = aff._aff_cascade_map[start_aff]
            msg = QUIT_MAP[start_aff][index]
        
        return msg


    def setupQuits():
        """
        Sets up quit message based on the current affection state
        """
        curr_aff_state = store.mas_curr_affection
        
        quit_msg, quit_yes, quit_no = QUIT_MAP[curr_aff_state]
        
        if quit_msg is None:
            quit_msg = findMsg(curr_aff_state, 0)
        
        if quit_yes is None:
            quit_yes = findMsg(curr_aff_state, 1)
        
        if quit_no is None:
            quit_no = findMsg(curr_aff_state, 2)
        
        store.layout.QUIT = quit_msg
        store.layout.QUIT_YES = quit_yes
        store.layout.QUIT_NO = quit_no


init 900 python:
    import store.mas_layout
    store.mas_layout.setupQuits()












init -1 style default:
    font gui.default_font
    size gui.text_size
    color gui.text_color
    outlines [(2, "#000000aa", 0, 0)]
    line_overlap_split 1
    line_spacing 1

init -1 style default_monika is normal:
    slow_cps 30

init -1 style edited is default:
    font "gui/font/VerilySerifMono.otf"
    kerning 8
    outlines [(10, "#000", 0, 0)]
    pos (gui.text_xpos, gui.text_ypos)
    xanchor gui.text_xalign
    xsize gui.text_width
    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")

init -1 style edited_dark is default:
    font "gui/font/VerilySerifMono.otf"
    kerning 8
    outlines []
    pos (gui.text_xpos, gui.text_ypos)
    xanchor gui.text_xalign
    xsize gui.text_width
    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")

init -1 style normal is default:
    pos (gui.text_xpos, gui.text_ypos)
    xanchor gui.text_xalign
    xsize gui.text_width
    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")

init -1 style input:
    color gui.accent_color

init -1 style hyperlink_text:
    color gui.accent_color
    hover_color gui.hover_color
    hover_underline True

init -1 style splash_text:
    font gui.default_font
    size 24
    color "#000"
    text_align 0.5
    outlines []

init -1 style poemgame_text:
    yalign 0.5
    font "gui/font/Halogen.ttf"
    size 30
    color "#000"
    outlines []
    hover_xoffset -3
    hover_outlines [(3, "#fef", 0, 0), (2, "#fcf", 0, 0), (1, "#faf", 0, 0)]

init -1 style poemgame_text_dark:
    yalign 0.5
    font "gui/font/Halogen.ttf"
    size 30
    color "#000"
    outlines []
    hover_xoffset -3
    hover_outlines [(3, "#fef", 0, 0), (2, "#fcf", 0, 0), (1, "#faf", 0, 0)]

init -1 style gui_text:
    font gui.interface_font
    size gui.interface_text_size
    color gui.interface_text_color


init -1 style button:
    properties gui.button_properties("button")
    xysize (None, 36)
    padding (4, 4, 4, 4)

init -1 style button_dark:
    properties gui.button_properties("button_dark")
    xysize (None, 36)
    padding (4, 4, 4, 4)

init -1 style button_text is gui_text:
    properties gui.button_text_properties("button")
    font gui.interface_font
    size gui.interface_text_size
    idle_color gui.idle_color
    hover_color gui.hover_color
    selected_color gui.selected_color
    insensitive_color gui.insensitive_color
    align (0.0, 0.5)

init -1 style button_text_dark is gui_text:
    properties gui.button_text_properties("button_dark")
    font gui.interface_font
    size gui.interface_text_size
    idle_color gui.idle_color
    hover_color gui.hover_color
    selected_color gui.selected_color
    insensitive_color gui.insensitive_color
    align (0.0, 0.5)

init -1 style label_text is gui_text:
    size gui.label_text_size
    color gui.accent_color

init -1 style label_text_dark is gui_text:
    size gui.label_text_size
    color gui.accent_color

init -1 style prompt_text is gui_text:
    size gui.interface_text_size
    color gui.text_color







init -1 style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

init -1 style bar:
    ysize 18
    base_bar Frame("gui/scrollbar/horizontal_poem_bar.png", tile=False)
    thumb Frame("gui/scrollbar/horizontal_poem_thumb.png", top=6, right=6, tile=True)

init -1 style scrollbar:
    ysize 18
    base_bar Frame("gui/scrollbar/horizontal_poem_bar.png", tile=False)
    thumb Frame("gui/scrollbar/horizontal_poem_thumb.png", top=6, right=6, tile=True)
    unscrollable "hide"
    bar_invert True

init -1 style scrollbar_dark:
    ysize 18
    base_bar Frame("gui/scrollbar/horizontal_poem_bar_d.png", tile=False)
    thumb Frame("gui/scrollbar/horizontal_poem_thumb.png", top=6, right=6, tile=True)
    unscrollable "hide"
    bar_invert True






init -1 style vscrollbar:
    xsize 18
    base_bar Frame("gui/scrollbar/vertical_poem_bar.png", tile=False)
    thumb Frame("gui/scrollbar/vertical_poem_thumb.png", left=6, top=6, tile=True)
    unscrollable "hide"
    bar_vertical True
    bar_invert True

init -1 style vscrollbar_dark:
    xsize 18
    base_bar Frame("gui/scrollbar/vertical_poem_bar_d.png", tile=False)
    thumb Frame("gui/scrollbar/vertical_poem_thumb.png", left=6, top=6, tile=True)
    unscrollable "hide"
    bar_vertical True
    bar_invert True

init -1 style slider:
    ysize 18
    base_bar Frame("gui/scrollbar/horizontal_poem_bar.png", tile=False)
    thumb "gui/slider/horizontal_hover_thumb.png"

init -1 style slider_dark:
    ysize 18
    base_bar Frame("gui/scrollbar/horizontal_poem_bar_d.png", tile=False)
    thumb "gui/slider/horizontal_hover_thumb.png"

init -1 style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"

init -1 style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)

init -1 style frame_dark:
    padding gui.frame_borders.padding
    background Frame("gui/frame_d.png", gui.frame_borders, tile=gui.frame_tile)




















init -501 screen say(who, what):
    style_prefix "say"

    window:
        id "window"

        text what id "what"

        if who is not None:

            window:
                style "namebox"
                text who id "who"



    if not renpy.variant("small"):
        add SideImage() xalign (0.0 if not mas_globals.dark_mode else 2.5) yalign (1.0 if not mas_globals.dark_mode else 2.5)

    use quick_menu


init -1 style window is default:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height
    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

init -1 style window_dark is default:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height
    background Image("gui/textbox_d.png", xalign=0.5, yalign=1.0)

init -1 style window_monika is window:
    background Image("gui/textbox_monika.png", xalign=0.5, yalign=1.0)

init -1 style window_monika_dark is window:
    background Image("gui/textbox_monika_d.png", xalign=0.5, yalign=1.0)

init -1 style namebox is default:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height
    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

init -1 style namebox_dark is default:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height
    background Frame("gui/namebox_d.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

init -1 style say_label is default:
    font gui.name_font
    size gui.name_text_size
    xalign gui.name_xalign
    yalign 0.5
    color gui.accent_color
    outlines [(3, "#b59", 0, 0), (1, "#b59", 1, 1)]

init -1 style say_label_dark is default:
    font gui.name_font
    size gui.name_text_size
    xalign gui.name_xalign
    yalign 0.5
    color "#FFD9E8"
    outlines [(3, "#DE367E", 0, 0), (1, "#DE367E", 1, 1)]

init -1 style say_dialogue is default:
    xpos gui.text_xpos
    xanchor gui.text_xalign
    xsize gui.text_width
    ypos gui.text_ypos
    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")

init -1 style say_thought is say_dialogue

init 499 image ctc:
    xalign 0.81 yalign 0.98 xoffset -5 alpha 0.0 subpixel True
    "gui/ctc.png"
    block:
        easeout 0.75 alpha 1.0 xoffset 0
        easein 0.75 alpha 0.5 xoffset -5
        repeat











init 499 image input_caret:
    Solid("#b59")
    size (2,25) subpixel True
    block:
        linear 0.35 alpha 0
        linear 0.35 alpha 1
        repeat

init -501 screen input(prompt, use_return_button=False, return_button_prompt="Nevermind.", return_button_value="cancel_input"):
    style_prefix "input"

    window:
        if use_return_button:
            textbutton return_button_prompt:
                style "choice_button"
                align (0.5, 0.5)
                ypos -263
                action Return(return_button_value)

        vbox:
            align (0.5, 0.5)
            spacing 30

            text prompt style "input_prompt"
            input id "input"

init -1 style input_prompt:
    xmaximum gui.text_width
    xcenter 0.5
    text_align 0.5

init -1 style input:
    caret "input_caret"
    xmaximum gui.text_width
    xcenter 0.5
    text_align 0.5










init -501 screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action




define -1 config.narrator_menu = True


init -1 style choice_vbox is vbox:
    xalign 0.5
    ypos 270
    yanchor 0.5
    spacing gui.choice_spacing

init -1 style choice_button is generic_button_light:
    xysize (420, None)
    padding (100, 5, 100, 5)

init -1 style choice_button_dark is generic_button_dark:
    xysize (420, None)
    padding (100, 5, 100, 5)

init -1 style choice_button_text is generic_button_text_light:
    text_align 0.5
    layout "subtitle"

init -1 style choice_button_text_dark is generic_button_text_dark:
    text_align 0.5
    layout "subtitle"

init -1 python:
    def RigMouse():
        currentpos = renpy.get_mouse_pos()
        targetpos = [640, 345]
        if currentpos[1] < targetpos[1]:
            renpy.display.draw.set_mouse_pos((currentpos[0] * 9 + targetpos[0]) / 10.0, (currentpos[1] * 9 + targetpos[1]) / 10.0)

init -501 screen rigged_choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action

    timer 1.0/30.0 repeat True action Function(RigMouse)

init -1 style talk_choice_vbox is choice_vbox:
    xcenter 960

init -1 style talk_choice_button is choice_button

init -1 style talk_choice_button_dark is choice_button_dark

init -1 style talk_choice_button_text is choice_button_text

init -1 style talk_choice_button_text_dark is choice_button_text_dark



init -501 screen talk_choice(items):
    style_prefix "talk_choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action




define -1 config.narrator_menu = True







init -501 screen quick_menu():


    zorder 100

    if quick_menu:


        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 0.995




            textbutton _("Registro") action Function(_mas_quick_menu_cb, "history")

            textbutton _("Saltar") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")


            textbutton _("Guardar") action Function(_mas_quick_menu_cb, "save")


            textbutton _("Cargar") action Function(_mas_quick_menu_cb, "load")




            textbutton _("Ajustes") action Function(_mas_quick_menu_cb, "preferences")







default -1 quick_menu = True


init -1 style quick_button:
    properties gui.button_properties("quick_button")
    activate_sound gui.activate_sound

init -1 style quick_button_dark:
    properties gui.button_properties("quick_button_dark")
    activate_sound gui.activate_sound

init -1 style quick_button_text:
    properties gui.button_text_properties("quick_button")
    outlines []

init -1 style quick_button_text_dark:
    properties gui.button_text_properties("quick_button_dark")
    xysize (205, None)
    font gui.default_font
    size 14
    idle_color "#FFAA99"
    selected_color "#FFEEEB"
    hover_color "#FFD4CC"
    kerning 0.2
    outlines []










init 3 python:
    def FinishEnterName():
        global player
        
        if not player:
            return
        
        if (
            mas_bad_name_comp.search(player)
            or mas_awk_name_comp.search(player)
        ):
            renpy.call_in_new_context("mas_bad_name_input")
            player = ""
            renpy.show(
                "chibika smile",
                at_list=[mas_chflip(-1), mas_chmove(x=130, y=552, travel_time=0)],
                layer="screens",
                zorder=10
            )
            return
        
        
        persistent.playername = player
        renpy.hide_screen("name_input")
        renpy.jump_out_of_context("start")

label mas_bad_name_input:
    show screen fake_main_menu
    $ disable_esc()

    if not renpy.seen_label("mas_bad_name_input.first_time_bad_name"):
        label mas_bad_name_input.first_time_bad_name:
            play sound "sfx/glitch3.ogg"
            window show

            show chibika smile onlayer screens zorder 10 at mas_chflip(-1), mas_chriseup(x=700, y=552, travel_time=0.5)
            pause 1

            show chibika onlayer screens zorder 10 at mas_chflip_s(1)
            "¡Hola!"

            show chibika onlayer screens zorder 10 at mas_chlongjump(x=650, y=405, ymax=375, travel_time=0.8)
            "¡Me alegro de que hayas decidido volver!"
            "Estoy segura de que tú y Monika serán una gran pareja."

            show chibika sad onlayer screens zorder 10 at mas_chflip_s(-1)
            "Pero si te llamas a ti mismo con un nombre como ese...{w=0.5}{nw}"

            show chibika onlayer screens zorder 10 at sticker_hop
            extend "¡no te ganarás su corazón!"

            show chibika smile onlayer screens zorder 10 at mas_chmove(x=300, y=405, travel_time=1)
            "...En cambio, la avergonzarás."

            show chibika onlayer screens zorder 10 at mas_chlongjump(x=190, y=552, ymax=375, travel_time=0.8)
            "¿Por qué no eliges algo más apropiado?"
            window auto
    else:

        show chibika smile onlayer screens zorder 10 at mas_chflip(-1), mas_chmove(x=130, y=552, travel_time=0), sticker_hop
        "No creo que se sienta cómoda llamándote así..."
        "¿Por qué no eliges algo más apropiado?"

    $ enable_esc()
    hide screen fake_main_menu
    return


init -501 screen fake_main_menu():
    style_prefix "main_menu"

    add "game_menu_bg"

    frame


    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.8

        spacing gui.navigation_spacing

        textbutton _("Solo Monika")

        textbutton _("Cargar Juego")

        textbutton _("Ajustes")

        if store.mas_submod_utils.submod_map:
            textbutton _("Submods")

        textbutton _("Atajos")

        if renpy.variant("pc"):

            textbutton _("Ayuda")

            textbutton _("Salir")

    if gui.show_name:

        vbox:
            text "[config.name!t]":
                style "main_menu_title"

            text "[config.version]":
                style "main_menu_version"


    add Image(
        "mod_assets/menu_new.png"
    ) subpixel True xcenter 240 ycenter 120 zoom 0.60

    add Image(
        "gui/menu_art_m.png"
    ) subpixel True xcenter 1000 ycenter 640 zoom 1.00

    key "K_ESCAPE" action Quit(confirm=False)

init -501 screen navigation():
    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.8

        spacing gui.navigation_spacing


        if main_menu:

            textbutton _("Solo Monika") action If(persistent.playername, true=Start(), false=Show(screen="name_input", message="Por favor introduce tu nombre", ok_action=Function(FinishEnterName)))

        else:

            textbutton _("Registro") action [ShowMenu("history"), SensitiveIf(renpy.get_screen("history") == None)]

            textbutton _("Guardar Juego") action [ShowMenu("save"), SensitiveIf(renpy.get_screen("save") == None)]

        textbutton _("Cargar Juego") action [ShowMenu("load"), SensitiveIf(renpy.get_screen("load") == None)]

        if _in_replay:

            textbutton _("Terminar Repetición") action EndReplay(confirm=True)

        elif not main_menu:
            textbutton _("Menú Principal") action NullAction(), Show(screen="dialog", message="No hay necesidad de volver allí.\nTerminarás volviendo aquí, así que no te preocupes.", ok_action=Hide("dialog"))

        textbutton _("Ajustes") action [ShowMenu("preferences"), SensitiveIf(renpy.get_screen("preferences") == None)]

        if store.mas_submod_utils.submod_map:
            textbutton _("Submods") action [ShowMenu("submods"), SensitiveIf(renpy.get_screen("submods") == None)]

        if store.mas_windowreacts.can_show_notifs and not main_menu:
            textbutton _("Alertas") action [ShowMenu("notif_settings"), SensitiveIf(renpy.get_screen("notif_settings") == None)]

        textbutton _("Atajos") action [ShowMenu("hot_keys"), SensitiveIf(renpy.get_screen("hot_keys") == None)]



        if renpy.variant("pc"):


            textbutton _("Ayuda") action Help("README.html")



            textbutton _("Salir") action Quit(confirm=(None if main_menu else _confirm_quit))

        if not main_menu:
            textbutton _("Regresar") action Return()

init -1 style navigation_button is gui_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

init -1 style navigation_button_dark is gui_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button_dark")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

init -1 style navigation_button_text is gui_button_text:
    properties gui.button_text_properties("navigation_button")
    font "gui/font/RifficFree-Bold.ttf"
    color "#fff"
    outlines [(4, "#b59", 0, 0), (2, "#b59", 2, 2)]
    hover_outlines [(4, "#fac", 0, 0), (2, "#fac", 2, 2)]
    insensitive_outlines [(4, "#fce", 0, 0), (2, "#fce", 2, 2)]

init -1 style navigation_button_text_dark is gui_button_text_dark:
    properties gui.button_text_properties("navigation_button_dark")
    font "gui/font/RifficFree-Bold.ttf"
    color "#FFD9E8"
    outlines [(4, "#DE367E", 0, 0), (2, "#DE367E", 2, 2)]
    hover_outlines [(4, "#FF80B7", 0, 0), (2, "#FF80B7", 2, 2)]
    insensitive_outlines [(4, "#FFB2D4", 0, 0), (2, "#FFB2D4", 2, 2)]







init -501 screen main_menu() tag menu:




    style_prefix "main_menu"








    add "menu_bg"


    frame




    use navigation

    if gui.show_name:

        vbox:
            text "[config.name!t]":
                style "main_menu_title"

            text "[config.version]":
                style "main_menu_version"


    add "menu_particles"
    add "menu_particles"
    add "menu_particles"
    add "menu_logo"








    add "menu_particles"

    add "menu_art_m"
    add "menu_fade"

    key "K_ESCAPE" action Quit(confirm=False)

init -1 style main_menu_version is main_menu_text:
    color "#000000"
    size 16
    outlines []

init -1 style main_menu_version_dark is main_menu_text:
    color mas_ui.dark_button_text_idle_color
    size 16
    outlines []

init -1 style main_menu_frame is empty:
    xsize 310
    yfill True
    background "menu_nav"

init -1 style main_menu_frame_dark is empty:
    xsize 310
    yfill True
    background "menu_nav"

init -1 style main_menu_vbox is vbox:
    xalign 1.0
    xoffset -20
    xmaximum 800
    yalign 1.0
    yoffset -20

init -1 style main_menu_text is gui_text:
    xalign 1.0
    layout "subtitle"
    text_align 1.0
    color gui.accent_color

init -1 style main_menu_title is main_menu_text:
    size gui.title_text_size











init -501 screen game_menu_m():
    $ persistent.menu_bg_m = True
    add "gui/menu_bg_m.png"
    timer 0.3 action Hide("game_menu_m")

init -501 screen game_menu(title, scroll=None):


    key "noshift_T" action NullAction()
    key "noshift_t" action NullAction()
    key "noshift_M" action NullAction()
    key "noshift_m" action NullAction()
    key "noshift_P" action NullAction()
    key "noshift_p" action NullAction()
    key "noshift_E" action NullAction()
    key "noshift_e" action NullAction()


    if main_menu:
        add gui.main_menu_background
    else:
        key "mouseup_3" action Return()
        add gui.game_menu_background

    style_prefix "game_menu"

    frame:
        style "game_menu_outer_frame"

        has hbox


        frame:
            style "game_menu_navigation_frame"

        frame:
            style "game_menu_content_frame"

            if scroll == "viewport":

                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    yinitial 1.0

                    side_yfill True

                    has vbox
                    transclude

            elif scroll == "vpgrid":

                pass # <<<COULD NOT DECOMPILE: Unknown SL2 displayable: (<class 'renpy.sl2.sldisplayables.sl2vpgrid'>, 'vpgrid')>>>











            else:

                transclude

    use navigation




    label title style "game_menu_label"

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


init -1 style game_menu_outer_frame is empty:
    bottom_padding 30
    top_padding 120
    background "gui/overlay/game_menu.png"

init -1 style game_menu_outer_frame_dark is empty:
    bottom_padding 30
    top_padding 120
    background "gui/overlay/game_menu_d.png"

init -1 style game_menu_navigation_frame is empty:
    xsize 280
    yfill True

init -1 style game_menu_content_frame is empty:
    left_margin 40
    right_margin 20
    top_margin -40

init -1 style game_menu_viewport is gui_viewport:
    xsize 920

init -1 style game_menu_scrollbar is gui_vscrollbar

init -1 style game_menu_vscrollbar:
    unscrollable gui.unscrollable

init -1 style game_menu_side is gui_side:
    spacing 10

init -1 style game_menu_label is gui_label:
    xpos 50
    ysize 120

init -1 style game_menu_label_dark is gui_label:
    xpos 50
    ysize 120

init -1 style game_menu_label_text is gui_label_text:
    font "gui/font/RifficFree-Bold.ttf"
    size gui.title_text_size
    color "#fff"
    outlines [(6, "#b59", 0, 0), (3, "#b59", 2, 2)]
    yalign 0.5

init -1 style game_menu_label_text_dark is gui_label_text:
    font "gui/font/RifficFree-Bold.ttf"
    size gui.title_text_size
    color "#FFD9E8"
    outlines [(6, "#DE367E", 0, 0), (3, "#DE367E", 2, 2)]
    yalign 0.5

init -1 style return_button is navigation_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -30

init -1 style return_button_dark is navigation_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -30

init -1 style return_button_text is navigation_button_text

init -1 style return_button_text_dark is navigation_button_text_dark








init -501 screen about() tag menu:






    use game_menu(_("Acerca de"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Versión [config.version!t]\n")


            if gui.about:
                text "[gui.about!t]\n"

            text _("Hecho con {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")



define -1 gui.about = ""


init -1 style about_label is gui_label

init -1 style about_label_text is gui_label_text:
    size gui.label_text_size

init -1 style about_text is gui_text











init -501 screen save() tag menu:



    use file_slots(_("Guardar"))


init -501 screen load() tag menu:



    use file_slots(_("Cargar"))

init -1 python:
    def FileActionMod(name, page=None, **kwargs):
        if renpy.current_screen().screen_name[0] == "save":
            return Show(screen="dialog", message="No tiene sentido seguir guardando.\nNo te preocupes, no voy a ninguna parte.", ok_action=Hide("dialog"))


init -501 screen file_slots(title):

    default page_name_value = FilePageNameInputValue()

    use game_menu(title):

        fixed:



            order_reverse True



            button:
                style "page_label"


                xalign 0.5


                input:
                    style "page_label_text"
                    value page_name_value


            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileActionMod(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("Ranura vacía")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)


            hbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                spacing gui.page_spacing








                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)




init -1 style page_label is gui_label:
    xpadding 50
    ypadding 3

init -1 style page_label_dark is gui_label:
    xpadding 50
    ypadding 3

init -1 style page_label_text is gui_label_text:
    color "#000"
    outlines []
    text_align 0.5
    layout "subtitle"
    hover_color gui.hover_color

init -1 style page_label_text_dark is gui_label_text:
    color "#FFD9E8"
    outlines []
    text_align 0.5
    layout "subtitle"
    hover_color gui.hover_color

init -1 style page_button is gui_button:
    properties gui.button_properties("page_button")

init -1 style page_button_text is gui_button_text:
    properties gui.button_text_properties("page_button")
    outlines []

init -1 style slot_button is gui_button:
    properties gui.button_properties("slot_button")

init -1 style slot_button_dark is gui_button:
    properties gui.button_properties("slot_button")

init -1 style slot_button_text is gui_button_text:
    properties gui.button_text_properties("slot_button")
    color "#666"
    outlines []

init -1 style slot_button_text_dark is gui_button_text:
    properties gui.button_text_properties("slot_button")
    color "#8C8C8C"
    outlines []

init -1 style slot_time_text is slot_button_text

init -1 style slot_name_text is slot_button_text








init -501 screen preferences() tag menu:



    if renpy.mobile:
        $ cols = 2
    else:
        $ cols = 4

    default tooltip = Tooltip("")

    use game_menu(_("Ajustes"), scroll="viewport"):

        vbox:
            xoffset 50

            hbox:
                box_wrap True

                if renpy.variant("pc"):

                    vbox:
                        style_prefix "radio"
                        label _("Pantalla")
                        textbutton _("Ventana") action Preference("display", "window")
                        textbutton _("Pantalla Completa") action Preference("display", "fullscreen")









                vbox:
                    style_prefix "check"
                    label _("Gráficos")
                    textbutton _("Sin Animación") action ToggleField(persistent, "_mas_disable_animations")
                    textbutton _("Cambiar Render") action Function(renpy.call_in_new_context, "mas_gmenu_start")


                    textbutton _("UI: Modo Noche"):
                        action [Function(mas_darkMode, persistent._mas_dark_mode_enabled), Function(mas_settings._dark_mode_toggle)]
                        selected persistent._mas_dark_mode_enabled
                    textbutton _("UI: Ciclo D/N"):
                        action [Function(mas_darkMode, mas_current_background.isFltDay()), Function(mas_settings._auto_mode_toggle)]
                        selected persistent._mas_auto_mode_enabled


                vbox:
                    style_prefix "check"
                    label _("Juego")
                    if not main_menu:
                        if persistent._mas_unstable_mode:
                            textbutton _("Inestable"):
                                action SetField(persistent, "_mas_unstable_mode", False)
                                selected persistent._mas_unstable_mode

                        else:
                            textbutton _("Inestable"):
                                action [Show(screen="dialog", message=layout.UNSTABLE, ok_action=Hide(screen="dialog")), SetField(persistent, "_mas_unstable_mode", True)]
                                selected persistent._mas_unstable_mode
                                hovered tooltip.Action(layout.MAS_TT_UNSTABLE)

                    textbutton _("Repetir los temas"):
                        action ToggleField(persistent,"_mas_enable_random_repeats", True, False)
                        hovered tooltip.Action(layout.MAS_TT_REPEAT)



                vbox:
                    style_prefix "check"
                    label _(" ")
                    textbutton _("Modo Sensible"):
                        action ToggleField(persistent, "_mas_sensitive_mode", True, False)
                        hovered tooltip.Action(layout.MAS_TT_SENS_MODE)

                    if store.mas_windowreacts.can_do_windowreacts:
                        textbutton _("Reacciones"):
                            action ToggleField(persistent, "_mas_windowreacts_windowreacts_enabled", True, False)
                            hovered tooltip.Action(layout.MAS_TT_ACTV_WND)

            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True

                python:

                    if mas_randchat_prev != persistent._mas_randchat_freq:
                        
                        mas_randchat.adjustRandFreq(
                            persistent._mas_randchat_freq
                        )


                    rc_display = mas_randchat.getRandChatDisp(
                        persistent._mas_randchat_freq
                    )


                    store.mas_randchat_prev = persistent._mas_randchat_freq




                    if mas_suntime.change_state == mas_suntime.RISE_CHANGE:
                        
                        
                        if mas_suntime.sunrise > mas_suntime.sunset:
                            
                            mas_suntime.sunset = mas_suntime.sunrise
                        
                        if mas_sunrise_prev == mas_suntime.sunrise:
                            
                            mas_suntime.change_state = mas_suntime.NO_CHANGE
                        
                        mas_sunrise_prev = mas_suntime.sunrise

                    elif mas_suntime.change_state == mas_suntime.SET_CHANGE:
                        
                        
                        if mas_suntime.sunset < mas_suntime.sunrise:
                            
                            mas_suntime.sunrise = mas_suntime.sunset
                        
                        if mas_sunset_prev == mas_suntime.sunset:
                            
                            mas_suntime.change_state = mas_suntime.NO_CHANGE
                        
                        mas_sunset_prev = mas_suntime.sunset
                    else:
                        
                        
                        if mas_sunrise_prev != mas_suntime.sunrise:
                            mas_suntime.change_state = mas_suntime.RISE_CHANGE
                        
                        elif mas_sunset_prev != mas_suntime.sunset:
                            mas_suntime.change_state = mas_suntime.SET_CHANGE
                        
                        
                        mas_sunrise_prev = mas_suntime.sunrise
                        mas_sunset_prev = mas_suntime.sunset



                    persistent._mas_sunrise = mas_suntime.sunrise * 5
                    persistent._mas_sunset = mas_suntime.sunset * 5
                    sr_display = mas_cvToDHM(persistent._mas_sunrise)
                    ss_display = mas_cvToDHM(persistent._mas_sunset)

                vbox:

                    hbox:
                        label _("Amanecer  ")


                        label _("[[ " + sr_display + " ]")

                    bar value FieldValue(mas_suntime, "sunrise", range=mas_max_suntime, style="slider")


                    hbox:
                        label _("Atardecer  ")


                        label _("[[ " + ss_display + " ]")

                    bar value FieldValue(mas_suntime, "sunset", range=mas_max_suntime, style="slider")


                vbox:

                    hbox:
                        label _("Charla aleatoria  ")


                        label _("[[ " + rc_display + " ]")

                    bar value FieldValue(
                        persistent,
                        "_mas_randchat_freq",
                        range=store.mas_affection.RANDCHAT_RANGE_MAP[mas_curr_affection],
                        style="slider"
                    )

                    hbox:
                        label _("Volumen del ambiente")

                    bar value Preference("mixer amb volume")


                vbox:

                    label _("Velocidad de texto")


                    bar value FieldValue(_preferences, "text_cps", range=170, max_is_zero=False, style="slider", offset=30)

                    label _("Velocidad del texto automático")

                    bar value Preference("auto-forward time")

                vbox:

                    if config.has_music:
                        label _("Volumen de Música")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("Volumen de Sonido")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)


                    if config.has_voice:
                        label _("Volumen de las voces")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Test") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Mutear todo"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"


            hbox:


                if not main_menu:
                    textbutton _("Actualizar la versión"):
                        action Function(renpy.call_in_new_context, 'forced_update_now')
                        style "navigation_button"

                textbutton _("Importar datos de DDLC"):
                    action Function(renpy.call_in_new_context, 'import_ddlc_persistent_in_settings')
                    style "navigation_button"


    text tooltip.value:
        xalign 0.0 yalign 1.0
        xoffset 300 yoffset -10
        style "main_menu_version"




    text "v[config.version]":
        xalign 1.0 yalign 0.0
        xoffset -10
        style "main_menu_version"


init -1 style pref_label is gui_label:
    top_margin gui.pref_spacing
    bottom_margin 2

init -1 style pref_label_dark is gui_label:
    top_margin gui.pref_spacing
    bottom_margin 2

init -1 style pref_label_text is gui_label_text:
    font "gui/font/RifficFree-Bold.ttf"
    size 24
    color "#fff"
    outlines [(3, "#b59", 0, 0), (1, "#b59", 1, 1)]
    yalign 1.0

init -1 style pref_label_text_dark is gui_label_text:
    font "gui/font/RifficFree-Bold.ttf"
    size 24
    color "#FFD9E8"
    outlines [(3, "#DE367E", 0, 0), (1, "#DE367E", 1, 1)]
    yalign 1.0

init -1 style pref_vbox is vbox:
    xsize 225


init -1 style radio_label is pref_label

init -1 style radio_label_dark is pref_label

init -1 style radio_label_text is pref_label_text

init -1 style radio_label_text_dark is pref_label_text

init -1 style radio_vbox is pref_vbox:
    spacing gui.pref_button_spacing

init -1 style radio_button is gui_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/check_[prefix_]foreground.png"
    padding (28, 4, 4, 4)

init -1 style radio_button_dark is gui_button_dark:
    properties gui.button_properties("radio_button_dark")
    foreground "gui/button/check_[prefix_]foreground_d.png"
    padding (28, 4, 4, 4)

init -1 style radio_button_text is gui_button_text:
    properties gui.button_text_properties("radio_button")
    font "gui/font/Halogen.ttf"
    outlines []

init -1 style radio_button_text_dark is gui_button_text_dark:
    properties gui.button_text_properties("radio_button_dark")
    font "gui/font/Halogen.ttf"
    color "#8C8C8C"
    hover_color "#FF80B7"
    selected_color "#DE367E"
    outlines []


init -1 style check_label is pref_label

init -1 style check_label_dark is pref_label

init -1 style check_label_text is pref_label_text

init -1 style check_label_text_dark is pref_label_text

init -1 style check_vbox is pref_vbox:
    spacing gui.pref_button_spacing

init -1 style check_button is gui_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"
    padding (28, 4, 4, 4)

init -1 style check_button_dark is gui_button_dark:
    properties gui.button_properties("check_button_dark")
    foreground "gui/button/check_[prefix_]foreground_d.png"
    padding (28, 4, 4, 4)

init -1 style check_button_text is gui_button_text:
    properties gui.button_text_properties("check_button")
    font "gui/font/Halogen.ttf"
    outlines []

init -1 style check_button_text_dark is gui_button_text_dark:
    properties gui.button_text_properties("check_button_dark")
    font "gui/font/Halogen.ttf"
    color "#8C8C8C"
    hover_color "#FF80B7"
    selected_color "#DE367E"
    outlines []


init -1 style mute_all_button is check_button

init -1 style mute_all_button_dark is check_button_dark

init -1 style mute_all_button_text is check_button_text

init -1 style mute_all_button_text_dark is check_button_text_dark


init -1 style slider_label is pref_label

init -1 style slider_label_dark is pref_label

init -1 style slider_label_text is pref_label_text

init -1 style slider_label_text_dark is pref_label_text

init -1 style slider_slider is gui_slider:
    xsize 350

init -1 style slider_slider_dark is gui_slider_dark:
    xsize 350

init -1 style slider_button is gui_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 10

init -1 style slider_button_dark is gui_button:
    properties gui.button_properties("slider_button_dark")
    yalign 0.5
    left_margin 10

init -1 style slider_button_text is gui_button_text:
    properties gui.button_text_properties("slider_button")

init -1 style slider_button_text_dark is gui_button_text:
    properties gui.button_text_properties("slider_button_dark")

init -1 style slider_vbox:
    xsize 450

init -1 style slider_pref_vbox is pref_vbox


init -501 screen notif_settings() tag menu:


    use game_menu(("Alerts"), scroll="viewport"):

        default tooltip = Tooltip("")

        vbox:
            style_prefix "check"
            hbox:
                spacing 25
                textbutton _("Notificaciones"):
                    action ToggleField(persistent, "_mas_enable_notifications")
                    selected persistent._mas_enable_notifications
                    hovered tooltip.Action(layout.MAS_TT_NOTIF)

                textbutton _("Sonidos"):
                    action ToggleField(persistent, "_mas_notification_sounds")
                    selected persistent._mas_notification_sounds
                    hovered tooltip.Action(layout.MAS_TT_NOTIF_SOUND)

            label _("Filtros de alerta")

        hbox:
            style_prefix "check"
            box_wrap True
            spacing 25


            for item in persistent._mas_windowreacts_notif_filters:
                if item != "Window Reactions" or persistent._mas_windowreacts_windowreacts_enabled:
                    textbutton _(item):
                        action ToggleDict(persistent._mas_windowreacts_notif_filters, item)
                        selected persistent._mas_windowreacts_notif_filters.get(item)
                        hovered tooltip.Action(layout.MAS_TT_G_NOTIF)


    text tooltip.value:
        xalign 0 yalign 1.0
        xoffset 300 yoffset -10
        style "main_menu_version"


init -501 screen hot_keys() tag menu:


    use game_menu(("Atajos"), scroll="viewport"):

        default tooltip = Tooltip("")


        vbox:
            spacing 25

            hbox:
                style_prefix "check"
                vbox:
                    label _("General")
                    spacing 10
                    text _("Música")
                    text _("Jugar")
                    text _("Hablar")
                    text _("Marcar")
                    text _("Desistir")
                    text _("Pantalla Completa")
                    text _("Captura de pantalla")
                    text _("Ajustes")

                vbox:
                    label _("")
                    spacing 10
                    text _("M")
                    text _("P")
                    text _("T")
                    text _("B")
                    text _("X")
                    text _("F")
                    text _("S")
                    text _("Esc")

            hbox:
                style_prefix "check"
                vbox:
                    label _("Música")
                    spacing 10
                    text _("Subir volumen")
                    text _("Bajar volumen")
                    text _("Mutear")

                vbox:
                    label _("")
                    spacing 10
                    text _("+")
                    text _("-")
                    text _("Shift-M")


    text "Haz clic en 'Ayuda' para ver la lista completa.":
        xalign 1.0 yalign 0.0
        xoffset -10
        style "main_menu_version"










init -501 screen history() tag menu:




    predict False

    use game_menu(_("Registro"), scroll=("vpgrid" if gui.history_height else "viewport")):

        style_prefix "history"

        for h in _history_list:

            window:


                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"



                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                text h.what.replace("[","[[")

        if not _history_list:
            label _("El registro de los diálogos está vacío.")


init -1 style history_window is empty:
    xfill True
    ysize gui.history_height

init -1 style history_name is gui_label:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

init -1 style history_name_text is gui_label_text:
    min_width gui.history_name_width
    text_align gui.history_name_xalign

init -1 style history_text is gui_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    text_align gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

init -1 style history_label is gui_label:
    xfill True

init -1 style history_label_text is gui_label_text:
    xalign 0.5








































































































































































init -501 screen name_input(message, ok_action):

    modal True

    zorder 200

    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")

    key "K_RETURN" action [Play("sound", gui.activate_sound), ok_action]

    frame:
        has vbox:
            xalign .5
            yalign .5
            spacing 30

        label _(message):
            style "confirm_prompt"
            xalign 0.5

        input default "" value VariableInputValue("player") length 12 allow "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

        hbox:
            xalign 0.5
            spacing 100

            textbutton _("OK") action ok_action

init -501 screen dialog(message, ok_action):

    modal True

    zorder 200

    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:
        has vbox:
            xalign .5
            yalign .5
            spacing 30

        label _(message):
            style "confirm_prompt"
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 100

            textbutton _("OK") action ok_action

init -501 screen quit_dialog(message, ok_action):

    modal True

    zorder 200

    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:
        has vbox:
            xalign .5
            yalign .5
            spacing 30

        label _(message):
            style "confirm_prompt"
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 100

            textbutton _("SALIR") action ok_action

init 499 image confirm_glitch:
    "gui/overlay/confirm_glitch.png"
    pause 0.02
    "gui/overlay/confirm_glitch2.png"
    pause 0.02
    repeat

init -501 screen confirm(message, yes_action, no_action):

    modal True

    zorder 200

    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:
        has vbox:
            xalign .5
            yalign .5
            spacing 30

        if in_sayori_kill and message == layout.QUIT:
            add "confirm_glitch" xalign 0.5

        else:
            label _(message):
                style "confirm_prompt"
                xalign 0.5

        hbox:
            xalign 0.5
            spacing 100

            if mas_in_finalfarewell_mode:
                textbutton _("-") action yes_action
                textbutton _("-") action yes_action
            else:
                textbutton _("Sí") action [SetField(persistent, "_mas_game_crashed", False), Show(screen="quit_dialog", message=layout.QUIT_YES, ok_action=yes_action)]
                textbutton _("No") action no_action, Show(screen="dialog", message=layout.QUIT_NO, ok_action=Hide("dialog"))





init -1 style confirm_frame is gui_frame:
    background Frame(["gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    align (0.5, 0.5)

init -1 style confirm_frame_dark is gui_frame:
    background Frame(["gui/confirm_frame.png", "gui/frame_d.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    align (0.5, 0.5)

init -1 style confirm_prompt is gui_prompt

init -1 style confirm_prompt_text is gui_prompt_text:
    color "#000"
    outlines []
    text_align 0.5
    layout "subtitle"

init -1 style confirm_prompt_text_dark is gui_prompt_text:
    color "#FD5BA2"
    outlines []
    text_align 0.5
    layout "subtitle"

init -1 style confirm_button is gui_medium_button:
    properties gui.button_properties("confirm_button")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

init -1 style confirm_button_text is navigation_button_text:
    properties gui.button_text_properties("confirm_button")



init -501 screen update_check(ok_action, cancel_action, mode):


    modal True

    zorder 200

    style_prefix "update_check"
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:

        has vbox:
            xalign .5
            yalign .5
            spacing 30

        if mode == 0:
            label _('¡Una actualización ya está disponible!'):
                style "confirm_prompt"
                xalign 0.5

        elif mode == 1:
            label _("No hay ninguna actualización disponible."):
                style "confirm_prompt"
                xalign 0.5

        elif mode == 2:
            label _('Buscando actualizaciones...'):
                style "confirm_prompt"
                xalign 0.5
        else:

            label _('El tiempo de espera se prolongó mientras se buscaban actualizaciones. Inténtalo de nuevo más tarde.'):
                style "confirm_prompt"
                xalign 0.5

        hbox:
            xalign 0.5
            spacing 100

            textbutton _("Instalar") action [ok_action, SensitiveIf(mode == 0)]

            textbutton _("Cancelar") action cancel_action

    timer 1.0 action Return("None")





init -1 style update_check_frame is confirm_frame
init -1 style update_check_prompt is confirm_prompt
init -1 style update_check_prompt_text is confirm_prompt_text
init -1 style update_check_button is confirm_button
init -1 style update_check_button_text is confirm_button_text





init -501 screen updater:
    modal True

    style_prefix "updater"

    frame:
        has side "t c b":
            spacing gui._scale(10)

        label _("Actualizador")

        fixed:
            vbox:
                if u.state == u.ERROR:
                    text _("Ha ocurrido un error:")
                elif u.state == u.CHECKING:
                    text _("Buscando actualizaciones.")
                elif u.state == u.UPDATE_AVAILABLE:
                    text _("La versión [u.version] está disponible. ¿Quieres instalarla?")

                elif u.state == u.UPDATE_NOT_AVAILABLE:
                    text _("Monika After Story está actualizado.")
                elif u.state == u.PREPARING:
                    text _("Preparándose para descargar las actualizaciones.")
                elif u.state == u.DOWNLOADING:
                    text _("Descargando las actualizaciones. (La barra de progreso puede no avanzar durante la descarga)")
                elif u.state == u.UNPACKING:
                    text _("Desempaquetando las actualizaciones.")
                elif u.state == u.FINISHING:
                    text _("Terminando.")
                elif u.state == u.DONE:
                    text _(_TXT_FINISHED_UPDATING)
                elif u.state == u.DONE_NO_RESTART:
                    text _("Las actualizaciones han sido instaladas.")
                elif u.state == u.CANCELLED:
                    text _("Las actualizaciones fueron canceladas.")

                if u.message is not None:
                    null height gui._scale(10)
                    text "[u.message!q]"

                if u.progress is not None:
                    null height gui._scale(10)
                    bar value u.progress range 1.0 left_bar Solid("#cc6699") right_bar Solid("#ffffff" if not mas_globals.dark_mode else "#13060d") thumb None

        hbox:
            spacing gui._scale(25)

            if u.can_proceed:
                textbutton _("Proceder") action u.proceed

            if u.can_cancel:
                textbutton _("Cancelar") action Return()


init -1 style updater_button is confirm_button
init -1 style updater_button_text is navigation_button_text
init -1 style updater_label is gui_label
init -1 style updater_label_text is game_menu_label_text
init -1 style updater_text is gui_text







init -501 screen fake_skip_indicator():
    use skip_indicator

init -501 screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        has hbox:
            spacing 6

        text _("Saltando")

        text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
        text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
        text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"



transform -1 delayed_blink(delay, cycle):
    alpha .5

    pause delay
    block:

        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


init -1 style skip_frame is empty:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

init -1 style skip_text is gui_text:
    size gui.notify_text_size

init -1 style skip_triangle is skip_text:


    font "DejaVuSans.ttf"









init -501 screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text message

    timer 3.25 action Hide('notify')


transform -1 notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


init -1 style notify_frame is empty:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

init -1 style notify_text is gui_text:
    size gui.notify_text_size







init -1 python:

    items = [(_("Introducción"),"example_chapter")
        ,(_("Ruta Parte 1, Cómo hacer un mod"),"tutorial_route_p1")
        ,(_("Ruta Parte 2, Música"),"tutorial_route_p2")
        ,(_("Ruta Parte 3, Escena"),"tutorial_route_p3")
        ,(_("Ruta Parte 4, Diálogo"),"tutorial_route_p4")
        ,(_("Ruta Parte 5, Menu"),"tutorial_route_p5")
        ,(_("Ruta Parte 6, Declaración de la lógica"),"tutorial_route_p6")
        ,(_("Ruta Parte 7, Sprite"),"tutorial_route_p7")
        ,(_("Ruta Parte 8, Posición"),"tutorial_route_p8")
        ,(_("Ruta Parte 9, Final"),"tutorial_route_p9")]












init -1 style classroom_vscrollbar is vscrollbar:
    base_bar Frame("gui/scrollbar/vertical_poem_bar.png", tile=False)

init -1 style classroom_vscrollbar_dark is vscrollbar_dark:
    base_bar Frame("gui/scrollbar/vertical_poem_bar.png", tile=False)




init -1 style scrollable_menu_vbox is vbox:
    xalign 0.5
    ypos 270
    yanchor 0.5
    spacing 5

init -1 style scrollable_menu_button is choice_button:
    xysize (560, None)
    padding (25, 5, 25, 5)

init -1 style scrollable_menu_button_dark is choice_button_dark:
    xysize (560, None)
    padding (25, 5, 25, 5)

init -1 style scrollable_menu_button_text is choice_button_text:
    text_align 0.0
    align (0.0, 0.0)

init -1 style scrollable_menu_button_text_dark is choice_button_text_dark:
    text_align 0.0
    align (0.0, 0.0)

init -1 style scrollable_menu_new_button is scrollable_menu_button

init -1 style scrollable_menu_new_button_dark is scrollable_menu_button_dark

init -1 style scrollable_menu_new_button_text is scrollable_menu_button_text:
    italic True

init -1 style scrollable_menu_new_button_text_dark is scrollable_menu_button_text_dark:
    italic True

init -1 style scrollable_menu_special_button is scrollable_menu_button

init -1 style scrollable_menu_special_button_dark is scrollable_menu_button_dark

init -1 style scrollable_menu_special_button_text is scrollable_menu_button_text:
    bold True

init -1 style scrollable_menu_special_button_text_dark is scrollable_menu_button_text_dark:
    bold True

init -1 style scrollable_menu_crazy_button is scrollable_menu_button

init -1 style scrollable_menu_crazy_button_dark is scrollable_menu_button_dark

init -1 style scrollable_menu_crazy_button_text is scrollable_menu_button_text:
    italic True
    bold True

init -1 style scrollable_menu_crazy_button_text_dark is scrollable_menu_button_text_dark:
    italic True
    bold True


init -1 style twopane_scrollable_menu_vbox is vbox:
    xalign 0.5
    ypos 270
    yanchor 0.5
    spacing 5

init -1 style twopane_scrollable_menu_button is choice_button:
    xysize (250, None)
    padding (25, 5, 25, 5)

init -1 style twopane_scrollable_menu_button_dark is choice_button_dark:
    xysize (250, None)
    padding (25, 5, 25, 5)

init -1 style twopane_scrollable_menu_button_text is choice_button_text:
    align (0.0, 0.0)
    text_align 0.0

init -1 style twopane_scrollable_menu_button_text_dark is choice_button_text_dark:
    align (0.0, 0.0)
    text_align 0.0

init -1 style twopane_scrollable_menu_new_button is twopane_scrollable_menu_button

init -1 style twopane_scrollable_menu_new_button_dark is twopane_scrollable_menu_button_dark

init -1 style twopane_scrollable_menu_new_button_text is twopane_scrollable_menu_button_text:
    italic True

init -1 style twopane_scrollable_menu_new_button_text_dark is twopane_scrollable_menu_button_text_dark:
    italic True

init -1 style twopane_scrollable_menu_special_button is twopane_scrollable_menu_button

init -1 style twopane_scrollable_menu_special_button_dark is twopane_scrollable_menu_button_dark

init -1 style twopane_scrollable_menu_special_button_text is twopane_scrollable_menu_button_text:
    bold True

init -1 style twopane_scrollable_menu_special_button_text_dark is twopane_scrollable_menu_button_text_dark:
    bold True


init -1 style check_scrollable_menu_button is scrollable_menu_button:
    foreground "mod_assets/buttons/checkbox/[prefix_]check_fg.png"
    padding (33, 5, 25, 5)

init -1 style check_scrollable_menu_button_dark is scrollable_menu_button_dark:
    foreground "mod_assets/buttons/checkbox/[prefix_]check_fg_d.png"
    padding (33, 5, 25, 5)

init -1 style check_scrollable_menu_button_text is scrollable_menu_button_text
init -1 style check_scrollable_menu_button_text_dark is scrollable_menu_button_text_dark
init -1 style check_scrollable_menu_new_button is scrollable_menu_new_button
init -1 style check_scrollable_menu_new_button_dark is scrollable_menu_new_button_dark
init -1 style check_scrollable_menu_new_button_text is scrollable_menu_new_button_text
init -1 style check_scrollable_menu_new_button_text_dark is scrollable_menu_new_button_text_dark
init -1 style check_scrollable_menu_special_button is scrollable_menu_special_button
init -1 style check_scrollable_menu_special_button_dark is scrollable_menu_special_button_dark
init -1 style check_scrollable_menu_special_button_text is scrollable_menu_special_button_text
init -1 style check_scrollable_menu_special_button_text_dark is scrollable_menu_special_button_text_dark
init -1 style check_scrollable_menu_crazy_button is scrollable_menu_crazy_button
init -1 style check_scrollable_menu_crazy_button_dark is scrollable_menu_crazy_button_dark
init -1 style check_scrollable_menu_crazy_button_text is scrollable_menu_crazy_button_text
init -1 style check_scrollable_menu_crazy_button_text_dark is scrollable_menu_crazy_button_text_dark


define -1 prev_adj = ui.adjustment()
define -1 main_adj = ui.adjustment()



init -501 screen twopane_scrollable_menu(prev_items, main_items, left_area, left_align, right_area, right_align, cat_length):
    on "hide" action Function(store.main_adj.change, 0)

    style_prefix "twopane_scrollable_menu"

    fixed:
        anchor (0, 0)
        pos (left_area[0], left_area[1])
        xsize left_area[2]

        if cat_length != 1:
            ysize left_area[3]
        else:
            ysize left_area[3] + evhand.LEFT_EXTRA_SPACE

        bar:
            adjustment prev_adj
            style "classroom_vscrollbar"
            xalign left_align

        vbox:
            ypos 0
            yanchor 0

            viewport:
                yadjustment prev_adj
                yfill False
                mousewheel True
                arrowkeys True

                has vbox
                for i_caption, i_label in prev_items:
                    textbutton i_caption:
                        if renpy.has_label(i_label) and not seen_event(i_label):
                            style "twopane_scrollable_menu_new_button"

                        elif not renpy.has_label(i_label):
                            style "twopane_scrollable_menu_special_button"

                        action Return(i_label)

            if cat_length != 1:
                null height 20

                if cat_length == 0:
                    textbutton _("No importa.") action [Return(False), Function(store.prev_adj.change, 0)]

                elif cat_length > 1:
                    textbutton _("Vuelve atrás") action [Return(-1), Function(store.prev_adj.change, 0)]

    if main_items:
        fixed:
            area right_area

            bar:
                adjustment main_adj
                style "classroom_vscrollbar"
                xalign right_align

            vbox:
                ypos 0
                yanchor 0

                viewport:
                    yadjustment main_adj
                    yfill False
                    mousewheel True
                    arrowkeys True

                    has vbox
                    for i_caption, i_label in main_items:
                        textbutton i_caption:
                            if renpy.has_label(i_label) and not seen_event(i_label):
                                style "twopane_scrollable_menu_new_button"

                            elif not renpy.has_label(i_label):
                                style "twopane_scrollable_menu_special_button"

                            action [Return(i_label), Function(store.prev_adj.change, 0)]

                null height 20

                textbutton _("No importa.") action [Return(False), Function(store.prev_adj.change, 0)]


init -501 screen scrollable_menu(items, display_area, scroll_align, nvm_text, remove=None):
    style_prefix "scrollable_menu"

    fixed:
        area display_area

        vbox:
            ypos 0
            yanchor 0

            viewport:
                id "viewport"
                yfill False
                mousewheel True

                has vbox
                for i_caption, i_label in items:
                    textbutton i_caption:
                        if renpy.has_label(i_label) and not seen_event(i_label):
                            style "scrollable_menu_new_button"

                        elif not renpy.has_label(i_label):
                            style "scrollable_menu_special_button"

                        action Return(i_label)

            null height 20

            if remove:

                textbutton _(remove[0]) action Return(remove[1])

            textbutton _(nvm_text) action Return(False)

        bar:
            style "classroom_vscrollbar"
            value YScrollValue("viewport")
            xalign scroll_align

























init -501 screen mas_gen_scrollable_menu(items, display_area, scroll_align, *args):
    style_prefix "scrollable_menu"

    fixed:
        area display_area

        vbox:
            ypos 0
            yanchor 0

            viewport:
                id "viewport"
                yfill False
                mousewheel True

                has vbox
                for item_prompt, item_value, is_italic, is_bold in items:
                    textbutton item_prompt:
                        if is_italic and is_bold:
                            style "scrollable_menu_crazy_button"

                        elif is_italic:
                            style "scrollable_menu_new_button"

                        elif is_bold:
                            style "scrollable_menu_special_button"

                        xsize display_area[2]
                        action Return(item_value)

            for final_items in args:
                if final_items[4] > 0:
                    null height final_items[4]

                textbutton _(final_items[0]):
                    if final_items[2] and final_items[3]:
                        style "scrollable_menu_crazy_button"

                    elif final_items[2]:
                        style "scrollable_menu_new_button"

                    elif final_items[3]:
                        style "scrollable_menu_special_button"

                    xsize display_area[2]
                    action Return(final_items[1])

        bar:
            style "classroom_vscrollbar"
            value YScrollValue("viewport")
            xalign scroll_align




















init -501 screen mas_check_scrollable_menu(items, display_area, scroll_align, selected_button_prompt="Done", default_button_prompt="Nevermind", return_all=False
):






    default buttons_data = {
        _tuple[1]: {
            "return_value": _tuple[3] if _tuple[2] else _tuple[4],
            "true_value": _tuple[3],
            "false_value": _tuple[4]
        }
        for _tuple in items
    }

    style_prefix "check_scrollable_menu"

    fixed:
        area display_area

        vbox:
            ypos 0
            yanchor 0

            viewport:
                id "viewport"
                yfill False
                mousewheel True

                has vbox
                for button_prompt, button_key, start_selected, true_value, false_value in items:
                    textbutton button_prompt:
                        selected buttons_data[button_key]["return_value"] == buttons_data[button_key]["true_value"]
                        xsize display_area[2]
                        action ToggleDict(
                                buttons_data[button_key],
                                "return_value",
                                true_value,
                                false_value
                            )

            null height 20

            textbutton store.mas_ui.check_scr_menu_choose_prompt(buttons_data, selected_button_prompt, default_button_prompt):
                style "scrollable_menu_button"
                xsize display_area[2]
                action Function(
                    store.mas_ui.check_scr_menu_return_values,
                    buttons_data,
                    return_all
                )

        bar:
            style "classroom_vscrollbar"
            value YScrollValue("viewport")
            xalign scroll_align







init -501 screen mas_background_timed_jump(timeout, timeout_label):
    timer timeout action Jump(timeout_label)


init -501 screen mas_generic_restart:




    modal True

    zorder 200

    style_prefix "confirm"
    add mas_ui.cm_bg

    frame:

        has vbox:
            xalign .5
            yalign .5
            spacing 30




        label _("Por favor, reinicia Monika After Story."):
            style "confirm_prompt"
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 100

            textbutton _("OK") action Return(True)



init -1 python:
    class PauseDisplayable(renpy.Displayable):
        """
        Pause until click variant of Pause
        This is because normal pause until click is broken for some reason
        """
        import pygame
        
        def __init__(self):
            super(renpy.Displayable, self).__init__()
        
        def render(self, width, height, st, at):
            
            return renpy.Render(width, height)
        
        def event(self, ev, x, y, st):
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button not in (4, 5):
                return True
            
            raise renpy.IgnoreEvent()






init -501 screen mas_generic_poem(_poem, paper="paper", _styletext="monika_text"):
    style_prefix "poem"
    vbox:
        add paper
    viewport id "vp":
        child_size (710, None)
        mousewheel True
        draggable True
        has vbox
        null height 40
        text "{0}\n\n{1}".format(renpy.substitute(_poem.title), renpy.substitute(_poem.text)) style _styletext
        null height 100
    vbar value YScrollValue(viewport="vp") style "poem_vbar"


init -1 style chibika_note_text:
    font "gui/font/Halogen.ttf"
    size 28
    color "#000"
    outlines []


init -501 screen submods() tag menu:


    use game_menu(("Submods")):

        default tooltip = Tooltip("")

        viewport id "scrollme":
            scrollbars "vertical"
            mousewheel True
            draggable True

            has vbox:
                style_prefix "check"
                xfill True
                xmaximum 1000

            for submod in sorted(store.mas_submod_utils.submod_map.values(), key=lambda x: x.name):
                vbox:
                    xfill True
                    xmaximum 1000

                    label submod.name:
                        yanchor 0
                        xalign 0
                        text_text_align 0.0

                    if submod.coauthors:
                        $ authors = "v{0}{{space=20}}by {1}, {2}".format(submod.version, submod.author, ", ".join(submod.coauthors))

                    else:
                        $ authors = "v{0}{{space=20}}by {1}".format(submod.version, submod.author)

                    text "[authors]":
                        yanchor 0
                        xalign 0
                        text_align 0.0
                        layout "greedy"
                        style "main_menu_version"

                    if submod.description:
                        text submod.description text_align 0.0

                if submod.settings_pane:
                    $ renpy.display.screen.use_screen(submod.settings_pane, _name="{0}_{1}".format(submod.author, submod.name))

    text tooltip.value:
        xalign 0 yalign 1.0
        xoffset 300 yoffset -10
        style "main_menu_version"
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
