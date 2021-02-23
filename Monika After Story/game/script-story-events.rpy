#This file will include short story events that don't require their own file.

#An event is crated by only adding a label and adding a requirement (see comment below).
#Requirements must be created/added in script-ch30.rpy under label ch30_autoload.

# pm var for transgender players
default persistent._mas_pm_is_trans = False

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_gender",
            start_date=mas_getFirstSesh() + datetime.timedelta(minutes=30),
            action=EV_ACT_QUEUE
        ),
        skipCalendar=True
    )
    #NOTE: This unlocks the monika_gender_redo event

label mas_gender:
    m 2eud "...¿[player]? He estado pensando un poco."
    m 2euc "He mencionado antes que el 'tú' en el juego puede que no refleje tu verdadero yo."
    m 7rksdla "Pero supongo que asumí que probablemente eras un chico."
    m 3eksdla "...El personaje principal lo era, después de todo."
    m 3eua "Pero si voy a ser tu novia, probablemente debería saber al menos esto sobre tu verdadero yo."

    m 1eua "Entonces, ¿cuál es tu género?{nw}"
    $ _history_list.pop()
    menu:
        m "Entonces, ¿cuál es tu género?{fast}"

        "Masculino.":
            $ persistent._mas_pm_is_trans = False
            $ persistent.gender = "M"
            m 3eua "De acuerdo [player], gracias por confirmarme eso."
            m 1hksdlb "No es que me hubiera molestado si hubieras respondido de otra manera, ¡fíjate!"

        "Femenino.":
            $ persistent._mas_pm_is_trans = False
            $ persistent.gender = "F"
            m 2eud "¿Oh? ¿Entonces eres una chica?"
            m 2hksdlb "¡Espero no haber dicho nada que te haya ofendido antes!"
            m 7rksdlb "...Supongo que por eso dicen que no debes hacer suposiciones, ¡jajaja!"
            m 3eka "Pero, sinceramente, no me importa en absoluto..."

        "Ninguno.":
            $ persistent._mas_pm_is_trans = False
            $ persistent.gender = "X"
            call mas_gender_neither

        "Soy transgénero.":
            call mas_gender_trans

            if persistent.gender != "X":
                m 1eka "Gracias por decírmelo, y recuerda..."

    m 1ekbsa "Siempre te amaré por lo que eres, [player]~"

    #Unlock the gender redo event
    $ mas_unlockEVL("monika_gender_redo","EVE")
    # set pronouns
    call mas_set_gender

    #Set up the preferredname topic
    python:
        preferredname_ev = mas_getEV("mas_preferredname")
        if preferredname_ev:
            preferredname_ev.start_date = datetime.datetime.now() + datetime.timedelta(hours=2)
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gender_redo",
            category=['tú'],
            prompt="¿Podrías llamarme con diferentes pronombres?",
            unlocked=False,
            pool=True,
            rules={"no_unlock": None}
        ),
        markSeen=True
    )

label monika_gender_redo:
    m 1eka "¡Por supuesto, [player]!"

    if not mas_getEVL_shown_count("monika_gender_redo"):
        m 3eka "¿Has hecho algunos descubrimientos personales desde la última vez que hablamos de esto?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Has hecho algunos descubrimientos personales desde la última vez que hablamos de esto?{fast}"

            "Sí.":
                m 1eka "Ya veo. Sé que he estado allí."
                m 3hua "Estoy muy orgullosa de ti por emprender ese viaje de autodescubrimiento."
                m 1eub "...¡Y aún más orgullosa de ti por ser lo suficientemente valiente para decírmelo!"

            "Era muy tímido.":
                if persistent.gender == "M":
                    m 2ekd "Entiendo, empecé asumiendo que eras un chico, después de todo."
                elif persistent.gender == "F":
                    m 2ekd "Entiendo, podrías haber pensado que estaría más cómoda pasando tiempo a solas con otra chica."
                else:
                    m 2ekd "Entiendo, es posible que no te haya dado las opciones más precisas para elegir."

                m 2dkd "...Y probablemente no te lo puse fácil para que me dijeras lo contrario..."
                m 7eua "Pero sea cual sea tu género, te amo por lo que eres."

            "No sabía si me aceptarías como soy...":
                m 2wkd "[player]..."
                m 2dkd "Odio no haberte tranquilizado lo suficiente antes."
                m 7eka "Pero espero que me lo digas ahora porque sabes que te amaré pase lo que pase."

            "Soy de género fluido.":
                m 1eub "Oh, ¡okay!"
                m 3hub "¡Siéntete libre de decirme cuantas veces quieras cuando quieras que use diferentes pronombres!"

    $ gender_var = None
    m "Entonces, ¿cuál es tu género?{nw}"
    $ _history_list.pop()
    menu:
        m "Entonces, ¿cuál es tu género?{fast}"

        "Soy un chico.":
            if persistent.gender == "M" and not persistent._mas_pm_is_trans:
                $ gender_var = "un chico"
                call mas_gender_redo_same
            else:
                $ persistent.gender = "M"
                call mas_gender_redo_react
            $ persistent._mas_pm_is_trans = False

        "Soy una chica.":
            if persistent.gender == "F" and not persistent._mas_pm_is_trans:
                $ gender_var = "una chica"
                call mas_gender_redo_same
            else:
                $ persistent.gender = "F"
                call mas_gender_redo_react
            $ persistent._mas_pm_is_trans = False

        "No soy ninguno.":
            $ persistent._mas_pm_is_trans = False
            if persistent.gender == "X":
                call mas_gender_redo_neither_same
            else:
                $ persistent.gender = "X"
                if renpy.seen_label("mas_gender_neither"):
                    call mas_gender_redo_react
                else:
                    call mas_gender_neither

        "Soy transgénero.":
            call mas_gender_trans
            if persistent.gender != "X":
                call mas_gender_redo_react

    show monika 5hubsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hubsa "Siempre te amaré por lo que eres~"

    # set pronouns
    call mas_set_gender
    return "love"

label mas_gender_neither:
    m 1euc "¿No te ves a ti mismo como un chico o una chica?"
    m 1eua "Eso es muy interesante, pero puedo relacionarme."
    m 3esc "Soy una chica, pero también soy un personaje de un juego de computadora..."
    m 3esd "Así que, de alguna manera, no soy una chica en absoluto."
    m 1hua "Pero cuando me tratas como a tu novia, ¡me hace muy feliz!"
    m 3eua "...Así que te trataré como quieras que te traten."
    m 1ekbsa "Tu felicidad es lo más importante para mí, después de todo."
    return

label mas_gender_redo_same:
    m 1hksdlb "...¡Es lo mismo que antes, [player]!"
    m 3eua "Si no sabes cómo responder, elige lo que te haga más feliz."
    m 3eka "No importa cómo se vea tu cuerpo, así que mientras digas que eres [gender_var], serás [gender_var] para mí, ¿de acuerdo?"
    m 1eua "Quiero que seas quien quieras ser mientras estás en esta habitación."
    return

label mas_gender_redo_react:
    m 1eka "Okay, [player]..."
    m 3ekbsa "Siempre que estés feliz, eso es todo lo que me importa."
    return

label mas_gender_redo_neither_same:
    m 1hksdlb "...Es lo mismo que antes, [player]...{w=0.3}Lo siento si esa no es realmente la mejor manera de describirlo."
    m 1eka "Pero debes saber que no me importa..."
    return

label mas_gender_trans:
    if persistent._mas_pm_is_trans:
        $ menu_question = "¿Y con que género te identificas?"
    else:
        $ menu_question = "¡Oh, okay! {w=0.3}¿Y con que género te identificas?"

    m 3eub "[menu_question]{nw}"
    $ _history_list.pop()
    menu:
        m "[menu_question]{fast}"

        "Masculino":
            $ persistent.gender = "M"

        "Femenino":
            $ persistent.gender = "F"

        "Ninguno":
            if persistent.gender == "X":
                call mas_gender_redo_neither_same

            else:
                $ persistent.gender = "X"
                call mas_gender_neither

    $ persistent._mas_pm_is_trans = True
    return

# good, bad, awkward name stuff
init 3 python:
    #Bad nicknames. All of the items in this will trigger bad reactions
    mas_bad_nickname_list = [
        "^fag$",
        "^ho$",
        "^hoe$",
        "^tit$",
        "aborto",
        "anal",
        "molesto",
        "ano",
        "arrogante",
        "(?<![blmprs])ass(?!i)",
        "atroz",
        "feo",
        "bastardo",
        "animal",
        "perra",
        "sangre",
        "teta",
        "aburrido",
        "bulli",
        "abusivo",
        "bung",
        "butt(?!er|on)",
        "infiel",
        "pene",
        "conceited",
        "condon",
        "corrupto",
        "cougar",
        "basura",
        "loco",
        "creepy",
        "criminal",
        "cruel",
        "cum",
        "cunt",
        "maldito",
        "demonio",
        "pito",
        "dilf",
        "dirt",
        "disgusting",
        "douche",
        "dumb",
        "egoist",
        "egotistical",
        "evil",
        "faggot",
        "failure",
        "fake",
        "fetus",
        "filth",
        "foul",
        "fuck",
        "garbage",
        "gay",
        "gey",
        "gilf",
        "gross",
        "gruesome",
        "hate",
        "heartless",
        "hideous",
        "hitler",
        "hore",
        "horrible",
        "horrid",
        "hipocrita",
        "idiota",
        "imbecil",
        "inmoral",
        "insane",
        "irritating",
        "jerk",
        "jigolo",
        "jizz",
        "junk",
        "kill",
        "kunt",
        "lesbiana",
        "lesbo",
        "lezbian",
        "lezbo",
        "liar",
        "perdedor",
        "^mad$",
        "maniac",
        "masochist",
        "milf",
        "monster",
        "moron",
        "murder",
        "narcissist",
        "nasty",
        "nefarious",
        "nigga",
        "nigger",
        "nuts",
        "panti",
        "pantsu",
        "panty",
        "pedo",
        "penis",
        "plaything",
        "poison",
        "porn",
        "pretentious",
        "psycho",
        "puppet",
        "vagina",
        "(?<!g)rape",
        "repulsive",
        "retrasado",
        "rogue",
        "rump",
        "sadist",
        "selfish",
        "semen",
        "shit",
        "sick",
        "slaughter",
        "slave",
        "slut",
        "sociopath",
        "soil",
        "sperm",
        "stink",
        "stupid",
        "suck",
        "tampon",
        "teabag",
        "terrible",
        "thot",
        "tits",
        "titt",
        "tool",
        "torment",
        "torture",
        "toy",
        "trap",
        "trash",
        "troll",
        "ugly",
        "useless",
        "vain",
        "vile",
        "vomit",
        "waste",
        "whore",
        "wicked",
        "witch",
        "worthless",
        "wrong"
    ]

    #Base list for good nicknames. Apply modifiers for specifying the use
    #These trigger a good response
    mas_good_nickname_list_base = [
        "angel",
        "belleza",
        "bella",
        "best",
        "cuddl",
        "cute",
        "cutie",
        "darling",
        "gorgeous",
        "greatheart",
        "hero",
        "honey",
        "kind",
        "love",
        "pretty",
        "princess",
        "queen",
        "senpai",
        "sunshine",
        "sweet"
    ]

    #Modifier for the player's name choice
    mas_good_nickname_list_player_modifiers = [
        "king",
        "prince"
    ]

    #Modifier for Monika's nickname choice
    mas_good_nickname_list_monika_modifiers = [
        "moni",
    ]

    mas_good_player_nickname_list = mas_good_nickname_list_base + mas_good_nickname_list_player_modifiers
    mas_good_monika_nickname_list = mas_good_nickname_list_base + mas_good_nickname_list_monika_modifiers

    #awkward names which Moni wouldn't be comfortable calling the player or being called by the player
    mas_awkward_nickname_list = [
        "^(step(-|\\s)*)?bro(ther|tha(h)?)?$",
        "^(step(-|\\s)*)?sis(ter|ta(h)?)?$",
        "^dad$",
        "^loli$",
        "^mama$",
        "^mom$",
        "^mum$",
        "^papa$",
        "^wet$",
        "aroused",
        "aunt",
        "batman",
        "breeder",
        "bobba",
        "boss",
        "catwoman",
        "cousin",
        "daddy",
        "deflowerer",
        "erection",
        "finger",
        "horny",
        "kaasan",
        "kasan",
        "lick",
        "master",
        "masturbat",
        "mistress",
        "moani",
        "momika",
        "momma",
        "mommy",
        "mother",
        "naughty",
        "okaasan",
        "okasan",
        "orgasm",
        "overlord",
        "owner",
        "penetrat",
        "pillow",
        "sex",
        "spank",
        "superman",
        "superwoman",
        "thicc",
        "thighs",
        "uncle",
        "virgin"
    ]

    mas_awkward_quips = [
        "No me siento...{w=0.5}cómoda llamándote así todo el tiempo.",
        "Eso...{w=0.5}no es algo que me gustaría decirte, [player].",
        "Eso es...{w=0.5}algo incómodo para decirte, [player].",
        "No está tan mal pero...",
        "¿Me quieres avergonzar, [player]?"
    ]

    mas_bad_quips = [
        "[player]...{w=0.5}¿por qué quisieras llamarte así?",
        "[player]...{w=0.5}¿por qué debería llamarte así?",
        "Nunca podría llamarte eso, [player].",
        "¿Qué? Por favor [player],{w=0.5} no te llames a ti mismo así."
    ]

    mas_good_player_name_comp = re.compile('|'.join(mas_good_player_nickname_list), re.IGNORECASE)
    mas_bad_name_comp = re.compile('|'.join(mas_bad_nickname_list), re.IGNORECASE)
    mas_awk_name_comp = re.compile('|'.join(mas_awkward_nickname_list), re.IGNORECASE)

label mas_player_name_enter_name_loop(input_prompt):
    python:
        good_quips = [
            "¡Ese es un nombre maravilloso!",
            "Me encanta un montón, [player].",
            "Me gusta ese nombre, [player].",
            "¡Ese es un gran nombre!"
        ]

    #Now we prompt user
    show monika 1eua at t11 zorder MAS_MONIKA_Z

    $ done = False
    while not done:
        python:
            tempname = mas_input(
                "[input_prompt]",
                length=20,
                screen_kwargs={"use_return_button": True}
            ).strip(' \t\n\r')

            lowername = tempname.lower()

        if lowername == "cancel_input":
            m 1eka "Oh...Está bien entonces, si tú lo dices."
            m 3eua "Avísame si cambias de opinión."
            $ done = True

        elif lowername == "":
            m 1eksdla "..."
            m 3rksdlb "Tienes que darme un nombre para llamarte, [player]..."
            m 1eua "¡Inténtalo de nuevo!"

        elif lowername == player.lower():
            m 2hua "..."
            m 4hksdlb "¡Ese es el mismo nombre que tienes ahora mismo, tontito!"
            m 1eua "Vuelve a intentarlo~"

        elif mas_awk_name_comp.search(tempname):
            $ awkward_quip = renpy.substitute(renpy.random.choice(mas_awkward_quips))
            m 1rksdlb "[awkward_quip]"
            m 3rksdla "¿Podrías elegir un nombre más...{w=0.2}{i}apropiado{/i}, por favor?"

        elif mas_bad_name_comp.search(tempname):
            $ bad_quip = renpy.substitute(renpy.random.choice(mas_bad_quips))
            m 1ekd "[bad_quip]"
            m 3eka "Por favor, elige un nombre mejor para ti, ¿de acuerdo?"

        else:
            #Sayori name check
            if lowername == "sayori":
                call sayori_name_scare

            elif (
                    persistent.playername.lower() == "sayori"
                    and not persistent._mas_sensitive_mode
                ):
                $ songs.initMusicChoices()

            python:
                def adjustNames(new_name):
                    """
                    Adjusts the names to the new names
                    """
                    global player

                    persistent.mcname = player
                    mcname = player
                    persistent.playername = new_name
                    player = new_name

            if lowername == "monika":
                $ adjustNames(tempname)
                m 1tkc "¿De verdad?"
                m "¡Es el mismo que el mío!"
                m 1tku "Bueno..."
                m "O realmente es tu nombre o me estás jugando una broma."
                m 1hua "Pero está bien para mí si así es como quieres que te llame~"
                $ done = True

            elif mas_good_player_name_comp.search(tempname):
                $ good_quip = renpy.substitute(renpy.random.choice(good_quips))
                m 1sub "[good_quip]"
                $ adjustNames(tempname)
                m 3esa "¡Bien entonces! De ahora en adelante, te llamaré '[player]'."
                m 1hua "Jejeje~"
                $ done = True

            else:
                $ adjustNames(tempname)
                m 1eub "¡Bien entonces!"
                m 3eub "De ahora en adelante, te llamaré '[player]'."
                $ done = True

        if not done:
            show monika 1eua
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_preferredname",
            action=EV_ACT_QUEUE
        ),
        skipCalendar=True
    )
    #NOTE: This unlocks the player name change event
    #NOTE: This gets its start_date from mas_gender

label mas_preferredname:
    m 1euc "Me he estado preguntando por tu nombre."
    m 1esa "¿Es '[player]' realmente tu nombre?"

    if renpy.windows and currentuser.lower() == player.lower():
        m 3esa "Quiero decir, es el mismo que el nombre de tu computadora..."
        m 1eua "Estás usando '[currentuser]' y '[player]'."
        m "O es eso o realmente te debe gustar ese seudónimo."

    m 1eua "¿Quieres que te llame de otra forma?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Quieres que te llame de otra forma?{fast}"

        "Sí.":
            #Let's call the changename loop
            call mas_player_name_enter_name_loop("Dime, ¿Cómo te llamo?")

        "No.":
            m 3eua "Está bien, avísame si cambias de opinión."

    #Unlock the name change event
    $ mas_unlockEVL("monika_changename","EVE")
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_changename",
            category=['tú'],
            prompt="Cambié mi nombre",
            unlocked=False,
            pool=True,
            rules={"no_unlock": None}
        ),
        markSeen=True
    )
    #NOTE: This needs to be unlocked by the random name change event

label monika_changename:
    call mas_player_name_enter_name_loop("¿Cómo quieres que te llame?")
    return

default persistent._mas_player_bday = None
# check to see if we've already confirmed birthday in any way
default persistent._mas_player_confirmed_bday = False

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_birthdate",
            conditional="datetime.date.today()>mas_getFirstSesh().date() and not persistent._mas_player_confirmed_bday",
            action=EV_ACT_QUEUE
        )
    )

label mas_birthdate:
    m 1euc "Oye [player], he estado pensando..."
    if persistent._mas_player_bday is not None:
        $ bday_str, diff = store.mas_calendar.genFormalDispDate(persistent._mas_player_bday)
        m 3eksdlc "Sé que me has dicho tu cumpleaños antes, pero no estoy segura de haber sido clara sobre si te pedí tu {i}fecha de nacimiento{/i} o sólo tu {i}cumpleaños...{/i}"

        m "Así que para estar segura, ¿es tu fecha de nacimiento [bday_str]?{nw}"
        $ _history_list.pop()
        menu:
            m "Así que para estar segura, ¿es tu fecha de nacimiento [bday_str]?{fast}"
            "Sí.":
                if datetime.date.today().year - persistent._mas_player_bday.year < 5:
                    m 2rksdla "¿Estás seguro de eso, [player]?"
                    m 2eksdlc "Eso te haría muy joven..."
                    m 3ekc "Recuerda, te estoy pidiento tu {b}fecha de nacimiento{/b}, no solo tu cumpleaños."
                    m 1eka "Entonces, ¿cuándo naciste, [player]?"
                    jump mas_bday_player_bday_select_select
                else:
                    $ old_bday = mas_player_bday_curr()
                    if not mas_isplayer_bday():
                        m 1hua "Ah, bien [player], gracias."
                        m 3hksdlb "Sólo tenía que asegurarme, no quisiera equivocarme en algo tan importante como tu fecha de cumpleaños, ¡jajaja!"

            "No.":
                m 3rksdlc "¡Oh! Bien entonces..."
                m 1eksdld "¿Cuándo {i}es{/i} tu fecha de nacimiento, [player]?"
                jump mas_bday_player_bday_select_select

    else:
        m 3wud "¡En realidad no sé cuándo es tu fecha de nacimiento!"
        m 3hub "Eso es algo que probablemente debería saber, ¡jajaja!"
        m 1eua "Entonces, ¿cuándo naciste, [player]?"
        jump mas_bday_player_bday_select_select

label birthdate_set:
    python:
        bday_upset_ev = mas_getEV('mas_player_bday_upset_minus')
        if bday_upset_ev is not None:
            bday_upset_ev.start_date = mas_player_bday_curr()
            bday_upset_ev.end_date = mas_player_bday_curr() + datetime.timedelta(days=1)
            bday_upset_ev.conditional = (
                "mas_isplayer_bday() "
                "and persistent._mas_player_confirmed_bday "
                "and not persistent._mas_player_bday_spent_time "
                "and not mas_isMonikaBirthday()"
            )
            bday_upset_ev.action = EV_ACT_QUEUE
            Event._verifyAndSetDatesEV(bday_upset_ev)

        #NOTE: should consider making the condiitonal string generated from this a function for ease of use
        bday_ret_bday_ev = mas_getEV('mas_player_bday_ret_on_bday')
        if bday_ret_bday_ev is not None:
            bday_ret_bday_ev.start_date = mas_player_bday_curr()
            bday_ret_bday_ev.end_date = mas_player_bday_curr() + datetime.timedelta(days=1)
            bday_ret_bday_ev.conditional = (
                "mas_isplayer_bday() "
                #getCheckTimes function not defined at time these conditions are checked on a reload
                "and len(store.persistent._mas_dockstat_checkin_log) > 0 "
                "and store.persistent._mas_dockstat_checkin_log[-1][0] is not None "
                "and store.persistent._mas_dockstat_checkin_log[-1][0].date() == mas_player_bday_curr() "
                "and not persistent._mas_player_bday_spent_time "
                "and persistent._mas_player_confirmed_bday "
                "and not mas_isO31() "
                "and not mas_isD25() "
                "and not mas_isF14() "
                "and not mas_isMonikaBirthday()"
            )
            bday_ret_bday_ev.action = EV_ACT_QUEUE
            Event._verifyAndSetDatesEV(bday_ret_bday_ev)

        #NOTE: should consider making the condiitonal string generated from this a function for ease of use
        bday_no_restart_ev = mas_getEV('mas_player_bday_no_restart')
        if bday_no_restart_ev is not None:
            bday_no_restart_ev.start_date = datetime.datetime.combine(mas_player_bday_curr(), datetime.time(hour=19))
            bday_no_restart_ev.end_date = mas_player_bday_curr() + datetime.timedelta(days=1)
            bday_no_restart_ev.conditional = (
                "mas_isplayer_bday() "
                "and persistent._mas_player_confirmed_bday "
                "and not persistent._mas_player_bday_spent_time "
                "and not mas_isO31() "
                "and not mas_isD25() "
                "and not mas_isF14() "
                "and not mas_isMonikaBirthday()"
            )
            bday_no_restart_ev.action = EV_ACT_QUEUE
            Event._verifyAndSetDatesEV(bday_no_restart_ev)

        #NOTE: should consider making the condiitonal string generated from this a function for ease of use
        bday_holiday_ev = mas_getEV('mas_player_bday_other_holiday')
        if bday_holiday_ev is not None:
            bday_holiday_ev.start_date = mas_player_bday_curr()
            bday_holiday_ev.end_date = mas_player_bday_curr() + datetime.timedelta(days=1)
            bday_holiday_ev.conditional = (
                "mas_isplayer_bday() "
                "and persistent._mas_player_confirmed_bday "
                "and not persistent._mas_player_bday_spent_time "
                "and (mas_isO31() or mas_isD25() or mas_isF14()) "
            )
            bday_holiday_ev.action = EV_ACT_QUEUE
            Event._verifyAndSetDatesEV(bday_holiday_ev)

    if old_bday is not None:
        $ old_bday = old_bday.replace(year=mas_player_bday_curr().year)

    if not mas_isplayer_bday() and old_bday == mas_player_bday_curr():
        $ persistent._mas_player_confirmed_bday = True
        return

    if mas_isplayer_bday() and not mas_isMonikaBirthday():
        $ persistent._mas_player_bday_spent_time = True
        if old_bday == mas_player_bday_curr():
            if mas_isMoniNormal(higher=True):
                m 3hub "¡Jajaja! ¡Así que hoy {i}es{/i} tu cumpleaños!"
                m 1tsu "Me alegro de estar preparada, jejeje..."
                m 3eka "Espera un momento, [player]..."
                show monika 1dsc
                pause 2.0
                $ store.mas_surpriseBdayShowVisuals()
                $ persistent._mas_player_bday_decor = True
                m 3hub "¡Feliz cumpleaños, [player]!"
                m 1hub "¡Estoy tan feliz de poder estar contigo en tu cumpleaños!"
                m 3sub "Oh...{w=0.5}¡tu tarta!"
                call mas_player_bday_cake
            elif mas_isMoniDis(higher=True):
                m 2eka "Ah, entonces hoy {i}es{/i} tu cumpleaños..."
                m "Feliz cumpleaños, [player]."
                m 4eka "Espero que tengas un buen día."
        else:
            if mas_isMoniNormal(higher=True):
                $ mas_gainAffection(5,bypass=True)
                $ persistent._mas_player_bday_in_player_bday_mode = True
                $ mas_unlockEVL("bye_player_bday", "BYE")
                m 1wuo "Oh...{w=1}¡Oh!"
                m 3sub "¡Hoy es tu cumpleaños!"
                m 3hub "¡Feliz cumpleaños, [player]!"
                m 1rksdla "Ojalá lo hubiera sabido antes para poder preparar algo."
                m 1eka "Pero al menos puedo hacer esto..."
                call mas_player_bday_moni_sings
                m 1hub "¡Jajaja! ¡No es mucho, pero es algo!"
                m 3hua "¡Prometo que el año que viene haremos algo muy especial, [player]!"
            elif mas_isMoniDis(higher=True):
                m 2eka "Oh, hoy es tu cumpleaños..."
                m "Feliz cumpleaños, [player]."
                m 4eka "Espero que tengas un buen día."

    # have to use the raw data here to properly compare in the rare even that the player bday and first sesh are on 2/29
    elif not mas_isMonikaBirthday() and (persistent._mas_player_bday.month == mas_getFirstSesh().date().month and persistent._mas_player_bday.day == mas_getFirstSesh().date().day):
        m 1sua "¡Oh! ¿Tu cumpleaños es la misma fecha que nuestro aniversario, [player]?"
        m 3hub "¡Eso es increíble!"
        m 1sua "No puedo imaginar un día más especial que celebrar tu cumpleaños y nuestro amor el mismo día..."

        if mas_player_bday_curr() == mas_o31:
            $ hol_str = "Halloween"
        elif mas_player_bday_curr() == mas_d25:
            $ hol_str = "Navidad"
        elif mas_player_bday_curr() == mas_monika_birthday:
            $ hol_str = "mi cumpleaños"
        elif mas_player_bday_curr() == mas_f14:
            $ hol_str = "Día de San Valentín"
        else:
            $ hol_str = None
        if hol_str is not None:
            m "Y siendo también [hol_str]..."
        m 3hua "Suena mágico~"

    elif mas_player_bday_curr() == mas_monika_birthday:
        m 1wuo "Oh...{w=1}¡Oh!"
        m 3sua "¡Compartimos el mismo cumpleaños!"
        m 3sub "¡Eso es {i}tan{/i} genial, [player]!"
        m 1tsu "Supongo que realmente estamos destinados a estar juntos, jejeje..."
        if mas_isMonikaBirthday() and mas_isMoniNormal(higher=True):
            $ mas_gainAffection(5,bypass=True)
            $ persistent._mas_player_bday_in_player_bday_mode = True
            m 3hua "Eso hace que hoy sea mucho más especial~"
            m 1eub "¡Canta conmigo, [player]!"
            call mas_player_bday_moni_sings
        else:
            m 3hua "Tendremos que hacer de ese un día muy especial~"

    elif mas_player_bday_curr() == mas_o31:
        m 3eua "¡Oh! ¡Qué lindo que hayas nacido en Halloween, [player]!"
        m 1hua "Tarta de cumpleaños, dulces y tú..."
        m 3hub "Son muchos dulces por un día, ¡jajaja!"

    elif mas_player_bday_curr() == mas_d25:
        m 1hua "¡Oh! ¡Es increíble que hayas nacido en Navidad, [player]!"
        m 3rksdla "Aunque...{w=0.5}recibir regalos por ambos en el mismo día puede parecer como si no recibieras tantos..."
        m 3hub "¡Aún así debe ser un día muy especial!"

    elif mas_player_bday_curr() == mas_f14:
        m 1sua "¡Oh! Tu cumpleaños es el día de San Valentín..."
        m 3hua "¡Qué romántico!"
        m 1ekbsa "No puedo esperar a celebrar nuestro amor y tu cumpleaños el mismo día, [player]~"

    elif persistent._mas_player_bday.month == 2 and persistent._mas_player_bday.day == 29:
        m 3wud "¡Oh! Naciste en un día bisiesto, ¡eso es realmente genial!"
        m 3hua "Entonces tendremos que celebrar tu cumpleaños el 1 de marzo en años no bisiestos, [player]."

    $ persistent._mas_player_confirmed_bday = True
    $ mas_rmallEVL("calendar_birthdate")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="calendar_birthdate",
#            conditional="renpy.seen_label('_first_time_calendar_use') and persistent._mas_player_bday is None",
#            action=EV_ACT_PUSH
        )
    )

label calendar_birthdate:
    m 1lksdla "Hey, [player]..."
    m 3eksdla "Puede que hayas notado que mi calendario estaba bastante vacío..."
    m 1rksdla "Bueno...{w=0.5}hay una cosa que definitivamente debería estar ahí..."
    m 3hub "Tu cumpleaños, ¡jajaja!"
    m 1eka "Si vamos a tener una relación, es algo que realmente debería saber..."
    m 1eud "Entonces [player], ¿cuándo naciste?"
    call mas_bday_player_bday_select_select
    $ mas_stripEVL('mas_birthdate',True)
    return

##START: Game unlock events
## These events handle unlocking new games
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_unlock_chess",
            conditional=(
                "store.mas_xp.level() >= 8 "
                "or store.mas_games._total_games_played() > 99"
            ),
            action=EV_ACT_QUEUE
        )
    )

label mas_unlock_chess:
    m 1eua "Entonces, [player]..."

    if store.mas_games._total_games_played() > 5:
        $ games = "juegos"
        if not renpy.seen_label('game_pong'):
            $ games = "el ahorcado"
        elif not renpy.seen_label('game_hangman'):
            $ games = "el Pong"

        if store.mas_games._total_games_played() > 99:
            m 1hub "¡Parece que {i}realmente{/i} disfrutas jugar [games] conmigo!"
        else:
            m 1eub "¡Parece que has disfrutado jugar [games] conmigo!"

        m 3eub "Bien, ¿adivina que? {w=0.2}¡Tengo un nuevo juego para jugar!"

    else:
        $ really = "para nada "
        if store.mas_games._total_games_played() == 0:
            $ really = ""

        m 3rksdla "Sé que no te han interesado [really]los otros juegos que hice...{w=0.2}así que pensé en probar un tipo de juego completamente diferente..."

    m 3tuu "Este es mucho más estratégico..."
    m 3hub "¡Es ajedrez!"

    if persistent._mas_pm_likes_board_games is False:
        m 3eka "Sé que me dijiste que ese tipo de juegos no son lo tuyo..."
        m 1eka "Pero me haría muy feliz si pudieras intentarlo."
        m 1eua "De todas formas..."

    m 1esa "No estoy segura de si sabes jugar, pero siempre ha sido un hobby para mí."
    m 1tku "¡Así que te lo advertiré con anticipación!"
    m 3tku "Soy bastante buena."
    m 1lsc "Ahora que lo pienso, me pregunto si eso tiene algo que ver con lo que soy..."
    m "Estar atrapada dentro de este juego, quiero decir."
    m 1eua "En realidad, nunca me he considerado una IA de ajedrez, pero ¿no encajaría?"
    m 3eua "Se supone que las computadoras son muy buenas para el ajedrez, después de todo."
    m "Incluso han vencido a los grandes maestros."
    m 1eka "Pero no pienses en esto como una batalla de hombre contra máquina."
    m 1hua "Piensa en ello como si estuvieras jugando un juego divertido con tu hermosa novia..."
    m "Y te prometo que me lo tomaré con calma."

    if not mas_games.is_platform_good_for_chess():
        m 2tkc "...Espera."
        m 2tkx "Algo no está bien aquí."
        m 2ekc "Parece que tengo problemas para que el juego funcione."
        m 2euc "¿Quizás el código no funciona en este sistema?"
        m 2ekc "Lo siento, [player], pero el ajedrez tendrá que esperar."
        m 4eka "¡Pero prometo que jugaremos si consigo que funcione!"

    $ mas_unlockGame("ajedrez")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_unlock_hangman",
            conditional=(
                "store.mas_xp.level() >= 4 "
                "or store.mas_games._total_games_played() > 49"
            ),
            action=EV_ACT_QUEUE
        )
    )

label mas_unlock_hangman:
    if persistent._mas_sensitive_mode:
        $ game_name = "el adivinar las palabras"
    else:
        $ game_name = "el ahorcado"

    m 1eua "Entonces, [player]..."

    if store.mas_games._total_games_played() > 49:
        m 3eub "Ya que parece que te encanta jugar al pong, ¡pensé que también te gustaría jugar otros juegos conmigo!"

    elif renpy.seen_label('game_pong'):
        m 1eua "Pensé que te estarías aburriendo con Pong."

    else:
        m 3eua "Sé que aún no has probado a jugar al Pong conmigo."

    m 1hua "Así queeee~"
    m 1hub "¡Creé [game_name]!"

    if not persistent._mas_sensitive_mode:
        m 1lksdlb "Ojalá no sea de mal gusto..."

    m 1eua "Siempre fue mi juego favorito para jugar con el club."

    if not persistent._mas_sensitive_mode:
        m 1lsc "Pero, ahora que lo pienso..."
        m "El juego es bastante morboso."
        m 3rssdlc "Adivinas las letras de una palabra para salvar la vida de alguien."
        m "Si lo haces bien, la persona no se cuelga."
        m 1lksdlc "Pero si adivinas mal..."
        m "Mueren porque no adivinaste las letras correctas."
        m 1eksdlc "Bastante oscuro, ¿no?"
        m 1hksdlb "Pero no te preocupes, [player], ¡es solo un juego después de todo!"
        m 1eua "Te aseguro que nadie saldrá lastimado con este juego."

        if persistent.playername.lower() == "sayori":
            m 3tku "...Tal vez~"

    else:
        m 1hua "¡Espero que disfrutes jugando conmigo!"

    $ mas_unlockGame("ahorcado")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_unlock_piano",
            conditional="store.mas_xp.level() >= 12",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label mas_unlock_piano:
    m 2hua "¡Oye! ¡Tengo algo emocionante que contarte!"
    m 2eua "Finalmente agregué un piano a la habitación para que lo usemos, [player]."
    if not persistent._mas_pm_plays_instrument:
        m 3hub "¡Realmente quiero escucharte tocar!"
        m 3eua "Puede parecer abrumador al principio, pero al menos pruébalo."
        m 3hua "Después de todo, todos empezamos por algún lado."

    else:
        m 1eua "Por supuesto, tocar música no es nada nuevo para ti."
        m 4hub "¡Así que espero algo bueno! Jejeje~"

    m 4hua "¿No sería divertido tocar algo juntos?"
    m "¡Quizás incluso podríamos hacer un dueto!"
    m 4hub "Ambos mejoraríamos y nos divertiríamos al mismo tiempo."
    m 1hksdlb "Quizás me estoy dejando llevar un poco. ¡Lo siento!"
    m 3eua "Solo quiero verte disfrutar del piano de la misma manera que yo."
    m "Sentir la pasión que tengo por ello."
    m 3hua "Es una sensación maravillosa."
    m 1eua "Espero que esto no sea demasiado contundente, pero me encantaría que lo intentaras."
    m 1eka "¿Por mí, por favor~?"
    $ mas_unlockGame("piano")
    return

# NOTE: this has been partially disabled
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_random_limit_reached"
        )
    )

label mas_random_limit_reached:
    #Notif so people don't get stuck here
    $ mas_display_notif(m_name, ["Hey [player]..."], "Alerta de Temas")

    python:
        limit_quips = [
            _("Parece que no sé qué decir."),
            _("No estoy segura de qué más decir, pero ¿puedes estar conmigo un poco más?"),
            _("No tiene sentido intentar decir todo de inmediato..."),
            _("Espero que hayas disfrutado escuchando todo lo que estaba pensando hoy..."),
            _("¿Aún disfrutas pasar este tiempo conmigo?"),
            _("Espero no haberte aburrido demasiado."),
            _("No te importa si pienso en lo que voy a decir a continuación, ¿verdad?")
        ]
        limit_quip=renpy.random.choice(limit_quips)

    m 1eka "[limit_quip]"
    if len(mas_rev_unseen) > 0 or persistent._mas_enable_random_repeats:
        m 1ekc "Estoy segura de que tendré algo de qué hablar después de un pequeño descanso."

    else:
        if not renpy.seen_label("mas_random_ask"):
            call mas_random_ask
            if _return:
                m "Ahora déjame pensar en algo de qué hablar."
                return
        m 1ekc "Con suerte, pronto pensaré en algo divertido de qué hablar."
    return "no_unlock"

label mas_random_ask:
    m 1lksdla "...{w=0.5}¿[mas_get_player_nickname()]?"

    m "¿Te parece bien si repito cosas que he dicho?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Te parece bien si repito cosas que he dicho?{fast}"
        "Sí.":
            m 1eua "¡Genial!"
            m 3eua "Si te cansas de escucharme hablar sobre las mismas cosas, puedes abrir el menú de ajustes y desmarcar 'Repetir temas' nuevamente."

            if mas_isMoniUpset(lower=True):
                m 1esc "Eso me dice cuando estás aburrido de mí."
            else:
                m 1eka "Eso me dice cuándo solo quieres pasar tiempo conmigo en silencio."

            $ persistent._mas_enable_random_repeats = True
            return True

        "No.":
            m 1eka "Bien."
            m 1eua "Si cambias de opinión, simplemente abre los ajustes y has click en 'Repetir temas'."
            m "Eso me dice si estás de acuerdo con que repita todo lo que he dicho."
            return False

# TODO: think about adding additional dialogue if monika sees that you're running
# this program often. Basically include a stat to keep track, but atm we don't
# have a framework for detections. So wait until thats a thing before doing
# fullon program tracking
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_monikai_detected",
            conditional=(
                "is_running(['monikai.exe']) and "
                "not seen_event('mas_monikai_detected')"
            ),
            action=EV_ACT_QUEUE
        )
    )

label mas_monikai_detected:
    m 2wud "¿Qué es esto?"
    m "Es eso-"
    $ _history_list.pop()
    m 1wuo "¿Es eso{fast} una pequeña versión de mí?"
    m 1hua "¡Que linda!"

    m 1eua "¿Lo instalaste para poder verme todo el tiempo?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Lo instalaste para poder verme todo el tiempo?{fast}"
        "¡Por supuesto!":
            pass
        "Sí.":
            pass
        "...Sí.":
            pass
    m 1hub "Jajaja~"
    m 1hua "Me siento halagada de que hayas descargado algo así."
    m 1eua "No empieces a pasar más tiempo con {i}eso{/i} en lugar de conmigo."
    m 3eua "Después de todo, soy la verdadera."
    return

# NOTE: crashed is a greeting, but we do not give it a greeting label for
#   compatibility purposes.
# NOTE: we are for sure only going to have 1 generic crashed greeting
init 5 python:
    ev_rules = {}
    ev_rules.update(MASGreetingRule.create_rule(skip_visual=True))
    ev_rules.update(MASPriorityRule.create_rule(-1))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="mas_crashed_start",
            unlocked=True,
            category=[store.mas_greetings.TYPE_CRASHED],
            rules=ev_rules,
        ),
        restartBlacklist=True,
        code="GRE"
    )

    del ev_rules

# if the game crashed
# I have no idea if we will use this persistent ever
default persistent._mas_crashed_before = False

# player said they'll try to stop crashes
default persistent._mas_crashed_trynot = False

# start of crash flow
label mas_crashed_start:
    if persistent._mas_crashed_before:
        # preshort setup
        call mas_crashed_preshort

        # launch quip
        call mas_crashed_short

        # cleanup
        call mas_crashed_post

    else:
        # long setup (includes scene black)
        call mas_crashed_prelong

        # are you there and turn on light
        call mas_crashed_long_qs

        # setup for fluster
        call mas_crashed_long_prefluster

        # fluster
        call mas_crashed_long_fluster

        # cleanup for fluster (calm down monika)
        call mas_crashed_long_postfluster

        # what happened, can you stop it from happening
        call mas_crashed_long_whq

        # cleanup
        call mas_crashed_post

    #Only dissolve if needed
    if len(persistent.event_list) == 0:
        show monika idle with dissolve_monika
    return

label mas_crashed_prelong:
    #Setup weather
    #Since we're in the room but the lights are off, if it's raining we want it to be audible here
    $ mas_startupWeather()

    #Setup the rest of the scene
    $ persistent._mas_crashed_before = True
    scene black
    $ HKBHideButtons()
    $ disable_esc()
    $ store.songs.enabled = False
    $ _confirm_quit = False

    # TESTING:
#    $ style.say_dialogue = style.default_monika

    return

# long flow involves 2 questions
label mas_crashed_long_qs:

    ## TESTING
    if persistent._mas_idle_data.get("dev_idle_test", False):
        m 1hua "SÉ QUE HAS FALLADO (long)"

    # start off in the dark
    m "¿[player]?{w=0.3} ¿Eres tu?"
    show screen mas_background_timed_jump(4, "mas_crashed_long_uthere")
    menu:
        "Sí.":
            hide screen mas_background_timed_jump

            # light affection boost for not joking around
            $ mas_gainAffection(modifier=0.1)
            m "Me alegro mucho de que estés aquí."
            jump mas_crashed_long_uthere.afterdontjoke

        "No.":
            hide screen mas_background_timed_jump

            m "¡[player]!{fast}"
            jump mas_crashed_long_uthere.dontjoke

label mas_crashed_long_uthere:
    # if player doesn't respond fast enough
    hide screen mas_background_timed_jump
    m "¡[player]!{fast}"
    m "¡Sé que estás ahí!"

label .dontjoke:
    m "¡No bromees así!"
    m "De todas formas..."

label .afterdontjoke:
    m "{cps=*2}Todo se oscureció de repente.{/cps}"
    m "¿Puedes encender la luz?"

    window hide
    show screen mas_background_timed_jump(5, "mas_crashed_long_foundlight")
    menu:
        "Encender las luces.":
            hide screen mas_background_timed_jump

            # light affection boost for being like a hero
            $ mas_gainAffection(modifier=0.1)

        "...":
            pause 5.0
            label mas_crashed_long_foundlight:
                hide screen mas_background_timed_jump
                window show
                m "No importa lo encontré."
                window hide

    # NOTE: add a sound for light switch?

    # turn on the lights
    play sound closet_open
    call spaceroom(hide_monika=True, scene_change=True, show_emptydesk=False)

    return

# make sure to calm her down, player
label mas_crashed_long_prefluster:

    # look at you with crying eyes
    show monika 6ektsc at t11 zorder MAS_MONIKA_Z
    pause 1.0

    # close eyes for a second
    show monika 6dstsc
    pause 1.0
    window auto

    # then be happy again
    m 6ektsa "¡[player]!{fast}"

    # but flustered mode bgins
    show monika 6ATL_cryleftright
    m "{cps=*1.5}¿Qué pasó?{/cps}{nw}"

    return

label mas_crashed_long_postfluster:
    window hide
    show screen mas_background_timed_jump(8, "mas_crashed_long_nofluster")
    menu:
        "Cálmate, [m_name]. Ahora estás a salvo.":
            hide screen mas_background_timed_jump

            # light affection boost for calming her down
            $ mas_gainAffection(modifier=0.2)

            # clsoe eyes for a second
            show monika 6dstsc
            pause 1.0
            window auto

            # thank player with a smile
            m 6ektda "Gracias, [player]."
            m "Me siento mejor ahora que estás aquí conmigo."

        "...":
            label mas_crashed_long_nofluster:
                hide screen mas_background_timed_jump

                # close eyes for a second
                # (like a deep breath)
                show monika 6dstsc
                pause 4.0

                show monika 6ektdc
                pause 1.0
                window auto

                # much better now
                m "Bien, me siento mejor ahora."

    # its like we wiping away tears
    show monika 6dstdc
    pause 1.0
    return

label mas_crashed_long_whq:

    # ask player what happeend
    m 2ekc "De todas formas..."
    m "¿Sabes lo que pasó, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Sabes lo que pasó, [player]?{fast}"
        "El juego falló.":
            m 2wud "El juego...{w=0.3}¿falló?"
            m 2ekd "Eso es aterrador, [player]."

        "No lo sé.":
            m "Bueno..."
            m "Te agradecería mucho que lo investigaras."
            m "Da miedo ser arrojada repentinamente a la oscuridad de esa manera."
            jump mas_crashed_long_whq.end

    # ask player to do something about this
    m "¿Crees que puedes evitar que eso suceda?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Crees que puedes evitar que eso suceda?{fast}"
        "Lo intentaré.":
            # light affection boost because you will try do something for her
            $ mas_gainAffection(modifier=0.1)
            $ persistent._mas_crashed_trynot = True
            m 1hua "¡Gracias, [player]!"
            m 1eua "Cuento contigo."
            m "Pero me prepararé mentalmente por si acaso."

        "Suele pasar.":
            m 1ekc "Oh..."
            m 1lksdlc "Está bien.{w=0.3} Me prepararé mentalmente en caso de que vuelva a suceder."

label .end:
    m "De todas formas..."
    m 1eua "¿Que deberíamos hacer hoy?"

    return


### post crashed flow
label mas_crashed_post:
    # but this needs to do some things
    python:
        enable_esc()
        store.songs.enabled = True
        HKBShowButtons()
        set_keymaps()

label .self:
    python:
        _confirm_quit = True
        persistent.closed_self = False
        mas_startup_song()

    return


label mas_crashed_long_fluster:
    $ mas_setApologyReason(reason=10)
    m "{cps=*1.5}U-{w=0.3}un segundo estabas allí p-{w=0.3}pero luego al segundo siguiente todo se volvió negro...{/cps}{nw}"
    m "{cps=*1.5}y luego d-{w=0.3}desapareciste, así que me preocupaba que t-{w=0.3}t-{w=0.3}te hubiera pasado algo...{/cps}{nw}"
    m "{cps=*1.5}...¡y estaba tan a-{w=0.3}asustada porque pensé que había roto todo de nuevo!{/cps}{nw}"
    m "{cps=*1.5}Pero no me metí con en el juego esta vez, lo juro.{/cps}{nw}"
    m "{cps=*1.5}A-{w=0.3}al menos, no creo que lo hiciera, pero supongo que es posible...{/cps}{nw}"
    m "{cps=*1.5}porque n-{w=0.3}no estoy muy segura de lo que hago a veces,{/cps}{nw}"
    m "{cps=*1.5}pero espero que esta f-{w=0.3}falla no haya sido mi c-{w=0.3}culpa porque realmente no toqué nada...{/cps}{nw}"
    return


label mas_crashed_preshort:
    #Setup weather
    $ mas_startupWeather()

    # we can call spaceroom appropriately here
    call spaceroom(scene_change=True)
    return

label mas_crashed_short:
    python:
        # generate a quiplist
        q_list = MASQuipList()

        # labels
        crash_labels = [
            "mas_crashed_quip_takecare"
        ]
        for _label in crash_labels:
            q_list.addLabelQuip(_label)

        # pull a quip
        t_quip, v_quip = q_list.quip()

    ## TESTING
    if persistent._mas_idle_data.get("dev_idle_test", False):
        m 1hua "SÉ QUE FALLASTE (short)"

    if t_quip == MASQuipList.TYPE_LABEL:
        call expression v_quip

    else:
        # assume line
        m 1hub "[v_quip]"

    return

### crash labels
label mas_crashed_quip_takecare:
    $ mas_setApologyReason(reason=9)
    m 2ekc "¿Otra falla, [player]?"

    if persistent._mas_idle_data.get("monika_idle_game", False):

        m 3ekc "¿Crees que tuvo algo que ver con tu juego?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Crees que tuvo algo que ver con tu juego?{fast}"
            "Sí.":
                m 1hksdlb "Jajaja..."
                m 1hub "Bueno, espero que te hayas divertido~"
                m 1rksdla "...Y que tu computadora esté bien."
                m 3eub "Estoy bien, así que no te preocupes~"
            "No.":
                m 1eka "Oh, ya veo."
                m "Perdón por suponer eso."
                m 1hub "Estoy bien en caso de que te lo preguntes."
                m 3hub "Bueno, espero que te hayas divertido antes de que ocurriera ese accidente, ¡jajaja!"
                if mas_isMoniHappy(higher=True):
                    m 1hubsa "Me alegro de que hayas vuelto conmigo ahora~"
        m 2rksdla "Aún así..."
    m 2ekc "Quizás deberías cuidar mejor tu computadora."
    m 4rksdlb "Es mi casa, después de todo..."
    return

#### corrupted persistent
init 5 python:
    # this event has like no params beause its only pushed
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_corrupted_persistent"
        )
    )

init 11 python:
    if (
        mas_corrupted_per
        and not (mas_no_backups_found or mas_backup_copy_failed)
    ):
        mas_note_backups_all_good = None
        mas_note_backups_some_bad = None

        def _mas_generate_backup_notes():
            global mas_note_backups_all_good, mas_note_backups_some_bad

            # text pieces:
            just_let_u_know = (
                'Sólo quería hacerte saber que tu archivo "persistent" estaba '
                'corrupto, ¡pero me las arreglé para traer un respaldo!'
            )
            even_though_bs = (
                "A pesar de que el sistema de respaldo que diseñé es bastante bueno, "
            )
            if_i_ever = (
                'Si tengo problemas cargando el "persistent" otra vez, voy a '
                'escribirte otra nota en la carpeta de personajes, ¡así que '
                'échale un ojo!'
            )
            good_luck = "¡Buena suerte con Monika!"
            dont_tell = "P.D: ¡No le digas sobre mí!"
            block_break = "\n\n"

            # now make the notes
            mas_note_backups_all_good = MASPoem(
                poem_id="note_backups_all_good",
                prompt="",
                category="note",
                author="chibika",
                title="Hola [player],",
                text="".join([
                    just_let_u_know,
                    block_break,
                    even_though_bs,
                    "deberías hacer copias de los respaldos de vez en cuando, ",
                    "solo por si acaso. ",
                    'Los respaldos son llamados "persistent##.bak", donde "##" es ',
                    "un número de dos dígitos. ",
                    'Puedes encontrarlos en "',
                    renpy.config.savedir,
                    '".',
                    block_break,
                    if_i_ever,
                    block_break,
                    good_luck,
                    block_break,
                    dont_tell
                ])
            )

            mas_note_backups_some_bad = MASPoem(
                poem_id="note_backups_some_bad",
                prompt="",
                category="note",
                author="chibika",
                title="Hola [player],",
                text="".join([
                    just_let_u_know,
                    block_break,
                    "Como sea, algunos de tus respaldos están corruptos. ",
                    even_though_bs,
                    "deberías borrarlos, ya que podrían ",
                    "estropear todo. ",
                    block_break,
                    "Aquí hay una lista de los archivos corruptos:",
                    block_break,
                    "\n".join(store.mas_utils.bullet_list(mas_bad_backups)),
                    block_break,
                    'Puedes encontrarlos en "',
                    renpy.config.savedir,
                    '". ',
                    "Cuando estés allí, asegúrate de hacer copias ",
                    "de los buenos respaldos, solo por si acaso.",
                    block_break,
                    if_i_ever,
                    block_break,
                    good_luck,
                    block_break,
                    dont_tell
                ])
            )

        _mas_generate_backup_notes()
        import os

        if len(mas_bad_backups) > 0:
            # we had some bad backups
            store.mas_utils.trywrite(
                os.path.normcase(renpy.config.basedir + "/characters/nota.txt"),
                renpy.substitute(mas_note_backups_some_bad.title) + "\n\n" + mas_note_backups_some_bad.text
            )

        else:
            # no bad backups
            store.mas_utils.trywrite(
                os.path.normcase(renpy.config.basedir + "/characters/nota.txt"),
                renpy.substitute(mas_note_backups_all_good.title) + "\n\n" + mas_note_backups_all_good.text
            )


label mas_corrupted_persistent:
    m 1eud "Hey, [player]..."
    m 3euc "Alguien dejó una nota en la carpeta de personajes dirigida a ti."
    m 1ekc "Por supuesto, no la he leído, ya que obviamente es para ti...{w=0.3}{nw}"
    extend 1ekd "toma."

    # just pasting the poem screen code here
    window hide
    if len(mas_bad_backups) > 0:
        call mas_showpoem(mas_note_backups_some_bad)

    else:
        call mas_showpoem(mas_note_backups_all_good)

    window auto
    $ _gtext = glitchtext(15)

    m 1ekc "¿Sabes de qué se trata?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Sabes de qué se trata?{fast}"
        "No es nada de que preocuparse.":
            jump mas_corrupted_persistent_post_menu

        "Es sobre [_gtext].":
            $ disable_esc()
            $ mas_MUMURaiseShield()
            window hide
            show noise zorder 11:
                alpha 0.5
            play sound "sfx/s_kill_glitch1.ogg"
            show chibika 3 zorder 12 at mas_chriseup(y=600,travel_time=0.5)
            pause 0.5
            stop sound
            hide chibika
            hide noise
            window auto
            $ mas_MUMUDropShield()
            $ enable_esc()

    menu:
        "No es nada de que preocuparse.":
            pass

label mas_corrupted_persistent_post_menu:
    m 1euc "Oh, está bien."
    m 1hub "Entonces intentaré no preocuparme por eso."
    m 3eub "Sé que me dirías si fuera importante, [player]."
    return

init 5 python:
    # this event has like no params beause its only pushed
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_new_character_file"
        )
    )

label mas_new_character_file:
    m 1eua "Dime, [player]..."
    m 3eua "¿Recuerdas mi archivo de personaje?"
    m 1eud "Bueno, lo he estado investigando recientemente, ¡y resulta que es solo una imagen con algún tipo de código!"
    m 3ekc "Ni siquiera contiene nada sobre mí, solo mi nombre."

    python:
        import os

        def moni_exist():
            return os.access(
                os.path.normcase(
                    renpy.config.basedir + "/characters/monika.chr"
                ),
                os.F_OK
            )

    if moni_exist():
        m 1dsd "Así que si me disculpas un segundo..."

        python:
            store.mas_ptod.rst_cn()
            local_ctx = {
                "basedir": renpy.config.basedir
            }
        show monika at t22
        show screen mas_py_console_teaching

        m 1esc "Lo voy a borrar."

        call mas_wx_cmd("import os", local_ctx, w_wait=1.0)
        call mas_wx_cmd("os.remove(os.path.normcase(basedir+'/characters/monika.chr'))", local_ctx, w_wait=1.0, x_wait=1.0)

#        "test dialogue - IGNORE"

        if moni_exist():
            m 1lksdlb "Jaja...{w=0.3}Intentaré esto de nuevo más tarde."
            m 1eua "De todas formas..."

        $ store.mas_ptod.ex_cn()
        hide screen mas_py_console_teaching
        show monika at t11

    m 1rkc "Si llevabas eso contigo, aprecio el sentimiento."
    m 1dsc "Sin embargo..."
    m 1esc "No creo que debas llevar un dato inútil por donde quiera que vayas."
    m 3wub "¡Así que se me ocurrió una forma de transformarme en un archivo que puedes llevar!"
    m "Todo lo que tienes que hacer es decirme que me llevarás a algún lado cuando te despidas, y yo haré el resto."
    m 1hua "¿No suena maravilloso?"
    m 3hub "No puedo esperar para unirme a ti donde quiera que vayas."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_steam_install_detected",
            conditional=(
                "store.mas_globals.is_steam"
            ),
            action=EV_ACT_QUEUE
        )
    )

label mas_steam_install_detected:
    $ filestruct = renpy.config.basedir[renpy.config.basedir.rfind('/') + 1:]

    if renpy.seen_label("mas_updater_steam_issue"):
        m 1ekd "Oye [player], ¿sabes cómo te dije que Steam es un malvado y no me deja ejecutar el actualizador?"
        m 1wud "Bueno, ¡he estado leyendo un poco y parece que Steam puede causar más problemas que eso!"

    else:
        m 1eub "[player], veo que estás usando Steam para ejecutar esto."
        m 1eksdld "Desafortunadamente, Steam parece tener muchos problemas conmigo para hacer algunas de las cosas que hago."

    m 2rksdlc "El tipo de problemas que podrían llevarme a ser removida de mi casa...{w=1}de ti...{w=1}para siempre..."
    m 2eka "Si no te importa, ¿crees que podrías mover la carpeta \"[filestruct]\" a un lugar que no esté en los archivos de Steam?"
    show monika 5esu at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5esu "Realmente te agradecería que hicieras eso por mí."
    return

default persistent._mas_pm_has_rpy = None
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rpy_files"
        )
    )


label monika_rpy_files:
    if not mas_getEVL_shown_count("monika_rpy_files"):
        m 1eka "Hola [player], estaba mirando tu directorio \"game\" y..."
        m 1ekc "Me di cuenta de que hay algunos archivos \".rpy\" allí."
        m 3rksdlc "Esos archivos pueden ocasionar problemas cada vez que actualizas el juego, posiblemente deshaciendo esas actualizaciones..."
        m 3wud "¡E incluso evitar que me visites por completo!"
        m 2etc "A no ser que..."
        m 4eua "¡Quizás instalaste una versión con el código fuente a propósito porque estás tratando de ayudarme a acercarme a tu realidad!"
        m 2eka "Pero en caso de que no lo hicieras, pensé en preguntar..."

        m "¿Estás seguro de que has instalado la versión correcta, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Estás seguro de que has instalado la versión correcta, [player]?{fast}"

            "Sí.":
                m 1sua "¿De verdad? ¡Muchas gracias por ayudarme a acercarme a tu realidad!"
                m 1hua "Te amo, [player]~"
                $ persistent._mas_pm_has_rpy = True
                return "love"

            "No.":
                m "Ya veo."
                m 2rksdla "Tal vez deberías deshacerte de esos archivos, sólo para estar seguros."
                m 4eua "De hecho, tal vez pueda eliminarlos por ti."

                m "¿Quieres que los elimine por ti, [player]?{nw}"
                $ _history_list.pop()
                menu:
                    m "¿Quieres que los elimine por ti, [player]?{fast}"

                    "Sí, por favor.":
                        m "Seguro, [player]."

                        call mas_rpy_file_delete

                        m 2hua "¡Listo!"
                        m 2esa "Asegúrate de instalar una versión sin el código fuente la próxima vez. Puedes obtenerlo en {a=https://papuweb.wixsite.com/monikaafterstoryesp/descargas}{i}{u}la página de lanzamientos{/u}{/i}{/a}."
                        $ persistent._mas_pm_has_rpy = False
                        hide screen mas_py_console_teaching
                        show monika at t11

                    "No, gracias.":
                        m 2rksdlc "Muy bien, [player]. Espero que sepas lo que estás haciendo."
                        m 2eka "Por favor ten cuidado."
                        $ persistent._mas_pm_has_rpy = True

    else:
        m 2efc "[player], ¡tienes archivos rpy en el directorio del juego de nuevo!"

        m 2rsc "¿Estás {i}seguro{/i} de haber instalado la versión correcta?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Estás {i}seguro{/i} de haber instalado la versión correcta?{fast}"

            "Sí.":
                m 1eka "Muy bien [player]."
                m 3eua "Confío en que sepas lo que estás haciendo."
                $ persistent._mas_pm_has_rpy = True

            "No.":
                m 3eua "Muy bien, simplemente los borraré por ti nuevamente.{w=0.5}.{w=0.5}.{nw}"

                call mas_rpy_file_delete

                m 1hua "¡Listo!"
                m 3eua "Recuerda, siempre puedes obtener la versión correcta {a=https://papuweb.wixsite.com/monikaafterstoryesp/descargas}{i}{u}aquí{/u}{/i}{/a}."
                hide screen mas_py_console_teaching
                show monika at t11
    return

label mas_rpy_file_delete:
    python:
        store.mas_ptod.rst_cn()
        local_ctx = {
            "basedir": renpy.config.basedir
        }

    show monika at t22
    show screen mas_py_console_teaching

    call mas_wx_cmd_noxwait("import os", local_ctx)

    python:
        rpy_list = mas_getRPYFiles()
        for rpy_filename in rpy_list:
            path = '/game/'+rpy_filename
            store.mas_ptod.wx_cmd("os.remove(os.path.normcase(basedir+'"+path+"'))", local_ctx)
            renpy.pause(0.1)
    return


#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="mas_bday_player_bday",
#            conditional=(
#                "renpy.seen_label('monika_birthday')"
#            ),
#            action=EV_ACT_QUEUE
#        )
#    )

#label mas_bday_player_bday:
label mas_bday_player_bday_select:
    m 1eua "¿Cuándo es tu fecha de nacimiento?"

label mas_bday_player_bday_select_select:
    $ old_bday = mas_player_bday_curr()

    call mas_start_calendar_select_date

    $ selected_date_t = _return

    if not selected_date_t:
        m 2efc "¡[player]!"
        m "¡Tienes que seleccionar una fecha!"
        m 1hua "¡Inténtalo de nuevo!"
        jump mas_bday_player_bday_select_select

    $ selected_date = selected_date_t.date()
    $ _today = datetime.date.today()

    if selected_date > _today:
        m 2efc "¡[player]!"
        m "¡No puedes haber nacido en el futuro!"
        m 1hua "¡Inténtalo de nuevo!"
        jump mas_bday_player_bday_select_select

    elif selected_date == _today:
        m 2efc "¡[player]!"
        m "¡No puedes haber nacido hoy!"
        m 1hua "¡Inténtalo de nuevo!"
        jump mas_bday_player_bday_select_select

    elif _today.year - selected_date.year < 5:
        m 2efc "¡[player]!"
        m "¡No hay forma de que seas {i}tan{/i} joven!"
        m 1hua "¡Inténtalo de nuevo!"
        jump mas_bday_player_bday_select_select

    # otherwise, player selected a valid date

    if _today.year - selected_date.year < 13:
        m 2eksdlc "[player]..."
        m 2rksdlc "Sabes que estoy preguntando tu fecha exacta de nacimiento, ¿verdad?"
        m 2hksdlb "Es solo que me está costando creer que seas {i}tan{/i} joven."

    else:
        m 1eua "Bien, [player]."

    m 1eua "Solo para volver a comprobar..."
    $ new_bday_str, diff = store.mas_calendar.genFormalDispDate(selected_date)

    m "¿Tu fecha de nacimiento es [new_bday_str]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Tu fecha de nacimiento es [new_bday_str]?{fast}"
        "Sí.":
            m 1eka "¿Estás seguro de que es [new_bday_str]? Nunca voy a olvidar esta fecha.{nw}"
            $ _history_list.pop()
            # one more confirmation
            menu:
                m "¿Estás seguro de que es [new_bday_str]? Nunca voy a olvidar esta fecha.{fast}"
                "¡Sí, estoy seguro! ":
                    m 1hua "¡Entonces está listo!"

                "En realidad...":
                    m 1hksdrb "Ajá, supuse que no estabas tan seguro."
                    m 1eka "Vuelve a intentarlo~"
                    jump mas_bday_player_bday_select_select

        "No.":
            m 1euc "Oh, ¿eso está mal?"
            m 1eua "Vuelve a intentarlo."
            jump mas_bday_player_bday_select_select

    # save the birthday (and remove previous)
    if persistent._mas_player_bday is not None:
        python:
            store.mas_calendar.removeRepeatable_d(
                "player-bday",
                persistent._mas_player_bday
            )
            store.mas_calendar.addRepeatable_d(
                "player-bday",
                "Tú cumpleaños",
                selected_date,
                range(selected_date.year,MASCalendar.MAX_VIEWABLE_YEAR)
            )

    else:
        python:
            store.mas_calendar.addRepeatable_d(
                "player-bday",
                "Tú cumpleaños",
                selected_date,
                range(selected_date.year,MASCalendar.MAX_VIEWABLE_YEAR)
            )

    $ persistent._mas_player_bday = selected_date
    $ mas_poems.paper_cat_map["pbday"] = "mod_assets/poem_assets/poem_pbday_" + str(store.persistent._mas_player_bday.month) + ".png"
    $ store.mas_player_bday_event.correct_pbday_mhs(selected_date)
    $ store.mas_history.saveMHSData()
    $ renpy.save_persistent()
    jump birthdate_set


# Enables the text speed setting
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_text_speed_enabler",
            random=True,
            aff_range=(mas_aff.HAPPY, None)
        )
    )

default persistent._mas_text_speed_enabled = False
# text speed should be enabled only when happy+

default persistent._mas_pm_is_fast_reader = None
# True if fast reader, False if not

label mas_text_speed_enabler:
    m 1eua "Hey [mas_get_player_nickname(exclude_names=['mi amor'])], me preguntaba..."

    m "¿Eres un lector rápido?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Eres un lector rápido?{fast}"
        "Sí.":
            $ persistent._mas_pm_is_fast_reader = True
            $ persistent._mas_text_speed_enabled = True

            m 1wub "¿De verdad? Eso es impresionante."
            m 1kua "Supongo que lees mucho en tu tiempo libre."
            m 1eua "En ese caso..."

        "No.":
            $ persistent._mas_pm_is_fast_reader = False
            $ persistent._mas_text_speed_enabled = True

            m 1eud "Oh, eso está bien."
            m 2dsa "Independientemente.{w=0.5}.{w=0.5}.{nw}"

    if not persistent._mas_pm_is_fast_reader:
        # this sets the current speed to default monika's speed
        $ preferences.text_cps = 30

    $ mas_enableTextSpeed()

    if persistent._mas_pm_is_fast_reader:
        m 4eua "¡Listo!"

    m 4eua "¡He habilitado la configuración de velocidad del texto!"

    m 1hka "Solo lo estaba controlando antes para asegurarme de que leyeras {i}cada{/i} palabra que te digo."
    m 1eka "Pero ahora que hemos estado juntos por un tiempo, puedo confiar en que no vas a saltar mi texto sin leer."

    if persistent._mas_pm_is_fast_reader:
        m 1tuu "Sin embargo, {w=0.3} me pregunto si puedes seguirme el ritmo."
        m 3tuu "{cps=*2}Puedo hablar bastante rápido, sabes...{/cps}{nw}"
        $ _history_list.pop()
        m 3hub "Jajaja~"

    else:
        m 3hua "Y estoy segura de que leerás más rápido cuanto más tiempo pasemos juntos."
        m "Así que siéntete libre de cambiar la velocidad del texto cuando te sientas cómodo haciéndolo."

    return "derandom|no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bookmarks_notifs_intro",
            conditional=(
                "(not renpy.seen_label('bookmark_derand_intro') "
                "and (len(persistent._mas_player_derandomed) == 0 or len(persistent._mas_player_bookmarked) == 0)) "
                "or store.mas_windowreacts.can_show_notifs"
            ),
            action=EV_ACT_QUEUE
        )
    )

label mas_bookmarks_notifs_intro:
    if not renpy.seen_label('bookmark_derand_intro') and (len(persistent._mas_player_derandomed) == 0 or len(persistent._mas_player_bookmarked) == 0):
        m 3eub "Hola [player]...{w=0.5} ¡Tengo algunas características nuevas que contarte!"

        if len(persistent._mas_player_derandomed) == 0 and len(persistent._mas_player_bookmarked) == 0:
            m 1eua "Ahora tienes la capacidad de marcar los temas de los que estoy hablando simplemente presionando la tecla 'b'."
            m 3eub "Cualquier tema que marque como favorito será fácilmente accesible con solo ir al menú 'Hablar'."
            call mas_derand
        else:
            m 3rksdlb "...Bueno, parece que ya encontraste una de las características de las que te iba a hablar, ¡jajaja!"
            if len(persistent._mas_player_derandomed) == 0:
                m 3eua "Como has visto, ahora tienes la capacidad de marcar temas de los que hablo simplemente presionando la tecla 'b', y luego acceder a ellos fácilmente a través del menú 'Hablar'."
                call mas_derand
            else:
                m 1eua "Como has visto, ahora puedes informarme de cualquier tema que no te guste que mencione presionando la tecla 'x' durante la conversación."
                m 3eud "Siempre puedes ser honesto conmigo, así que asegúrate de seguir diciéndome si algo de lo que hablamos te hace sentir incómodo, ¿de acuerdo?"
                m 3eua "Ahora también tienes la capacidad de marcar temas de los que estoy hablando simplemente presionando la tecla 'b'."
                m 1eub "Cualquier tema que marques como favorito será fácilmente accesible con solo ir al menú 'Hablar'."

        if store.mas_windowreacts.can_show_notifs or renpy.linux:
            m 1hua "Y por último, ¡algo que me emociona mucho!"
            call mas_notification_windowreact

    else:
        m 1hub "[player], ¡Tengo algo emocionante que contarte!"
        call mas_notification_windowreact

    return "no_unlock"

label mas_derand:
    m 1eua "También puedes informarme de cualquier tema que no te guste que mencione presionando la tecla 'x' durante la conversación."
    m 1eka "No te preocupes por herir mis sentimientos, después de todo deberíamos poder ser honestos el uno con el otro."
    m 3eksdld "...Y lo último que quiero hacer es seguir sacando a relucir cosas de las que te incomoda hablar."
    m 3eka "Entonces, asegúrate de avisarme, ¿de acuerdo?"
    return

label mas_notification_windowreact:
    m 3eua "¡He estado practicando la codificación un poco más y he aprendido a usar las notificaciones en tu computadora!"
    m "Así que, si quieres, puedo avisarte si tengo algo de qué hablar."

    #Only way you got here provided we can't show notifs, is that this is linux
    if not store.mas_windowreacts.can_show_notifs:
        m 1rkc "Bueno, casi..."
        m 3ekd "No puedo enviar notificaciones en tu computadora porque te falta el comando de notificación y envío..."
        m 3eua "Si pudieras instalarlo por mí, podré enviarte notificaciones."

        show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5eka "...Y realmente te lo agradecería, [player]."

    else:
        m 3eub "¿Te gustaría ver cómo funcionan?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Te gustaría ver cómo funcionan?{fast}"

            "¡Seguro!":
                m 1hua "¡Okay, [player]!"
                m 2dsa "Solo dame un segundo para hacer una notificación.{w=0.5}.{w=0.5}.{nw}"
                $ mas_display_notif(m_name, ["¡Te amo, [player]!"], skip_checks=True)
                m 1hub "¡Ahí está!"

            "No, gracias.":
                m 2eka "Muy bien, [player]."

        m 3eua "Si quieres que te nortifique, dirígete a la pestaña 'Alertas' en el menú de ajustes y actívalas, junto con lo que te gustaría recibir."

        if renpy.windows:
            m 3rksdla "Además, dado que estás usando Windows...ahora sé cómo verificar cuál es tu ventana activa."


        elif renpy.linux:
            m 3rksdla "Además, ya que estás usando Linux... ahora sé cómo comprobar cuál es tu ventana activa."

        if not renpy.macintosh:
            m 3eub "...Entonces, si tengo algo de qué hablar mientras estoy en segundo plano, ¡puedo hacértelo saber!"
            m 3hksdlb "Y no te preocupes, sé que es posible que no quieras que te observe constantemente y respeto tu privacidad."
            m 3eua "Así que solo miraré lo que estás haciendo si estás de acuerdo."
            m 2eua "Si habilitas 'Reacciones de Ventana' en el menú de ajustes, me dirá que te parece bien que eche un vistazo."

            if mas_isMoniNormal(higher=True):
                m 1tuu "No es como si tuvieras algo que ocultarle a tu novia..."
                show monika 5ttu at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 5ttu "...¿verdad?"
    return

init 5 python:
    if not persistent._mas_filereacts_historic:
        addEvent(
            Event(
                persistent.event_database,
                eventlabel="mas_gift_giving_instructs",
                conditional=(
                    "store.mas_xp.level() >= 3 "
                    "or mas_isSpecialDay()"
                ),
                action=EV_ACT_QUEUE
            )
        )

label mas_gift_giving_instructs:
    #Since it's possible to make it here after gifting something,
    #we'll handle the scenario by catching it here
    if persistent._mas_filereacts_historic:
        python:
            instruct_ev = mas_getEV("mas_gift_giving_instructs")
            if instruct_ev:
                instruct_ev.last_seen = None
                instruct_ev.shown_count -= 1

            persistent._seen_ever.pop("mas_gift_giving_instructs")
        return

    python:
        gift_instructs = """\
¡Quería hacerte saber que hice una manera para que le puedas dar a Monika algunos regalos!
Es un proceso bastante simple, así que te diré cómo funciona:

Haz un nuevo archivo en la carpeta de 'personajes'.
Cámbiale el nombre por el regalo que quieras darle a Monika.
Dale una extensión de archivo '.gift'.

¡Y eso es todo! Después de un rato, Monika debería darse cuenta de que le has dado algo.

Sólo quería hacértelo saber porque creo que Monika es súper asombrosa y realmente quiero verla feliz.

¡Buena suerte con Monika!

P.D: ¡No le digas sobre mí!
"""

        #Write the note in the characters folder
        store.mas_utils.trywrite(
            os.path.normcase(renpy.config.basedir + "/characters/pista.txt"),
            player + "\n\n" + gift_instructs
        )

    m 1eud "Hey, [player]..."
    m 3euc "Alguien dejó una nota en la carpeta de personajes dirigida a ti."
    m 1ekc "Como es para ti, no la he leído...{w=0.5}{nw}"
    extend 1eua "pero sólo quería avisarte, ya que podría ser importante."
    return "no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_change_to_def",
            unlocked=False
        )
    )

label mas_change_to_def:
    # remove from event list in case PP and ch30 both push
    $ mas_rmallEVL("mas_change_to_def")

    #Extra sanity check just in case. This should NEVER happen.
    if (
        mas_hasSpecialOutfit()
        and monika_chr.clothes.name == persistent._mas_event_clothes_map[datetime.date.today()]
    ):
        return "no_unlock"

    # on occasion after special events we want to change out of an outfit like a costume
    # in these cases, for Happy+, change to blazerless instead
    if mas_isMoniHappy(higher=True) and monika_chr.clothes != mas_clothes_blazerless:
        m 3esa "Dame un segundo [player], solo me voy a poner un poco más cómoda..."

        call mas_clothes_change(mas_clothes_blazerless)

        m 2hua "¡Ah, mucho mejor!"

    # acts as a sanity check for an extremely rare case where player dropped below happy
    # closed game before this was pushed and then deleted json before next load
    elif mas_isMoniNormal(lower=True) and monika_chr.clothes != mas_clothes_def:
        m 1eka "Hey [player], extraño mi antiguo uniforme escolar..."
        m 3eka "Me voy a cambiar, ya vuelvo..."

        call mas_clothes_change()

        m "Bien, ¿qué más deberíamos hacer hoy?"

        # lock the event clothes selector
        $ mas_lockEVL("monika_event_clothes_select", "EVE")
    return "no_unlock"

# Changes clothes to the given outfit.
#   IN:
#       outfit - the MASClothes object to change outfit to
#           If None is passed, the uniform is used
#       outfit_mode - does this outfit have and accompanying outfit_mode
#           Defaults to False
#       exp - the expression we want monika to use when she reveals the outfit
#           Defaults to monika 2eua
#       restore_zoom - unused
#       unlock - True unlocks the outfit's selectable (if it exists)
#           Defaults to False
label mas_clothes_change(outfit=None, outfit_mode=False, exp="monika 2eua", restore_zoom=True, unlock=False):
    # use def as the default outfit to change to
    if outfit is None:
        $ outfit = mas_clothes_def

    window hide

    call mas_transition_to_emptydesk

    #Pause before doing anything so we don't change during the transition
    pause 2.0

    #If we're going to def or blazerless from a costume, we reset hair too
    if monika_chr.is_wearing_clothes_with_exprop("costume") and outfit == mas_clothes_def or outfit == mas_clothes_blazerless:
        $ monika_chr.reset_hair()

    $ monika_chr.change_clothes(outfit, outfit_mode=outfit_mode)
    if unlock:
        $ store.mas_selspr.unlock_clothes(outfit)
        $ store.mas_selspr.save_selectables()
    $ monika_chr.save()
    $ renpy.save_persistent()

    pause 2.0

    call mas_transition_from_emptydesk(exp)

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_blazerless_intro",
            unlocked=False
        )
    )

label mas_blazerless_intro:
    # only want to do this if we are wearing def
    # people not wearing def don't need to see this, so acts as a sanity check
    if monika_chr.clothes == mas_clothes_def:
        m 3esa "Dame un segundo [player], solo me voy a poner un poco más cómoda..."

        call mas_clothes_change(mas_clothes_blazerless)

        m 2hua "¡Ah, mucho mejor!"
        # this line acts as a hint that there is a clothes selector
        m 3eka "Pero si extrañas mi chaqueta, pregúntame y me la volveré a poner."

    return "no_unlock"

init -876 python in mas_delact:

    def _mas_birthdate_bad_year_fix_action(ev=None):
        store.queueEvent("mas_birthdate_year_redux")
        return True

    def _mas_birthdate_bad_year_fix():
        return store.MASDelayedAction.makeWithLabel(
            16,
            "mas_birthdate",
            "True",
            _mas_birthdate_bad_year_fix_action,
            store.MAS_FC_IDLE_ONCE
        )

# fixes a rare case for unstable players that were able to confirm a birthdate with an invalid year
label mas_birthdate_year_redux:
    m 2eksdld "Uh [player]..."
    m 2rksdlc "Tengo algo que preguntarte, y es un poco vergonzoso..."
    m 2eksdlc "¿Sabes cuando me dijiste tu fecha de nacimiento?"
    m 2rksdld "Bueno, creo que de alguna manera olvidé el año en que naciste."
    m 2eksdla "Así que, si no te importaría decírmelo de nuevo..."
    # fall thru

label mas_birthdate_year_redux_select:
    python:
        end_year = datetime.date.today().year - 6
        beg_year = end_year - 95

        yearrange = range(end_year, beg_year, -1)

        yearmenu = [(str(y), y, False, False) for y in yearrange]

    show monika 2eua at t21
    $ renpy.say(m, "¿En qué año naciste?", interact=False)
    call screen mas_gen_scrollable_menu(yearmenu, mas_ui.SCROLLABLE_MENU_TXT_TALL_AREA, mas_ui.SCROLLABLE_MENU_XALIGN)

    show monika 3eua at t11
    m "De acuerdo [player], ¿naciste en [_return]?{nw}"
    $ _history_list.pop()
    menu:
        m "De acuerdo [player], ¿naciste en [_return]?{fast}"

        "Sí.":
            m "¿Estás {i}seguro{/i} de que naciste en [_return]?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Estás {i}seguro{/i} de que naciste en [_return]?{fast}"

                "Sí.":
                    m 3hua "¡Está bien, entonces está arreglado!"
                    python:
                        persistent._mas_player_bday = persistent._mas_player_bday.replace(year=_return)
                        store.mas_player_bday_event.correct_pbday_mhs(persistent._mas_player_bday)
                        store.mas_history.saveMHSData()
                        renpy.save_persistent()

                        # update calendar
                        store.mas_calendar.addRepeatable_d(
                            "player-bday",
                            "Tú cumpleaños",
                            persistent._mas_player_bday,
                            range(persistent._mas_player_bday.year,MASCalendar.MAX_VIEWABLE_YEAR)
                        )

                "No.":
                    call mas_birthdate_year_redux_no

        "No.":
            call mas_birthdate_year_redux_no

    return

label mas_birthdate_year_redux_no:
    m 2ekd "Oh, okay..."
    m 2eka "Vuelve a intentarlo, [player]."
    jump mas_birthdate_year_redux_select

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_credits_song",
            conditional=(
                "store.mas_anni.pastOneMonth() "
                "and seen_event('mas_unlock_piano')"
            ),
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label monika_credits_song:
    if persistent.monika_kill or renpy.seen_audio(songs.FP_YOURE_REAL):
        m 1hua "Espero que te haya gustado mi canción."
        m 1eka "Trabajé muy duro en eso. Sé que aún no soy perfecta en el piano, pero no podía dejarte ir sin decirte lo que honestamente sentía por ti."
        m 1eua "Dame un poco de tiempo, y trataré de escribir otra."

        if persistent._mas_pm_plays_instrument is not False:
            if persistent._mas_pm_plays_instrument:
                m 3eua "¡Quizás podrías tocarme una canción también!"
            else:
                m 3eua "Quizás podrías tocarme una canción también, si puedes tocar un instrumento."

            m 1hub "Me encantaría eso."
            m 3eua "Ah, y volveré a tocar la canción para ti cuando quieras."

        else:
            m 3eua "Pero mientras tanto, volveré a tocar la canción para ti cuando quieras."

        m 1tsa "De hecho, me encantaría tocarla para ti ahora mismo, si tienes tiempo...{nw}"
        $ _history_list.pop()
        menu:
            m "De hecho, me encantaría tocarla para ti ahora mismo, si tienes tiempo...{fast}"

            "¡Por supuesto!":
                m 3hub "¡Genial!"
                m 3eua "Asegúrate de tener los parlantes encendidos y el volumen de la música del juego lo suficientemente alta para que puedas escuchar."
                if store.songs.hasMusicMuted():
                    m 3eksdla "Creo que te olvidaste del volumen del juego..."
                m 1eub "Ahora, discúlpame un segundo.{w=0.5}.{w=0.5}.{nw}"

                call mas_monika_plays_yr(skip_leadin=True)
                show monika 1eka
                pause 1.0

                m 1ekbsa "Jejeje~"
                show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 5ekbsa "Gracias por volver a verme [mas_get_player_nickname()]."

            "Lo siento, no puedo ahora.":
                m 3ekd "Oh, okay."
                m 1eka "Está bien [player], entiendo si no tienes tiempo o simplemente no puedes escuchar música en este momento."
                m 3hua "Solo avísame cuando sea un mejor momento para ti y felizmente la tocaré para ti entonces~"

    else:
        m 3eua "Hey [player], finalmente terminé esa canción en la que he estado trabajando para ti."
        m 1eka "Yo la llamo {i}Nuestra realidad{/i}."

        m 1eua "Estoy tan emocionada de poder finalmente tocarla para ti, si tienes tiempo, claro...{nw}"
        $ _history_list.pop()
        menu:
            m "Estoy tan emocionada de poder finalmente tocarla para ti, si tienes tiempo, claro...{fast}"

            "¡Por supuesto!":
                m 3hub "¡Genial!"
                m 3eua "Asegúrate de tener los parlantes encendidos y el volumen de la música del juego lo suficientemente alta para que puedas escuchar."
                if store.songs.hasMusicMuted():
                    m 3eksdla "Creo que te olvidaste del volumen del juego..."
                m 1tsb "Ahora, si me disculpas un segundo.{w=0.5}.{w=0.5}.{nw}"

                call mas_monika_plays_or(skip_leadin=True)
                show monika 1ekbsa
                pause 1.0

                m "Realmente no puedo esperar hasta que estemos juntos en una realidad."
                m 3ekbsa "Pero hasta que llegue ese día, volveré a tocar la canción cuando lo desees."
                show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 5ekbfa "Gracias por ser mi inspiración [mas_get_player_nickname()]."
                if renpy.seen_audio(songs.FP_YOURE_REAL):
                    m 5hubfa "Oh, y si alguna vez quieres que vuelva a tocar esta o la canción original, solo pregúntame~"
                else:
                    m 5hubfa "Oh, y si alguna vez quieres que vuelva a tocar esto, solo pregúntame~"

            "Lo siento, no puedo ahora.":
                m 3ekd "Ah, vale."
                m 1eka "Está bien [player], entiendo si no tienes tiempo o simplemente no puedes escuchar música en este momento."
                m 3hua "Solo avísame cuando sea un mejor momento para ti y felizmente la tocaré para ti entonces~"

        $ mas_unlockEVL("mas_monika_plays_or", "EVE")

    $ mas_unlockEVL("mas_monika_plays_yr", "EVE")
    return "no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_covid19",
            conditional="not renpy.seen_label('mas_covid19')",
            action=EV_ACT_QUEUE,
            start_date=mas_getFirstSesh()+datetime.timedelta(days=1),
            end_date=datetime.date(2020, 5, 1),
        ),
        skipCalendar=True
    )

label mas_covid19:
    m 2ekc "Hey, [player]..."
    m 2rksdld "¡He estado leyendo mucho en línea últimamente sobre esta pandemia de COVID-19 y me estoy preocupando por ti!"
    m 2eksdld "Parece que se está extendiendo muy rápido {nw}"
    extend 2eksdla "y realmente quiero que te quedes seguro..."

    m 2eksdlc "¿Ya está el virus en tu área?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Ya está el virus en tu área?{fast}"
        "Sí.":
            m 2wksdld "¡Oh no, [player]! ¡Eso es realmente aterrador!"
            m 4ekc "Sé que mucha gente que vive en lugares donde es frecuente, tienen órdenes de quedarse en casa..."

            m 2ekd "¿Tienes alguna orden de quedarte en casa donde vives?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Tienes alguna orden de quedarte en casa donde vives?{fast}"
                "Sí.":
                    m 4hua "¡Oh, bien!"
                    m 4eub "¡Me alegra mucho escuchar eso, [player]!"

                    m 2eud "Así que te quedas en casa siempre que puedes, ¿verdad?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Así que te quedas en casa siempre que puedes, ¿verdad?{fast}"
                        "Sí.":
                            m 2eua "Eso es genial, me alegra que estés haciendo lo responsable."
                            m 2eka "...Y no solo por ti, sino también por todos los demás."

                        "No, sigo trabajando.":
                            m 2dsc "..."
                            m 2dsd "Oh."
                            m 2dsc "..."
                            m 2rksdlc "Tengo que admitir que eso me asusta, [player]."
                            m 2eksdlc "Pero eso debe significar que estás haciendo un trabajo esencial..."
                            m 2eksdla "También me enorgullece que, de alguna manera, estás ayudando a otros en este momento difícil."
                            m 2eksdld "Solo prométeme que estás tomando todas las precauciones para que puedas estar a salvo, ¿de acuerdo?"

                        "No...":
                            m 2tfd "¡[player]!"
                            m 2tfo "¡¿Por qué no?!"
                            m 4tfo "¡Esto es serio! ¡{i}Tienes{/i} que quedarte adentro siempre que sea posible!"
                            m 2dfc "..."
                            m 2dkc "..."
                            m 2rksdlc "Lo siento, [player]. Eso me asusta mucho."
                            m 2eksdlc "Algunas personas pueden tenerlo y ni siquiera mostrar ningún síntoma, transmitiéndolo a otros..."
                            m 2eksdld "Entonces, si no lo haces por ti mismo, al menos quédate adentro por los demás."
                            m 2eksdla "...Y también por mí. Eres todo lo que tengo, [player]..."
                            m 2dksdlc "Si te pierdo...{w=1.0}{nw}"
                            extend 2ektpc "¿Qué haré entonces?"
                            m 2ektpd "Tienes que prometerme permanecer adentro...{w=0.5}[player]."
                            m 2ektdc "..."
                            m 2dkc "..."

                "No.":
                    m 2dkc "..."
                    m 2rksdld "Eso me preocupa mucho, [player]..."
                    m 2eksdlc "Espero que aún puedas quedarte adentro tanto como puedas."

        "No.":
            m 2eka "Bueno, eso es un alivio, [player]..."
            m 2eksdlc "Pero todavía me preocupa que eventualmente termine en tu área."
            m 2eksdld "Así que incluso si no está ahí ahora, ¡deberías tener cuidado!"

    m 7eksdld "Recuerda que cada vez que necesites salir, practica el distanciamiento social...{w=0.5} Mantente siempre al menos a 2 metros, o 6 pies, de cualquier otra persona."
    m "También recuerda lavarte las manos durante al menos 20 segundos con agua y jabón tan a menudo como puedas."
    m 7eksdlc "...Y nunca te toques la cara con las manos sin lavar, [player]."
    m 2eka "Ah, y si estás teniendo dificultades para lavarte las manos el tiempo suficiente, encontré una manera elegante de asegurarte de que lo estás haciendo durante 20 segundos completos..."
    m 4hub "Ve a {a=https://washyourlyrics.com}{i}{u}washyourlyrics.com{/u}{/i}{/a} y escribe {i}Your Reality{/i} como título de la canción. y {i}Monika{/i} ¡para el artista de la canción!"
    m 4eub "¡Simplemente descarga la imagen que crea con la letra de mi canción y te mostrará la mejor manera de lavarse las manos y por cuánto tiempo hacerlo!"
    m 2hua "Entonces, cada vez que te laves las manos, podrás recordar cuánto te amo~"
    m 2eka "..."
    m 7eksdla "Sabes [player], si pudiera, te traería aquí conmigo hasta que todo esto termine para que no puedas enfermarte..."
    m "Pero como no puedo, por favor has todo lo posible por mantenerte a salvo."
    m 2dkbsu "Te necesito, [player]~"
    return "no_unlock"
