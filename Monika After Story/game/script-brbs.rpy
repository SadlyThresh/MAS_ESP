





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


label mas_brb_back_to_idle:

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
        m 1eua "Alright, [player]."
        m 1hub "Hurry back, I'll be waiting here for you~"

    elif mas_isMoniNormal(higher=True):
        m 1hub "Hurry back, [player]!"

    elif mas_isMoniDis(higher=True):
        m 2rsc "Oh...{w=0.5}okay."
    else:

        m 6ckc "..."


    $ mas_idle_mailbox.send_idle_cb("monika_brb_idle_callback")

    $ persistent._mas_idle_data["monika_idle_brb"] = True
    return "idle"

label monika_brb_idle_callback:
    $ wb_quip = mas_brbs.get_wb_quip()

    if mas_isMoniAff(higher=True):
        m 1hub "Welcome back, [player]. I missed you~"
        m 1eua "[wb_quip]"

    elif mas_isMoniNormal(higher=True):
        m 1hub "Welcome back, [player]!"
        m 1eua "[wb_quip]"

    elif mas_isMoniDis(higher=True):
        m 2esc "Oh, back already?"
    else:

        m 6ckc "..."
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
            m 1eub "Oh! You're going to{cps=*2} write me a love letter, [player]?{/cps}{nw}"
            $ _history_list.pop()
            m "Oh! You're going to{fast} go write something?"
        else:

            m 1eub "Oh! You're going to go write something?"

        m 1hua "That makes me so glad!"
        m 3eua "Maybe someday you could share it with me...{w=0.3} {nw}"
        extend 3hua "I'd love to read your work, [player]!"
        m 3eua "Anyway, just let me know when you're done."
        m 1hua "I'll be waiting right here for you~"

    elif mas_isMoniUpset():
        m 2esc "Alright."

    elif mas_isMoniDis():
        m 6lkc "I wonder what you have on your mind..."
        m 6ekd "Don't forget to come back when you're done..."
    else:

        m 6ckc "..."


    $ mas_idle_mailbox.send_idle_cb("monika_writing_idle_callback")

    $ persistent._mas_idle_data["monika_idle_writing"] = True
    return "idle"

label monika_writing_idle_callback:

    if mas_isMoniNormal(higher=True):
        $ wb_quip = mas_brbs.get_wb_quip()
        m 1eua "Done writing, [player]?"
        m 1eub "[wb_quip]"

    elif mas_isMoniUpset():
        m 2esc "Done? Welcome back, [player]."

    elif mas_isMoniDis():
        m 6ekc "Oh...{w=0.5} You're back..."
    else:

        m 6ckc "..."
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
        m 1eua "Going to go shower?"

        if renpy.random.randint(1, 50) == 1:
            m 3tub "Can I come with you?{nw}"
            $ _history_list.pop()
            show screen mas_background_timed_jump(2, "bye_brb_shower_timeout")
            menu:
                m "Can I come with you?{fast}"
                "Sí.":

                    hide screen mas_background_timed_jump
                    m 2wubsd "Oh, uh...{w=0.5}you sure answered that fast."
                    m 2hkbfsdlb "You...{w=0.5}sure seem eager to let me tag along, huh?"
                    m 2rkbfa "Well..."
                    m 7tubfu "I'm afraid you'll just have to go without me while I'm stuck here."
                    m 7hubfb "Sorry, [player], ahaha!"
                    show monika 5kubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5kubfu "Maybe another time~"
                "No.":

                    hide screen mas_background_timed_jump
                    m 2eka "Aw, you rejected me so fast."
                    m 3tubsb "Are you shy, [player]?"
                    m 1hubfb "Ahaha!"
                    show monika 5tubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5tubfu "Alright, I won't follow you this time, ehehe~"
        else:

            m 1hua "I'm glad you're keeping yourself clean, [player]."
            m 1eua "Have a nice shower~"

    elif mas_isMoniNormal(higher=True):
        m 1eub "Going to go shower? Alright."
        m 1eua "See you when you're done~"

    elif mas_isMoniUpset():
        m 2esd "Enjoy your shower, [player]..."
        m 2rkc "Hopefully it'll help you clear your mind."

    elif mas_isMoniDis():
        m 6ekc "Hmm?{w=0.5} Have a nice shower, [player]."
    else:

        m 6ckc "..."


    $ mas_idle_mailbox.send_idle_cb("monika_idle_shower_callback")

    $ persistent._mas_idle_data["monika_idle_shower"] = True
    return "idle"

label monika_idle_shower_callback:
    if mas_isMoniNormal(higher=True):
        m 1eua "Welcome back, [player]."

        if (
            mas_isMoniLove()
            and renpy.seen_label("monikaroom_greeting_ear_bathdinnerme")
            and mas_getEVL_shown_count("monika_idle_shower") != 1 
            and renpy.random.randint(1,20) == 1
        ):
            m 3tubsb "Now that you've had your shower, would you like your dinner, or maybe{w=0.5}.{w=0.5}.{w=0.5}."
            m 1hubsa "You could just relax with me some more~"
            m 1hub "Ahaha!"
        else:

            m 1hua "I hope you had a nice shower."
            if mas_getEVL_shown_count("monika_idle_shower") == 1:
                m 3eub "Now we can get back to having some good, {i}clean{/i} fun together..."
                m 1hub "Ahaha!"

    elif mas_isMoniUpset():
        m 2esc "I hope you enjoyed your shower. Welcome back, [player]."

    elif mas_isMoniDis():
        m 6ekc "Oh, it's nice to see you again..."
    else:

        m 6ckc "..."
    return

label bye_brb_shower_timeout:
    hide screen mas_background_timed_jump
    $ _history_list.pop()
    m 1hubsa "Ehehe~"
    m 3tubfu "Nevermind that, [player]."
    m 1hubfb "I hope you have a nice shower!"


    $ mas_idle_mailbox.send_idle_cb("monika_idle_shower_callback")

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
        m 1eud "Oh, you're going to play another game?"
        m 1eka "That's alright, [player]."

        label monika_idle_game.skip_intro:
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
        m 2tsc "Enjoy your other games."

    elif mas_isMoniDis():
        m 6ekc "Please...{w=0.5}{nw}"
        extend 6dkc "don't forget about me..."
    else:

        m 6ckc "..."

    $ mas_idle_mailbox.send_idle_cb("monika_idle_game_callback")
    $ persistent._mas_idle_data["monika_idle_game"] = True
    return "idle"

label monika_idle_game_callback:
    if mas_isMoniNormal(higher=True):
        m 1eub "Welcome back, [player]!"
        m 1eua "I hope you had fun with your game."
        m 1hua "Ready to spend some more time together? Ehehe~"

    elif mas_isMoniUpset():
        m 2tsc "Had fun, [player]?"

    elif mas_isMoniDis():
        m 6ekd "Oh...{w=0.5} You actually came back to me..."
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
        m 1eua "Oh! Going to code something?"

        if persistent._mas_pm_has_code_experience is False:
            m 1etc "I thought you didn't do that."
            m 1eub "Did you pick up programming since we talked about it last time?"

        elif persistent._mas_pm_has_contributed_to_mas or persistent._mas_pm_wants_to_contribute_to_mas:
            m 1tua "Something for me, perhaps?"
            m 1hub "Ahaha~"
        else:

            m 3eub "Do your best to keep your code clean and easy to read."
            m 3hksdlb "...You'll thank yourself later!"

        m 1eua "Anyway, just let me know when you're done."
        m 1hua "I'll be right here, waiting for you~"

    elif mas_isMoniUpset():
        m 2euc "Oh, you're going to code?"
        m 2tsc "Well, don't let me stop you."

    elif mas_isMoniDis():
        m 6ekc "Alright."
    else:

        m 6ckc "..."

    $ mas_idle_mailbox.send_idle_cb("monika_idle_coding_callback")
    $ persistent._mas_idle_data["monika_idle_coding"] = True
    return "idle"

label monika_idle_coding_callback:
    if mas_isMoniNormal(higher=True):
        $ wb_quip = mas_brbs.get_wb_quip()
        if mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=20), "monika_idle_coding"):
            m 1eua "Done for now, [player]?"
        else:
            m 1eua "Oh, done already, [player]?"

        m 3eub "[wb_quip]"

    elif mas_isMoniUpset():
        m 2esc "Welcome back."

    elif mas_isMoniDis():
        m 6ekc "Oh, you're back."
    else:

        m 6ckc "..."
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
        m 1hub "Okay, [player]!"
        if persistent._mas_pm_works_out is False:
            m 3eub "Working out is a great way to take care of yourself!"
            m 1eka "I know it might be hard to start out,{w=0.2}{nw}"
            extend 3hua " but it's definitely a habit worth forming."
        else:
            m 1eub "It's good to know you're taking care of your body!"
        m 3esa "You know how the saying goes, 'A healthy mind in a healthy body.'"
        m 3hua "So go work up a good sweat, [player]~"
        m 1tub "Just let me know when you've had enough."

    elif mas_isMoniUpset():
        m 2esc "Good to know you're taking care of{cps=*2} something, at least.{/cps}{nw}"
        $ _history_list.pop()
        m "Good to know you're taking care of{fast} yourself, [player]."
        m 2euc "I'll be waiting for you to get back."

    elif mas_isMoniDis():
        m 6ekc "Alright."
    else:

        m 6ckc "..."

    $ mas_idle_mailbox.send_idle_cb("monika_idle_workout_callback")
    $ persistent._mas_idle_data["monika_idle_workout"] = True
    return "idle"

label monika_idle_workout_callback:
    if mas_isMoniNormal(higher=True):
        $ wb_quip = mas_brbs.get_wb_quip()
        if mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=60), "monika_idle_workout"):



            m 2esa "You sure took your time, [player].{w=0.3}{nw}"
            extend 2eub " That must've been one heck of a workout."
            m 2eka "It's good to push your limits, but you shouldn't overdo it."

        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=10), "monika_idle_workout"):
            m 1esa "Done with your workout, [player]?"
        else:

            m 1euc "Back already, [player]?"
            m 1eka "I'm sure you can go on for a bit longer if you try."
            m 3eka "Taking breaks is fine, but you shouldn't leave your workouts unfinished."
            m 3ekb "Are you sure you can't keep going?{nw}"
            $ _history_list.pop()
            menu:
                m "Are you sure you can't keep going?{fast}"
                "Estoy seguro.":

                    m 1eka "That's okay."
                    m 1hua "I'm sure you did your best, [player]~"
                "Intentaré seguir adelante.":


                    m 1hub "That's the spirit!"

                    $ brb_label = "monika_idle_workout"
                    $ pushEvent("mas_brb_back_to_idle",skipeval=True)
                    return

        m 7eua "Make sure to rest properly and maybe get a snack to get some energy back."
        m 7eub "[wb_quip]"

    elif mas_isMoniUpset():
        m 2euc "Done with your workout, [player]?"

    elif mas_isMoniDis():
        m 6ekc "Oh, you came back."
    else:

        m 6ckc "..."
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
        m 1eua "Going to take a nap, [player]?"
        m 3eua "They're a healthy way to rest during the day if you're feeling tired."
        m 3hua "I'll watch over you, don't worry~"
        m 1hub "Sweet dreams!"

    elif mas_isMoniUpset():
        m 2eud "Alright, I hope you feel rested afterwards."
        m 2euc "I hear naps are good for you, [player]."

    elif mas_isMoniDis():
        m 6ekc "Alright."
    else:

        m 6ckc "..."

    $ mas_idle_mailbox.send_idle_cb("monika_idle_nap_callback")
    $ persistent._mas_idle_data["monika_idle_nap"] = True
    return "idle"

label monika_idle_nap_callback:
    if mas_isMoniNormal(higher=True):
        if mas_brbs.was_idle_for_at_least(datetime.timedelta(hours=5), "monika_idle_nap"):
            m 2hksdlb "Oh, [player]! You're finally awake!"
            m 7rksdlb "When you said you were going to take a nap, I was expecting you take maybe an hour or two..."
            m 1hksdlb "I guess you must have been really tired, ahaha..."
            m 3eua "But at least after sleeping for so long, you'll be here with me for a while, right?"
            m 1hua "Ehehe~"

        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(hours=1), "monika_idle_nap"):
            m 1hua "Welcome back, [player]!"
            m 1eua "Did you have a nice nap?"
            m 3hua "You were out for some time, so I hope you're feeling rested~"
            m 1eua "Is there anything else you wanted to do today?"

        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=5), "monika_idle_nap"):
            m 1hua "Welcome back, [player]~"
            m 1eub "I hope you had a nice little nap."
            m 3eua "What else would you like to do today?"
        else:

            m 1eud "Oh, back already?"
            m 1euc "Did you change your mind?"
            m 3eka "Well, I'm not complaining, but you should take a nap if you feel like it later."
            m 1eua "I wouldn't want you to be too tired, after all."

    elif mas_isMoniUpset():
        m 2euc "Done with your nap, [player]?"

    elif mas_isMoniDis():
        m 6ekc "Oh, you're back."
    else:

        m 6ckc "..."
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
        m 1eub "Oh, okay!"
        m 1hua "I'm proud of you for taking your studies seriously."
        m 1eka "Don't forget to come back to me when you're done~"

    elif mas_isMoniDis(higher=True):
        m 2euc "Alright...{w=0.5}"
        if random.randint(1,5) == 1:
            m 2rkc "...Good luck with your homework, [player]."
    else:

        m 6ckc "..."


    $ mas_idle_mailbox.send_idle_cb("monika_idle_homework_callback")

    $ persistent._mas_idle_data["monika_idle_homework"] = True
    return "idle"

label monika_idle_homework_callback:
    if mas_isMoniDis(higher=True):
        m 2esa "All done, [player]?"

        if mas_isMoniNormal(higher=True):
            m 2ekc "I wish I could've been there to help you, but there isn't much I can do about that just yet, sadly."
            m 7eua "I'm sure we could both be a lot more efficient doing homework if we could work together."

            if mas_isMoniAff(higher=True) and random.randint(1,5) == 1:
                m 3rkbla "...Although, that's assuming we don't get {i}too{/i} distracted, ehehe..."

            m 1eua "But anyway,{w=0.2} {nw}"
            extend 3hua "now that you're done, let's enjoy some more time together."
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
        m 1eua "Alright, [player]."
        m 1eub "Don't forget to take a break every now and then!"

        if mas_isMoniAff(higher=True):
            m 3rkb "I wouldn't want my sweetheart to spend more time on [his] work than with me~"

        m 1hua "Good luck with your work!"

    elif mas_isMoniDis(higher=True):
        m 2euc "Okay, [player]."

        if random.randint(1,5) == 1:
            m 2rkc "...Please come back soon..."
    else:

        m 6ckc "..."


    $ mas_idle_mailbox.send_idle_cb("monika_idle_working_callback")

    $ persistent._mas_idle_data["monika_idle_working"] = True
    return "idle"

label monika_idle_working_callback:
    if mas_isMoniNormal(higher=True):
        m 1eub "Finished with your work, [player]?"
        show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hua "Then let's relax together, you've earned it~"

    elif mas_isMoniDis(higher=True):
        m 2euc "Oh, you're back..."
        m 2eud "...Was there anything else you wanted to do, now that you're done with your work?"
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
                m 3eka "You haven't been here for that long but if you say you need a break, then you need a break."

            elif mas_getSessionLength() < datetime.timedelta(hours=2, minutes=30):
                m 1eua "Going to rest your eyes for a bit?"
            else:

                m 1lksdla "Yeah, you probably need that, don't you?"

            m 1hub "I'm glad you're taking care of your health, [player]."

            if not persistent._mas_pm_works_out and random.randint(1,3) == 1:
                m 3eua "Why not take the opportunity to do a few stretches as well, hmm?"
                m 1eub "Anyway, come back soon!~"
            else:

                m 1eub "Come back soon!~"
        else:

            m 1eua "Taking another break, [player]?"
            m 1hua "Come back soon!~"

    elif mas_isMoniUpset():
        m 2esc "Oh...{w=0.5} {nw}"
        extend 2rsc "Okay."

    elif mas_isMoniDis():
        m 6ekc "Alright."
    else:

        m 6ckc "..."

    $ mas_idle_mailbox.send_idle_cb("monika_idle_screen_break_callback")
    $ persistent._mas_idle_data["monika_idle_screen_break"] = True
    return "idle"

label monika_idle_screen_break_callback:
    if mas_isMoniNormal(higher=True):
        $ wb_quip = mas_brbs.get_wb_quip()
        m 1eub "Welcome back, [player]."

        if mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=30), "monika_idle_screen_break"):
            m 1hksdlb "You must've really needed that break, considering how long you were gone."
            m 1eka "I hope you're feeling a little better now."
        else:
            m 1hua "I hope you're feeling a little better now~"

        m 1eua "[wb_quip]"

    elif mas_isMoniUpset():
        m 2esc "Welcome back."

    elif mas_isMoniDis():
        m 6ekc "Oh...{w=0.5} You're back."
    else:

        m 6ckc "..."

    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
