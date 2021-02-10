init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_pinterest",
            category=['pinterest'],
            rules={
                "notif-group": "Reacciones de Ventana",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_pinterest:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "¿Algo nuevo hoy, [player]?",
            "¿Algo interesante, [player]?",
            "¿Ves algo que te guste?"
        ],
        'Reacciones de Ventana'
    )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_pinterest')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_duolingo",
            category=['duolingo'],
            rules={
                "notif-group": "Reacciones de Ventana",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_duolingo:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Aprender nuevas formas de decir 'te amo', [player]?",
            "¿Aprendiendo un nuevo lenguaje, [player]?",
            "¿Qué idioma estás aprendiendo, [player]?"
        ],
        'Reacciones de Ventana'
    )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_duolingo')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_wikipedia",
            category=['wikipedia'],
            rules={
                "notif-group": "Reacciones de Ventana",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_wikipedia:
    $ wikipedia_reacts = [
        "¿Aprendiendo algo nuevo, [player]?",
        "¿Investigando un poco, [player]?"
    ]

    #Items in here will get the wiki article you're looking at for reacts.
    python:
        wind_name = mas_getActiveWindow(friendly=True)
        try:
            cutoff_index = wind_name.index(" - Wikipedia")

            #If we're still here, we didn't value error
            #Now we get the article
            wiki_article = wind_name[:cutoff_index]

            # May contain clarification in trailing parentheses
            wiki_article = re.sub("\\s*\\(.+\\)$", "", wiki_article)
            wikipedia_reacts.append(renpy.substitute("'[wiki_article]'...\nParece interesante, [player]."))

        except ValueError:
            pass

    $ wrs_success = mas_display_notif(
        m_name,
        wikipedia_reacts,
        'Reacciones de Ventana'
    )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_wikipedia')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_virtualpiano",
            category=["virtual", "piano"],
            rules={
                "notif-group": "Reacciones de Ventana",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_virtualpiano:
    python:
        virtualpiano_reacts = [
            "Awww, ¿vas a tocar para mí?\nEres tan dulce~",
            "¡Toca algo para mí, [player]!"
        ]

        if mas_isGameUnlocked("piano"):
            virtualpiano_reacts.append("¿Supongo que necesitas un piano más grande?\nJajaja~")

        wrs_success = mas_display_notif(
            m_name,
            virtualpiano_reacts,
            'Reacciones de Ventana'
        )

        if not wrs_success:
            mas_unlockFailedWRS('mas_wrs_virtualpiano')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_youtube",
            category=['youtube'],
            rules={
                "notif-group": "Reacciones de Ventana",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_youtube:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "¿Qué estás viendo, [mas_get_player_nickname()]?",
            "¿Estás viendo algo interesante, [mas_get_player_nickname()]?"
        ],
        'Reacciones de Ventana'
    )

    #Unlock again if we failed
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
    $ mas_display_notif(m_name, ["Hey, [player]...¿qué estás mirando?"],'Reacciones de Ventana')

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
            rules={
                "notif-group": "Reacciones de Ventana",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_monikamoddev:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Awww, ¿estás haciendo algo por mí?\nEres tan dulce~",
            "¿Me vas a ayudar a acercarme a tu realidad?\nEres tan dulce, [player]~"
        ],
        'Reacciones de Ventana'
    )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_monikamoddev')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_twitter",
            category=['twitter'],
            rules={
                "notif-group": "Reacciones de Ventana",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_twitter:
    python:
        temp_line = renpy.substitute("Te amo, [mas_get_player_nickname(exclude_names=['amor', 'mi amor'])].")
        temp_len = len(temp_line)

        # quip: is_ily
        ily_quips_map = {
            "¿Ves algo que quieras compartir conmigo, [player]?": False,
            "¿Algo interesante que compartir, [player]?": False,
            "¿280 caracteres? Sólo necesito [temp_len]...\n[temp_line]": True
        }
        quip = renpy.random.choice(ily_quips_map.keys())

        wrs_success = mas_display_notif(
            m_name,
            [quip],
            'Reacciones de Ventana'
        )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_twitter')
    return "love" if ily_quips_map[quip] else None

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_monikatwitter",
            category=['twitter', 'lilmonix3'],
            rules={
                "notif-group": "Reacciones de Ventana",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_monikatwitter:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "¿Estás aquí para confesar tu amor por mí a todo el mundo, [player]?",
            "No me estás espiando, ¿verdad?\nJajaja, solo bromeo~",
            "No me importa cuántos seguidores tengo mientras te tenga a ti~"
        ],
        'Reacciones de Ventana'
    )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_monikatwitter')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_4chan",
            category=['4chan'],
            rules={
                "notif-group": "Reacciones de Ventana",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_4chan:
    #TODO: consider adding reactions for /vg/ and /ddlc/
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Así que este es el lugar donde todo comenzó, ¿eh?\nEs... realmente único.",
            "Espero que no acabes discutiendo con otros anons todo el día, [player].",
            "He oído que hay hilos que discuten sobre el Club de Literatura aquí.\nDiles que les mando saludos~",
            "Estaré pendiente de los tableros por los que navegas por si se te ocurre alguna idea, ¡jajaja!",
        ],
        'Reacciones de Ventana'
    )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_4chan')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_pixiv",
            category=['pixiv'],
            rules={
                "notif-group": "Reacciones de Ventana",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_pixiv:
    #Make a list of notif quips for this
    python:
        pixiv_quips = [
            "Me pregunto si la gente ha dibujado arte de mí...\n¿Te importaría buscar algunos?\nSin embargo, asegúrate de mantenerlo sano~",
            "Este es un lugar muy interesante... tanta gente capacitada publicando su trabajo.",
        ]

        #Monika doesn't know if you've drawn art of her, or she knows that you have drawn art of her
        if persistent._mas_pm_drawn_art is None or persistent._mas_pm_drawn_art:
            pixiv_quips.extend([
                "Este es un lugar muy interesante... tanta gente capacitada publicando su trabajo.\n¿Eres uno de ellos, [player]?",
            ])

            #Specifically if she knows you've drawn art of her
            if persistent._mas_pm_drawn_art:
                pixiv_quips.extend([
                    "¿Estás aquí para publicar tu arte de mí, [player]?",
                    "¿Vas a publicar algo que dibujaste de mí?",
                ])

        wrs_success = mas_display_notif(
            m_name,
            pixiv_quips,
            'Reacciones de Ventana'
        )

        #Unlock again if we failed
        if not wrs_success:
            mas_unlockFailedWRS('mas_wrs_pixiv')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_reddit",
            category=['reddit'],
            rules={
                "notif-group": "Reacciones de Ventana",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_reddit:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "¿Ha encontrado algún buen post, [player]?",
            "¿Navegando por Reddit? Asegúrate de no pasarte el día mirando memes, ¿vale?",
            "Me pregunto si hay algún subreddit dedicado a mí...\nJajaja, solo bromeo, [player].",
        ],
        'Reacciones de Ventana'
    )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_reddit')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_mal",
            category=['myanimelist'],
            rules={
                "notif-group": "Reacciones de Ventana",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_mal:
    python:
        myanimelist_quips = [
            "Tal vez podamos ver anime juntos algún día, [player]~",
        ]

        if persistent._mas_pm_watch_mangime is None:
            myanimelist_quips.append("¿Entonces te gusta el anime y el manga, [player]?")

        wrs_success = mas_display_notif(m_name, myanimelist_quips, 'Reacciones de Ventana')

        #Unlock again if we failed
        if not wrs_success:
            mas_unlockFailedWRS('mas_wrs_mal')

    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_deviantart",
            category=['deviantart'],
            rules={
                "notif-group": "Reacciones de Ventana",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_deviantart:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "¡Hay tanto talento aquí!",
            "Me encantaría aprender a dibujar algún día...",
        ],
        'Reacciones de Ventana'
    )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_deviantart')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_netflix",
            category=['netflix'],
            rules={
                "notif-group": "Reacciones de Ventana",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_netflix:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "¡Me encantaría ver una película romántica contigo [player]!",
            "¿Qué estamos viendo hoy, [player]?",
            "¿Qué vas a ver, [player]?"
        ],
        'Reacciones de Ventana'
    )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_netflix')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_twitch",
            category=['-twitch'],
            rules={
                "notif-group": "Reacciones de Ventana",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_twitch:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "¿Viendo un stream, [player]?",
            "¿Te importa si miro contigo?",
            "¿Qué estamos viendo hoy, [player]?"
        ],
        'Reacciones de Ventana'
    )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_twitch')
    return
