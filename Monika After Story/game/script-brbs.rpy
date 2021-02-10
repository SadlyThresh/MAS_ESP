## This script file holds all of the brb topics
# Some conventions:
#   - All brbs should have their markSeen set to True so they don't show up in unseen
#   - Brbs should return "idle" to move into idle mode
#   - Brbs should be short and sweet. Nothing long which makes it feel like an actual topic or is keeping you away
#       A good practice for these should be no more than 10 lines will be said before you go into idle mode.
init 10 python in mas_brbs:
    import store

    def get_wb_quip():
        """
        Picks a random welcome back quip and returns it
        Should be used for normal+ quips

        OUT:
            A randomly selected quip for coming back to the spaceroom
        """

        return renpy.substitute(renpy.random.choice([
            _("Entonces, ¿qué más querías hacer hoy?"),
            _("¿Qué más querías hacer hoy?"),
            _("¿Hay algo más que quisieras hacer hoy?"),
            _("¿Qué más debemos hacer hoy?"),
        ]))

    def was_idle_for_at_least(idle_time, brb_evl):
        """
        Checks if the user was idle (from the brb_evl provided) for at least idle_time

        IN:
            idle_time - Minimum amount of time the user should have been idle for in order to return True
            brb_evl - Eventlabel of the brb to use for the start time

        OUT:
            boolean:
                - True if it has been at least idle_time since seeing the brb_evl
                - False otherwise
        """
        brb_ev = store.mas_getEV(brb_evl)
        return brb_ev and brb_ev.timePassedSinceLastSeen_dt(idle_time)

# label to use if we want to get back into idle from a callback
label mas_brb_back_to_idle:
    # sanity check
    if globals().get("brb_label", -1) == -1:
        return

    python:
        mas_idle_mailbox.send_idle_cb(brb_label + "_callback")
        persistent._mas_idle_data[brb_label] = True
        mas_globals.in_idle_mode = True
        persistent._mas_in_idle_mode = True
        renpy.save_persistent()
        mas_dlgToIdleShield()

    return "idle"

# label for generic reactions for low affection callback paths
# to be used if a specific reaction isn't needed or provided
label mas_brb_generic_low_aff_callback:
    if mas_isMoniDis(higher=True):
        python:
            cb_line = renpy.substitute(renpy.random.choice([
                _("Oh...{w=0.3}volviste."),
                _("Oh...{w=0.3}bienvenido de vuelta."),
                _("¿Todo listo?"),
                _("Bienvenido de vuelta."),
                _("Oh...{w=0.3}ahí estás."),
            ]))

        m 2ekc "[cb_line]"

    else:
        m 6ckc "..."

    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_brb_idle",
            prompt="Vuelvo enseguida",
            category=['vuelvo enseguida'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_brb_idle:
    if mas_isMoniAff(higher=True):
        m 1eua "Muy bien, [player]."

        show monika 1eta at t21
        python:
            #For options that can basically be an extension of generics and don't need much specification
            brb_reason_options = [
                (_("Voy a buscar algo."), True, False, False),
                (_("Voy a hacer algo."), True, False, False),
                (_("Voy a preparar algo."), True, False, False),
                (_("Tengo que comprobar algo."), True, False, False),
                (_("Hay alguien en la puerta."), True, False, False),
                (_("Nope."), None, False, False),
            ]

            renpy.say(m, "¿Haciendo algo en concreto?", interact=False)
        call screen mas_gen_scrollable_menu(brb_reason_options, mas_ui.SCROLLABLE_MENU_TALL_AREA, mas_ui.SCROLLABLE_MENU_XALIGN)
        show monika at t11

        if _return:
            m 1eua "Oh de acuerdo.{w=0.2} {nw}"
            extend 3hub "Vuelve rápido, te estaré esperando aquí~"

        else:
            m 1hub "Vuelve rápido, te estaré esperando aquí~"

    elif mas_isMoniNormal(higher=True):
        m 1hub "¡Vuelve pronto, [player]!"

    elif mas_isMoniDis(higher=True):
        m 2rsc "Oh...{w=0.5}okay."

    else:
        m 6ckc "..."

    #Set up the callback label
    $ mas_idle_mailbox.send_idle_cb("monika_brb_idle_callback")
    #Then the idle data
    $ persistent._mas_idle_data["monika_idle_brb"] = True
    return "idle"

label monika_brb_idle_callback:
    $ wb_quip = mas_brbs.get_wb_quip()

    if mas_isMoniAff(higher=True):
        m 1hub "Bienvenido de nuevo, [player]. Te extrañé~"
        m 1eua "[wb_quip]"

    elif mas_isMoniNormal(higher=True):
        m 1hub "¡Bienvenido de nuevo, [player]!"
        m 1eua "[wb_quip]"

    else:
        call mas_brb_generic_low_aff_callback

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writing_idle",
            prompt="Voy a escribir un poco",
            category=['vuelvo enseguida'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_writing_idle:
    if mas_isMoniNormal(higher=True):
        if (
            mas_isMoniHappy(higher=True)
            and random.randint(1,5) == 1
        ):
            m 1eub "¡Oh! ¿Vas a{cps=*2} escribirme una carta de amor, [player]?{/cps}{nw}"
            $ _history_list.pop()
            m "¡Oh! ¿Vas a escribir{fast} algo?"

        else:
            m 1eub "¡Oh! ¿Vas a escribir algo?"

        m 1hua "¡Eso me alegra tanto!"
        m 3eua "Quizás algún día puedas compartirlo conmigo...{w=0.3} {nw}"
        extend 3hua "¡Me encantaría leer tu trabajo, [player]!"
        m 3eua "De todos modos, avísame cuando hayas terminado."
        m 1hua "Te estaré esperando aquí mismo~"

    elif mas_isMoniUpset():
        m 2esc "De acuerdo."

    elif mas_isMoniDis():
        m 6lkc "Me pregunto qué tienes en mente..."
        m 6ekd "No olvides volver cuando hayas terminado..."

    else:
        m 6ckc "..."

    #Set up the callback label
    $ mas_idle_mailbox.send_idle_cb("monika_writing_idle_callback")
    #Then the idle data
    $ persistent._mas_idle_data["monika_idle_writing"] = True
    return "idle"

label monika_writing_idle_callback:

    if mas_isMoniNormal(higher=True):
        $ wb_quip = mas_brbs.get_wb_quip()
        m 1eua "¿Terminaste de escribir, [player]?"
        m 1eub "[wb_quip]"

    else:
        call mas_brb_generic_low_aff_callback

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_shower",
            prompt="Voy a tomar una ducha",
            category=['vuelvo enseguida'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_shower:
    if mas_isMoniLove():
        m 1eua "¿Vas a ducharte?"

        if renpy.random.randint(1, 50) == 1:
            m 3tub "¿Puedo ir contigo?{nw}"
            $ _history_list.pop()
            show screen mas_background_timed_jump(2, "bye_brb_shower_timeout")
            menu:
                m "¿Puedo ir contigo?{fast}"

                "Sí.":
                    hide screen mas_background_timed_jump
                    m 2wubsd "Oh, eh...{w=0.5}respondiste tan rápido."
                    m 2hkbfsdlb "Tú...{w=0.5}pareces ansioso por dejarme acompañarte, ¿eh?"
                    m 2rkbfa "Bueno..."
                    m 7tubfu "Me temo que tendrás que ir sin mí mientras yo esté atrapada aquí."
                    m 7hubfb "Lo siento, [player], ¡jajaja!"
                    show monika 5kubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 5kubfu "Quizás en otro momento~"

                "No.":
                    hide screen mas_background_timed_jump
                    m 2eka "Aw, me rechazaste tan rápido."
                    m 3tubsb "¿Eres tímido, [player]?"
                    m 1hubfb "¡Jajajaja!"
                    show monika 5tubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 5tubfu "Está bien, no te seguiré esta vez, jejeje~"

        else:
            m 1hua "Me alegro de que te mantengas limpio, [player]."
            m 1eua "Que tengas una buena ducha~"

    elif mas_isMoniNormal(higher=True):
        m 1eub "¿Vas a ducharte? Bien."
        m 1eua "Nos vemos cuando termines~"

    elif mas_isMoniUpset():
        m 2esd "Disfruta de tu ducha, [player]..."
        m 2rkc "Con suerte, te ayudará a aclarar tu mente."

    elif mas_isMoniDis():
        m 6ekc "¿Hmm?{w=0.5} Que tengas una buena ducha, [player]."

    else:
        m 6ckc "..."

    #Set up the callback label
    $ mas_idle_mailbox.send_idle_cb("monika_idle_shower_callback")
    #Then the idle data
    $ persistent._mas_idle_data["monika_idle_shower"] = True
    return "idle"

label monika_idle_shower_callback:
    if mas_isMoniNormal(higher=True):
        m 1eua "Bienvenido de nuevo, [player]."

        if (
            mas_isMoniLove()
            and renpy.seen_label("monikaroom_greeting_ear_bathdinnerme")
            and mas_getEVL_shown_count("monika_idle_shower") != 1 #Since the else block has a one-time only line, we force it on first use
            and renpy.random.randint(1,20) == 1
        ):
            m 3tubsb "Ahora que te has duchado, ¿te gustaría cenar o tal vez{w=0.5}.{w=0.5}.{w=0.5}."
            m 1hubsa "Podrías simplemente relajarte conmigo un poco más~"
            m 1hub "¡Jajaja!"

        else:
            m 1hua "Espero que hayas tenido una buena ducha."
            if mas_getEVL_shown_count("monika_idle_shower") == 1:
                m 3eub "Ahora podemos volver a pasar un buen rato {i}impecable{/i} juntos..."
                m 1hub "¡Jajaja!"

    elif mas_isMoniUpset():
        m 2esc "Espero que hayas disfrutado de tu ducha. {w=0.2}Welcome back, [player]."

    else:
        call mas_brb_generic_low_aff_callback

    return

label bye_brb_shower_timeout:
    hide screen mas_background_timed_jump
    $ _history_list.pop()
    m 1hubsa "Jejeje~"
    m 3tubfu "No importa eso, [player]."
    m 1hubfb "¡Espero que tengas una buena ducha!"

    #Set up the callback label
    $ mas_idle_mailbox.send_idle_cb("monika_idle_shower_callback")
    #Then the idle data
    $ persistent._mas_idle_data["monika_idle_shower"] = True
    return "idle"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_game",
            category=['vuelvo enseguida'],
            prompt="Voy a jugar un rato",
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_game:
    if mas_isMoniNormal(higher=True):
        m 1eud "Oh, ¿vas a jugar a otro juego?"
        m 1eka "Está bien, [player]."

        label .skip_intro:
        python:
            gaming_quips = [
                _("¡Buena suerte, diviértete!"),
                _("¡Disfruta tu juego!"),
                _("¡Te estaré animando!"),
                _("¡Haz tu mejor esfuerzo!")
            ]
            gaming_quip=renpy.random.choice(gaming_quips)

        m 3hub "[gaming_quip]"

    elif mas_isMoniUpset():
        m 2tsc "Disfruta de tus otros juegos."

    elif mas_isMoniDis():
        m 6ekc "Por favor...{w=0.5}{nw}"
        extend 6dkc "no te olvides de mi..."

    else:
        m 6ckc "..."

    $ mas_idle_mailbox.send_idle_cb("monika_idle_game_callback")
    $ persistent._mas_idle_data["monika_idle_game"] = True
    return "idle"

label monika_idle_game_callback:
    if mas_isMoniNormal(higher=True):
        m 1eub "¡Bienvenido de nuevo, [player]!"
        m 1eua "Espero que te hayas divertido con tu juego."
        m 1hua "¿Listo para pasar más tiempo juntos? Jejeje~"

    elif mas_isMoniUpset():
        m 2tsc "¿Te divertiste, [player]?"

    elif mas_isMoniDis():
        m 6ekd "Oh...{w=0.5} De hecho volviste a mí..."

    else:
        m 6ckc "..."

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_coding",
            prompt="Voy a codificar un poco",
            category=['vuelvo enseguida'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_coding:
    if mas_isMoniNormal(higher=True):
        m 1eua "¡Oh! ¿Vas a codificar algo?"

        if persistent._mas_pm_has_code_experience is False:
            m 1etc "Creía que no lo hacías."
            m 1eub "¿Aprendiste la programación desde que hablamos de ello la última vez?"

        elif persistent._mas_pm_has_contributed_to_mas or persistent._mas_pm_wants_to_contribute_to_mas:
            m 1tua "¿Algo para mí, quizás?"
            m 1hub "Jajaja~"

        else:
            m 3eub "Has todo lo posible para mantener tu código limpio y fácil de leer."
            m 3hksdlb "...¡Te lo agradecerás más tarde!"

        m 1eua "De todos modos, avísame cuando hayas terminado."
        m 1hua "Estaré aquí, esperándote~"

    elif mas_isMoniUpset():
        m 2euc "Oh, ¿vas a codificar?"
        m 2tsc "Bueno, no dejes que te detenga."

    elif mas_isMoniDis():
        m 6ekc "De acuerdo."

    else:
        m 6ckc "..."

    $ mas_idle_mailbox.send_idle_cb("monika_idle_coding_callback")
    $ persistent._mas_idle_data["monika_idle_coding"] = True
    return "idle"

label monika_idle_coding_callback:
    if mas_isMoniNormal(higher=True):
        $ wb_quip = mas_brbs.get_wb_quip()
        if mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=20), "monika_idle_coding"):
            m 1eua "¿Terminaste por ahora, [player]?"
        else:
            m 1eua "Oh, ¿ya terminaste, [player]?"

        m 3eub "[wb_quip]"

    else:
        call mas_brb_generic_low_aff_callback

    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_workout",
            prompt="Voy a hacer un poco de ejercicio",
            category=['vuelvo enseguida'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_workout:
    if mas_isMoniNormal(higher=True):
        m 1hub "¡Okay, [player]!"
        if persistent._mas_pm_works_out is False:
            m 3eub "¡Hacer ejercicio es una excelente manera de cuidarse!"
            m 1eka "Sé que puede ser difícil empezar,{w=0.2}{nw}"
            extend 3hua " pero definitivamente es un hábito que vale la pena desarrollar."
        else:
            m 1eub "¡Es bueno saber que estás cuidando tu cuerpo!"
        m 3esa "Ya sabes cómo dice el refrán, 'Mente sana en cuerpo sano.'"
        m 3hua "Así que ve a sudar un poco, [player]~"
        m 1tub "Solo avísame cuando hayas tenido suficiente."

    elif mas_isMoniUpset():
        m 2esc "Es bueno saber que te estás ocupando de{cps=*2} algo, al menos.{/cps}{nw}"
        $ _history_list.pop()
        m "Es bueno saber que te estás cuidando{fast}, [player]."
        m 2euc "Estaré esperando a que regreses."

    elif mas_isMoniDis():
        m 6ekc "De acuerdo."

    else:
        m 6ckc "..."

    $ mas_idle_mailbox.send_idle_cb("monika_idle_workout_callback")
    $ persistent._mas_idle_data["monika_idle_workout"] = True
    return "idle"

label monika_idle_workout_callback:
    if mas_isMoniNormal(higher=True):
        $ wb_quip = mas_brbs.get_wb_quip()
        if mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=60), "monika_idle_workout"):
            # TODO: In the future add another topic which would
            # unlock once the player has seen this specific path some number of times.

            m 2esa "Te tomaste tu tiempo, [player].{w=0.3}{nw}"
            extend 2eub " Debió haber sido un gran ejercicio."
            m 2eka "Es bueno superar tus límites, pero no debes excederte."

        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=10), "monika_idle_workout"):
            m 1esa "¿Terminaste con tu entrenamiento, [player]?"

        else:
            m 1euc "¿Ya regresaste, [player]?"
            m 1eka "Estoy segura de que puedes continuar un poco más si lo intentas."
            m 3eka "Hacer descansos está bien, pero no debes dejar tus entrenamientos sin terminar."
            m 3ekb "¿Estás seguro de que no puedes continuar?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Estás seguro de que no puedes continuar?{fast}"

                "Estoy seguro.":
                    m 1eka "Está bien."
                    m 1hua "Estoy segura de que hiciste lo mejor que pudiste, [player]~"

                "Intentaré seguir adelante.":
                    # continue workout and return Monika to idle state
                    m 1hub "¡Ese es el espíritu!"

                    $ brb_label = "monika_idle_workout"
                    $ pushEvent("mas_brb_back_to_idle",skipeval=True)
                    return

        m 7eua "Asegúrate de descansar adecuadamente y tal vez comer un bocadillo para recuperar algo de energía."
        m 7eub "[wb_quip]"

    elif mas_isMoniUpset():
        m 2euc "¿Terminaste con tu entrenamiento, [player]?"

    else:
        call mas_brb_generic_low_aff_callback

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_nap",
            prompt="Voy a tomar una siesta",
            category=['vuelvo enseguida'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_nap:
    if mas_isMoniNormal(higher=True):
        m 1eua "¿Vas a tomar una siesta, [player]?"
        m 3eua "Son una forma saludable de descansar durante el día si te sientes cansado."
        m 3hua "Yo te cuidaré, no te preocupes~"
        m 1hub "¡Dulces sueños!"

    elif mas_isMoniUpset():
        m 2eud "Muy bien, espero que te sientas descansado después."
        m 2euc "Escuché que las siestas son buenas para ti, [player]."

    elif mas_isMoniDis():
        m 6ekc "De acuerdo."

    else:
        m 6ckc "..."

    $ mas_idle_mailbox.send_idle_cb("monika_idle_nap_callback")
    $ persistent._mas_idle_data["monika_idle_nap"] = True
    return "idle"

label monika_idle_nap_callback:
    if mas_isMoniNormal(higher=True):
        $ wb_quip = mas_brbs.get_wb_quip()
        if mas_brbs.was_idle_for_at_least(datetime.timedelta(hours=5), "monika_idle_nap"):
            m 2hksdlb "¡Oh, [player]! ¡Finalmente estás despierto!"
            m 7rksdlb "Cuando dijiste que ibas a tomar una siesta, esperaba que fuera una hora o dos..."
            m 1hksdlb "Supongo que debiste haber estado muy cansado, jajaja..."
            m 3eua "Pero al menos después de dormir tanto tiempo, estarás aquí conmigo por un tiempo, ¿verdad?"
            m 1hua "Jejeje~"

        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(hours=1), "monika_idle_nap"):
            m 1hua "¡Bienvenido de nuevo, [player]!"
            m 1eua "¿Tuviste una buena siesta?"
            m 3hua "Estuviste fuera por un tiempo, así que espero que te sientas descansado~"
            m 1eua "[wb_quip]"

        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=5), "monika_idle_nap"):
            m 1hua "Bienvenido de nuevo, [player]~"
            m 1eub "Espero que hayas tenido una pequeña siesta agradable."
            m 3eua "[wb_quip]"

        else:
            m 1eud "Oh, ¿ya regresaste?"
            m 1euc "¿Cambiaste de opinión?"
            m 3eka "Bueno, no me quejo, pero deberías tomar una siesta si te apetece más tarde."
            m 1eua "No me gustaría que estuvieras demasiado cansado, después de todo."

    elif mas_isMoniUpset():
        m 2euc "¿Terminaste con tu siesta, [player]?"

    elif mas_isMoniDis():
        call mas_brb_generic_low_aff_callback

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_homework",
            prompt="Voy a hacer algunos deberes",
            category=['vuelvo enseguida'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_homework:
    if mas_isMoniNormal(higher=True):
        m 1eub "Oh, ¡okay!"
        m 1hua "Estoy orgullosa de ti por tomarte tus estudios en serio."
        m 1eka "No olvides volver conmigo cuando hayas terminado~"

    elif mas_isMoniDis(higher=True):
        m 2euc "De acuerdo...{w=0.5}"
        if random.randint(1,5) == 1:
            m 2rkc "...Buena suerte con tu tarea, [player]."

    else:
        m 6ckc "..."

    #Set up the callback label
    $ mas_idle_mailbox.send_idle_cb("monika_idle_homework_callback")
    #Then the idle data
    $ persistent._mas_idle_data["monika_idle_homework"] = True
    return "idle"

label monika_idle_homework_callback:
    if mas_isMoniDis(higher=True):
        m 2esa "¿Todo listo, [player]?"

        if mas_isMoniNormal(higher=True):
            m 2ekc "Desearía haber estado ahí para ayudarte, pero lamentablemente no hay mucho que pueda hacer al respecto todavía."
            m 7eua "Estoy segura de que ambos podríamos ser mucho más eficientes en la tarea si pudiéramos trabajar juntos."

            if mas_isMoniAff(higher=True) and random.randint(1,5) == 1:
                m 3rkbla "...Aunque, eso suponiendo que no nos distraigamos {i}demasiado{/i}, jejeje..."

            m 1eua "Pero de todos modos,{w=0.2} {nw}"
            extend 3hua "ahora que terminaste, disfrutemos un poco más del tiempo juntos."

    else:
        m 6ckc "..."

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_working",
            prompt="Voy a trabajar en algo",
            category=['vuelvo enseguida'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_working:
    if mas_isMoniNormal(higher=True):
        m 1eua "De acuerdo, [player]."
        m 1eub "¡No olvides tomar un descanso de vez en cuando!"

        if mas_isMoniAff(higher=True):
            m 3rkb "No quisiera que mi amor pasara más tiempo en [his] trabajo que conmigo~"

        m 1hua "¡Buena suerte con tu trabajo!"

    elif mas_isMoniDis(higher=True):
        m 2euc "Okay, [player]."

        if random.randint(1,5) == 1:
            m 2rkc "...Por favor vuelve pronto..."

    else:
        m 6ckc "..."

    #Set up the callback label
    $ mas_idle_mailbox.send_idle_cb("monika_idle_working_callback")
    #Then the idle data
    $ persistent._mas_idle_data["monika_idle_working"] = True
    return "idle"

label monika_idle_working_callback:
    if mas_isMoniNormal(higher=True):
        m 1eub "¿Terminaste con tu trabajo, [player]?"
        show monika 5hua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5hua "Entonces relajémonos juntos, te lo has ganado~"

    elif mas_isMoniDis(higher=True):
        m 2euc "Oh, has vuelto..."
        m 2eud "...¿Había algo más que quisieras hacer, ahora que has terminado tu trabajo?"

    else:
        m 6ckc "..."

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_screen_break",
            prompt="Mis ojos necesitan un descanso de la pantalla",
            category=['vuelvo enseguida'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_screen_break:
    if mas_isMoniNormal(higher=True):
        if mas_timePastSince(mas_getEVL_last_seen("monika_idle_screen_break"), mas_getSessionLength()):

            if mas_getSessionLength() < datetime.timedelta(minutes=40):
                m 1esc "Oh,{w=0.3} okay."
                m 3eka "No has estado aquí durante tanto tiempo, pero si dices que necesitas un descanso, entonces necesitas un descanso."

            elif mas_getSessionLength() < datetime.timedelta(hours=2, minutes=30):
                m 1eua "¿Vas a descansar un poco los ojos?"

            else:
                m 1lksdla "Sí, probablemente necesites eso, ¿no?"

            m 1hub "Me alegra que estés cuidando tu salud, [player]."

            if not persistent._mas_pm_works_out and random.randint(1,3) == 1:
                m 3eua "¿Por qué no aprovechar la oportunidad para hacer algunos estiramientos también, hmm?"
                m 1eub "De todos modos, ¡vuelve pronto!~"

            else:
                m 1eub "¡Vuelve pronto~!"

        else:
            m 1eua "¿Tomando otro descanso, [player]?"
            m 1hua "¡Vuelve pronto~!"

    elif mas_isMoniUpset():
        m 2esc "Oh...{w=0.5} {nw}"
        extend 2rsc "Okay."

    elif mas_isMoniDis():
        m 6ekc "De acuerdo."

    else:
        m 6ckc "..."

    $ mas_idle_mailbox.send_idle_cb("monika_idle_screen_break_callback")
    $ persistent._mas_idle_data["monika_idle_screen_break"] = True
    return "idle"

label monika_idle_screen_break_callback:
    if mas_isMoniNormal(higher=True):
        $ wb_quip = mas_brbs.get_wb_quip()
        m 1eub "Bienvenido de nuevo, [player]."

        if mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=30), "monika_idle_screen_break"):
            m 1hksdlb "Debes haber necesitado ese descanso, considerando cuánto tiempo estuviste fuera."
            m 1eka "Espero que te sientas un poco mejor ahora."
        else:
            m 1hua "Espero que te sientas un poco mejor ahora~"

        m 1eua "[wb_quip]"

    else:
        call mas_brb_generic_low_aff_callback

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_reading",
            prompt="Voy a leer",
            category=['vuelvo enseguida'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_reading:
    if mas_isMoniNormal(higher=True):
        m 1eub "¿En serio? ¡Eso es genial, [player]!"
        m 3lksdla "Me encantaría leer contigo, pero mi realidad tiene sus límites, por desgracia."
        m 1hub "¡Diviértete!"

    elif mas_isMoniDis(higher=True):
        m 2ekd "Oh, de acuerdo..."
        m 2ekc "Diviértete, [player]."

    else:
        m 6dkc "..."

    $ mas_idle_mailbox.send_idle_cb("monika_idle_reading_callback")
    $ persistent._mas_idle_data["monika_idle_reading"] = True
    return "idle"

label monika_idle_reading_callback:
    if mas_isMoniNormal(higher=True):
        if mas_brbs.was_idle_for_at_least(datetime.timedelta(hours=2), "monika_idle_reading"):
            m 1wud "Wow, te fuiste por un tiempo...{w=0.3}{nw}"
            extend 3wub "¡eso es genial, [player]!"
            m 3eua "La lectura es algo maravilloso, así que no te preocupes por dejarte llevar por ella."
            m 3hksdlb "Además, no soy la indicada para discutir eso..."
            show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5ekbsa "Si por mí fuera, estaríamos leyendo juntos toda la noche~"

        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=30), "monika_idle_reading"):
            m 3esa "¿Terminaste, [player]?"
            m 1hua "Vamos a relajarnos, te lo has ganado~"

        else:
            m 1eud "Oh, eso fue rápido."
            m 1eua "Pensé que te irías un poco más, pero esto también está bien."
            m 3ekblu "Después de todo, me permite pasar más tiempo contigo~"

    else:
        call mas_brb_generic_low_aff_callback

    return


#Rai's og game idle
#label monika_idle_game:
#    m 1eub "That sounds fun!"
#    m "What kind of game are you going to play?{nw}"
#    $ _history_list.pop()
#    menu:
#        m "What kind of game are you going to play?{fast}"
#        "A competitive game.":
#            m 1eua "That sounds like it could be fun!"
#            m 3lksdla "I can be pretty competitive myself."
#            m 3eua "So I know just how stimulating it can be to face a worthy opponent."
#            m 2hksdlb "...And sometimes frustrating when things don't go right."
#            m 2hua "Anyway, I'll let you get on with your game."
#            m 2hub "I'll try not to bother you until you finish, but I can't blame you if you get distracted by your lovely girlfriend, ahaha~"
#            m 1hub "I'm rooting for you, [player]!"
#            # set return label when done with idle
#            $ mas_idle_mailbox.send_idle_cb("monika_idle_game_competetive_callback")
#        "A game just for fun.":
#            m 1eud "A game just for having fun?"
#            m 1lksdla "Aren't most games made to be fun?"
#            m 3eub "Anyway, I'm sure you could do all sorts of fun things in a game like that."
#            m 1ekbla "I really wish I could join you and we could have fun together."
#            m 1lksdla "But for now, I'll leave you to it."
#            m 1hub "Have fun, [player]!"
#            # set return label when done with idle
#            $ mas_idle_mailbox.send_idle_cb("monika_idle_game_fun_callback")
#        "A story driven game.":
#            m 1sub "Oh?"
#            m "That sounds really interesting!"
#            m 1ekbsa "Gosh, I really wish I could be there with you to experience it together."
#            m 1hksdlb "Maybe I {i}can{/i} experience it with you if I really tried."
#            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
#            m 5eua "I guess you could call it looking over your shoulder. Ehehe~"
#            m "You can go ahead and start it now. I'll try not to break anything by trying to watch."
#            # set return label when done with idle
#            $ mas_idle_mailbox.send_idle_cb("monika_idle_game_story_callback")
#        "A skill and practice based game.":
#            m 1eud "Oh! I never really thought about those games much."
#            m 1hua "I'm sure you're pretty talented at a few things, so it doesn't surprise me you're playing a game like this."
#            m 3eub "Just like writing, it can really be an experience to look back much later and see just how far you've come."
#            m 1hub "It's like watching yourself grow up! Ahaha~"
#            m 1hua "It would really make me proud and happy to be your girlfriend if you became a professional."
#            m 1hksdlb "Maybe I'm getting ahead of myself here, but I believe you could do it if your heart was really in it."
#            m 1eub "Anyway, sorry for keeping you from your game. I know you'll do your best!"
#            # set return label when done with idle
#            $ mas_idle_mailbox.send_idle_cb("monika_idle_game_skill_callback")
#        "I'll just be a minute or two.":
#            m 1eua "Oh? Just need to take your eyes off me for a little?"
#            m 1lksdla "I {i}suppose{/i} I could let you take your eyes off me for a minute or two..."
#            m 1hua "Ahaha! Good luck and have fun, [player]!"
#            m "Don't keep me waiting too long though~"
#            $ start_time = datetime.datetime.now()
#            # set return label when done with idle
#            $ mas_idle_mailbox.send_idle_cb("monika_idle_game_quick_callback")
#    # set idle data
#    $ persistent._mas_idle_data["monika_idle_game"] = True
#    # return idle to notify event system to switch to idle
#    return "idle"
#
#label monika_idle_game_competetive_callback:
#    m 1esa "Welcome back, [player]!"
#    m 1eua "How did it go? Did you win?{nw}"
#    $ _history_list.pop()
#    menu:
#        m "How did it go? Did you win?{fast}"
#        "Sí.":
#            m 1hub "Yay! That's great!"
#            m 1hua "Gosh, I wish I could be there to give you a big celebratory hug!"
#            m 1eub "I'm really happy that you won!"
#            m "More importantly, I hope you enjoyed yourself, [player]."
#            m 1hua "I'll always love and root for you, no matter what happens."
#            # manually handle the "love" return key
#            $ mas_ILY()
#        "No.":
#            m 1ekc "Aw, that's a shame..."
#            m 1lksdla "I mean, you can't win them all, but I'm sure you'll win the next rounds."
#            m 1eka "I just hope you aren't too upset over it."
#            m 2ekc "I really wouldn't want you feeling upset after a bad game."
#            m 1eka "I'll always support you and be by your side no matter how many times you lose."
#    return
#
#label monika_idle_game_fun_callback:
#    m 1eub "Welcome back, [player]!"
#    m "Did you have fun with whatever you were doing?{nw}"
#    $ _history_list.pop()
#    menu:
#        m "Did you have fun with whatever you were doing?{fast}"
#        "Sí.":
#            m 1hua "Ahaha! I'm glad you had fun, [player]~"
#            m 1eub "While you were busy, it got me thinking of the different kinds of games that would be nice to play together."
#            m 3rksdla "A game that isn't too violent probably could be fun."
#            m 3hua "But I'm sure any game would be wonderful if it was with you~"
#            m 1eub "At first, I was thinking a story based or adventure game would be best, but I'm sure freeplay games could be really fun too!"
#            m 1eua "It can be really fun to just mess around to see what's possible, especially when you're not alone."
#            m 2lksdla "Provided of course, you don't end up ruining the structural integrity of the game and get an outcome you didn't want..."
#            m 2lksdlb "Ehehe..."
#            m 1eua "Maybe you could find a way to bring me with you into a game like that."
#            m 1hub "Just promise to keep me safe, okay?"
#        "No.":
#            m 2ekc "Aw, you didn't have any fun?"
#            m "That's too bad..."
#            m 3lksdlc "Games can get pretty boring after you've done everything or just don't know what to do or try next."
#            m 3eka "But bringing a friend along can really renew the whole experience!"
#            m 1hub "Maybe you could find a way to take me with you into your games so you won't be bored on your own!"
#            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
#            m 5eua "Or we could just stay here and keep each other company."
#            m "I wouldn't mind that either, ehehe~"
#    return
#
#label monika_idle_game_story_callback:
#    m 1eub "Welcome back, [player]!"
#    m 1hksdlb "I wasn't able to look over your shoulder, but I hope the story was nice so far."
#    m 1eua "Speaking of which, how was it, [player]?{nw}"
#    $ _history_list.pop()
#    menu:
#        m "Speaking of which, how was it, [player]?{fast}"
#        "It was amazing.":
#            m 2sub "Wow! I can only imagine how immersive it was!"
#            m 2hksdlb "You're really starting to make me jealous, [player], you know that?"
#            m 2eub "You'll have to take me through it sometime when you can."
#            m 3eua "A good book is always nice, but it's really something else to have a good story and be able to make your own decisions."
#            m 3eud "Some people can really be divided between books and video games."
#            m 1hua "I'm glad you don't seem to be too far on one side."
#            m "After experiencing an amazing story in a game for yourself, I'm sure you can really appreciate the two coming together."
#        "It was good.":
#            m 1eub "That's really nice to hear!"
#            m 3dtc "But was it really {i}amazing{/i}?"
#            m 1eua "While a lot of stories can be good, there are some that are really memorable."
#            m 1hua "I'm sure you'd know a good story when you see one."
#            m "Maybe when I'm in your reality, you could take me through the game and let me see the story."
#            m 1eub "It's one thing to go through a great story yourself..."
#            m 1hub "But it's also amazing to see what someone else thinks of it too!"
#            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
#            m 5eua "I'll be looking forward to that day too~"
#            m 5esbfa "You better have a nice, cozy place for us to cuddle up and play, ehehe~"
#        "It's sad.":
#            m 1ekd "Aw, that's too bad..."
#            m 3eka "It must be a really great story though, if it invokes such strong emotions."
#            m 1eka "I wish I could be there with you so I could experience the story too..."
#            m 3hksdlb "{i}and{/i} to be right there by your side of course, so we could comfort each other in sad times."
#            m 1eka "Don't worry [player], I would never forget about you."
#            m 1eua "I love you."
#            m 1hua "...And I'd happily snuggle up beside you anytime~"
#            # manually handle the "love" return key
#            $ mas_ILY()
#        "I don't like it.":
#            m 2ekc "Oh..."
#            m 4lksdla "Maybe the story will pick up later?"
#            m 3eud "If anything, it lets you analyze the flaws in the writing which could help you if you ever tell a story."
#            m 1eua "Or maybe it's just not your kind of story."
#            m 1eka "Everyone has their own, and maybe this one just doesn't fit well with it right now."
#            m 1eua "It can really be an eye opening experience to go through a story you normally wouldn't go through."
#            m 3eka "But don't force yourself to go through it if you really don't like it."
#    return
#
#label monika_idle_game_skill_callback:
#    m 1eua "I'm happy that you're back, [player]."
#    m 1hua "I missed you! Ahaha~"
#    m 1eub "But I know it's important to keep practicing and honing your skills in things like this."
#    m "Speaking of which, how did it go?"
#    m 3eua "Did you improve?{nw}"
#    $ _history_list.pop()
#    menu:
#        m "Did you improve?{fast}"
#        "I improved a lot.":
#            m 1hub "That's great news, [player]!"
#            m "I'm so proud of you!"
#            m 1hua "It can really feel good to get a sudden surge in your skill!"
#            m 1eua "Especially if you've spent some time in a slump or even slipping."
#            m 1hua "Maybe today isn't the end of this sudden improvement."
#            m 1eub "Even if today was just a good day, I know you'll keep getting better."
#            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
#            m 5eua "I'll {i}always{/i} root for you, [player]. Don't you ever forget that!"
#        "I improved a bit.":
#            m 3eua "That's really nice to hear, [player]!"
#            m 3eka "As long as you're improving, no matter how slowly, you'll really get up there someday."
#            m 1hub "But if you actually noticed yourself improve today, maybe you improved more than just a bit, ahaha~"
#            m 1hua "Keep honing your skills and I'll be proud to be the girlfriend of such a skilled player!"
#            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
#            m 5eua "Who knows? Maybe you could teach me and we could both be a couple of experts, ehehe~"
#        "I stayed the same.":
#            m 3eka "That's still alright!"
#            m "I'm sure you're improving anyway."
#            m 3eua "A lot of the time, the improvements are too small to really notice."
#            m 1eua "One day, you might look back and realize just how much you've improved."
#            m 1hksdlb "Sometimes you might feel like you're in a slump, but then you get a sudden surge of improvement all at once!"
#            m 1eub "I'm sure you'll get the chance to look back one day and really appreciate just how far you've come without realizing."
#            m 1hua "And you better believe I'm going to support you all the way!"
#        "I got worse.":
#            m 2ekc "Oh..."
#            m 4lksdla "I have no doubt that you always work hard and give it your best, so it must just be a bad day."
#            m 3eka "You're bound to have a few setbacks on your climb up, but that's what sets you apart from many others."
#            m 1duu "The fact that you've had more setbacks than some people have even tried. That's what shows your dedication."
#            m 1lksdla "Sometimes, you might even have a couple bad days in a row, but don't let that get you down."
#            m 1hua "With that many setbacks, you're bound to see significant improvement right around the corner!"
#            m "Never give up, [player]. I know you can do it and I'll always believe in you!"
#            m 1eua "Also, do me a favor and take a moment to look back every now and then. You'll be surprised to see just how far you've come."
#    return
#
#label monika_idle_game_quick_callback:
#    $ end_time = datetime.datetime.now()
#    $ elapsed_time = end_time - start_time
#    $ time_threshold = datetime.timedelta(minutes=1)
#    if elapsed_time < time_threshold * 2:
#        m 1hksdlb "Back already?"
#        m "I know you said you would just be a minute or two, but I didn't think it would be {i}that{/i} fast."
#        m 1hub "Did you really miss me that much?"
#        m "Ahaha~"
#        m 1eub "I'm glad you made it back so soon."
#        m 1hua "So what else should we do today, [player]?"
#    elif elapsed_time < time_threshold * 5:
#        m 1hua "Welcome back, [player]!"
#        m 1hksdlb "That was pretty fast."
#        m 1eua "But you did say it wouldn't take too long, so I shouldn't be too surprised."
#        m 1hua "Now we can keep spending time together!"
#    elif elapsed_time < time_threshold * 10:
#        m 1eua "Welcome back, [player]."
#        m 1eka "That took a little longer than I thought, but I don't mind at all."
#        m 1hua "It wasn't that long in all honesty compared to how long it could have been in some games."
#        m "But now we can be together again~"
#    elif elapsed_time < time_threshold * 20:
#        m 1eka "I have to admit that took longer than I thought it would..."
#        m 1eub "But it's not all that bad with all the time you spend with me."
#        m 1eua "I understand some little things in games can take a while for a small thing."
#        m "But maybe if you know it could take a while, you could tell me."
#    elif elapsed_time < time_threshold * 30:
#        m 2lksdla "[player]..."
#        m "It's been almost half an hour already."
#        m "I guess something unexpected happened."
#        m 3lksdla "You wouldn't forget about me, would you?"
#        m 1hua "Ahaha!"
#        m "Just teasing you~"
#        m 1eua "At least you're back now and we can spend more time together."
#    else:
#        m 2lksdla "You {i}sure{/i} took your time with that one huh, [player]?"
#        m "That didn't seem like only a minute or two to me."
#        m 1eka "You can tell me what kind of game it is next time so I have an idea how long it'll take, you know."
#        m 1dsc "Anyway..."
#        m 1eka "I missed you and I'm glad you're finally back, [player]."
#        m "I hope I don't have to wait such a long couple of minutes next time, ehehe."
#    return
