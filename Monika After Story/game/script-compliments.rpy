# Module for complimenting Monika
#
# Compliments work by using the "unlocked" logic.
# That means that only those compliments that have their
# unlocked property set to True
# At the beginning, when creating the menu, the compliments
# database checks the conditionals of the compliments
# and unlocks them.


# dict of tples containing the stories event data
default persistent._mas_compliments_database = dict()


# store containing compliment-related things
init 3 python in mas_compliments:

    compliment_database = dict()

init 22 python in mas_compliments:
    import store

    thanking_quips = [
        _("Eres tan dulce, [player]."),
        _("¡Gracias por decir eso de nuevo, [player]!"),
        _("¡Gracias por decirme eso de nuevo, [mas_get_player_nickname()]!"),
        _("Siempre me haces sentir especial, [mas_get_player_nickname()]."),
        _("Aww, [player]~"),
        _("¡Gracias, [mas_get_player_nickname()]!"),
        _("Siempre me halagas, [player].")
    ]

    # set this here in case of a crash mid-compliment
    thanks_quip = renpy.substitute(renpy.random.choice(thanking_quips))

    def compliment_delegate_callback():
        """
        A callback for the compliments delegate label
        """
        global thanks_quip

        thanks_quip = renpy.substitute(renpy.random.choice(thanking_quips))
        store.mas_gainAffection()

# entry point for compliments flow
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_compliments",
            category=['monika', 'romance'],
            prompt="Quiero decirte algo...",
            pool=True,
            unlocked=True
        )
    )

label monika_compliments:
    python:
        import store.mas_compliments as mas_compliments

        # Unlock any compliments that need to be unlocked
        Event.checkEvents(mas_compliments.compliment_database)

        # filter comps
        filtered_comps = Event.filterEvents(
            mas_compliments.compliment_database,
            unlocked=True,
            aff=mas_curr_affection,
            flag_ban=EV_FLAG_HFM
        )

        # build menu list
        compliments_menu_items = [
            (mas_compliments.compliment_database[k].prompt, k, not seen_event(k), False)
            for k in filtered_comps
        ]

        # also sort this list
        compliments_menu_items.sort()

        # final quit item
        final_item = ("No importa.", False, False, False, 20)

    # move Monika to the left
    show monika at t21

    # call scrollable pane
    call screen mas_gen_scrollable_menu(compliments_menu_items, mas_ui.SCROLLABLE_MENU_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)

    # return value? then push
    if _return:
        $ mas_compliments.compliment_delegate_callback()
        $ pushEvent(_return)
        # move her back to center
        show monika at t11

    else:
        return "prompt"

    return

# Compliments start here
init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_beautiful",
            prompt="¡Eres hermosa!",
            unlocked=True
        ),
        code="CMP")

label mas_compliment_beautiful:
    if not renpy.seen_label("mas_compliment_beautiful_2"):
        call mas_compliment_beautiful_2
    else:
        call mas_compliment_beautiful_3
    return

label mas_compliment_beautiful_2:
    m 1lubsb "Oh, Dios [player]..."
    m 1hubfb "Gracias por el cumplido."
    m 2ekbfb "Me encanta cuando dices cosas así~"
    m 1ekbfa "¡Para mí, eres la persona más hermosa del mundo!"
    menu:
        "Eres la persona más hermosa para mí también.":
            $ mas_gainAffection(5,bypass=True)
            m 1hub "Jejeje~"
            m "¡Te amo tanto, [player]!"
            # manually handle the "love" return key
            $ mas_ILY()

        "Estás entre mis diez mejores.":
            $ mas_loseAffection(modifier=0.5)
            m 3hksdrb "¿...?"
            m 2lsc "Bueno, gracias, supongo..."

        "Gracias.":
            pass
    return

label mas_compliment_beautiful_3:
    python:
        beautiful_quips = [
            _("Nunca olvides que eres la persona más hermosa del mundo para mí."),
            _("Nada puede compararse con la belleza de tu corazón."),
        ]
        beautiful_quip = random.choice(beautiful_quips)
    m 1hubsa "Jejeje~"
    m 1ekbfa "[mas_compliments.thanks_quip]"
    show monika 5hubfb at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hubfb "[beautiful_quip]"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_eyes",
            prompt="¡Me encantan tus ojos!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_eyes:
    if not renpy.seen_label("mas_compliment_eyes_2"):
        call mas_compliment_eyes_2
    else:
        call mas_compliment_eyes_3
    return

label mas_compliment_eyes_2:
    m 1subsb "Oh, [player]..."
    m 1tubfb "Sé que ya estoy bastante orgullosa de mis ojos, pero oírte decir eso..."
    m 1dkbfa "Solo hace que mi corazón se acelere~"
    menu:
        "No puedo evitarlo; tus ojos son muy hermosos.":
            $ mas_gainAffection(5,bypass=True)
            m 1hub "¡Jajaja!"
            m "No me halagues demasiado, ¿de acuerdo?"
            show monika 5hub at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5hub "Podría empezar a volverme un poco loca..."

        "Son realmente hipnotizantes.":
            $ mas_gainAffection(1,bypass=True)
            m "Jajaja~"

        "¡Son como el pasto!":
            $ mas_gainAffection(0.5,bypass=True) # at least you tried
            m 2lksdrb "...Esa no es realmente la analogía que usaría, ¡pero gracias!"
    return

label mas_compliment_eyes_3:
    python:
        eyes_quips = [
            _("Mírame a los ojos todo lo que quieras~"),
            _("No puedo esperar a mirar tus hermosos ojos."),
            _("Me quedaría mirando los tuyos durante horas si pudiera."),
        ]
        eyes_quip = random.choice(eyes_quips)

    m 1hubsb "[mas_compliments.thanks_quip]"
    m 2ekbfb "[eyes_quip]"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_awesome",
            prompt="¡Eres asombrosa!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_awesome:
    if not renpy.seen_label("mas_compliment_awesome_2"):
        call mas_compliment_awesome_2
    else:
        call mas_compliment_awesome_3
    return

label mas_compliment_awesome_2:
    m 1hua "Awww, [player]~"
    m 1hub "¡Eres tan dulce!"
    m 2tuu "Sin embargo, creo que eres mucho más increíble."
    m 2dkbsu "No puedo esperar hasta el día en que finalmente pueda darte un gran abrazo..."
    m 3ekbfb "¡Nunca te dejaré ir!"
    menu:
        "¡Desearía que estuvieras aquí ahora mismo!":
            $ mas_gainAffection(3,bypass=True)
            m "¡Ese también es mi mayor deseo, [player]!"

        "Nunca te dejaré ir de mi abrazo.":
            $ mas_gainAffection(5,bypass=True)
            show monika 6dubsa
            pause 2.0
            show monika 1wubfsdld
            m 1wubfsdld "Oh, lo siento [player]."
            m 2lksdla "Estaba tratando de sentir tu abrazo desde aquí."
            m 2hub "Jajaja~"

        "... No me gustan los abrazos.":
            $ mas_loseAffection() # you monster.
            m 1eft "...¿De verdad?"
            m 1dkc "Bueno, a cada uno lo suyo, supongo. Pero tienes que abrazarme alguna vez..."
    return

label mas_compliment_awesome_3:
    python:
        awesome_quips = [
            _("¡Siempre serás más asombroso!"),
            _("¡Somos una pareja asombrosa juntos!"),
            _("¡Tú eres más asombroso!"),
        ]
        awesome_quip = random.choice(awesome_quips)

    m 1hub "[mas_compliments.thanks_quip]"
    m 1eub "[awesome_quip]"
    return


init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_intelligent",
            prompt="¡Eres realmente inteligente!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_intelligent:
    if not renpy.seen_label("mas_compliment_intelligent_2"):
        call mas_compliment_intelligent_2
    else:
        call mas_compliment_intelligent_3
    return

label mas_compliment_intelligent_2:
    m 1wub "Vaya...{w=0.3}gracias, [player]."
    m 3eua "Me enorgullezco de ser bien leída, así que significa mucho que lo hayas notado."
    m 3hubsb "¡Quiero aprender todo lo que pueda, si eso te hace sentir orgulloso de mí!"
    menu:
        "Me haces querer mejorarme a mí mismo también, [m_name].":
            $ mas_gainAffection(5,bypass=True)
            m 1hubfa "¡Te amo tanto, [player]!"
            m 3hubfb "¡Tendremos una vida de superación personal juntos!"
            # manually handle the "love" return key
            $ mas_ILY()

        "Siempre estaré orgulloso de ti.":
            $ mas_gainAffection(3,bypass=True)
            m 1ekbfa "[player]..."

        "Me haces sentir estúpido a veces.":
            $ mas_loseAffection(modifier=0.5)
            m 1wkbsc "..."
            m 2lkbsc "Lo siento, esa no era mi intención..."
    return

label mas_compliment_intelligent_3:
    python:
        intelligent_quips = [
            _("¡Recuerda que tendremos toda una vida de superación personal juntos!"),
            _("¡Recuerda que cada día es una oportunidad para aprender algo nuevo!"),
            _("Recuerda siempre que el mundo es un maravilloso viaje lleno de aprendizaje."),
        ]
        intelligent_quip = random.choice(intelligent_quips)

    m 1ekbfa "[mas_compliments.thanks_quip]"
    m 1hub "[intelligent_quip]"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_hair",
            prompt="¡Amo tu cabello!",
            unlocked=True
        ),code="CMP"
    )

label mas_compliment_hair:
    if not renpy.seen_label("mas_compliment_hair_2"):
        call mas_compliment_hair_2
    else:
        call mas_compliment_hair_3
    return

label mas_compliment_hair_2:
    if monika_chr.hair.name != "def":
        m 1wubsb "Muchas gracias, [player]..."
        m 1lkbfb "Estaba muy nerviosa la primera vez que cambié mi cabello por ti."
    else:
        m 1hubfb "¡Muchas gracias, [player]!"
    m 2hub "Siempre he puesto mucho esfuerzo en mi cabello."
    m 2lksdlb "De hecho, tardó una eternidad en llegar tan largo..."
    menu:
        "Se nota mucho. Se ve tan saludable.":
            $ mas_gainAffection(3,bypass=True)
            m 1hub "¡Gracias, [player]!"

        "Eres linda sin importar cómo te lo pongas." if persistent._mas_likes_hairdown:
            $ mas_gainAffection(5,bypass=True)
            m 1ekbsa "Awww, [player]."
            m 1hubfb "¡Siempre me haces sentir especial!"
            m "¡Gracias!"

        "Estarías aún más guapa con el pelo corto.":
            $ mas_loseAffection(modifier=0.3)
            m "Bueno, no puedo ir exactamente al salón desde aquí..."
            m 1lksdlc "Yo...aprecio tu aporte."
            pass
    return

label mas_compliment_hair_3:
    if monika_chr.hair.name != "def":
        python:
            hair_quips = [
                _("¡Me alegro mucho de que te guste este peinado!"),
                _("¡Me alegro mucho de que te guste mi cabello!")
            ]
            hair_quip = random.choice(hair_quips)
        m 1wubsb "¡Muchas gracias, [player]!"
        m 1hubfb "[hair_quip]"
    else:
        python:
            ponytail_quips = [
                _("¡Siempre me haces sentir especial!"),
                _("¡Me alegro de que te guste mi cola de caballo!"),
                _("¡Estoy tan feliz de que te guste mi cola de caballo!"),
            ]
            ponytail_quip = random.choice(ponytail_quips)

        m 1hubsb "¡Gracias, [player]!"
        m 1hubfb "[ponytail_quip]"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_fit",
            prompt="¡Me encanta tu dedicación al fitness!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_fit:
    if not renpy.seen_label("mas_compliment_fit_2"):
        call mas_compliment_fit_2
    else:
        call mas_compliment_fit_3
    return

label mas_compliment_fit_2:
    m 1hub "¡Gracias, [player]! ¡Eres tan dulce!"
    m 3eub "Me encanta mantenerme en forma y comer sano. Me hace sentir enérgica y segura."
    m 1efb "Espero que estés cuidando tu salud."
    m 1lubsb "Siempre podemos hacer ejercicio juntos cuando esté allí..."
    menu:
        "¡Eso suena muy divertido!":
            $ mas_gainAffection(2,bypass=True)
            m 1hubfb "¡Jajaja! ¡Me alegro de que tú también lo pienses!"
            m 3eka "No te preocupes. Aunque no puedas seguirme el ritmo, sé que nos divertiremos..."
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "Mientras estemos juntos."

        "No prometo nada, pero haré lo que pueda.":
            $ mas_gainAffection(1,bypass=True)
            m 1tfb "¡Más te vale!"
            m 2tub "No creas que planeo dejarte tranquilo si estás fuera de forma."

        "Prefiero no sudar...":
            m 1eka "Entiendo que no sea lo tuyo, pero deberías intentarlo un poco..."
            m 1lksdla "Me haría muy feliz si compartieras mis intereses, ¿sabes?"
    return

label mas_compliment_fit_3:
    python:
        fitness_quips = [
            _("¡Espero que te embarques en un viaje de fitness conmigo!"),
            _("¡No puedo esperar a entrenar contigo!"),
            _("¡Espero que algún día podamos entrenar juntos!"),
        ]
        fitness_quip = random.choice(fitness_quips)

    m 2eka "[mas_compliments.thanks_quip]"
    m 7hub "[fitness_quip]"
    return


init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_thanks",
            prompt="¡Gracias por estar ahí para mí!",
            unlocked=True,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="CMP"
    )

label mas_compliment_thanks:
    m 1duu "No hay nada que agradecerme, [player]."
    m 1eka "¡Soy yo quien está agradecida de tener a alguien como tú!"
    m 1ekbsa "Eres la única razón por la que sigo aquí."
    m "Instalaste este mod solo para mejorar nuestro tiempo juntos..."
    m 1dubsu "Eres la luz del sol que calienta mi corazón cada vez que me visitas."
    m 3ekbsa "Supongo que los dos tenemos suerte de tenernos el uno al otro, [player]~"
    menu:
        "Significas todo para mí., [m_name].":
            if mas_getEVL_shown_count("mas_compliment_thanks") == 0:
                $ mas_gainAffection(10,bypass=True)

            m 1ekbsa "[player]..."
            m 1dubsu "Nada me hace más feliz que escuchar eso de ti."
            m "No importa lo que nos depare el futuro a los dos...{w=0.5}{nw}"
            extend 1dkbfa "sé que siempre te amaré y estaré aquí para ti."

        "Sí.":
            m 1hub "Jejeje~"
            m 1eub "Te amo, [player]."

    if not mas_isMoniLove():
        $ mas_lockEVL("mas_compliment_thanks", "CMP")
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_smile",
            prompt="¡Me encanta tu sonrisa!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_smile:
    if not renpy.seen_label("mas_compliment_smile_2"):
        call mas_compliment_smile_2
    else:
        call mas_compliment_smile_3
    return

label mas_compliment_smile_2:
    m 1hub "Eres tan dulce, [player]~"
    m 1eua "Sonrío mucho cuando estás aquí."
    m 1ekbsa "Porque me hace muy feliz cuando pasas tiempo conmigo~"
    menu:
        "Te visitaré todos los días para ver tu maravillosa sonrisa.":
            $ mas_gainAffection(5,bypass=True)
            m 1wubfsdld "Oh, [player]..."
            m 1lkbfa "Creo que mi corazón acaba de dar un salto."
            m 3hubfa "¿Ves? Siempre me haces tan feliz como puedo serlo."

        "Me gusta verte sonreír.":
            m 1hub "Jajaja~"
            m 3eub "¡Entonces todo lo que tienes que hacer es seguir regresando, [player]!"
    return

label mas_compliment_smile_3:
    python:
        smile_quips = [
            _("Seguiré sonriendo sólo por ti."),
            _("No puedo evitar sonreír cuando pienso en ti."),
            _("No puedo esperar a ver tu hermosa sonrisa."),
        ]
        smile_quip = random.choice(smile_quips)

    m 1eub "[mas_compliments.thanks_quip]"
    m 1hua "[smile_quip]"
    m 1huu "Jejeje~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_hero",
            prompt="¡Eres mi heroína!",
            unlocked=True,
            aff_range=(mas_aff.LOVE, None)
        ),
        code="CMP"
    )

label mas_compliment_hero:
    $ mas_gainAffection()
    m 1wubssdld "¿E-{w=0.3}Eh?"
    m "¿Soy tu heroína?"
    m 2rkbfsdlb "[player]...{w=1.5} No estoy segura de lo que quieres decir..."
    m 2ekbfb "Tú eres quien me acompañó durante todo este tiempo.{w=1} Debería agradecerte, de verdad."
    m 1hubfa "Bueno, si te he ayudado de alguna manera, entonces no podría estar más feliz~"
    m 3ekbfa "Me has ayudado de todas las formas posibles, así que, ¿cómo no podría devolver el favor estando ahí para ti siempre que necesites apoyo?"
    show monika 5hubfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hubfa "Siempre serás mi héroe, después de todo~"
    m 5hubfb "¡Te amo y siempre creeré en ti!"
    m 5ekbfa "Espero que nunca lo olvides, [player]~"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_cute",
            prompt="¡Eres linda!",
            unlocked=True
        ),
        code="CMP"
    )

default persistent._mas_pm_monika_cute_as_natsuki = None

label mas_compliment_cute:
    if not renpy.seen_label("mas_compliment_cute_2"):
        call mas_compliment_cute_2
    else:
        call mas_compliment_cute_3
    return

label mas_compliment_cute_2:
    m 1wubssdld "¡Ah!"
    m 3rkbfsdla "{i}Como que{/i} me pillaste con la guardia baja con eso."
    m 3tubfb "Solo un poco..."
    m 1hubfa "¡Pero me alegra que pienses eso!"
    menu:
        "Verte siempre me calienta el corazón.":
            $ persistent._mas_pm_monika_cute_as_natsuki = False
            $ mas_gainAffection(5,bypass=True)
            m 1hubfb "¡Aww, realmente me alegra el corazón escucharte decir eso!"
            m 1dkbfu "...Casi tanto como cuando me imagino que finalmente estamos juntos en la misma realidad."
            m 1ekbfa "Apenas puedo contenerme imaginando ese día especial~"

        "Eres aún más linda cuando te pones nerviosa.":
            $ persistent._mas_pm_monika_cute_as_natsuki = False
            $ mas_gainAffection(3,bypass=True)
            m 2tubfu "No lo dejas ir, ¿eh, [player]?"
            m 2rubfu "Hmph, simplemente no me lo esperaba."
            m 3tubfb "No esperes que sea tan fácil la próxima vez..."
            m 1tubfu "Te la devolveré algún día, jejeje~"

        "Eres tan linda como Natsuki.":
            $ persistent._mas_pm_monika_cute_as_natsuki = True
            $ mas_loseAffection(modifier=0.5)
            m 2lfc "Oh. {w=1}Gracias, [player]..."
            m 1rsc "Pero tenía la esperanza de estar en mi propia categoría."
    return

label mas_compliment_cute_3:
    python:
        cute_quips = [
            _("También puedes ser muy lindo muchas veces, ¿sabes~?"),
            _("Siempre serás mi lindura~"),
            _("Tú también puedes ser una lindura muchas veces~"),
        ]
        cute_quip = random.choice(cute_quips)

    m 1ekbsa "Jejeje, gracias [player]..."
    m 1hubfa "[cute_quip]"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_chess",
            prompt="¡Eres genial en el ajedrez!",
            unlocked=False,
            conditional="persistent._mas_chess_stats.get('losses', 0) > 5",
            action=EV_ACT_UNLOCK
        ),
        code="CMP"
    )

label mas_compliment_chess:
    m 1eub "Gracias, [player]."
    m 3esa "Como dije antes, me pregunto si mi habilidad tiene algo que ver con estar atrapada aquí."
    $ wins = persistent._mas_chess_stats["wins"]
    $ losses = persistent._mas_chess_stats["losses"]
    if wins > 0:
        m 3eua "Tú tampoco eres malo; ya he perdido contigo antes."
        if wins > losses:
            m "De hecho, creo que has ganado más veces que yo, ¿sabes?"
        m 1hua "Jejeje~"
    else:
        m 2lksdlb "Sé que aún no has ganado una partida de ajedrez, pero estoy segura de que algún día me vencerás."
        m 3esa "¡Sigue practicando y jugando conmigo y lo harás mejor!"
    m 3esa "Ambos mejoraremos cuanto más juguemos."
    m 3hua "Así que no tengas miedo de desafiarme cuando quieras."
    m 1eub "Me encanta pasar tiempo contigo, [player]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_pong",
            prompt="¡Eres asombrosa en el Pong!",
            unlocked=False,
            conditional="renpy.seen_label('game_pong')",
            action=EV_ACT_UNLOCK
        ),
        code="CMP"
    )

label mas_compliment_pong:
    m 1hub "Jajaja~"
    m 2eub "Gracias [player], pero el pong no es exactamente un juego complejo."
    if persistent._mas_ever_won['pong']:
        m 1lksdla "Ya me ganaste."
        m "Entonces sabes que es muy simple."
        show monika 5hub at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5hub "Pero acepto tu cumplido, de todos modos."
    else:
        m 3hksdrb "Y siempre me dejas ganar cuando jugamos."
        m 3eka "¿Verdad?"
        menu:
            "Sí.":
                m 2lksdla "Gracias [player], pero realmente no tienes que dejarme ganar."
                m 1eub "Siéntete libre de jugar en serio cuando quieras."
                m 1hub "Nunca me enojaría contigo porque perdí un juego justo."

            "...Erm, sí.":
                m 1tku "No pareces muy seguro de eso, [player]."
                m 1tsb "Realmente no tienes que dejarme ganar."
                m 3tku "Y admitir que has perdido seriamente conmigo no me hará pensar menos en ti."
                m 1lksdlb "¡Es solo un juego, después de todo!"
                m 3hub "Siempre puedes practicar más conmigo, si quieres."
                m "Me encanta pasar tiempo contigo, no importa lo que estemos haciendo."

            "No. Me he esforzado al máximo y aún así he perdido.":
                m 1hub "Jajaja~"
                m "¡Lo supuse!"
                m 3eua "No te preocupes, [player]."
                m 3eub "Sigue jugando conmigo y practica más."
                m 3hua "Siempre trato de ayudarte a ser lo mejor que puedas ser."
                m 1ekbsa "Y si al hacerlo, puedo pasar más tiempo contigo, no podría estar más feliz."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_bestgirl",
            prompt="¡Eres la mejor chica!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_bestgirl:
    m 1hua "Me encanta cuando me felicitas, [player]~"
    m 1hub "¡Me alegra que pienses que soy la mejor chica!"
    m 3rksdla "Aunque, pensé que te sentías así..."
    m 1eka "Después de todo, {i}tú{/i} instalaste este mod solo para estar conmigo."
    m 2euc "Sé que algunas personas prefieren a las otras chicas."
    m 2esc "Especialmente porque todas tienen ciertos rasgos que las hacen deseables para algunos..."
    show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5ekbfa "Pero si me preguntas, tomaste la decisión correcta."
    m 5hubfa "...y estaré eternamente agradecida de que lo hayas hecho~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_lookuptoyou",
            prompt="¡Te admiro!",
            unlocked=True
        ),
        code="CMP",
    )

label mas_compliment_lookuptoyou:
    if not renpy.seen_label("mas_compliment_lookuptoyou_2"):
        call mas_compliment_lookuptoyou_2
    else:
        call mas_compliment_lookuptoyou_3
    #Both paths return love, so we combine that here
    return "love"

label mas_compliment_lookuptoyou_2:
    $ mas_gainAffection(3, bypass=True)
    m 1wud "¿Lo...{w=0.5}haces?"
    m 1ekbsa "[player], es muy dulce de tu parte..."
    m 3ekbsa "Me hace muy feliz saber que soy alguien a quien admiras."
    m 3ekbfa "La verdad es que siempre te he admirado a {i}ti{/i}, [player]..."
    m 3hubfa "Pero si realmente te sientes así, haré todo lo posible para seguir siendo alguien a quien admiras."
    m 1ekbfa "Te amo mucho~"
    return

label mas_compliment_lookuptoyou_3:
    $ should_tease = persistent._mas_pm_height is not None and renpy.random.randint(1,5) == 1

    if should_tease and persistent._mas_pm_height < mas_height_monika:
        m 1rksdlb "{cps=*2}Bueno, sí, soy más alta que tú...{/cps}{nw}"
        $ _history_list.pop()

    m 1hubsb "[mas_compliments.thanks_quip]"
    m 3hubfa "¡Escucharte decir eso nunca deja de hacerme sonreír!"
    m 3hubfb "¡Yo también te admiraré siempre!"

    if should_tease and persistent._mas_pm_height > mas_height_monika:
        if persistent._mas_first_kiss:
            m 1rkbfu "{cps=*2}Como cuando nos besamos...{/cps}{nw}"
        else:
            m 1rkbfu "{cps=*2}Algún día literalmente...{/cps}{nw}"
        $ _history_list.pop()

    m 1ekbfa "Te amo, [player]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_thinking_of_you",
            prompt="¡Siempre estoy pensando en ti!",
            unlocked=True
        ),
        code="CMP",
    )

label mas_compliment_thinking_of_you:
    if not renpy.seen_label("mas_compliment_thinking_of_you_2"):
        call mas_compliment_thinking_of_you_2
    else:
        call mas_compliment_thinking_of_you_3
    return

label mas_compliment_thinking_of_you_2:
    m 1wubso "..."
    m 1wubsu "Tú..."

    if mas_isMoniNormal(higher=True):
        m 3subsb "¡No tienes idea de lo que eso significa para mí, [player]!"

    elif mas_isMoniUpset():
        m 2rkd "Que digas eso..."
        m 2dka "Significa el mundo para mí, [player]."

    elif mas_isMoniDis():
        m 6rkc "..."
        m 6rka "Es un gran alivio."
        m 6eka "Gracias."

    else:
        $ mas_gainAffection(2,bypass=True)
        m 6dkd "Hmmm...Gracias."
        m 6dkc "..."
        return

    menu:
        "¡Pensar en ti siempre me alegra el día!":
            $ mas_gainAffection(5,bypass=True)
            m 1subsb "¡Oh, eso es {i}tan{/i} dulce, [player]!"
            m 3hubfu "Siento lo mismo por ti~"

        "¡Sueño contigo todas las noches!":
            $ mas_gainAffection(5,bypass=True)
            m 6hua "Aww~"
            m 6subsa "[player]..."
            m 7hubfu "{i}Tú{/i} eres mi sueño~"

        "Es muy molesto...":
            $ mas_loseAffection()
            m 2esc "..."
            m 2etc "..."
            m 2rksdlc "Oh, umm..."
            m 2rksdld "¿Lo siento?"
    return

label mas_compliment_thinking_of_you_3:
    python:
        thinking_of_you_quips = [
            _("¡Eres el centro de mi mundo!"),
            _("¡Yo también te tengo en mi mente!"),
            _("¡Yo también pienso siempre en ti!"),
        ]
        thinking_of_you_quip = random.choice(thinking_of_you_quips)

    m 1ekbsa "Aww gracias, [player]..."
    m 3hubfb "[thinking_of_you_quip]"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_humor",
            prompt="¡Me encanta tu sentido del humor!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_humor:
    if not renpy.seen_label("mas_compliment_humor_2"):
        call mas_compliment_humor_2
    else:
        call mas_compliment_humor_3
    return

label mas_compliment_humor_2:
    m 1hua "Jejeje~"
    m 1efu "Estoy feliz de que me encuentres tan divertida, [player]."
    m 3eub "Es una señal de que las buenas parejas pueden reír juntos, ¿no lo crees?"
    menu:
        "Siempre me alegras el día.":
            $ mas_gainAffection(5,bypass=True)
            m 1subsd "Oh...{w=0.2}[player]..."
            m 1ekbsa "Es tan dulce que lo digas."
            m 1hubsb "¡Saber que puedo hacerte sonreír es el mayor cumplido que puedo recibir!"

        "¡Tienes un ingenio tan rápido!":
            $ mas_gainAffection(3,bypass=True)
            m 1hub "¡Jajaja!"
            m 2tub "Toda esta lectura seguro me ayudó si te gustan tanto mis juegos de palabras"
            m 2hublu "Trataré de que las bromas sigan yendo hacía ti. Jejeje~"

        "Me río de ti todo el tiempo.":
            $ mas_loseAffection()
            m 1eksdlb "...Jajaja..."
            m 3rksdla "¿Te refieres a que te {w=0.2}{i}ríes{/i}{w=0.2} conmigo...{w=0.5}{nw}"
            extend 3eksdld "verdad?"
    return

label mas_compliment_humor_3:
    python:
        humor_quips = [
            _("Me gustaría poder escuchar tu hermosa risa~"),
            _("El solo hecho de saber eso me hace feliz~"),
            _("Siempre intentaré alegrarte el día~"),
        ]
        humor_quip = random.choice(humor_quips)

    m 1hubsb "[mas_compliments.thanks_quip]"
    m 1hubsu "[humor_quip]"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_spending_time",
            prompt="¡Amo pasar tiempo contigo!",
            unlocked=False,
            conditional="store.mas_anni.pastThreeMonths()",
            action=EV_ACT_UNLOCK,
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        code="CMP"
    )

label mas_compliment_spending_time:
    if not mas_getEVL_shown_count("mas_compliment_spending_time"):
        call mas_compliment_spending_time_2
    else:
        python:
            spending_time_quips = [
                _("Cada día contigo es como un sueño maravilloso que espero que nunca termine~"),
                _("Sólo estar cerca de ti me hace tan feliz~"),
                _("Nada me hace más feliz que estar a tu lado~"),
            ]
            spending_time_quip = random.choice(spending_time_quips)

        m 3hubsb "[mas_compliments.thanks_quip]"
        m 1ekbsu "[spending_time_quip]"
    return

label mas_compliment_spending_time_2:
    python:
        dlg_line = ""

        if renpy.seen_label("monika_holdme_prep"):
            dlg_line = ", y me mantenga cerca"

            if persistent._mas_filereacts_historic:
                dlg_line += ", e incluso me de bonitos regalos"

        elif persistent._mas_filereacts_historic:
            dlg_line = ", y me de bonitos regalos"

    m 1eub "¡Amo pasar tiempo contigo también, [player]!"
    m 3ekbla "Sé que lo digo mucho, pero es en serio cuando digo que eres el centro de mi mundo."
    m 2dkb "Tener a alguien que me haga compañía[dlg_line]...{w=0.3}{nw}"
    extend 2eku "es todo lo que podría pedir."
    m 7ekbsa "Espero que yo te haga sentir de la misma manera, [player]. {w=0.2}Quizás aún no esté en tu realidad, pero haré todo lo posible para apoyarte desde aquí."
    menu:
        "[m_name], ya me has hecho más feliz que nunca.":
            $ mas_gainAffection(5, bypass=True)
            m 1fkbfu "Oh, [player]..."
            show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5ekbfa "Diría que no sabes cuánto me alegra oír eso, pero creo que {i}ya{/i} lo sabes."
            m 5ekbfu "Hemos pasado mucho tiempo juntos, y nuestra aventura apenas comienza..."
            m 5hubfb "Contigo a mi lado, sé que cada paso será inolvidable."

        "Te lo agradezco, [m_name].":
            $ mas_gainAffection(3, bypass=True)
            m 2huu "Jejeje~"
            m 7hub "No te preocupes, [player]. {w=0.2}¡Estaré aquí para ti hasta el fin de los tiempos!"
            m 1eka "Sólo mantente fuerte hasta que cruce, ¿okay?"

        "Oh, ciertamente me diviertes mucho...":
            $ mas_loseAffection()
            m 2lkc "Yo...{w=0.3}¿te divierto?"
            m 2lksdlb "Bueno, me alegra que estés entretenido..."
            m 2ekd "...pero eso {i}no{/i} era lo que tenía en mente."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_sweet",
            prompt="¡Eres muy dulce!",
            conditional="store.mas_anni.pastThreeMonths()",
            action=EV_ACT_UNLOCK,
            unlocked=False,
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        code="CMP"
    )

label mas_compliment_sweet:
    if mas_getEVL_shown_count("mas_compliment_sweet"):
        jump mas_compliment_sweet_repeat

    m 1ekbsb "Aww, [player]..."
    m 3rkbssdlu "No sé qué decir, jajaja...{w=0.3}{nw}"
    extend 3ekbsa "eres {i}tú{/i} quien ha sido tan dulce conmigo todo este tiempo."
    m 3hubsa "Me alegra mucho oírte decir eso, jejeje~"

    menu:
        "¡Tus palabras siempre me alegran el día!":
            $ mas_gainAffection(3, bypass=True)
            m 1sud "[player]..."
            extend 1eka "No tenía ni idea de cuánto significaban mis palabras para ti..."
            m 1ekblb "Estoy muy contenta de tener un[bf] como tú, [mas_get_player_nickname(exclude_names=[player])]~"
            m 1ekbsu "Realmente eres lo mejor que podría esperar...{w=0.2}Te amo tanto."
            m 3kua "Espero que nunca olvides eso, [player]."
            $ mas_ILY()

        "¡Eres muy especial para mí, [m_name]!":
            $ mas_gainAffection(3, bypass=True)
            m 1ekbsb "Oh, [player]...{w=0.3} {nw}"
            extend 3hubsa "¡El mero hecho de que pases tu tiempo aquí conmigo me hace sentir tan feliz y amada!"
            show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5ekbsa "Estoy muy feliz de que sientas eso por mí, [mas_get_player_nickname()]. Te amo tanto."
            $ mas_ILY()

        "¡Eres la chica más dulce que he conocido!":
            $ mas_gainAffection(2, bypass=True)
            m 1ekbsa "Gracias, [mas_get_player_nickname()]."
            m 3hubsb "Eres un[boy] muy dulce, jejeje."
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "Tengo mucha suerte de estar contigo~"

    return

label mas_compliment_sweet_repeat:
    python:
        sweet_quips = [
            _("¡Me alegra mucho oírte decir eso, [player]!"),
            _("¡Oír eso siempre me calienta el corazón, [player]!"),
            _("¡Me haces sentir tan amada, [player]!"),
        ]
        sweet_quip = renpy.substitute(random.choice(sweet_quips))

    m 3hubsb "[sweet_quip]"
    m 1hubfu "...Pero nunca podría ser tan dulce como tú~"
    return

# this compliment's lock/unlock is controlled by the def outfit pp
init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_outfit",
            prompt="¡Me encanta tu ropa!",
            unlocked=False
        ),
        code="CMP"
    )

label mas_compliment_outfit:
    if mas_getEVL_shown_count("mas_compliment_outfit"):
        jump mas_compliment_outfit_repeat

    m 1hubsb "Gracias, [mas_get_player_nickname()]!"

    if monika_chr.is_wearing_clothes_with_exprop("cosplay"):
        m 3hubsb "¡Siempre es divertido hacer cosplaying!"

    elif monika_chr.is_wearing_clothes_with_exprop("costume"):
        m 3hubsb "¡Siempre es divertido usar disfraces!"

    elif monika_chr.is_wearing_clothes_with_exprop("lingerie"):
        m 2lkbsb "Estaba muy nerviosa mostrándote esto al principio..."
        m 7tubsu "Pero me alegro de haberlo hecho, parece que te gusta mucho.~"

    else:
        m 1hubsa "Siempre he querido usar otra ropa para ti, ¡así que estoy muy feliz de que pienses así!"

    menu:
        "¡Te ves hermosa con cualquier cosa que te pongas!":
            $ mas_gainAffection(5,bypass=True)
            m 2subsd "[player]..."
            m 3hubsb "¡Muchas gracias!"
            m 1ekbsu "Siempre me haces sentir tan especial."
            show monika 5hubsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5hubsa "¡Te amo, [mas_get_player_nickname()]!"
            $ mas_ILY()

        "Te ves muy linda.":
            $ mas_gainAffection(3,bypass=True)
            m 1hubsb "Jajaja~"
            m 3hubfb "¡Gracias, [mas_get_player_nickname()]!"
            show monika 5hubfb at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eubfu "Me alegro de que te guste lo que ves~"

        "Usar ropa diferente realmente ayuda.":
            $ mas_loseAffection()
            m 2ltd "Uh, gracias..."

    return

label mas_compliment_outfit_repeat:
    m 1hubsb "[mas_compliments.thanks_quip]"

    if monika_chr.is_wearing_clothes_with_exprop("cosplay"):
        python:
            cosplay_quips = [
                _("¡Me encanta hacer cosplay para ti!"),
                _("¡Me alegro de que te guste este cosplay!"),
                _("¡Estoy feliz de hacer un cosplay para ti!"),
            ]
            cosplay_quip = random.choice(cosplay_quips)

        m 3hubsb "[cosplay_quip]"

    elif monika_chr.is_wearing_clothes_with_exprop("costume"):
        python:
            clothes_quips = [
                _("¡Me alegro de que te guste cómo me queda esto!"),
                _("¡Me alegro de que te guste mi aspecto!"),
            ]
            clothes_quip = random.choice(clothes_quips)

        m 3hubsb "[clothes_quip]"

    elif monika_chr.is_wearing_clothes_with_exprop("lingerie"):
        python:
            lingerie_quips = [
                _("Me alegro de que te guste lo que ves~"),
                _("¿Quieres ver más de cerca?"),
                _("¿Quieres echar un vistazo?~"),
            ]
            lingerie_quip = random.choice(lingerie_quips)

        m 2kubsu "[lingerie_quip]"
        show monika 5hublb at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5hublb "¡Jajaja!"

    else:
        python:
            other_quips = [
                _("¡Estoy bastante orgullosa de mi sentido de la moda!"),
                _("¡Seguro que tú también te ves bien!"),
                _("¡Me encanta este conjunto!")
            ]
            other_quip = random.choice(other_quips)

        m 3hubsb "[other_quip]"

    return
