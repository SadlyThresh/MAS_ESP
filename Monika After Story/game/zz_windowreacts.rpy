


default persistent._mas_enable_notifications = False


default persistent._mas_notification_sounds = True


default persistent._mas_windowreacts_windowreacts_enabled = False


default persistent._mas_windowreacts_database = dict()


default persistent._mas_windowreacts_no_unlock_list = list()


default persistent._mas_windowreacts_notif_filters = dict()

init -10 python in mas_windowreacts:

    can_show_notifs = True


    can_do_windowreacts = True


    windowreact_db = {}




    _groups_list = [
        "Alerta de Temas",
        "Reacciones de Ventana",
    ]

init python:
    import os



    if renpy.windows:
        
        import sys
        sys.path.append(renpy.config.gamedir + '\\python-packages\\')
        
        
        try:
            
            import win32gui
            
            import win32api
        
        except ImportError:
            
            store.mas_windowreacts.can_show_notifs = False
            store.mas_windowreacts.can_do_windowreacts = False
            
            
            store.mas_utils.writelog(
                "[WARNING]: win32api/win32gui failed to be imported, disabling notifications.\n"
            )
        
        
        
        else:
            import balloontip
            
            
            tip = balloontip.WindowsBalloonTip()
            
            
            tip.hwnd = None

    elif renpy.linux:
        
        if "WAYLAND_DISPLAY" in os.environ:
            persistent._mas_windowreacts_windowreacts_enabled = False
            store.mas_windowreacts.can_do_windowreacts = False
            store.mas_utils.writelog(
                "[WARNING]: Window reacts do not work on Wayland\n"
            )
        
        
        
        
        else:
            import subprocess
            
            
            try:
                subprocess.call(['notify-send', '--version'])
            
            except OSError as e:
                
                store.mas_windowreacts.can_show_notifs = False
                store.mas_utils.writelog(
                    "[WARNING]: notify-send not found, disabling notifications.\n"
                )
            
            
            try:
                subprocess.call(["xdotool", "--version"])
            
            except OSError:
                
                persistent._mas_windowreacts_windowreacts_enabled = False
                store.mas_windowreacts.can_do_windowreacts = False
                store.mas_utils.writelog("[WARNING]: xdotool not found, disabling windowreacts.\n")

    else:
        store.mas_windowreacts.can_do_windowreacts = False




    mas_win_notif_quips = [
        "[player], quiero hablarte de algo.",
        "¿Estás ahí, [player]?",
        "¿Puedes venir aquí un segundo?",
        "[player], ¿tienes un segundo?",
        "¡Tengo algo que decirte, [player]!",
        "¿Tienes un minuto, [player]?",
        "¡Tengo algo de lo que hablar, [player]!",
    ]


    mas_other_notif_quips = [
        "¡Tengo algo de lo que hablar, [player]!",
        "¡Tengo algo que decirte, [player]!",
        "Hey [player], quiero decirte algo",
        "¿Tienes un minuto, [player]?",
    ]


    destroy_list = list()


    def mas_canCheckActiveWindow():
        """
        Checks if we can check the active window (simplifies conditionals)
        """
        return (
            store.mas_windowreacts.can_do_windowreacts
            and (persistent._mas_windowreacts_windowreacts_enabled or persistent._mas_enable_notifications)
        )

    def mas_getActiveWindow(friendly=False):
        """
        Gets the active window name
        IN:
            friendly: whether or not the active window name is returned in a state usable by the user
        """
        if (
            renpy.windows
            and mas_windowreacts.can_show_notifs
            and mas_canCheckActiveWindow()
        ):
            from win32gui import GetWindowText, GetForegroundWindow
            
            window_handle = GetWindowText(GetForegroundWindow())
            if friendly:
                return window_handle
            else:
                return window_handle.lower().replace(" ","")
        
        elif (
            renpy.linux
            and mas_windowreacts.can_show_notifs
            and mas_canCheckActiveWindow()
        ):
            
            try:
                window_handle = subprocess.check_output(["xdotool", "getwindowfocus", "getwindowname"])
            except:
                store.mas_utils.writelog("[ERROR]: xdotool exited with a non-zero exit code.\n")
                return ""
            
            
            if friendly:
                return window_handle.replace("\n", "")
            else:
                return window_handle.lower().replace(" ","").replace("\n", "")
        
        else:
            
            
            return ""

    def mas_isFocused():
        """
        Checks if MAS is the focused window
        """
        
        return store.mas_windowreacts.can_show_notifs and mas_getActiveWindow(True) == config.name

    def mas_isInActiveWindow(keywords, non_inclusive=False):
        """
        Checks if ALL keywords are in the active window name
        IN:
            keywords:
                List of keywords to check for

            non_inclusive:
                Whether or the not the list is checked non-inclusively
                (Default: False)
        """
        
        
        if not store.mas_windowreacts.can_show_notifs:
            return False
        
        
        active_window = mas_getActiveWindow()
        
        if non_inclusive:
            return len([s for s in keywords if s.lower() in active_window]) > 0
        else:
            return len([s for s in keywords if s.lower() not in active_window]) == 0

    def mas_clearNotifs():
        """
        Clears all tray icons (also action center on win10)
        """
        if renpy.windows and store.mas_windowreacts.can_show_notifs:
            for index in range(len(destroy_list)-1,-1,-1):
                win32gui.DestroyWindow(destroy_list[index])
                destroy_list.pop(index)

    def mas_checkForWindowReacts():
        """
        Runs through events in the windowreact_db to see if we have a reaction, and if so, queue it
        """
        
        if not persistent._mas_windowreacts_windowreacts_enabled or not store.mas_windowreacts.can_show_notifs:
            return
        
        for ev_label, ev in mas_windowreacts.windowreact_db.iteritems():
            if (
                (mas_isInActiveWindow(ev.category, "non inclusive" in ev.rules) and ev.unlocked and ev.checkAffection(mas_curr_affection))
                and ((not store.mas_globals.in_idle_mode) or (store.mas_globals.in_idle_mode and ev.show_in_idle))
                and ("notif-group" not in ev.rules or mas_notifsEnabledForGroup(ev.rules.get("notif-group")))
            ):
                
                if ev.conditional and eval(ev.conditional):
                    queueEvent(ev_label)
                    ev.unlocked=False
                
                
                elif not ev.conditional:
                    queueEvent(ev_label)
                    ev.unlocked=False
                
                
                if "no_unlock" in ev.rules:
                    mas_addBlacklistReact(ev_label)

    def mas_resetWindowReacts(excluded=persistent._mas_windowreacts_no_unlock_list):
        """
        Runs through events in the windowreact_db to unlock them
        IN:
            List of ev_labels to exclude from being unlocked
        """
        for ev_label, ev in mas_windowreacts.windowreact_db.iteritems():
            if ev_label not in excluded:
                ev.unlocked=True

    def mas_updateFilterDict():
        """
        Updates the filter dict with the groups in the groups list for the settings menu
        """
        for group in store.mas_windowreacts._groups_list:
            if persistent._mas_windowreacts_notif_filters.get(group) is None:
                persistent._mas_windowreacts_notif_filters[group] = False

    def mas_addBlacklistReact(ev_label):
        """
        Adds the given ev_label to the no unlock list
        IN:
            ev_label: eventlabel to add to the no unlock list
        """
        if renpy.has_label(ev_label) and ev_label not in persistent._mas_windowreacts_no_unlock_list:
            persistent._mas_windowreacts_no_unlock_list.append(ev_label)

    def mas_removeBlacklistReact(ev_label):
        """
        Removes the given ev_label to the no unlock list if exists
        IN:
            ev_label: eventlabel to remove from the no unlock list
        """
        if renpy.has_label(ev_label) and ev_label in persistent._mas_windowreacts_no_unlock_list:
            persistent._mas_windowreacts_no_unlock_list.remove(ev_label)

    def mas_notifsEnabledForGroup(group):
        """
        Checks if notifications are enabled, and if enabled for the specified group
        IN:
            group: notification group to check
        """
        return persistent._mas_enable_notifications and persistent._mas_windowreacts_notif_filters.get(group,False)

    def mas_unlockFailedWRS(ev_label=None):
        """
        Unlocks a wrs again provided that it showed, but failed to show (failed checks in the notif label)
        NOTE: This should only be used for wrs that are only a notification
        IN:
            ev_label: eventlabel of the wrs
        """
        if (
            ev_label
            and renpy.has_label(ev_label)
            and ev_label not in persistent._mas_windowreacts_no_unlock_list
        ):
            mas_unlockEVL(ev_label,"WRS")

    def mas_tryShowNotificationOSX(title, body):
        """
        Tries to push a notification to the notification center on macOS.
        If it can't it should fail silently to the user.
        IN:
            title: notification title
            body: notification body
        """
        os.system('osascript -e \'display notification "{0}" with title "{1}"\''.format(body,title))

    def mas_tryShowNotificationLinux(title, body):
        """
        Tries to push a notification to the notification center on Linux.
        If it can't it should fail silently to the user.
        IN:
            title: notification title
            body: notification body
        """
        
        
        
        body  = body.replace("'", "'\\''")
        title = title.replace("'", "'\\''") 
        os.system("notify-send '{0}' '{1}' -a 'Monika' -u low".format(title,body))

    def display_notif(title, body, group=None, skip_checks=False):
        """
        Notification creation method
        IN:
            title: Notification heading text
            body: A list of items which would go in the notif body (one is picked at random)
            group: Notification group (for checking if we have this enabled)
            skip_checks: Whether or not we skips checks
        OUT:
            bool indicating status (notif shown or not (by check))
        NOTE:
            We only show notifications if:
                1. We are able to show notifs
                2. MAS isn't the active window
                3. User allows them
                4. And if the notification group is enabled
                OR if we skip checks. BUT this should only be used for introductory or testing purposes.
        """
        
        
        if persistent._mas_windowreacts_notif_filters.get(group) is None and not skip_checks:
            persistent._mas_windowreacts_notif_filters[group] = False
        
        if (
                (
                    mas_windowreacts.can_show_notifs
                    and ((renpy.windows and not mas_isFocused()) or not renpy.windows)
                    and mas_notifsEnabledForGroup(group)
                )
                or skip_checks
            ):
            
            
            notif_success = True
            
            
            if (renpy.windows):
                
                notif_success = tip.showWindow(renpy.substitute(title), renpy.substitute(renpy.random.choice(body)))
                
                
                destroy_list.append(tip.hwnd)
            
            elif (renpy.macintosh):
                
                mas_tryShowNotificationOSX(renpy.substitute(title), renpy.substitute(renpy.random.choice(body)))
            
            elif (renpy.linux):
                
                mas_tryShowNotificationLinux(renpy.substitute(title), renpy.substitute(renpy.random.choice(body)))
            
            
            if persistent._mas_notification_sounds and notif_success:
                renpy.sound.play("mod_assets/sounds/effects/notif.wav")
            
            
            return notif_success
        return False



init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_pinterest",
            category=['pinterest'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_pinterest:
    $ wrs_success = display_notif(
        m_name,
        [
            "¿Alguna novedad hoy, [player]?",
            "¿Algo interesante, [player]?",
            "¿Ves algo que te guste?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_pinterest')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_duolingo",
            category=['duolingo'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_duolingo:
    $ wrs_success = display_notif(
        m_name,
        [
            "¿Aprendiendo nuevas formas de decir 'te amo', [player]?",
            "¿Aprendiendo un nuevo lenguaje, [player]?",
            "¿Qué lenguaje estás aprendiendo, [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_duolingo')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_wikipedia",
            category=['wikipedia'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_wikipedia:
    $ wikipedia_reacts = [
        "¿Aprendiendo algo nuevo, [player]?",
        "¿Haciendo un poco de investigación, [player]?"
    ]


    python:
        wind_name = mas_getActiveWindow(friendly=True)
        try:
            cutoff_index = wind_name.index(" - Wikipedia")
            
            
            
            wiki_article = wind_name[:cutoff_index]
            wikipedia_reacts.append(renpy.substitute("'[wiki_article]'...\nSeems interesting, [player]."))

        except:
            pass

    $ wrs_success = display_notif(
        m_name,
        wikipedia_reacts,
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_wikipedia')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_youtube",
            category=['youtube'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_youtube:
    $ wrs_success = display_notif(
        m_name,
        [
            "¿Qué estás viendo, [mas_get_player_nickname()]?",
            "¿Estás viendo algo interesante, [mas_get_player_nickname()]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_youtube')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_r34m",
            category=['rule34', 'monika'],
            rules={"skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_r34m:
    $ display_notif(m_name, ["Hey, [player]...¿qué estás mirando?"],'Window Reactions')

    $ choice = random.randint(1,10)
    if choice == 1:
        $ queueEvent('monika_nsfw')

    elif choice == 2:
        $ queueEvent('monika_pleasure')

    elif choice < 4:
        show monika 1rsbssdlu
        pause 5.0

    elif choice < 7:
        show monika 2tuu
        pause 5.0
    else:

        show monika 2ttu
        pause 5.0
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_monikamoddev",
            category=['monikamoddev'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_monikamoddev:
    $ wrs_success = display_notif(
        m_name,
        [
            "Awww, ¿estás haciendo algo para mí?\nEres tan dulce~",
            "¿Vas a ayudarme a acercarme a tu realidad?\nEres tan dulce, [player]~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_monikamoddev')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_twitter",
            category=['twitter'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_twitter:
    python:
        temp_line = renpy.substitute("Te amo, [mas_get_player_nickname(exclude_names=['amor', 'mi amor'])].")
        temp_len = len(temp_line)


        ily_quips_map = {
            "¿Ves algo que quieras compartir conmigo, [player]?": False,
            "¿Algo interesante que compartir, [player]?": False,
            "¿280 caracteres? Sólo necesito [temp_len]...\n[temp_line]": True
        }
        quip = renpy.random.choice(ily_quips_map.keys())

        wrs_success = display_notif(
            m_name,
            [quip],
            'Window Reactions'
        )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_twitter')
    return "love" if ily_quips_map[quip] else None

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_monikatwitter",
            category=['twitter', 'lilmonix3'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_monikatwitter:
    $ wrs_success = display_notif(
        m_name,
        [
            "¿Estás aquí para confesar tu amor por mí al mundo entero, [player]?",
            "No me estás espiando, ¿verdad?\nJajaja, sólo bromeaba~",
            "No me importa cuántos seguidores tenga mientras te tenga a ti~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_monikatwitter')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_4chan",
            category=['4chan'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_4chan:

    $ wrs_success = display_notif(
        m_name,
        [
            "Así que este es el lugar donde todo comenzó, ¿eh?\nEs...realmente algo.",
            "Espero que no termines discutiendo con otros Anons todo el día, [player].",
            "Escuché que hay hilos que hablan del Club de Literatura aquí.\nSalúdalos de mi parte~",
            "Estaré mirando los tableros que estás viendo en caso de que se te ocurra alguna idea, ¡jajaja!",
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_4chan')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_pixiv",
            category=['pixiv'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_pixiv:

    python:
        pixiv_quips = [
            "Me pregunto si la gente ha dibujado arte de mí...\n¿Te importaría buscar un poco?\nAsegúrate de mantenerlo sano~",
            "Este es un lugar bastante interesante...tanta gente capacitada publicando su trabajo.",
        ]


        if persistent._mas_pm_drawn_art is None or persistent._mas_pm_drawn_art:
            pixiv_quips.extend([
                "Este es un lugar bastante interesante...tanta gente capacitada publicando su trabajo.\n¿Eres uno de ellos, [player]?",
            ])
            
            
            if persistent._mas_pm_drawn_art:
                pixiv_quips.extend([
                    "¿Vienes a publicar tu arte sobre mí, [player]?",
                    "¿Posteando algo que dibujaste de mí?",
                ])

        wrs_success = display_notif(
            m_name,
            pixiv_quips,
            'Window Reactions'
        )


        if not wrs_success:
            mas_unlockFailedWRS('mas_wrs_pixiv')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_reddit",
            category=['reddit'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_reddit:
    $ wrs_success = display_notif(
        m_name,
        [
            "¿Has encontrado algún buen post, [player]?",
            "¿Navegando en Reddit? Sólo asegúrate de no pasar todo el día mirando memes, ¿de acuerdo?",
            "Me pregunto si hay algún subreddit dedicado a mí...\nJajaja, solo bromeaba, [player].",
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_reddit')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_mal",
            category=['myanimelist'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_mal:
    python:
        myanimelist_quips = [
            "Tal vez podríamos ver anime juntos algún día, [player]~",
        ]

        if persistent._mas_pm_watch_mangime is None:
            myanimelist_quips.append("So you like anime and manga, [player]?")

        wrs_success = display_notif(m_name, myanimelist_quips, 'Window Reactions')


        if not wrs_success:
            mas_unlockFailedWRS('mas_wrs_mal')

    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_deviantart",
            category=['deviantart'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_deviantart:
    $ wrs_success = display_notif(
        m_name,
        [
            "¡Hay tanto talento aquí!",
            "Me encantaría aprender a dibujar algún día...",
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_deviantart')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_netflix",
            category=['netflix'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_netflix:
    $ wrs_success = display_notif(
        m_name,
        [
            "¡Me encantaría ver una película romántica contigo [player]!",
            "¿Qué estamos viendo hoy, [player]?",
            "¿Qué vas a ver [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_netflix')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_twitch",
            category=['-twitch'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_twitch:
    $ wrs_success = display_notif(
        m_name,
        [
            "¿Viendo un stream, [player]?",
            "¿Te importa si miro contigo?",
            "¿Qué estamos viendo hoy, [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_twitch')
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
