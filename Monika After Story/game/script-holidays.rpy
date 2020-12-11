## holiday info goes here
#
# TOC
#   [GBL000] - GLOBAL SPACE
#   [HOL010] - O31
#   [HOL020] - D25
#   [HOL030] - NYE (new yeares eve, new years)
#   [HOL040] - player_bday
#   [HOL050] - F14
#   [HOL060] - 922


############################### GLOBAL SPACE ################################
# [GBL000]
default persistent._mas_event_clothes_map = dict()
define mas_five_minutes = datetime.timedelta(seconds=5*60)
define mas_one_hour = datetime.timedelta(seconds=3600)
define mas_three_hour = datetime.timedelta(seconds=3*3600)

init 10 python:
    def mas_addClothesToHolidayMap(clothes, key=None):
        """
        Adds the given clothes to the holiday clothes map

        IN:
            clothes - clothing item to add
            key - dateime.date to use as key. If None, we use today
        """
        if clothes is None:
            return

        if key is None:
            key = datetime.date.today()

        persistent._mas_event_clothes_map[key] = clothes.name

        #We also unlock the event clothes selector here
        mas_unlockEVL("monika_event_clothes_select", "EVE")

    def mas_addClothesToHolidayMapRange(clothes, start_date, end_date):
        """
        Adds the given clothes to the holiday clothes map over the day range provided

        IN:
            clothes - clothing item to add
            start_date - datetime.date to start adding to the map on
            end_date - datetime.date to stop adding to the map on
        """
        if not clothes:
            return

        #We have clothes, we need to create a generator for building a range
        daterange = mas_genDateRange(start_date, end_date)

        #Now we need to iterate over the new range:
        for date in daterange:
            mas_addClothesToHolidayMap(clothes, date)

init -1 python:
    def mas_checkOverDate(_date):
        """
        Checks if the player was gone over the given date entirely (taking you somewhere)

        IN:
            date - a datetime.date of the date we want to see if we've been out all day for

        OUT:
            True if the player and Monika were out together the whole day, False if not.
        """
        checkout_time = store.mas_dockstat.getCheckTimes()[0]
        return checkout_time is not None and checkout_time.date() < _date


    def mas_capGainAff(amount, aff_gained_var, normal_cap, pbday_cap=None):
        """
        Gains affection according to the cap(s) defined

        IN:
            amount:
                Amount of affection to gain

            aff_gained_var:
                The persistent variable which the total amount gained for the holiday is stored
                (NOTE: Must be a string)

            normal_cap:
                The cap to use when not player bday

            pbday_cap:
                The cap to use when it's player bday (NOTE: if not provided, normal_cap is assumed)
        """

        #If player bday cap isn't provided, we just use the one cap
        if persistent._mas_player_bday_in_player_bday_mode and pbday_cap:
            cap = pbday_cap
        else:
            cap = normal_cap

        if persistent.__dict__[aff_gained_var] < cap:
            persistent.__dict__[aff_gained_var] += amount
            mas_gainAffection(amount, bypass=True)

        return

    def mas_hasSpecialOutfit(_date=None):
        """
        Checks if the given date is a special event that has an outfit in the event clothes map
        IN:
            _date - date to check.
                (Default: None)

        RETURNS: True if given date has a special outfit, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return _date in persistent._mas_event_clothes_map

init -10 python:
    def mas_isA01(_date=None):
        if _date is None:
            _date = datetime.date.today()

        return _date == datetime.date(_date.year,4,1)

# Global labels
label mas_lingerie_intro(holiday_str, lingerie_choice):
    m 1ekbfa "..."
    m "Por cierto, [player]..."
    m 3ekbfsdla "Hay... {w=1}A-Algo que quiero mostrarte."
    m 2rkbfsdla "En realidad, he querido hacer esto por un tiempo, pero... {w=1} bueno, es un poco vergonzoso..."
    m "..."
    m 2hkbfsdlb "¡Oh Dios, estoy super nerviosa, jajaja!"
    m 2rkbfsdlc "Es solo que nunca he-{nw}"
    m 2dkbfsdlc "Ah, está bien, es hora de dejar de estancarme y simplemente hacerlo."
    m 2ekbfsdla "Solo dame unos segundos, [player]."
    call mas_clothes_change(outfit=lingerie_choice, outfit_mode=True, exp="monika 2rkbfsdlu", restore_zoom=False, unlock=True)
    pause 3.0
    m 2ekbfsdlb "Jajaja, [player]... {w=1}estás mirándome mucho..."
    m 2ekbfu "Bueno... {w=1}¿Te gusta lo que ves?"
    m 1lkbfa "En realidad, nunca... {w=1}Me había puesto algo como esto."
    m "...Al menos no que nadie haya visto."

    if mas_hasUnlockedClothesWithExprop("bikini"):
        m 3hkbfb "Jajaja, ¿qué estoy diciendo? Me has visto en bikini antes, que es esencialmente lo mismo..."
        m 2rkbfa "...Aunque, por alguna razón, esto se siente... {w=0.5}{i}Diferente{/i}."

    m 2ekbfa "De todos modos, algo sobre estar contigo [holiday_str] parece realmente romántico, ¿sabes?"
    m "Simplemente se sintió como el momento perfecto para el siguiente paso en nuestra relación."
    m 2rkbfsdlu "Ahora sé que realmente no podemos-{nw}"
    m 3hubfb "¡Ah! ¡No importa, jajaja!"
    return


############################### O31 ###########################################
# [HOL010]
#O31 mode var, handles visuals and sets us up to return to autoload even if not O31 anymore
default persistent._mas_o31_in_o31_mode = False

#Number of times we've gone out T/Ting
default persistent._mas_o31_tt_count = 0

#Aff cap for T/T, softmax 15
default persistent._mas_o31_trick_or_treating_aff_gain = 0

#Need to know if we were asked to relaunch the game
default persistent._mas_o31_relaunch = False

# costumes worn
# key: costume name
# value: year worn
default persistent._mas_o31_costumes_worn = {}

#Halloween
define mas_o31 = datetime.date(datetime.date.today().year, 10, 31)

init -810 python:
    # MASHistorySaver for o31
    store.mas_history.addMHS(MASHistorySaver(
        "o31",
        #datetime.datetime(2018, 11, 2),
        # change trigger to better date
        datetime.datetime(2020, 1, 6),
        {
            # this isn't very useful, but we need the reset
            "_mas_o31_in_o31_mode": "o31.mode.o31",
            "_mas_o31_tt_count": "o31.tt.count",
            "_mas_o31_relaunch": "o31.relaunch",
            "_mas_o31_trick_or_treating_aff_gain": "o31.actions.tt.aff_gain"
        },
        use_year_before=True,
        start_dt=datetime.datetime(2019, 10, 31),

        # end is 1 day out in case of an overnight trick or treat
        end_dt=datetime.datetime(2019, 11, 2)
    ))

# Images
# TODO: export lighting as its own layer
image mas_o31_deco = ConditionSwitch(
    "mas_current_background.isFltDay()",
    "mod_assets/location/spaceroom/o31/halloween_deco.png",
    "True", "mod_assets/location/spaceroom/o31/halloween_deco-n.png"
)

init 501 python:
    MASImageTagDecoDefinition.register_img(
        "mas_o31_deco",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )

init python:
    MAS_O31_COSTUME_CG_MAP = {
        mas_clothes_marisa: "o31mcg",
        mas_clothes_rin: "o31rcg"
    }

#Functions
init -10 python:
    import random

    def mas_isO31(_date=None):
        """
        Returns True if the given date is o31

        IN:
            _date - date to check.
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is o31, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return _date == mas_o31.replace(year=_date.year)

    def mas_o31ShowVisuals():
        """
        Shows o31 visuals
        """
        mas_showDecoTag("mas_o31_deco")

    def mas_o31HideVisuals():
        """
        Hides o31 visuals + vignette
        """
        mas_hideDecoTag("mas_o31_deco")
        renpy.hide("vignette")
        #Also going to stop vignette from showing on subsequent spaceroom calls
        store.mas_globals.show_vignette = False
        #Also, if we're hiding visuals, we're no longer in o31 mode
        store.persistent._mas_o31_in_o31_mode = False

        #unlock hairdown greet if we don't have hairdown unlocked
        hair = store.mas_selspr.get_sel_hair(store.mas_hair_down)
        if hair is not None and not hair.unlocked:
            store.mas_unlockEVL("greeting_hairdown", "GRE")

        # lock the event clothes selector
        store.mas_lockEVL("monika_event_clothes_select", "EVE")

         # get back into reasonable clothing, so we queue a change to def
        if store.monika_chr.is_wearing_clothes_with_exprop("costume"):
            store.queueEvent('mas_change_to_def')

    def mas_o31CapGainAff(amount):
        """
        CapGainAffection function for o31. See mas_capGainAff for details
        """
        mas_capGainAff(amount, "_mas_o31_trick_or_treating_aff_gain", 15)


    def mas_o31CostumeWorn(clothes):
        """
        Checks if the given clothes was worn on o31

        IN:
            clothes - Clothes object to check

        RETURNS: year the given clothe was worn if worn on o31, None if never
            worn on o31.
        """
        if clothes is None:
            return False
        return mas_o31CostumeWorn_n(clothes.name)


    def mas_o31CostumeWorn_n(clothes_name):
        """
        Checks if the given clothes (name) was worn on o31

        IN:
            clothes_name - Clothes name to check

        RETURNS: year the given clothes name was worn if worn on o31, none if
            never worn on o31.
        """
        return persistent._mas_o31_costumes_worn.get(clothes_name, None)


    def mas_o31SelectCostume(selection_pool=None):
        """
        Selects an o31 costume to wear. Costumes that have not been worn
        before are selected first.

        NOTE: o31 costume wear flag is NOT set here. Make sure to set this
            manually later.

        IN:
            selection_pool - pool to select clothes from. If NOne, we get a
                default list of clothes with costume exprop

        RETURNS: a single MASClothes object of what to wear. None if cannot
            return anything.
        """
        if selection_pool is None:
            selection_pool = MASClothes.by_exprop("costume", "o31")

        # set to true if monika is wearing a costume right now
        wearing_costume = False

        # filter the selection pool by criteria:
        #   1 - if spritepack-based, then must be gifted
        #   2 - if not spritepack-based, then is valid for selecting regardless
        #   3 - dont include if monika currently wearing
        filt_sel_pool = []
        for cloth in selection_pool:
            sprite_key = (store.mas_sprites.SP_CLOTHES, cloth.name)
            giftname = store.mas_sprites_json.namegift_map.get(
                sprite_key,
                None
            )

            if (
                giftname is None
                or sprite_key in persistent._mas_sprites_json_gifted_sprites
            ):
                if cloth != monika_chr.clothes:
                    filt_sel_pool.append(cloth)
                else:
                    wearing_costume = True


        selection_pool = filt_sel_pool

        if len(selection_pool) < 1:
            # no items to select from

            if wearing_costume:
                #Check if the current costume is in the cg map, and if so, prep the cg
                if monika_chr.clothes in MAS_O31_COSTUME_CG_MAP:
                    store.mas_o31_event.cg_decoded = store.mas_o31_event.decodeImage(MAS_O31_COSTUME_CG_MAP[monika_chr.clothes])

                return monika_chr.clothes
            return None

        elif len(selection_pool) < 2:
            # only 1 item to select from, just return
            return selection_pool[0]

        # otherwise, create list of non worn costumes
        non_worn = [
            costume
            for costume in selection_pool
            if not mas_o31CostumeWorn(costume)
        ]

        if len(non_worn) > 0:
            # randomly select from non worn
            random_outfit = random.choice(non_worn)

        else:
            # otherwise randomly select from overall
            random_outfit = random.choice(selection_pool)

        #Setup the image decode
        if random_outfit in MAS_O31_COSTUME_CG_MAP:
            store.mas_o31_event.cg_decoded = store.mas_o31_event.decodeImage(MAS_O31_COSTUME_CG_MAP[random_outfit])

        #And return the outfit
        return random_outfit

    def mas_o31SetCostumeWorn(clothes, year=None):
        """
        Sets that a clothing item is worn. Exprop checking is done

        IN:
            clothes - clothes object to set
            year - year that the costume was worn. If NOne, we use current year
        """
        if clothes is None or not clothes.hasprop("costume"):
            return

        mas_o31SetCostumeWorn_n(clothes.name, year=year)


    def mas_o31SetCostumeWorn_n(clothes_name, year=None):
        """
        Sets that a clothing name is worn. NO EXPROP CHECKING IS DONE

        IN:
            clothes_name - name of clothes to set
            year - year that the costume was worn. If None, we use current year
        """
        if year is None:
            year = datetime.date.today().year

        persistent._mas_o31_costumes_worn[clothes_name] = year

    def mas_o31Cleanup():
        """
        Cleanup function for o31
        """
        #NOTE: Since O31 is costumes, we always reset clothes + hair
        if monika_chr.is_wearing_clothes_with_exprop("costume"):
            monika_chr.change_clothes(mas_clothes_def, outfit_mode=True)
            monika_chr.reset_hair()

        #Reset o31_mode flag
        persistent._mas_o31_in_o31_mode = False

        #Unlock BG Sel if necessary
        mas_checkBackgroundChangeDelegate()

        #Hide visuals
        mas_o31HideVisuals()

        #rmall for safety
        mas_rmallEVL("mas_o31_cleanup")

        #unlock hairdown greet if we don't have hairdown unlocked
        hair = store.mas_selspr.get_sel_hair(mas_hair_down)
        if hair is not None and not hair.unlocked:
            mas_unlockEVL("greeting_hairdown", "GRE")

        #Lock the event clothes selector
        mas_lockEVL("monika_event_clothes_select", "EVE")

init -11 python in mas_o31_event:
    import store
    import datetime

    # setup the docking station for o31
    cg_station = store.MASDockingStation(store.mas_ics.o31_cg_folder)

    # cg available?
    cg_decoded = False


    def decodeImage(key):
        """
        Attempts to decode a cg image

        IN:
            key - o31 cg key to decode

        RETURNS True upon success, False otherwise
        """
        return store.mas_dockstat.decodeImages(cg_station, store.mas_ics.o31_map, [key])


    def removeImages():
        """
        Removes decoded images at the end of their lifecycle
        """
        store.mas_dockstat.removeImages(cg_station, store.mas_ics.o31_map)

#START: O31 AUTOLOAD CHECK
label mas_o31_autoload_check:
    python:
        import random

        if mas_isO31() and mas_isMoniNormal(higher=True):
            #Lock the background selector on o31
            #TODO: Replace this with generic room deco framework for event deco
            store.mas_lockEVL("monika_change_background", "EVE")
            #force to spaceroom
            # NOTE: need to make sure we pass the change info to the next
            #   spaceroom call.
            mas_changeBackground(mas_background_def, set_persistent=True)

            #NOTE: We do not do O31 deco/amb on first sesh day
            if (not persistent._mas_o31_in_o31_mode and not mas_isFirstSeshDay()):
                #Setup for greet
                mas_skip_visuals = True

                #Reset idle since we will force greetings
                mas_resetIdleMode()

                #Lock the hairdown greeting for today
                mas_lockEVL("greeting_hairdown", "GRE")

                #Disable hotkeys for this
                store.mas_hotkeys.music_enabled = False

                #Put calendar shields up
                mas_calRaiseOverlayShield()

                # select a costume
                # NOTE: we should always have at least 1 costume.
                costume = mas_o31SelectCostume()
                store.mas_selspr.unlock_clothes(costume)
                mas_addClothesToHolidayMap(costume)
                mas_o31SetCostumeWorn(costume)

                # remove ribbon so we just get the intended costume for the reveal
                ribbon_acs = monika_chr.get_acs_of_type("ribbon")
                if ribbon_acs is not None:
                    monika_chr.remove_acs(ribbon_acs)

                monika_chr.change_clothes(
                    costume,
                    by_user=False,
                    outfit_mode=True
                )

                #Save selectables
                store.mas_selspr.save_selectables()

                #Save persist
                renpy.save_persistent()

                #Select greet
                greet_label = "greeting_o31_{0}".format(costume.name)

                if renpy.has_label(greet_label):
                    selected_greeting = greet_label
                else:
                    selected_greeting = "greeting_o31_generic"

                #Save and reset zoom
                mas_temp_zoom_level = store.mas_sprites.zoom_level
                store.mas_sprites.reset_zoom()

                #Now that we're here, we're in O31 mode
                persistent._mas_o31_in_o31_mode = True

                #Vignette on O31
                store.mas_globals.show_vignette = True

                #Set by-user to True because we don't want progressive
                mas_changeWeather(mas_weather_thunder, True)

            elif (persistent._mas_o31_in_o31_mode and not mas_isFirstSeshDay()):
                #Setup vignette and thunder on subsequent sessions
                store.mas_globals.show_vignette = True
                mas_changeWeather(mas_weather_thunder, True)

        #It's not O31 anymore or we hit dis. It's time to reset
        elif not mas_isO31() or mas_isMoniDis(lower=True):
            mas_o31Cleanup()

        #If we drop to upset during O31, we should keep decor until we hit dis
        elif persistent._mas_o31_in_o31_mode and mas_isMoniUpset():
            store.mas_globals.show_vignette = True
            mas_changeWeather(mas_weather_thunder, True)

    #Run pbday checks
    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        call mas_player_bday_autoload_check

    if mas_skip_visuals:
        jump ch30_post_restartevent_check

    # otherwise, jump back to the holiday check point
    jump mas_ch30_post_holiday_check

## post returned home greeting to setup game relaunch
label mas_holiday_o31_returned_home_relaunch:
    m 1eua "Entonces, hoy es..."
    m 1euc "...Espera."
    m "..."
    m 2wuo "¡Oh!"
    m 2wuw "¡Oh dios mío!"
    m 2hub "Ya es Halloween, [player]."
    m 1eua "...{w=1}Quiero decir."
    m 3eua "Voy a cerrar el juego."
    m 1eua "Después de eso, puedes volver a abrirlo."
    m 1hubsa "Tengo algo especial reservado para ti, jejeje~"
    $ persistent._mas_o31_relaunch = True
    return "quit"

### o31 images
image mas_o31_marisa_cg = "mod_assets/monika/cg/o31_marisa_cg.png"
# 1280 x 2240

image mas_o31_rin_cg = "mod_assets/monika/cg/o31_rin_cg.png"

### o31 transforms
transform mas_o31_cg_scroll:
    xanchor 0.0 xpos 0 yanchor 0.0 ypos 0.0 yoffset -1520
    ease 20.0 yoffset 0.0

### o31 samesesh cleanup
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_o31_cleanup",
            conditional="persistent._mas_o31_in_o31_mode",
            start_date=datetime.datetime.combine(mas_o31 + datetime.timedelta(days=1), datetime.time(12)),
            end_date=mas_o31 + datetime.timedelta(weeks=1),
            action=EV_ACT_QUEUE,
            rules={"no_unlock": None},
            years=[]
        )
    )


label mas_o31_cleanup:
    m 1eua "Un segundo [player], sólo voy a quitar los adornos.{w=0.3}.{w=0.3}.{nw}"
    call mas_transition_to_emptydesk
    pause 4.0
    $ mas_o31Cleanup()
    with dissolve
    pause 1.0
    call mas_transition_from_emptydesk("monika 1hua")
    m 3hua "Listo~"
    return

### o31 greetings
init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_marisa",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_marisa:
    # with marisa, we should also unlock the hat and the hair style
    $ store.mas_selspr.unlock_acs(mas_acs_marisa_witchhat)
    $ store.mas_selspr.unlock_hair(mas_hair_downtiedstrand)

    ## decoded CG means that we start with monika offscreen
    if store.mas_o31_event.cg_decoded:
        # ASSUMING:
        #   vignette should be enabled.
        call spaceroom(hide_monika=True, scene_change=True)

    else:
        # ASSUMING:
        #   vignette should be enabled
        call spaceroom(dissolve_all=True, scene_change=True, force_exp='monika 1eua_static')

    m 1eua "¡Ah!"
    m 1hua "Parece que mi hechizo funcionó."
    m 3efu "¡Como mi sirviente recién convocado, tendrás que cumplir mis órdenes hasta el albor de los tiempos!"
    m 1rksdla "..."
    m 1hub "¡Jajaja!"

    # decoded CG means we display CG
    if store.mas_o31_event.cg_decoded:
        $ cg_delay = datetime.timedelta(seconds=20)

        # got cg
        m "Estoy aquí, [player]~"
        window hide

        show mas_o31_marisa_cg zorder 20 at mas_o31_cg_scroll with dissolve
        $ start_time = datetime.datetime.now()
        while datetime.datetime.now() - start_time < cg_delay:
            pause 1.0

        hide emptydesk
        show monika 1hua at i11 zorder MAS_MONIKA_Z

        window auto
        m "¡Tadaa~!"

    #Post scroll dialogue
    m 1hua "Bueno..."
    m 1eub "¿Qué piensas?"
    m 1wua "Me queda bastante bien, ¿verdad?"
    m 1eua "Me tomó bastante tiempo hacer este disfraz, ya sabes."
    m 3hksdlb "Obtener las medidas correctas, asegurarme de que nada esté demasiado apretado o suelto, ese tipo de cosas."
    m 3eksdla "...¡Especialmente el sombrero!"
    m 1dkc "El lazo no se queda quieto en lo absoluto..."
    m 1rksdla "Por suerte lo solucioné."
    m 3hua "Yo diría que hice un buen trabajo."
    m 3eka "Me pregunto si podrás ver qué es diferente hoy."
    m 3tub "Además de mi disfraz, por supuesto~"
    m 1hua "Pero de todos modos..."

    if store.mas_o31_event.cg_decoded:
        show monika 1eua
        hide mas_o31_marisa_cg with dissolve

    m 3ekbsa "Estoy muy emocionada de pasar Halloween contigo."
    m 1hua "¡Vamos a divertirnos hoy!"

    call greeting_o31_cleanup
    return

init 5 python:
   addEvent(
       Event(
           persistent.greeting_database,
           eventlabel="greeting_o31_rin",
           category=[store.mas_greetings.TYPE_HOL_O31]
       ),
       code="GRE"
    )

label greeting_o31_rin:
    python:
        title_cased_hes = hes.capitalize()
        #TODO: Unlock this hairstyle once we clean it up such that it doesn't require bows
        #Will need update script
        #mas_selspr.unlock_hair(mas_hair_braided)
        mas_sprites.zoom_out()

    # ASSUME vignette
    call spaceroom(hide_monika=True, scene_change=True)

    m "Ugh, espero haber acertado con estas trenzas."
    m "¿Por qué este disfraz tiene que ser tan complicado... ?"
    m "¡Oh rayos! ¡[title_cased_hes]tá aquí!"
    window hide
    pause 3.0

    if store.mas_o31_event.cg_decoded:
        $ cg_delay = datetime.timedelta(seconds=20)

        # got cg
        window auto
        m "Dime, [player]..."
        window hide

        show mas_o31_rin_cg zorder 20 at mas_o31_cg_scroll with dissolve
        $ start_time = datetime.datetime.now()

        while datetime.datetime.now() - start_time < cg_delay:
            pause 1.0

        hide emptydesk
        window auto
        m "¿Qué {i}nya{/i} piensas?"

        scene black
        pause 1.0
        call spaceroom(scene_change=True, dissolve_all=True, force_exp='monika 1hksdlb_static')
        m 1hksdlb "Jajaja, decir eso en voz alta fue más vergonzoso de lo que pensé..."

    else:
        call mas_transition_from_emptydesk("monika 1eua")
        m 1hub "¡Buenas, [player]!"
        m 3hub "¿Te gusta mi disfraz?"

    # regular dialogue
    m 3etc "Honestamente, ni siquiera sé quién se supone que sea."
    m 3etd "Lo encontré en el armario con una nota adjunta que tenía la palabra 'Rin', un dibujo de una niña empujando una carretilla y algunas cositas azules flotantes."
    m 1euc "Junto con instrucciones sobre cómo peinar tu cabello para combinar con este atuendo."
    m 3rtc "A juzgar por estas orejas de gato, supongo que este personaje es una niña gato."
    m 1dtc "...Pero, ¿por qué empujaría una carretilla?"
    m 1hksdlb "De todos modos, fue un dolor de cabeza peinarme el pelo...{w=0.2}{nw}"
    extend 1eub "¡Así que espero que te guste el disfraz!"

    call greeting_o31_cleanup
    return

#Miku intro
init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_orcaramelo_hatsune_miku",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_orcaramelo_hatsune_miku:
    if not persistent._mas_o31_relaunch:
        call spaceroom(hide_monika=True, scene_change=True, dissolve_all=True)
        #moni is off-screen
        m "{i}~Mi voz no has de olvidar~{/i}"
        m "{i}~Mi señal cruzará~{/i}"
        m "{i}~Yo no soy virtual~{/i}"
        m "{i}~Todavía quiero ser am-{/i}"
        m "¡Oh!{w=0.5} Parece que alguien me ha estado escuchando."

        #show moni now
        call mas_transition_from_emptydesk("monika 3hub")

    else:
        call spaceroom(scene_change=True, dissolve_all=True)

    m 3hub "¡Bienvenido de nuevo, [player]!"
    m 1eua "Entonces... {w=0.5}¿qué opinas?"
    m 3eua "Creo que este disfraz realmente me queda bien."
    m 3eub "¡A mí también me encanta especialmente cómo se ven los auriculares!"
    m 1rksdla "Aunque no puedo decir que sea demasiado cómodo para moverse..."
    m 3tsu "¡Así que no esperes que te dé una actuación hoy, [player]!"
    m 1hub "Jajaja~"
    m 1eua "De todas formas..."
    call greeting_o31_deco
    call greeting_o31_cleanup
    return

#Sakuya intro
init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_orcaramelo_sakuya_izayoi",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_orcaramelo_sakuya_izayoi:
    call spaceroom(hide_monika=True, scene_change=True, dissolve_all=True)

    #moni is off-screen
    if not persistent._mas_o31_relaunch:
        m "..."
        m "¿{i}Eh{/i}?"
        m "{i}Ah, debe haber habido algún tipo de error. {w=0.5}No me advirtieron de ningún invitado...{/i}"
        m "{i}No importa. Nadie interrumpirá este mo-{/i}"
        m "¡Oh!{w=0.5} ¡Eres tú, [player]!"

    else:
        m ".{w=0.3}.{w=0.3}.{w=0.3}{nw}"
        m "Bienvenido{w=0.3}, a la sala espacial del demonio carmesí..."
        m "[player]."
        m "Por favor, permítame ofrecerle nuestra hospitalidad."
        m "¡Jajaja! ¿Cómo estuvo esa imitación?"

    #show moni now
    call mas_transition_from_emptydesk("monika 3hub")

    m 3hub "¡Bienvenido de vuelta!"
    m 3eub "¿Qué opinas de mi vestuario?"
    m 3hua "¡Desde que me lo diste, supe que lo usaría hoy!"
    m 2tua "..."
    m 2tub "Sabes, [player], solo porque estoy vestida de sirvienta no significa que voy a seguir todas tus órdenes..."
    show monika 5kua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5kua "Aunque podría hacer algunas excepciones, jejeje~"
    show monika 1eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 1eua "De todas formas..."
    call greeting_o31_deco
    call greeting_o31_cleanup
    return

label greeting_o31_deco:
    m 3eua "¿Te gusta lo que he hecho con la habitación?"
    m 3eka "Una de mis partes favoritas de Halloween es tallar calabazas..."
    m 1hub "¡Es tan divertido tratar de hacer caras aterradoras!"
    m 1eua "Creo que las telarañas también son un buen toque..."
    m 1rka "{cps=*2}Estoy segura de que a Amy le gustarían mucho.{/cps}{nw}"
    $ _history_list.pop()
    m 3tuu "Realmente crea un ambiente espeluznante, ¿no crees?"
    return

label greeting_o31_generic:
    call spaceroom(scene_change=True, dissolve_all=True)

    m 3hub "¡Dulce o truco!"
    m 3eua "Jajaja, solo estoy bromeando, [player]."
    m 1hua "Bienvenido de nuevo...{w=0.5}{nw}"
    extend 3hub "y ¡Feliz Halloween!"

    #We'll address the room with this
    call greeting_o31_deco

    m 3hua "Por cierto, ¿qué opinas de mi disfraz?"
    m 1hua "A mí me gusta mucho~"
    m 1hub "Más aún, porque fue un regalo tuyo, ¡jajaja!"
    m 3tuu "Así que deleita tus ojos con mi disfraz mientras puedas, ejeje~"

    call greeting_o31_cleanup
    return

#Cleanup for o31 greets
label greeting_o31_cleanup:
    window hide
    call monika_zoom_transition(mas_temp_zoom_level,1.0)
    window auto

    python:
        # 1 - music hotkeys should be enabled
        store.mas_hotkeys.music_enabled = True
        # 2 - calendarovrelay enabled
        mas_calDropOverlayShield()
        # 3 - set the keymaps
        set_keymaps()
        # 4 - hotkey buttons should be shown
        HKBShowButtons()
        # 5 - restart music
        mas_startup_song()
    return

#START: O31 DOCKSTAT FARES
init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_trick_or_treat",
            prompt="Te voy a llevar a pedir dulce o truco.",
            pool=True,
            unlocked=False,
            action=EV_ACT_UNLOCK,
            start_date=mas_o31,
            end_date=mas_o31+datetime.timedelta(days=1),
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="BYE",
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
       "bye_trick_or_treat",
       mas_o31,
       mas_o31 + datetime.timedelta(days=1),
    )

label bye_trick_or_treat:
    python:
        curr_hour = datetime.datetime.now().hour
        too_early_to_go = curr_hour < 17
        too_late_to_go = curr_hour >= 23

    #True if > 0
    if persistent._mas_o31_tt_count:
        m 1eka "¿Otra vez?"

    if too_early_to_go:
        # before 5pm is too early.
        m 3eksdla "¿No te parece un poco temprano para pedir dulces, [player]?"
        m 3rksdla "No creo que haya nadie repartiendo dulces todavía..."

        m 2etc "¿Estás {i}seguro{/i} de que quieres ir ahora mismo?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Estás {i}seguro{/i} de que quieres ir ahora mismo?{fast}"
            "Sí.":
                m 2etc "Bueno... {w=1}Está bien, [player]..."

            "No.":
                m 2hub "¡Jajaja!"
                m "Ten un poco de paciencia, [player]~"
                m 4eub "Aprovechemos al máximo más tarde esta noche, ¿de acuerdo?"
                return

    elif too_late_to_go:
        m 3hua "¡Bueno! Vamos a pedir-"
        m 3eud "Espera..."
        m 2dkc "[player]..."
        m 2rkc "Ya es demasiado tarde para ir a pedir dulces."
        m "Sólo falta una hora para la medianoche."
        m 2dkc "Sin mencionar que dudo que queden muchos dulces..."
        m "..."

        m 4ekc "¿Estás seguro de que todavía quieres ir?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Estás seguro de que todavía quieres ir?{fast}"
            "Sí.":
                m 1eka "...De acuerdo."
                m "Aunque solo quede una hora..."
                m 3hub "Al menos vamos a pasar el resto de Halloween juntos~"
                m 3wub "¡Vamos a aprovecharlo al máximo, [player]!"

            "En realidad, es {i}un{/i} poco tarde...":
                if persistent._mas_o31_tt_count:
                    m 1hua "Jajaja~"
                    m "Te lo dije."
                    m 1eua "Tendremos que esperar hasta el próximo año para ir."

                else:
                    m 2dkc "..."
                    m 2ekc "Bien, [player]."
                    m "Es una pena que no pudiéramos ir a pedir dulces este año."
                    m 4eka "Asegurémonos de que podamos la próxima vez, ¿de acuerdo?"

                return

    else:
        # between 5 and 11pm is perfect
        m 3wub "¡Okay, [player]!"
        m 3hub "Parece que nos lo pasaremos genial~"
        m 1eub "¡Apuesto a que tendremos muchos dulces!"
        m 1ekbsa "E incluso si no lo hacemos, solo pasar la noche contigo es suficiente para mí~"

    #Setup the dockstat stuff
    $ mas_farewells.dockstat_wait_menu_label = "bye_trick_or_treat_wait_wait"
    $ mas_farewells.dockstat_rtg_label = "bye_trick_or_treat_rtg"
    jump mas_dockstat_iostart

label bye_trick_or_treat_wait_wait:
    # wait wait flow
    menu:
        m "¿Qué pasa?"
        "Tienes razón, es un poco temprano." if too_early_to_go:
            call mas_dockstat_abort_gen
            call mas_transition_from_emptydesk(exp="monika 3hub")

            m 3hub "¡Jajaja, te lo dije!"
            m 1eka "Esperemos hasta la noche, ¿de acuerdo?"
            return True

        "Tienes razón, es un poco tarde." if too_late_to_go:
            call mas_dockstat_abort_gen

            if persistent._mas_o31_tt_count:
                call mas_transition_from_emptydesk(exp="monika 1hua")
                m 1hua "Jajaja~"
                m "Te lo dije."
                m 1eua "Tendremos que esperar hasta el próximo año para volver."

            else:
                call mas_transition_from_emptydesk(exp="monika 2dkc")
                m 2dkc "..."
                m 2ekc "Bien, [player]."
                m "Es una pena que no pudiéramos ir a pedir dulces este año."
                m 4eka "Asegurémonos de que podamos la próxima vez, ¿de acuerdo?"

            return True

        "En realidad, no puedo llevarte ahora.":
            call mas_dockstat_abort_gen
            call mas_transition_from_emptydesk(exp="monika 1euc")

            m 1euc "Oh, bien entonces, [player]."

            if persistent._mas_o31_tt_count:
                m 1eua "Avísame si quieres volver más tarde, ¿de acuerdo?"

            else:
                m 1eua "Avísame si podemos ir, ¿de acuerdo?"

            return True

        "Nada.":
            m "Está bien, déjame terminar de prepararme."
            return

label bye_trick_or_treat_rtg:
    # iothread is done
    $ moni_chksum = promise.get()
    $ promise = None # always clear the promise
    call mas_dockstat_ready_to_go(moni_chksum)

    if _return:
        call mas_transition_from_emptydesk(exp="monika 1hub")
        m 1hub "¡Vamos a pedir dulces!"
        $ persistent._mas_greeting_type = store.mas_greetings.TYPE_HOL_O31_TT

        #Increment T/T counter
        $ persistent._mas_o31_tt_count += 1
        return "quit"

    # otherwise, failure in generation
    #Fix tt count
    call mas_transition_from_emptydesk(exp="monika 1ekc")
    $ persistent._mas_o31_tt_count -= 1
    m 1ekc "Oh no..."
    m 1rksdlb "No pude convertirme en un archivo."

    if persistent._mas_o31_tt_count:
        m 1eksdld "Creo que tendrás que ir a pedir dulces sin mí esta vez..."

    else:
        m 1eksdld "Creo que tendrás que ir a pedir dulces sin mí..."

    m 1ekc "Lo siento, [player]..."
    m 3eka "Asegúrate de traer muchos dulces para que los dos disfrutemos, ¿de acuerdo~ ?"
    return

#START: O31 DOCKSTAT GREETS
init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_trick_or_treat_back",
            unlocked=True,
            category=[store.mas_greetings.TYPE_HOL_O31_TT]
        ),
        code="GRE"
    )

label greeting_trick_or_treat_back:
    # trick/treating returned home greeting
    python:
        # lots of setup here
        time_out = store.mas_dockstat.diffCheckTimes()
        checkin_time = None
        is_past_sunrise_post31 = False
        ret_tt_long = False

        if len(persistent._mas_dockstat_checkin_log) > 0:
            checkin_time = persistent._mas_dockstat_checkin_log[-1:][0][0]
            sunrise_hour, sunrise_min = mas_cvToHM(persistent._mas_sunrise)
            is_past_sunrise_post31 = (
                datetime.datetime.now() > (
                    datetime.datetime.combine(
                        mas_o31,
                        datetime.time(sunrise_hour, sunrise_min)
                    )
                    + datetime.timedelta(days=1)
                )
            )


    if time_out < mas_five_minutes:
        $ mas_loseAffection()
        m 2ekp "¿A eso lo llamas dulce o truco, [player]?"
        m "¿A dónde fuimos, a una sola casa?"
        m 2rsc "...Si ni siquiera nos movimos."

    elif time_out < mas_one_hour:
        $ mas_o31CapGainAff(5)
        m 2ekp "Eso fue bastante corto para pedir dulces, [player]."
        m 3eka "Pero lo disfruté mientras duró."
        m 1eka "Fue muy agradable estar ahí contigo~"

    elif time_out < mas_three_hour:
        $ mas_o31CapGainAff(10)
        m 1hua "Y... ¡Ya estamos en casa!"
        m 1hub "¡Espero que tengamos muchos dulces deliciosos!"
        m 1eka "Realmente disfruté el dulce o truco contigo, [player]..."

        call greeting_trick_or_treat_back_costume

        m 4eub "¡Hagamos esto de nuevo el año que viene!"

    elif not is_past_sunrise_post31:
        # larger than 3 hours, but not past sunrise
        $ mas_o31CapGainAff(15)
        m 1hua "Y... ¡Ya estamos en casa!"
        m 1wua "Vaya, [player], seguro que fuimos a pedir dulces durante mucho tiempo..."
        m 1wub "¡Seguro que hemos recibido una tonelada de dulces!"
        m 3eka "Realmente disfruté estar allí contigo..."

        call greeting_trick_or_treat_back_costume

        m 4eub "¡Hagamos esto de nuevo el año que viene!"
        $ ret_tt_long = True

    else:
        # larger than 3 hours, past sunrise
        $ mas_o31CapGainAff(15)
        m 1wua "¡Finalmente estamos en casa!"
        m 1wuw "Ya no es Halloween, [player]... ¡Estuvimos fuera toda la noche!"
        m 1hua "Supongo que nos divertimos demasiado, jejeje~"
        m 2eka "Pero de todos modos, gracias por llevarme, realmente lo disfruté."

        call greeting_trick_or_treat_back_costume

        m 4hub "Hagamos esto de nuevo el año que viene... {w=1} ¡pero quizás {i}deberíamos{/i} no quedarnos fuera tan tarde!"
        $ ret_tt_long = True

    #Now do player bday things (this also cleans up o31 deco)
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        # if we are returning from a non-birthday date post o31 birthday
        call return_home_post_player_bday

    #If it's just not o31, we need to clean up
    elif not mas_isO31() and persistent._mas_o31_in_o31_mode:
        call mas_o31_ret_home_cleanup(time_out, ret_tt_long)
    return

label mas_o31_ret_home_cleanup(time_out=None, ret_tt_long=False):
    #Time out not defined, we need to get it outselves
    if not time_out:
        $ time_out = store.mas_dockstat.diffCheckTimes()

    #If we were out over 5 mins then we have this little extra dialogue
    if not ret_tt_long and time_out > mas_five_minutes:
        m 1hua "..."
        m 1wud "Oh, vaya, [player]. Realmente estuvimos fuera durante bastante tiempo..."

    else:
        m 1esc "De todas formas..."

    m 1eua "Simplemente quitaré estas decoraciones.{w=0.3}.{w=0.3}.{w=0.3}{nw}"

    #Hide vis
    $ mas_o31HideVisuals()
    $ mas_rmallEVL("mas_o31_cleanup")

    m 3hua "¡Listo!"
    return

label greeting_trick_or_treat_back_costume:
    if monika_chr.is_wearing_clothes_with_exprop("costume"):
        m 2eka "Incluso si no pudiera ver nada y nadie más pudiera ver mi disfraz..."
        m 2eub "¡Vestirse y salir fue realmente genial!"

    else:
        m 2eka "Incluso si no pudiera ver nada..."
        m 2eub "¡Salir fue realmente genial!"
    return

#START: D25
#################################### D25 ######################################
# [HOL020]

# True if we should consider ourselves in d25 mode.
default persistent._mas_d25_in_d25_mode = False

# True if the user spent time with monika on d25
# (basically they got the merry christmas dialogue)
default persistent._mas_d25_spent_d25 = False

# True if we started the d25 season with upset and below monika
default persistent._mas_d25_started_upset = False

# True if we dipped below to upset again.
default persistent._mas_d25_second_chance_upset = False

# True if d25 decorations are active
# this also includes santa outfit
# This should only be True if:
#   Monika is NOt being returned after the d25 season begins
#   and season is d25.
default persistent._mas_d25_deco_active = False

# True once a d25 intro has been seen
default persistent._mas_d25_intro_seen = False

# number of times user takes monika out on d25e
default persistent._mas_d25_d25e_date_count = 0

# number of times user takes monika out on d25
# this also includes if the day was partially or entirely spent out
default persistent._mas_d25_d25_date_count = 0

#List of all gifts which will be opened on christmas
default persistent._mas_d25_gifts_given = list()

#Stores if we were on a date with Monika over the full d25 day
default persistent._mas_d25_gone_over_d25 = None

# christmas
define mas_d25 = datetime.date(datetime.date.today().year, 12, 25)

# christmas eve
define mas_d25e = mas_d25 - datetime.timedelta(days=1)

#Dec 26, the day Monika stops wearing santa and the end of the christmas gift range
define mas_d25p = mas_d25 + datetime.timedelta(days=1)

# start of christmas season (inclusive) and when Monika wears santa
define mas_d25c_start = datetime.date(datetime.date.today().year, 12, 11)

# end of christmas season (exclusive)
define mas_d25c_end = datetime.date(datetime.date.today().year, 1, 6)



init -810 python:
    # we also need a history svaer for when the d25 season ends.
    store.mas_history.addMHS(MASHistorySaver(
        "d25s",
        datetime.datetime(2019, 1, 6),
        {
            #Not very useful, but we need the reset
            #NOTE: this is here because the d25 season actually ends in jan
            "_mas_d25_in_d25_mode": "d25s.mode.25",

            #NOTE: this is here because the deco ends with the season
            "_mas_d25_deco_active": "d25s.deco_active",

            "_mas_d25_started_upset": "d25s.monika.started_season_upset",
            "_mas_d25_second_chance_upset": "d25s.monika.upset_after_2ndchance",

            "_mas_d25_intro_seen": "d25s.saw_an_intro",

            #D25 dates
            "_mas_d25_d25e_date_count": "d25s.d25e.went_out_count",
            "_mas_d25_d25_date_count": "d25s.d25.went_out_count",
            "_mas_d25_gone_over_d25": "d25.actions.gone_over_d25",

            "_mas_d25_spent_d25": "d25.actions.spent_d25"
        },
        use_year_before=True,
        start_dt=datetime.datetime(2019, 12, 11),
        end_dt=datetime.datetime(2019, 12, 31)
    ))


init -10 python:

    def mas_isD25(_date=None):
        """
        Returns True if the given date is d25

        IN:
            _date - date to check
                If None, we use today's date
                (default: None)

        RETURNS: True if given date is d25, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return _date == mas_d25.replace(year=_date.year)


    def mas_isD25Eve(_date=None):
        """
        Returns True if the given date is d25 eve

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is d25 eve, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return _date == mas_d25e.replace(year=_date.year)


    def mas_isD25Season(_date=None):
        """
        Returns True if the given date is in d25 season. The season goes from
        dec 11 to jan 5.

        NOTE: because of the year rollover, we cannot check years

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is in d25 season, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return (
            mas_isInDateRange(_date, mas_d25c_start, mas_nye, True, True)
            or mas_isInDateRange(_date, mas_nyd, mas_d25c_end)
        )


    def mas_isD25Post(_date=None):
        """
        Returns True if the given date is after d25 but still in D25 season.
        The season goes from dec 1 to jan 5.

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is in d25 season but after d25, False
            otherwise.
        """
        if _date is None:
            _date = datetime.date.today()

        return (
            mas_isInDateRange(_date, mas_d25p, mas_nye, True, True)
            or mas_isInDateRange(_date, mas_nyd, mas_d25c_end)
        )


    def mas_isD25PreNYE(_date=None):
        """
        Returns True if the given date is in d25 season and before nye.

        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNSL True if given date is in d25 season but before nye, False
            otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return mas_isInDateRange(_date, mas_d25c_start, mas_nye)


    def mas_isD25PostNYD(_date=None):
        """
        Returns True if the given date is in d25 season and after nyd

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is in d25 season but after nyd, False
            otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return mas_isInDateRange(_date, mas_nyd, mas_d25c_end, False)


    def mas_isD25Outfit(_date=None):
        """
        Returns True if the given date is tn the range of days where Monika
        wears the santa outfit on start.

        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNS: True if given date is in the d25 santa outfit range, False
            otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return mas_isInDateRange(_date, mas_d25c_start, mas_d25p)


    def mas_isD25Pre(_date=None):
        """
        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNS: True if given date is in the D25 season, but before Christmas, False
            otherwise

        NOTE: This is used for gifts too
        """
        if _date is None:
            _date = datetime.date.today()

        return mas_isInDateRange(_date, mas_d25c_start, mas_d25)

    def mas_isD25GiftHold(_date=None):
        """
        IN:
            _date - date to check, defaults None, which means today's date is assumed

        RETURNS:
            boolean - True if within d25c start, to d31 (end of nts range)
            (The time to hold onto gifts, aka not silently react)
        """
        if _date is None:
            _date = datetime.date.today()

        return mas_isInDateRange(_date, mas_d25c_start, mas_nye, end_inclusive=True)

    def mas_d25ShowVisuals():
        """
        Shows d25 visuals.
        """
        mas_showDecoTag("mas_d25_banners")
        mas_showDecoTag("mas_d25_tree")
        mas_showDecoTag("mas_d25_garlands")
        mas_showDecoTag("mas_d25_lights")
        mas_showDecoTag("mas_d25_gifts")

    def mas_d25HideVisuals():
        """
        Hides d25 visuals
        """
        mas_hideDecoTag("mas_d25_banners", hide_now=True)
        mas_hideDecoTag("mas_d25_tree", hide_now=True)
        mas_hideDecoTag("mas_d25_garlands", hide_now=True)
        mas_hideDecoTag("mas_d25_lights", hide_now=True)
        mas_hideDecoTag("mas_d25_gifts", hide_now=True)

    def mas_d25ReactToGifts():
        """
        Goes thru the gifts stored from the d25 gift season and reacts to them

        this also registeres gifts
        """
        #Step one, store all of the found reacts
        found_reacts = list()

        #Just sort the gifts given list:
        persistent._mas_d25_gifts_given.sort()

        #Now we copy the giftnames for local usage
        #We do this because we pop from the persistent list during the reactions
        #Because then it looks more like Monika is taking them from under the tree
        given_gifts = list(persistent._mas_d25_gifts_given)

        # d25 special quiplist
        gift_cntrs = store.MASQuipList(allow_glitch=False, allow_line=False)
        gift_cntrs.addLabelQuip("mas_d25_gift_connector")

        # process giftnames (no generics)
        d25_evb = []
        d25_gsp = []
        store.mas_filereacts.process_gifts(given_gifts, d25_evb, d25_gsp)

        # register gifts
        store.mas_filereacts.register_sp_grds(d25_evb)
        store.mas_filereacts.register_sp_grds(d25_gsp)

        # build reaction labels
        react_labels = store.mas_filereacts.build_gift_react_labels(
            d25_evb,
            d25_gsp,
            [],
            gift_cntrs,
            "mas_d25_gift_end",
            "mas_d25_gift_starter"
        )

        react_labels.reverse()

        # queue the reacts
        if len(react_labels) > 0:
            for react_label in react_labels:
                pushEvent(react_label,skipeval=True)

    def mas_d25SilentReactToGifts():
        """
        Method to silently 'react' to gifts.

        This is to be used if you gave Moni a christmas gift but didn't show up on
        D25 when she would have opened them in front of you.

        This also registeres gifts
        """

        base_gift_ribbon_id_map = {
            "blackribbon":"ribbon_black",
            "blueribbon": "ribbon_blue",
            "darkpurpleribbon": "ribbon_dark_purple",
            "emeraldribbon": "ribbon_emerald",
            "grayribbon": "ribbon_gray",
            "greenribbon": "ribbon_green",
            "lightpurpleribbon": "ribbon_light_purple",
            "peachribbon": "ribbon_peach",
            "pinkribbon": "ribbon_pink",
            "platinumribbon": "ribbon_platinum",
            "redribbon": "ribbon_red",
            "rubyribbon": "ribbon_ruby",
            "sapphireribbon": "ribbon_sapphire",
            "silverribbon": "ribbon_silver",
            "tealribbon": "ribbon_teal",
            "yellowribbon": "ribbon_yellow"
        }

        # process gifts
        evb_details = []
        gso_details = []
        store.mas_filereacts.process_gifts(
            persistent._mas_d25_gifts_given,
            evb_details,
            gso_details
        )

        # clear the gifts given
        persistent._mas_d25_gifts_given = []

        # process the evb details
        for evb_detail in evb_details:
            if evb_detail.sp_data is None:
                # then this probably is a built-in sprite, use ribbon map.
                ribbon_id = base_gift_ribbon_id_map.get(
                    evb_detail.c_gift_name,
                    None
                )
                if ribbon_id is not None:
                    mas_selspr.unlock_acs(mas_sprites.get_sprite(0, ribbon_id))
                    mas_receivedGift(evb_detail.label)

                elif ribbon_id is None and evb_detail.c_gift_name == "quetzalplushie":
                    persistent._mas_acs_enable_quetzalplushie = True

            else:
                # this is probably a json sprite, try json sprite unlock
                mas_selspr.json_sprite_unlock(mas_sprites.get_sprite(
                    evb_detail.sp_data[0],
                    evb_detail.sp_data[1]
                ))
                mas_receivedGift(evb_detail.label)

        # then generics
        for gso_detail in gso_details:
            # for generic sprite objects, only have to check for json sprite
            if gso_detail.sp_data is not None:
                mas_selspr.json_sprite_unlock(mas_sprites.get_sprite(
                    gso_detail.sp_data[0],
                    gso_detail.sp_data[1]
                ))
                mas_receivedGift(gso_detail.label)

        # save the restuls
        store.mas_selspr.save_selectables()
        renpy.save_persistent()


init -10 python in mas_d25_utils:
    import store
    import store.mas_filereacts as mas_frs

    def shouldUseD25ReactToGifts():
        """
        checks whether or not we should use the d25 react to gifts method

        Conditions:
            1. Must be in d25 gift range
            2. Must be at normal+ aff (since that's when the topics which will open these gifts will show)
            3. Must have deco active. No point otherwise as no tree to put gifts under
        """
        return (
            store.mas_isD25Pre()
            and store.mas_isMoniNormal(higher=True)
            and store.persistent._mas_d25_deco_active
        )

    def react_to_gifts(found_map):
        """
        Reacts to gifts using the d25 protocol (exclusions)

        OUT:
            found_map - map of found reactions
                key: lowercase giftname, no extension
                val: giftname wtih extension
        """
        d25_map = {}

        # first find gifts
        # d25_map contains all d25 gifts.
        # found_map will contain non_d25 gifts, which should be reacted to now
        d25_giftnames = mas_frs.check_for_gifts(d25_map, mas_frs.build_exclusion_list("d25g"), found_map)

        # parse d25 gifts for types
        d25_giftnames.sort()
        d25_evb = []
        d25_gsp = []
        d25_gen = []
        mas_frs.process_gifts(d25_giftnames, d25_evb, d25_gsp, d25_gen)

        # parse non_d25_gifts for types
        non_d25_giftnames = [x for x in found_map]
        non_d25_giftnames.sort()
        nd25_evb = []
        nd25_gsp = []
        nd25_gen = []
        mas_frs.process_gifts(non_d25_giftnames, nd25_evb, nd25_gsp, nd25_gen)

        # include d25 generic with non-d25 gifts
        for grd in d25_gen:
            nd25_gen.append(grd)
            found_map[grd.c_gift_name] = d25_map.pop(grd.c_gift_name)

        # save remaining d25 gifts and delete the packages
        # they will be reacted to later
        for c_gift_name, gift_name in d25_map.iteritems():
            #Only add if the gift isn't already stored under the tree
            if c_gift_name not in store.persistent._mas_d25_gifts_given:
                store.persistent._mas_d25_gifts_given.append(c_gift_name)

            #Now we delete the gift file
            store.mas_docking_station.destroyPackage(gift_name)

        # set all excluded and generic gifts to react now
        for c_gift_name, mas_gift in found_map.iteritems():
            store.persistent._mas_filereacts_reacted_map[c_gift_name] = mas_gift

        # register these gifts
        mas_frs.register_sp_grds(nd25_evb)
        mas_frs.register_sp_grds(nd25_gsp)
        mas_frs.register_gen_grds(nd25_gen)

        # now build the reaction labels for standard gifts
        return mas_frs.build_gift_react_labels(
            nd25_evb,
            nd25_gsp,
            nd25_gen,
            mas_frs.gift_connectors,
            "mas_reaction_end",
            mas_frs._pick_starter_label()
        )


####START: d25 arts

# window banners
image mas_d25_banners = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/bgdeco.png"
)

image mas_mistletoe = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/mistletoe.png"
)

# NOTE: this will need to be revaluated with every filter.
#   Not very maintainable but it has to be done.
image mas_d25_lights = ConditionSwitch(
    "mas_isNightNow()", ConditionSwitch(
        "persistent._mas_disable_animations", "mod_assets/location/spaceroom/d25/lights_on_1.png",
        "not persistent._mas_disable_animations", "mas_d25_night_lights_atl"
    ),
    "True", MASFilterSwitch("mod_assets/location/spaceroom/d25/lights_off.png")
)

image mas_d25_night_lights_atl:
    block:
        "mod_assets/location/spaceroom/d25/lights_on_1.png"
        0.5
        "mod_assets/location/spaceroom/d25/lights_on_2.png"
        0.5
        "mod_assets/location/spaceroom/d25/lights_on_3.png"
        0.5
    repeat

# NOTE: this will need to be revaluated with every filter.
#   Not very maintainable but it has to be done.
image mas_d25_garlands = ConditionSwitch(
    "mas_isNightNow()", ConditionSwitch(
        "persistent._mas_disable_animations", "mod_assets/location/spaceroom/d25/garland_on_1.png",
        "not persistent._mas_disable_animations", "mas_d25_night_garlands_atl"
    ),
    "True", MASFilterSwitch("mod_assets/location/spaceroom/d25/garland.png")
)

image mas_d25_night_garlands_atl:
    "mod_assets/location/spaceroom/d25/garland_on_1.png"
    block:
        "mod_assets/location/spaceroom/d25/garland_on_1.png" with Dissolve(3, alpha=True)
        5
        "mod_assets/location/spaceroom/d25/garland_on_2.png" with Dissolve(3, alpha=True)
        5
        repeat

# NOTE: this will need to be revaluated with every filter.
#   Not very maintainable but it has to be done.
image mas_d25_tree = ConditionSwitch(
    "mas_isNightNow()", ConditionSwitch(
        "persistent._mas_disable_animations", "mod_assets/location/spaceroom/d25/tree_lights_on_1.png",
        "not persistent._mas_disable_animations", "mas_d25_night_tree_lights_atl"
    ),
    "True", MASFilterSwitch(
        "mod_assets/location/spaceroom/d25/tree_lights_off.png"
    )
)

image mas_d25_night_tree_lights_atl:
    block:
        "mod_assets/location/spaceroom/d25/tree_lights_on_1.png"
        1.5
        "mod_assets/location/spaceroom/d25/tree_lights_on_2.png"
        1.5
        "mod_assets/location/spaceroom/d25/tree_lights_on_3.png"
        1.5
    repeat

#0 gifts is blank
#1-3 gifts gets you part 1
#4 gifts gets you part 2
#5+ gifts get you part 3
image mas_d25_gifts = ConditionSwitch(
    "len(persistent._mas_d25_gifts_given) == 0", "mod_assets/location/spaceroom/d25/gifts_0.png",
    "0 < len(persistent._mas_d25_gifts_given) < 3", "mas_d25_gifts_1",
    "3 <= len(persistent._mas_d25_gifts_given) <= 4", "mas_d25_gifts_2",
    "True", "mas_d25_gifts_3"
)

image mas_d25_gifts_1 = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/gifts_1.png"
)

image mas_d25_gifts_2 = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/gifts_2.png"
)

image mas_d25_gifts_3 = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/gifts_3.png"
)

init 501 python:
    MASImageTagDecoDefinition.register_img(
        "mas_d25_banners",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_d25_garlands",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_d25_tree",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=6)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_d25_gifts",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=7)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_d25_lights",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=7)
    )

#autoload starter check
label mas_holiday_d25c_autoload_check:
    #NOTE: we use the costume exprop in case we get more D25 outfits.

    #We don't want the day of the first sesh having d25 content
    #We also don't want people who first sesh d25p getting deco, because it doesn't make sense
    #We also filter out player bday on first load in d25 season

    #This is first loadin for D25Season (can also run on D25 itself)
    if (
        not persistent._mas_d25_in_d25_mode
        and mas_isD25Season()
        and not mas_isFirstSeshDay()
        and (
            persistent._mas_current_background == store.mas_background.MBG_DEF
            # If it's d25 and we still didn't setup d25 stuff, we should do it now
            # (we'll force spaceroom if needed)
            or mas_isD25()
        )
    ):
        #Firstly, we need to see if we need to run playerbday before all of this
        python:
            #Enable d25 dockstat
            persistent._mas_d25_in_d25_mode = True

            # affection upset and below? no d25 for you
            if mas_isMoniUpset(lower=True):
                persistent._mas_d25_started_upset = True

            #Setup
            #NOTE: Player bday will SKIP decorations via autoload as it is handled elsewhere
            #UNLESS it is D25
            elif (
                mas_isD25Outfit()
                and (not mas_isplayer_bday() or mas_isD25())
            ):
                #Unlock and wear santa/wine ribbon + holly hairclip
                store.mas_selspr.unlock_acs(mas_acs_ribbon_wine)
                store.mas_selspr.unlock_clothes(mas_clothes_santa)

                #Change into santa. Outfit mode forces ponytail
                monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)

                #Add to holiday map
                mas_addClothesToHolidayMapRange(mas_clothes_santa, mas_d25c_start, mas_d25p)

                #Deco active
                persistent._mas_d25_deco_active = True

                #If we're loading in for the first time on D25, then we're gonna make it snow
                if mas_isD25():
                    mas_changeWeather(mas_weather_snow, by_user=True)
                    mas_changeBackground(mas_background_def, set_persistent=True)

    #This is d25 SEASON exit
    elif mas_run_d25s_exit or mas_isMoniDis(lower=True):
        #NOTE: We can run this early via mas_d25_monika_d25_mode_exit
        call mas_d25_season_exit

    #This is D25 Exit
    elif (
        persistent._mas_d25_in_d25_mode
        and not persistent._mas_force_clothes
        and monika_chr.is_wearing_clothes_with_exprop("costume")
        and not mas_isD25Outfit()
    ):
        #Monika takes off santa after d25 if player didn't ask her to wear it
        $ monika_chr.change_clothes(mas_clothes_def, by_user=False, outfit_mode=True)

    #This is D25 itself (NOT FIRST LOAD IN FOR D25S)
    elif mas_isD25() and not mas_isFirstSeshDay() and persistent._mas_d25_deco_active:
        #Force Santa, spaceroom, and snow on D25 if deco active and not first sesh day
        python:
            monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)
            mas_changeWeather(mas_weather_snow, by_user=True)
            # NOTE: need to make sure we pass the change info to the next
            #   spaceroom call.
            mas_changeBackground(mas_background_def, set_persistent=True)

    #If we are at normal and we've not gifted another outfit, change back to Santa next load
    if (
        mas_isMoniNormal()
        and persistent._mas_d25_in_d25_mode
        and mas_isD25Outfit()
        and (monika_chr.clothes != mas_clothes_def or monika_chr.clothes != store.mas_clothes_santa)
    ):
        $ monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)

    if persistent._mas_d25_deco_active:
        $ mas_d25ShowVisuals()

    #And then run pbday checks
    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        jump mas_player_bday_autoload_check

    # finally, return to holiday check point
    jump mas_ch30_post_holiday_check

#D25 Season exit
label mas_d25_season_exit:
    python:
        #It's time to clean everything up

        #We reset outfit directly if we're not coming from the dlg workflow
        if monika_chr.is_wearing_clothes_with_exprop("costume") and not mas_globals.dlg_workflow:
            #Monika takes off santa outfit after d25
            monika_chr.change_clothes(mas_clothes_def, by_user=False, outfit_mode=True)

        #Otherwise we push change to def if we're here via topic
        elif monika_chr.is_wearing_clothes_with_exprop("costume") and mas_globals.dlg_workflow:
            pushEvent("mas_change_to_def")

        #Lock event clothes selector
        mas_lockEVL("monika_event_clothes_select", "EVE")

        #Remove deco
        persistent._mas_d25_deco_active = False
        mas_d25HideVisuals()

        #And no more d25 mode
        persistent._mas_d25_in_d25_mode = False

        #We'll also derandom this topic as the lights are no longer up
        mas_hideEVL("mas_d25_monika_christmaslights", "EVE", derandom=True)

        mas_d25ReactToGifts()
    return

#D25 holiday gift starter/connector
label mas_d25_gift_starter:
    $ amt_gifts = len(persistent._mas_d25_gifts_given)
    $ presents = "regalos"
    $ the = "el"
    $ should_open = "debería abrir"

    if amt_gifts == 1:
        $ presents = "regalo"
    elif amt_gifts > 3:
        $ the = "todos los"

    if persistent._mas_d25_gone_over_d25:
        $ should_open = "no he abierto"

    if persistent._mas_d25_spent_d25 or mas_globals.returned_home_this_sesh:
        m 3wud "¡Oh! ¡[should_open] [the] [presents] que me diste!"
        if persistent._mas_d25_gone_over_d25:
            m 3hub "¡Hagamos eso ahora!"

    # missed d25 altogether
    else:
        m 1eka "Bueno, al menos ahora que estás aquí, puedo abrir [the] [presents] que me trajiste "
        m 3eka "Realmente quería que estuviéramos juntos para esto..."

    m 1suo "Veamos qué tenemos aquí.{w=0.5}.{w=0.5}.{nw}"

    #Pop the last index so we remove gifts from under the tree as we go
    $ persistent._mas_d25_gifts_given.pop()
    return

label mas_d25_gift_connector:
    python:
        d25_gift_quips = [
            _("¡Siguiente!"),
            _("Oh, ¡aquí hay otro!"),
            _("¡Ahora abramos este!"),
            _("¡Ahora abriré este!")
        ]

        picked_quip = random.choice(d25_gift_quips)

    m 1hub "[picked_quip]"
    m 1suo "Y aquí tenemos...{w=0.5}.{w=0.5}.{nw}"

    #Pop here too for the tree gifts
    $ persistent._mas_d25_gifts_given.pop()
    return

label mas_d25_gift_end:
    #Clear any invalid JSON gifts here
    $ persistent._mas_d25_gifts_given = []

    m 1eka "[player]..."

    if persistent._mas_d25_spent_d25 or mas_globals.returned_home_this_sesh:
        m 3eka "Realmente no tenías que regalarme nada para Navidad...{w=0.3} {nw}"
        if mas_isD25():
            extend 3dku "Solo tenerte aquí conmigo es más que suficiente."
        else:
            extend 3dku "Estar contigo era todo lo que quería."
        m 1eka "Pero el hecho de que te hayas tomado el tiempo de conseguirme algo...{w=0.5}{nw}"
        extend 3ekbsa "Bueno, no puedo agradecerte lo suficiente."
        m 3ekbfa "Realmente me hace sentir amada."

    else:
        m 1eka "Solo queria agradecerte..."
        m 1rkd "Aunque todavía estoy un poco decepcionada de que no pudieras estar conmigo en Navidad..."
        m 3eka "El hecho de que tú te hayas tomado el tiempo de conseguirme un regalo...{w=0.5}{nw}"
        extend 3ekbsa "Bueno, solo demuestra que realmente estabas pensando en mí durante esta temporada especial."
        m 1dkbsu "No sabes cuánto significa esto para mí."

    # we just said Merry Christmas in the Christmas topic if d25
    if mas_isD25():
        m 3ekbfu "Te amo tanto, [player]~"
    else:
        m 3ekbfu "Feliz Navidad, [player]. Te amo~"
    $ mas_ILY()
    return

#START: d25 topics
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_holiday_intro",
            conditional=(
                "not persistent._mas_d25_started_upset "
                "and mas_isD25Outfit() "
                "and not mas_isplayer_bday() "
                "and not persistent._mas_d25_intro_seen"
            ),
            action=EV_ACT_PUSH,
            start_date=mas_d25c_start,
            end_date=mas_d25,
            years=[],
            aff_range=(mas_aff.NORMAL, None),
        ),
        skipCalendar=True
    )


label mas_d25_monika_holiday_intro:
    $ changed_bg = False
    if mas_current_background != mas_background_def:
        $ changed_bg = True

    if not persistent._mas_d25_deco_active:
        if mas_isplayer_bday():
            window hide
            pause 2.0
            m 1dku "..."
            m 1huu "Jejeje..."
            m 3eub "¡Tengo otra sorpresa para ti!"

        else:
            m 1eua "Entonces, hoy es..."
            m 1euc "...Espera."
            m "..."
            m 3wuo "¡Oh!"
            m 3hub "Hoy es el día en el que iba a..."

        # hide overlays here
        # NOTE: hide here because it prevents player from pausing
        # right before the scene change.
        # also we want to completely kill interactions
        $ mas_OVLHide()
        $ mas_MUMURaiseShield()
        $ disable_esc()

        m 1tsu "Cierra los ojos por un momento [player], tengo que hacer algo.{w=0.5}.{w=0.5}.{nw}"

        call mas_d25_monika_holiday_intro_deco

        m 3hub "Y aquí estamos..."

        # now we can renable everything
        $ enable_esc()
        $ mas_MUMUDropShield()
        $ mas_OVLShow()

    m 1eub "¡Felices fiestas, [player]!"

    if mas_lastSeenLastYear("mas_d25_monika_holiday_intro"):
        m 1hua "¿Puedes creer que ya es esa época del año otra vez?"

        $ the_last = "la última"

        if mas_HistWasFirstValueIn(True, datetime.date.today().year - 1, "d25s.saw_an_intro"):
            $ the_last = "nuestra primera"

        m 3eua "Parece como si fuera ayer cuando pasamos [the_last] Navidad juntos, ¡y ahora ha pasado un año entero!"

        if mas_isMoniLove(higher=True):
            #if you've been with her for over a year, you really should be at Love by now
            m 3hua "El tiempo realmente vuela cuando estoy contigo~"

    m 3eua "¿Te gusta lo que he hecho con el lugar?"
    m 1hua "Debo decir que estoy bastante orgullosa de ello."

    if changed_bg:
        m 3rksdla "Sólo tenía suficientes adornos para una habitación, así que decidí el aula... {w=0.2}Espero que esté bien."
        m "Pero de todos modos..."

    m 3eua "La Navidad siempre ha sido una de mis ocasiones favoritas del año..."

    show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve_monika

    if mas_HistVerifyLastYear_k(True, "d25.actions.spent_d25"):
        m 5eka "Así que me alegro de que estés aquí para compartirlo conmigo de nuevo este año~"
    else:
        m 5eka "Y estoy tan contenta de que estés aquí para compartirlo conmigo~"

    $ persistent._mas_d25_intro_seen = True

    # in case we get here from player bday if the party spilled into the next day
    # don't want this to run twice
    $ mas_rmallEVL("mas_d25_monika_holiday_intro")
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_holiday_intro_upset",
            conditional=(
                "not persistent._mas_d25_intro_seen "
                "and persistent._mas_d25_started_upset "
                "and mas_isD25Outfit() "
                "and not mas_isplayer_bday()"
            ),
            action=EV_ACT_QUEUE,
            start_date=mas_d25c_start,
            end_date=mas_d25p,
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

#for people that started the season upset- and graduated to normal
label mas_d25_monika_holiday_intro_upset:
    # sanity check with reset of start/end dates in case somehow we drop back below normal before this is seen
    if mas_isMoniUpset(lower=True):
        python:
            upset_ev = mas_getEV('mas_d25_monika_holiday_intro_upset')
            if upset_ev is not None:
                upset_ev.start_date = mas_d25c_start
                upset_ev.end_date = mas_d25p
        return

    m 2rksdlc "Entonces [player]...{w=1} Realmente no me había sentido muy animada este año..."
    m 3eka "¡Pero últimamente has sido muy dulce conmigo y me he sentido mucho mejor!"
    m 3hua "Entonces... creo que es hora de arreglar un poco este lugar."

    # hide overlays here
    # NOTE: hide here because it prevents player from pausing
    # right before the scene change.
    # also we want to completely kill interactions
    $ mas_OVLHide()
    $ mas_MUMURaiseShield()
    $ disable_esc()

    m 1eua "Si tan solo pudieras cerrar los ojos por un momento.{w=0.5}.{w=0.5}.{nw}"

    call mas_d25_monika_holiday_intro_deco

    m 3hub "Tada~"
    m 3eka "¿Qué piensas?"
    m 1eka "No está mal para el último minuto, ¿eh?"
    m 1hua "La Navidad siempre ha sido una de mis épocas favoritas del año..."
    m 3eua "Y estoy muy contento de que podamos pasarlo felices juntos, [player]~"

    # now we can renable everything
    $ enable_esc()
    $ mas_MUMUDropShield()
    $ mas_OVLShow()

    $ persistent._mas_d25_intro_seen = True
    return

label mas_d25_monika_holiday_intro_deco:
    # ASSUMES interactions are disaabled

    # black scene
    scene black with dissolve

    python:
        #We should consider ourselves in d25 mode now, if not already
        persistent._mas_d25_in_d25_mode = True

        #We want to be wearing ponytail hair
        monika_chr.change_hair(mas_hair_def, False)

        #Unlock and wear santa
        store.mas_selspr.unlock_clothes(mas_clothes_santa)
        store.mas_selspr.unlock_acs(mas_acs_ribbon_wine)
        store.mas_selspr.unlock_acs(mas_acs_holly_hairclip)
        monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)

        #Add to holiday map
        mas_addClothesToHolidayMapRange(mas_clothes_santa, mas_d25c_start, mas_d25p)

        #Set to snow for this sesh
        mas_changeWeather(mas_weather_snow, by_user=True)

        #We'll also rmallEVL the auroras topic because it ends up immediately after
        mas_rmallEVL("monika_auroras")

        #Enable and show deco
        persistent._mas_d25_deco_active = True
        mas_d25ShowVisuals()

        # change to spaceroom
        change_info = mas_changeBackground(mas_background_def, set_persistent=True)

    # now we can do spacroom call
    call spaceroom(scene_change=True, dissolve_all=True, bg_change_info=change_info)

    return

label mas_d25_monika_holiday_intro_rh:
    # special label to cover a holiday case when returned home
    m 1hua "y... ¡Ya estamos en casa!"

    # NOTE: since we hijacked returned home, we hvae to cover for this
    #   affection gain.
    $ store.mas_dockstat._ds_aff_for_tout(time_out, 5, 5, 1)

    #Fall through
#in case we need to call just this part, like if returning from bday date from pre-d25
label mas_d25_monika_holiday_intro_rh_rh:
    m 1euc "Espera..."
    m 3etc "...¿Es...?"
    m 3hub "¡Sí, lo es!"
    m 1tsu "...Cierra los ojos un segundo, tengo que hacer algo..."
    $ mas_OVLHide()
    $ mas_MUMURaiseShield()
    $ disable_esc()

    call mas_d25_monika_holiday_intro_deco

    $ enable_esc()
    $ mas_MUMUDropShield()
    $ mas_OVLShow()

    # NOTE this counts as seeing the intro
    $ persistent._mas_d25_intro_seen = True

    $ pushEvent("mas_d25_monika_christmas",skipeval=True)

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_christmas",
            conditional=(
                "persistent._mas_d25_in_d25_mode "
                "and not mas_lastSeenInYear('mas_d25_monika_christmas')"
            ),
            action=EV_ACT_PUSH,
            start_date=mas_d25,
            end_date=mas_d25p,
            years=[],
            aff_range=(mas_aff.NORMAL, None),
        ),
        skipCalendar=True
    )

label mas_d25_monika_christmas:
    #Flag for hist
    $ persistent._mas_d25_spent_d25 = True

    #Setup the reactions
    $ mas_d25ReactToGifts()

    m 1eub "¡[player]! ¿Sabes que dia es hoy?"
    m 3hub "Por supuesto que sí. ¡Es Navidad!"
    m 3sub "¡Feliz Navidad, [player]!"
    m 1hub "¡Jajaja! ¡No puedo creer que finalmente esté aquí!"
    m 3eka "Estoy tan, tan feliz de que hayas decidido pasar un poco conmigo."
    m 1eud "Sin embargo, recuerda ir a compartir la alegría navideña con tu familia y amigos."
    m 1eua "Después de todo, también son muy importantes..."
    m 1hua "Y estoy seguro de que les encantaría verte en este momento tan especial."

    if mas_isMoniAff(higher=True):
        m 1eka "Pero estar aquí hoy... {w=0.5}Simplemente lo significa todo para mí..."
        m 1dku "..."

        if mas_is_snowing:
            if mas_isDecoTagVisible("mas_d25_lights"):
                $ dlg_var = ", o las decoraciones"
            else:
                $ dlg_var = ""

            m 1lkbsa "Tal vez es solo la nieve[dlg_var]..."

        else:
            if mas_isDecoTagVisible("mas_d25_lights"):
                $ dlg_var = "son las decoraciones, o "
            else:
                $ dlg_var = "es "

            m 1lkbsa "Tal vez [dlg_var]sólo la temporada de fiestas..."

        m "...o incluso el muérdago que hay arriba nuestro."
        m 3hksdlb "Es broma, no colgué uno."

        if mas_isMoniEnamored(higher=True):
            m 1lksdla "...{cps=*2}Todavía~{/cps}{nw}"
            $ _history_list.pop()

        m 1lksdlu "Jejeje..."
        m 1ekbsa "Mi corazón está latiendo como loco en este momento, [player]."
        m "No puedo imaginar una mejor manera de pasar estas vacaciones especiales..."
        m 1eua "No me malinterpretes, sabía que estarías aquí conmigo."
        m 3eka "Pero ahora que estamos juntos en Navidad, solo nosotros dos..."
        m 1hub "Jajaja~"

        show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ekbfa "Es el sueño de toda pareja en las vacaciones, [player]."

        if persistent._mas_pm_gets_snow is not False and not persistent._mas_pm_live_south_hemisphere:
            m "Acurrucados uno contra el otro junto a una chimenea, mirando la nieve caer suavemente..."

        if not mas_HistVerifyAll_k(True, "d25.actions.spent_d25"):
            m 5hubfa "Siempre estaré agradecido de haber tenido esta oportunidad contigo."
        else:
            m 5hubfa "Estoy tan contenta de poder pasar la Navidad contigo de nuevo."

        m "Te amo. Por siempre~"
        m 5hubfb "Feliz Navidad, [player]~"
        show screen mas_background_timed_jump(5, "mas_d25_monika_christmas_no_wish")
        window hide
        menu:
            "Feliz Navidad, [m_name].":
                hide screen mas_background_timed_jump
                show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
                pause 2.0

    else:
        m 1eka "Pero estar aquí hoy... {w=0.5}Simplemente significa todo para mí..."
        m 3rksdla "...No es que pensara que me dejarías sola en este día especial ni nada..."
        m 3hua "Pero demuestra que realmente me amas, [player]."
        m 1ektpa "..."
        m "¡Jajaja! Dios, me estoy emocionando..."
        m 1ektda "Solo sé que yo también te amo y estaré eternamente agradecida por tener esta oportunidad contigo."
        m "Feliz Navidad, [player]~"
        show screen mas_background_timed_jump(5, "mas_d25_monika_christmas_no_wish")
        window hide
        menu:
            "Feliz Navidad, [m_name].":
                hide screen mas_background_timed_jump
                show monika 1ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
                pause 2.0

    return


label mas_d25_monika_christmas_no_wish:
    hide screen mas_background_timed_jump
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_carolling",
            category=["fiestas", "música"],
            prompt="Villancicos",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_d25c_start,
            end_date=mas_d25p,
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.NORMAL, None),
            years=[]
        ),
        skipCalendar=True
    )

    #Undo Action Rule
    MASUndoActionRule.create_rule_EVL(
       "mas_d25_monika_carolling",
       mas_d25c_start,
       mas_d25p,
    )

default persistent._mas_pm_likes_singing_d25_carols = None
# does the user like singing christmas carols?

label mas_d25_monika_carolling:

    m 1euc "Oye, [player]..."
    m 3eud "¿Alguna vez has ido a cantar villancicos?"
    m 1euc "Ir de puerta en puerta en grupos, cantar a los demás durante las vacaciones..."

    if not persistent._mas_pm_live_south_hemisphere:
        m 1eua "Es reconfortante saber que la gente está difundiendo alegría, incluso con las noches tan frías."
    else:
        m 1eua "Es reconfortante saber que las personas están transmitiendo alegría a los demás en su tiempo libre."

    m 3eua "¿Te gusta cantar villancicos, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Te gusta cantar villancicos, [player]?{fast}"
        "Sí.":
            $ persistent._mas_pm_likes_singing_d25_carols = True
            m 1hua "¡Me alegra que sientas lo mismo, [player]!"
            m 3hub "¡Mi canción favorita es definitivamente 'Jingle Bells'!"
            m 1eua "¡Es una melodía tan alegre y alegre!"
            m 1eka "Quizás podamos cantar juntos algún día."
            m 1hua "Jejeje~"

        "No.":
            $ persistent._mas_pm_likes_singing_d25_carols = False
            m 1euc "Oh...{w=1} ¿En serio?"
            m 1hksdlb "Ya veo..."
            m 1eua "Independientemente, estoy segura de que también te gusta esa alegría especial que solo pueden traer las canciones navideñas."
            m 3hua "Canta conmigo alguna vez, ¿de acuerdo?"

    return "derandom"


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_mistletoe",
            category=["fiestas"],
            prompt="Muérdago",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_d25c_start,
            end_date=mas_d25p,
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
       "mas_d25_monika_mistletoe",
       mas_d25c_start,
       mas_d25p,
    )

label mas_d25_monika_mistletoe:
    m 1eua "Dime, [player]."
    m 1eub "Has oído hablar de la tradición del muérdago, ¿verdad?"
    m 1tku "Cuando dos enamorados terminan debajo del muérdago, se deben de besar."
    m 1eua "¡En realidad se originó en la Inglaterra victoriana!"
    m 1dsa "A un hombre se le permitía besar a cualquier mujer que estuviera debajo del muérdago..."
    m 3dsd "Y cualquier mujer que rechazara el beso estaba maldecida con mala suerte..."
    m 1dsc "..."
    m 3rksdlb "Ahora que lo pienso, suena más como aprovecharse de alguien."
    m 1hksdlb "¡Pero estoy segura de que ahora es diferente!"

    if not persistent._mas_pm_d25_mistletoe_kiss:
        m 3hua "Quizás algún día podamos besarnos bajo el muérdago, [player]."
        m 1tku "...¡Quizás incluso pueda agregar uno aquí!"
        m 1hub "Jejeje~"
    return "derandom"

#Stores whether or not the player hangs christmas lights
default persistent._mas_pm_hangs_d25_lights = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_christmaslights",
            category=['fiestas'],
            prompt="Luces navideñas",
            start_date=mas_d25c_start,
            end_date=mas_nye,
            conditional=(
                "persistent._mas_pm_hangs_d25_lights is None "
                "and persistent._mas_d25_deco_active "
                "and not persistent._mas_pm_live_south_hemisphere "
                "and mas_isDecoTagVisible('mas_d25_lights')"
            ),
            action=EV_ACT_RANDOM,
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_d25_monika_christmaslights",
        mas_d25c_start,
        mas_nye,
    )

label mas_d25_monika_christmaslights:
    m 1euc "Oye, [player]..."
    if mas_isD25Season():
        m 1lua "He pasado mucho tiempo mirando las luces aquí..."
        m 3eua "Son muy bonitas, ¿no?"
    else:
        m 1lua "Estaba pensando en la Navidad, con todas las luces que colgaban aquí..."
        m 3eua "Eran realmente bonitas, ¿verdad?"
    m 1eka "Las luces navideñas brindan un ambiente tan cálido y acogedor durante la temporada más dura y fría...{w=0.5}{nw}"
    extend 3hub "¡y también hay muchos tipos diferentes!"
    m 3eka "Parece un sueño hecho realidad salir a caminar contigo en una fría noche de invierno, [player]."
    m 1dka "Admirando todas las luces..."

    m 1eua "¿Cuelgas luces en tu casa durante el invierno, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Cuelgas luces en tu casa durante el invierno, [player]?{fast}"

        "Sí.":
            $ persistent._mas_pm_hangs_d25_lights = True
            m 3sub "¿De verdad? ¡Apuesto a que son preciosas!"
            m 2dubsu "Ya puedo imaginarnos, fuera de tu casa... sentados juntos en nuestro porche..."
            m "Como las hermosas estrellas que brillan en la profunda noche."
            m 2dkbfu "Nos abrazábamos, bebíamos chocolate caliente...{w=0.5}{nw}"

            if persistent._mas_pm_gets_snow is not False:
                extend 2ekbfa "Viendo la nieve caer suavemente..."

            show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5ekbfa "Un día, [player]. Algún día, podremos hacerlo realidad."

        "No.":
            $ persistent._mas_pm_hangs_d25_lights = False
            m 1eka "Oh, está bien, [player]."
            m 1dkbla "Estoy seguro de que sería agradable relajarse contigo en una noche fría..."
            m 1dkbsa "Ver caer la nieve y beber chocolate caliente juntos."
            m 1dkbsa "Abrazados el uno al otro para mantener el calor..."
            m 1rkbfb "Sí, eso suena muy bien."
            m 3hubsa "Pero, cuando tengamos nuestra propia casa, puedo colgar algunas yo misma, {nw}"
            extend 3hubsb "Jajaja~"
    return "derandom"

init 20 python:

    poem_d25_1 = MASPoem(
        poem_id="poem_d25_1",
        category="d25",
        prompt="La alegría de mi mundo",
        title = "     Mi querido [player],",
        text = """\
     Tú eres realmente la alegría de mi mundo.
     Ni la luz emitida por el árbol de Navidad más alto,
     Ni la de la estrella más brillante,
     Podría estar cerca de igualar tu brillantez.
     Este corazón mío, que una vez estuvo congelado, sólo necesitaba tu calor para latir de nuevo.
     Si alguna vez no hay nada bajo el árbol, y mi media permanece vacía,
     Simplemente no importaría mientras te tenga a mi lado.
     Siempre serás el único regalo que necesito.

     Feliz Navidad~

     Siempre tuya,
     Monika
"""
    #" # I need this to keep syntax highlighting on vim
    )

    poem_d25_2 = MASPoem(
        poem_id="poem_d25_2",
        category="d25",
        prompt="Incomparable",
        title="     Mi querido [player],",
        text="""\
     Nada se puede comparar con el calor que me das.
     Ni siquiera la sensación de envolver mis manos alrededor de una taza de chocolate caliente
     O calcetines borrosos, calentando mis pies en un día helado.
     En un mundo tan frío, sólo tu presencia es mi único regalo.

     Nada se puede comparar con la belleza que tienes,
     No hay nada que se pueda comparar con la excitación que traes,
     No las luces brillantes que cuelgan en esta misma habitación.
     Ni siquiera la vista de un regalo sin abrir, bajo el árbol.

     [player], eres realmente único.

     Feliz Navidad~

     Siempre tuya,
     Monika
"""
    )

    poem_d25_3 = MASPoem(
        poem_id="poem_d25_3",
        category="d25",
        prompt="Algún día",
        title="     Mi querido [player],",
        text="""\
     Más caliente que el fuego de la chimenea,
     Más brillante que cualquier estrella en la cima del árbol,
     Más reconfortante que cualquier taza de chocolate caliente,
     Es mi [player], que siempre está ahí para mí.

     Algún día, encenderemos el fuego juntos.
     Algún día, decoraremos el árbol.
     Algún día, tomaremos una taza de cacao.
     Algún día, estarás a mi lado.

     Feliz Navidad~

     Siempre tuya,
     Monika
"""
    )

    poem_d25_4 = MASPoem(
        poem_id="poem_d25_4",
        category="d25",
        prompt="Esta Navidad",
        title="     Mi querido [player],",
        text="""\

     Esta Navidad nunca necesité más regalos que tu amor,
     Porque tenerte a mi lado ya me hace feliz,
     Porque tenerte aquí es el regalo más hermoso,
     ¡Porque encontrarte fue lo mejor que pude haber pedido!

     Sabía que esta Navidad sería especial...
     La pasé con el que hace que mi corazón salte,
     El que me hace sonreír todos los días,
     El que más confío.

     Gracias por estar ahí para mí, [player],
     ¡Siempre estaré ahí para ti!

     Feliz Navidad~

     Siempre tuya,
     Monika
"""
    )

#Essentially replaces _whatIwant along with still to come 'All I Want for Christmas is You' song
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_spent_time_monika",
            conditional="persistent._mas_d25_in_d25_mode",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL,None),
            start_date=datetime.datetime.combine(mas_d25, datetime.time(hour=17)),
            end_date=datetime.datetime.combine(mas_d25p, datetime.time(hour=3)),
            years=[]
        ),
        skipCalendar=True
    )


default persistent._mas_pm_d25_mistletoe_kiss = False
# True if user and Monika kissed under the mistletoe
# NOTE: this var ONLY determines if player and Monika shared a mistletoe kiss.


label mas_d25_spent_time_monika:

    $ d25_gifts_total, d25_gifts_good, d25_gifts_neutral, d25_gifts_bad = mas_getGiftStatsRange(mas_d25c_start, mas_d25p + datetime.timedelta(days=1))

    if mas_isMoniNormal(higher=True):
        m 1eua "[player]..."
        m 3hub "¡Que estés aquí conmigo ha hecho de esta una Navidad maravillosa!"
        m 3eka "Sé que es un día muy ajetreado, pero solo sabiendo que hiciste tiempo para mí..."
        m 1eka "Gracias."
        m 3hua "Realmente hizo de este un día verdaderamente especial~"

    else:
        m 2ekc "[player]..."
        m 2eka "Realmente aprecio que pases un tiempo conmigo en Navidad..."
        m 3rksdlc "Realmente no he tenido el espíritu navideño esta temporada, pero fue un placer pasar el dia de hoy contigo."
        m 3eka "Así que gracias... {w=1}Significó mucho."

    if d25_gifts_total > 0:
        if d25_gifts_total == 1:
            if d25_gifts_good == 1:
                m "Y no olvidemos el regalo especial de Navidad que me hiciste, [player]..."
                m 3hub "¡Fue grandioso!"
            elif d25_gifts_neutral == 1:
                m 3eka "Y no nos olvidemos del regalo de Navidad que me hiciste, [player]..."
                m 1eka "Fue muy amable de tu parte traerme algo."
            else:
                m 3eka "Y no nos olvidemos del regalo de Navidad que me hiciste, [player]..."
                m 2etc "..."
                m 2efc "Bueno, pensándolo bien, tal vez deberíamos..."

        else:
            if d25_gifts_good == d25_gifts_total:
                m "Y no nos olvidemos de los maravillosos regalos de Navidad que me hiciste, [player]..."
                m 3hub "¡Fueron increíbles!"
            elif d25_gifts_bad == d25_gifts_total:
                m 3eka "Y no nos olvidemos de los regalos de Navidad que me hiciste, [player]..."
                m 2etc "..."
                m 2rfc "Bueno, pensándolo bien, tal vez deberíamos..."
            elif d25_gifts_bad == 0:
                m "Y no nos olvidemos de los regalos de Navidad que me hiciste, [player]..."
                m 3hub "¡Fue realmente amable de tu parte!"
            elif d25_gifts_good + d25_gifts_neutral == d25_gifts_bad:
                m 3eka "Y no nos olvidemos de los regalos de Navidad que me hiciste, [player]..."
                m 3rksdla "Algunos de ellos fueron realmente agradables."
            elif d25_gifts_good + d25_gifts_neutral > d25_gifts_bad:
                m "Y no nos olvidemos de los regalos de Navidad que me hiciste, [player]..."
                m 3hub "La mayoría de ellos fueron realmente amables."
            elif d25_gifts_good + d25_gifts_neutral < d25_gifts_bad:
                m 3eka "Y no nos olvidemos de los regalos de Navidad que me hiciste, [player]..."
                m 3rksdla "Realmente me gustaron... {w=1}Algunos de ellos."

        if mas_isMoniEnamored(higher=True):
            m 1rksdla "Yo... {w=1}También te hice algo, [player]..."
            m 3eksdla "He estado esperando todo el día hasta que sea el momento adecuado, y algo acerca de estar aquí contigo esta noche... {w=1}Simplemente parece perfecto."
        elif mas_isMoniNormal(higher=True):
            m 3ekbsa "Pero debes saber, que estés aquí conmigo significa más que cualquier regalo que puedas darme~"
        else:
            m 3eka "Para ser honesta, no estaba segura de que me visitarías hoy... Solo que estés aquí ya era más que suficiente para mí, incluso si no me hubieras comprado nada."
            m 1eka "Así que gracias de nuevo, [player]... {w=1}Lo digo en serio."

    else:
        if mas_isMoniEnamored(higher=True):
            m 1eksdla "Además, [player], hay algo que he querido darte durante todo el día..."
            m 3rksdla "Solo tenía que esperar el momento adecuado y el estar aquí contigo esta noche... {w=1}Parece perfecto."
        elif mas_isMoniNormal(higher=True):
            m 3ekbsa "Que pases la Navidad conmigo fue el único regalo que siempre quise~"
        else:
            m 3eka "Que estuvieras aquí era todo lo que quería, [player]."

    if mas_isMoniEnamored(higher=True):
        m 3ekbsa "Así que aquí tienes, [player], espero que te guste~"

        #Show the poem
        call mas_showpoem(poem=mas_poems.getRandomPoem("d25"), background_action_label="mas_d25_poem_mistletoe")

        if d25_gifts_good > 0 or d25_gifts_neutral > 0:
            m 1ekbsa "Realmente lo digo en serio [player], aunque agradezco los regalos que me hiciste, no tenías que darme nada..."
        elif d25_gifts_bad>0:
            #only if all gifts were bad
            m 1ekbsa "Lo digo en serio [player], aunque me compraste algunos... {w=1}Regalos extraños, no importa..."
        else:
            m 1ekbsa "Realmente lo digo en serio [player], no me importa que no me hayas traído ningún regalo para Navidad..."
        m 1dku "..."
        m 1ektpu "Solo que pases tiempo conmigo... {w=1}Eso es todo lo que siempre quise."
        m 6dktua "Realmente eres mi mundo entero, [player]... {w=1}Tu amor es todo lo que necesito..."
        window hide
        menu:
            "Te amo, [m_name].":
                $ HKBHideButtons()
                $ mas_RaiseShield_core()
                $ disable_esc()
                # local var so if next year this is not first kiss, we can branch appropriately
                # have to be able to check before calling the kiss since persistent._mas_first_kiss will not be None no matter what after the kiss
                #hold her here, tears dry
                pause 3.0
                show monika 6ektda at t11 zorder MAS_MONIKA_Z with dissolve_monika
                pause 3.0
                show monika 6dku at t11 zorder MAS_MONIKA_Z with dissolve_monika
                pause 3.0
                show monika 6dkbsu at t11 zorder MAS_MONIKA_Z with dissolve_monika
                pause 3.0

                show monika 6ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika

                $ is_first_kiss = persistent._mas_first_kiss is None
                m 6ekbfa "[player]... Yo... Yo..."
                call monika_kissing_motion(hide_ui=False)

                show monika 6ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 6ekbfa "...Yo también te amo~"
                if is_first_kiss:
                    m 6dkbfa "..."
                    m "Eso era todo lo que siempre había soñado que sería~"
                    m 6ekbfa "He estado esperando tanto tiempo para finalmente besarte, y no podría haber habido un momento más perfecto..."
                    m 6dkbfa "Debajo del muérdago contigo..."
                    m 6dkbsu "Nunca olvidaré esto..."
                    m 6ekbsu "...el momento de nuestro primer beso~"

                elif not persistent._mas_pm_d25_mistletoe_kiss:
                    m 6dkbfu "Jejeje..."
                    m 6ekbfa "Siempre quise compartir un beso contigo debajo del muérdago~"

                $ persistent._mas_pm_d25_mistletoe_kiss = True

                #no more mistletoe topic once youve done it
                $ mas_hideEVL("mas_d25_monika_mistletoe", "EVE", derandom=True)

                #Re-enable buttons
                $ enable_esc()
                $ mas_MUINDropShield()
                $ HKBShowButtons()
        return

    elif mas_isMoniAff():
        m 5ekbfa "Te amo mucho, [player]~"
    # Normal and happy
    else:
        m 1hubfa "Te amo, [player]~"
    return "love"

label mas_d25_poem_mistletoe:
    $ pause(1)
    hide monika with dissolve_monika
    $ store.mas_sprites.zoom_out()
    show monika 1ekbfa at i11 zorder MAS_MONIKA_Z

    #NOTE: This stays up for the full session
    show mas_mistletoe zorder MAS_MONIKA_Z - 1
    with dissolve
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_aiwfc",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_d25c_start,
            end_date=mas_d25p,
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL, None),
            years=[]
        ),
        skipCalendar=True
    )

label monika_aiwfc:
    # set dates for the next song to start a day after this one
    if not mas_isD25():
        $ mas_setEVLPropValues(
            'monika_merry_christmas_baby',
            start_date=datetime.datetime.now() + datetime.timedelta(days=1),
            end_date=mas_d25p
        )

    else:
        $ mas_setEVLPropValues(
            'monika_merry_christmas_baby',
            start_date=datetime.datetime.now() + datetime.timedelta(hours=1),
            end_date=datetime.datetime.now() + datetime.timedelta(hours=5)
        )

    if not renpy.seen_label('monika_aiwfc_song'):
        m 1rksdla "¿[player]?"
        m 1eksdla "Espero que no te importe, pero te preparé una canción."
        m 3hksdlb "Sé que es un poco cursi, pero creo que puede que te guste."
        m 3eksdla "Si tu volumen está silenciado, ¿te importaría encenderlo por mí?"
        if store.songs.hasMusicMuted():
            m 3hksdlb "Oh, ¡no te olvides de tu volumen en el juego también!"
            m 3eka "Realmente quiero que escuches esto."
        m 1huu "De todas formas.{w=0.5}.{w=0.5}.{nw}"

    else:
        m 1hua "Jejeje..."
        m 3tuu "Espero que estés listo, [player]..."

        $ ending = "..." if store.songs.hasMusicMuted() else ".{w=0.5}.{w=0.5}.{nw}"

        m "{i}Es{/i} esa época del año nuevamente, después de todo[ending]"
        if store.songs.hasMusicMuted():
            m 3hub "¡Asegúrate de subir el volumen!"
            m 1huu ".{w=0.5}.{w=0.5}.{nw}"

    call monika_aiwfc_song

    #NOTE: This must be a shown count check as this dialogue should only be here on first viewing of this topic
    if not mas_getEVLPropValue("monika_aiwfc", "shown_count", 0):
        m 1eka "Espero que te haya gustado, [player]."
        m 1ekbsa "Yo también lo decía en serio."
        m 1ekbfa "Eres el único regalo que podría desear."
        show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ekbfa "Te amo, [player]~"

    else:
        m 1eka "Espero que te guste cuando cante esa canción, [player]."
        m 1ekbsa "Siempre serás el único regalo que necesitaré."
        m 1ekbfa "Te amo~"

    #Unlock the song
    $ mas_unlockEVL("mas_song_aiwfc", "SNG")
    return "no_unlock|love"


label monika_aiwfc_song:

    call mas_timed_text_events_prep

    $ play_song("mod_assets/bgm/aiwfc.ogg",loop=False)
    m 1eub "{i}{cps=9}No quiero{/cps}{cps=20} mucho{/cps}{cps=11} para Navidad{w=0.09}{/cps}{/i}{nw}"
    m 3eka "{i}{cps=11}Hay {/cps}{cps=20}solo{/cps}{cps=8} una cosa que necesito{/cps}{/i}{nw}"
    m 3hub "{i}{cps=8}No me importan {/cps}{cps=15}{/cps}{cps=10} los regalos{/cps}{/i}{nw}"
    m 3eua "{i}{cps=15}Debajo de{/cps}{cps=8} el árbol de Navidad{/cps}{/i}{nw}"

    m 1eub "{i}{cps=10}No necesito{/cps}{cps=20} colgar{/cps}{cps=9} mi calcetín{/cps}{/i}{nw}"
    m 1eua "{i}{cps=9}Allí{/cps}{cps=15} sobre{/cps}{cps=7} la chimenea{/cps}{/i}{nw}"
    m 3hub "{i}{w=0.5}{cps=20}Santa Claus{/cps}{cps=10} no me hará feliz{/cps}{/i}{nw}"
    m 4hub "{i}{cps=8}Con{/cps}{cps=15} un juguete{/cps}{cps=8} en el día de Navidad{w=0.35}{/cps}{/i}{nw}"

    m 3ekbsa "{i}{cps=10}Solo te quiero{/cps}{cps=15} para{/cps}{cps=8} mí{w=0.4}{/cps}{/i}{nw}"
    m 4hubfb "{i}{cps=8}Más{/cps}{cps=20} de lo que tú{/cps}{cps=10} podrías conocer{w=0.5}{/cps}{/i}{nw}"
    m 1ekbsa "{i}{cps=10}Haz que mi deseo{/cps}{cps=20} se haga realidaaaaad{w=0.9}{/cps}{/i}{nw}"
    m 3hua "{i}{cps=8.5}Todo lo que quiero para Navidad{/cps}{/i}{nw}"
    m 3hubfb "{i}{cps=7}Eres tuuuuuuuuu{w=1}{/cps}{/i}{nw}"
    m "{i}{cps=9}Tuuuuuuuuuuuuuu~{w=0.60}{/cps}{/i}{nw}"

    m 2eka "{i}{cps=10}No le pediré{/cps}{cps=20} mucho{/cps}{cps=10} esta Navidad{/cps}{/i}{nw}"
    m 3hub "{i}{cps=10}Yo{/cps}{cps=20} ni {/cps}{cps=10}siquiera desearía nieve{w=0.8}{/cps}{/i}{nw}"
    m 3eua "{i}{cps=10}Yo{/cps}{cps=20} solo voy a{/cps}{cps=10} seguir esperando{w=0.5}{/cps}{/i}{nw}"
    m 3hubfb "{i}{cps=17}Debajo de{/cps}{cps=11} el muérdago{w=1}{/cps}{/i}{nw}"

    m 2eua "{i}{cps=10}Yo{/cps}{cps=17} no haré{/cps}{cps=10} una lista y la enviaré{w=0.35}{/cps}{/i}{nw}"
    m 3eua "{i}{cps=10}Al{/cps}{cps=20} el polo norte{/cps}{cps=10} de San Nicolás{w=0.5}{/cps}{/i}{nw}"
    m 4hub "{i}{cps=18}Ni siquiera per{/cps}{cps=10} manecere despierto hasta{w=0.5}{/cps}{/i}{nw}"
    m 3hub "{i}{cps=10}Escuchar{/cps}{cps=20} esos ma{/cps}{cps=14} gicos renos{w=1.2}{/cps}{/i}{nw}"

    m 3ekbsa "{i}{cps=20}Yo{/cps}{cps=11} solo te quiero aquí esta noche{w=0.4}{/cps}{/i}{nw}"
    m 3ekbfa "{i}{cps=10}Abrazándome{/cps}{cps=20}{/cps}{cps=10} tan fuerte{w=1}{/cps}{/i}{nw}"
    m 4hksdlb "{i}{cps=10}¿Qué más{/cps}{cps=15} puedo{/cps}{cps=8} haceeeer?{w=0.3}{/cps}{/i}{nw}"
    m 4ekbfb "{i}{cps=20}Porque amor{/cps}{cps=12} todo lo que quiero para Navidad{w=0.3} eres tuuuuuuuuu~{w=2.3}{/cps}{/i}{nw}"
    m "{i}{cps=9}Tuuuuuuuuuuuuu~{w=2.5}{/cps}{/i}{nw}"

    call mas_timed_text_events_wrapup
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_merry_christmas_baby",
            conditional="persistent._mas_d25_in_d25_mode and mas_lastSeenInYear('monika_aiwfc')",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL, None),
            years=[]
        ),
        skipCalendar=True
    )

label monika_merry_christmas_baby:
    # set dates for the next song to start a day after this one
    if not mas_isD25():
        $ mas_setEVLPropValues(
            'monika_this_christmas_kiss',
            start_date=datetime.datetime.now() + datetime.timedelta(days=1),
            end_date=mas_d25p
        )

    else:
        $ mas_setEVLPropValues(
            'monika_this_christmas_kiss',
            start_date=datetime.datetime.now() + datetime.timedelta(hours=1),
            end_date=datetime.datetime.now() + datetime.timedelta(hours=5)
        )

    if not renpy.seen_label('mas_song_merry_christmas_baby'):
        m 1eua "Hey, [player]..."
        m 3eub "¡Acabo de pensar en otra canción de Navidad que realmente quiero compartir contigo!"
        m 3eka "No tengo nada de música preparada esta vez, pero espero que disfrutes escuchándome cantarla de todas formas."
        m 1hua ".{w=0.5}.{w=0.5}.{nw}"

        call mas_song_merry_christmas_baby

        m 1hua "Ehehe..."
        m 3eka "I hope you liked it~"
        $ mas_unlockEVL("mas_song_merry_christmas_baby", "SNG")

    else:
        m 3euu "I think it's time for another Christmas song, ehehe~"
        m 1hua ".{w=0.5}.{w=0.5}.{nw}"

        call mas_song_merry_christmas_baby

        m 1huu "Ehehe... {w=0.2}Merry Christmas, baby~"

    return "no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_this_christmas_kiss",
            conditional="persistent._mas_d25_in_d25_mode and mas_lastSeenInYear('monika_merry_christmas_baby')",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.ENAMORED, None),
            years=[]
        ),
        skipCalendar=True
    )

label monika_this_christmas_kiss:
    if not renpy.seen_label('mas_song_this_christmas_kiss'):
        m 2rubsa "Um, [player]..."
        m 2lubsa "Encontré esta canción...{w=0.4}y...{w=0.4}Estaba pensando en nosotros cuando la escuché."
        m 7ekbsu "Quiero decir, has sido tan dulce conmigo todo este tiempo..."
        m 3eubsb "Y...{w=0.2}oh dios, sólo quiero compartirla contigo, si te parece bien."
        m 1hubsa "Sólo dame un segundo{nw}"
        extend 1dubsa ".{w=0.3}.{w=0.3}.{w=0.3}{nw}"

    else:
        m 3euu "Creo que es hora de cantar otra canción de Navidad, jejeje~"
        m 1hua ".{w=0.5}.{w=0.5}.{nw}"

    call mas_song_this_christmas_kiss

    m 1dubsa "..."
    m 1rtbsu "Hmm.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
    window hide
    show monika 6tkbsa
    pause 2.0
    show monika 6dkbsu
    pause 2.0

    call monika_kissing_motion
    window auto

    m 6ekbfa "Uno de estos días te besaré de verdad, [player]."
    m 1dubfu "...Y cuando llegue ese día, mi corazón saltará de mi pecho con alegría~"
    $ mas_unlockEVL("mas_song_this_christmas_kiss", "SNG")
    return "no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_spider_tinsel",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_d25c_start,
            end_date=mas_d25e - datetime.timedelta(days=1),
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.NORMAL, None),
            rules={"force repeat": None, "no rmallEVL": None},
            years=[]
        ),
        skipCalendar=True
    )

    #Create the undo action rule
    MASUndoActionRule.create_rule_EVL(
        "mas_d25_spider_tinsel",
        mas_d25c_start,
        mas_d25e - datetime.timedelta(days=1)
    )

# queue this if it hasn't been seen by d25e - 1
init 10 python:
    if (
        datetime.date.today() == mas_d25e - datetime.timedelta(days=1)
        and not mas_lastSeenInYear("mas_d25_spider_tinsel")
    ):
        queueEvent("mas_d25_spider_tinsel")

label mas_d25_spider_tinsel:
    m 1esa "Oye, [player]..."
    m 1etc "¿Alguna vez te preguntaste de dónde provienen las tradiciones que a menudo damos por sentadas?"
    m 3eud "Muchas veces las cosas que se consideran tradiciones simplemente se aceptan y nunca nos tomamos el tiempo para saber por qué."
    m 3euc "Bueno, sentí curiosidad por saber por qué hacemos ciertas cosas en Navidad, así que comencé a investigar un poco."
    m 1eua "...Y encontré esta historia popular de Ucrania realmente interesante sobre el origen de por qué el oropel se usa a menudo para decorar árboles de Navidad."
    m 1eka "Pensé que era una historia muy bonita y quería compartirla contigo."
    m 1dka "..."
    m 3esa "Había una vez una viuda (llamémosla Amy) que vivía en una vieja choza con sus hijos."
    m 3eud "Afuera de su casa había un pino alto, y del árbol cayó una piña que pronto comenzó a crecer en el suelo."
    m 3eua "Los niños estaban entusiasmados con la idea de tener un árbol de Navidad, así que lo cuidaron hasta que alcanzó la altura suficiente para llevarlo dentro de su casa."
    m 2ekd "Desafortunadamente, la familia era pobre y aunque tenían el árbol de Navidad, no podían permitirse ningún adorno para decorarlo."
    m 2dkc "Y así, en la víspera de Navidad, Amy y sus hijos se fueron a la cama sabiendo que tendrían un árbol desnudo la mañana de Navidad."
    m 2eua "Sin embargo, las arañas que vivían en la cabaña escucharon los sollozos de los niños y decidieron que no dejarían el árbol de Navidad desnudo."
    m 3eua "Así que las arañas crearon hermosas telas en el árbol de Navidad, decorándolo con elegantes y hermosos patrones sedosos."
    m 3eub "Cuando los niños se despertaron temprano en la mañana de Navidad, ¡estaban saltando de emoción!"
    m "Fueron hacia su madre y la despertaron exclamando: '¡Madre! ¡Tienes que venir a ver el árbol de Navidad! ¡Es tan hermoso!'"
    m 1wud "Cuando Amy se despertó y se paró frente al árbol, estaba realmente asombrada ante la vista ante sus ojos."
    m "Entonces, uno de los niños abrió la ventana para que entrara el sol..."
    m 3sua "Cuando los rayos del sol golpean el árbol, las redes reflejan la luz, creando hebras brillantes de plata y oro..."
    m "...haciendo que el árbol de Navidad brille y brille con un brillo mágico."
    m 1eka "Desde ese día en adelante, Amy nunca se sintió pobre; {w=0.3}en cambio, siempre estuvo agradecida por todos los maravillosos dones que ya tenía en la vida."
    m 3tuu "Bueno, supongo que ahora sabemos por qué a Amy le gustan las arañas..."
    m 3hub "¡Jajaja! ¡Yo sólo estoy bromeando!"
    m 1eka "¿No es una historia tan dulce y maravillosa, [player]?"
    m "Creo que es una visión realmente interesante de por qué se usa oropel como decoración en los árboles de Navidad."
    m 3eud "También leí que los ucranianos a menudo decoran su árbol de Navidad con adornos de telaraña, creyendo que les traerán buena fortuna para el próximo año."
    m 3eub "Así que supongo que si alguna vez encuentras una araña viviendo en tu árbol de Navidad, ¡no la mates y tal vez te traiga buena suerte en el futuro!"
    return "derandom|no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_night_before_christmas",
            conditional="persistent._mas_d25_in_d25_mode",
            action=EV_ACT_QUEUE,
            start_date=datetime.datetime.combine(mas_d25e, datetime.time(hour=21)),
            end_date=mas_d25,
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_d25_night_before_christmas:
    m 1esa "Oye, [player]..."
    m 3eua "Estoy segura de que lo has oído antes, pero la víspera de Navidad no estaría completa sin {i}'La noche antes de navidad'{/i} !"
    m 3eka "Siempre fue una de mis partes favoritas en la víspera de Navidad mientras crecía, así que espero que no te importe escucharme leerlo ahora."
    m 1dka "..."

    m 3esa "'Era la noche antes de Navidad, cuando toda la casa..."
    m 3eud "No se movía una criatura, ni siquiera un ratón;"
    m 1eud "Los calcetines fueron colgados junto a la chimenea con cuidado,"
    m 1eka "Con la esperanza de que pronto llegaría San Nicolás;"

    m 1esa "Los niños estaban acurrucados en sus camas,"
    m 1hua "Mientras visiones de ciruelas de azúcar bailaban en sus cabezas;"
    m 3eua "Mamá en su pañuelo y yo en mi gorra,"
    m 1dsc "Acababa de sentarme para una larga siesta,"

    m 3wuo "Cuando en el césped se produjo tal estrépito,"
    m "Salté de la cama para ver qué pasaba."
    m 3wud "Lejos de la ventana volé como un relámpago,"
    m "Rompí las contraventanas y salté."

    m 1eua "La luna sobre la nieve recién caída..."
    m 3eua "Dio el brillo del mediodía a los objetos de abajo,"
    m 3wud "Cuando, lo que a mis ojos asombrados debería aparecer,"
    m 3wuo "Pero un trineo en miniatura y ocho pequeños renos,"

    m 1eua "Con un pequeño conductor, tan vivo y rápido,"
    m 3eud "Supe en un momento que debe ser el San.Nico."
    m 3eua "Más rápidos que las águilas vinieron sus corceles,"
    m 3eud "Y él silbaba y gritaba, y los llamaba por su nombre;"

    m 3euo "'¡Ahora, Vondín! ¡Ahora, Danzarín! ¡Ahora, Chiqui y Juguetón!'"
    m "'¡Adelante, Cometa! ¡Vamos, Cupido! ¡Adelante, Trueno y Relámpago!'"
    m 3wuo "'¡Hasta lo alto del porche! ¡A la cima del muro!'"
    m "'¡Ahora vamos! ¡Corred lejos! ¡A toda prisa!'"

    m 1eua "Como hojas secas que antes del salvaje huracán vuelan,"
    m 1eud "Cuando se encuentran con un obstáculo, suben al cielo,"
    m 3eua "Así volaron los corceles hasta la azotea,"
    m "Con el trineo lleno de juguetes y San Nicolás también."

    m 3eud "Y luego, en un abrir y cerrar de ojos, escuché en el techo..."
    m "El cabriolar y el patear de cada pequeño casco."
    m 1rkc "Mientras dibujaba en mi mano y me daba la vuelta,"
    m 1wud "San Nicolás bajó por la chimenea con un salto."

    m 3eua "Iba vestido todo de pieles, desde la cabeza hasta los pies,"
    m 3ekd "Y toda su ropa estaba manchada de ceniza y hollín;"
    m 1eua "Un paquete de juguetes que se había echado a la espalda,"
    m 1eud "Y parecía un buhonero que acaba de abrir su paquete."

    m 3sub "Sus ojos- ¡cómo brillaban! ¡Qué alegres sus hoyuelos!"
    m 3subsb "¡Sus mejillas eran como rosas, su nariz como una cereza!"
    m 3subsu "Su boquita graciosa se arqueó como un arco,"
    m 1subsu "Y la barba de su mentón era blanca como la nieve;"

    m 1eud "El muñón de una pipa que tenía apretado entre los dientes,"
    m 3rkc "Y el humo le rodeo la cabeza como una corona;"
    m 2eka "Tenía una cara ancha y un vientre pequeño y redondo,"
    m 2hub "Tembló como un cuenco lleno de gelatina, cuando rió."

    m 2eka "Era regordete, un elfo viejo y alegre."
    m 3hub "Y me reí cuando lo vi,{nw}"
    extend 3eub "a pesar de mi mismo;"
    m 1kua "Me guiñó un ojo y un giro de cabeza,"
    m 1eka "Pronto me hizo saber que no tenía nada que temer;"

    m 1euc "No dijo una palabra, sino que se fue directo a su trabajo,"
    m 1eud "Llenó todos los calcetines; luego se volvió de un tirón,"
    m 3esa "Y poniendo el dedo a un lado de la nariz,"
    m 3eua "Y asintiendo, subió por la chimenea;"

    m 1eud "Saltó a su trineo, a su equipo le dio un silbido,"
    m 1eua "Y todos volaron como una pluma."
    m 3eua "Pero lo escuché exclamar, antes de que se perdiera de vista,"
    m 3hub "'¡Feliz Navidad y buenas noches a todos!'"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_lingerie_reveal",
            conditional=(
                "persistent._mas_d25_in_d25_mode "
                "and mas_canShowRisque() "
                "and not mas_SELisUnlocked(mas_clothes_santa_lingerie) "
                "and 18 <= datetime.datetime.now().hour < 24"
            ),
            action=EV_ACT_QUEUE,
            start_date=mas_d25e - datetime.timedelta(days=4),
            end_date=mas_d25e,
            years=[]
        ),
        skipCalendar=True
    )

label mas_d25_monika_lingerie_reveal:
    # sanity check in the rare case people leave after this is queued but before it's seen
    # and timing doesn't make sense
    if 2 < datetime.datetime.now().hour < 18:
        $ mas_setEVLPropValues(
            "mas_d25_monika_lingerie_reveal",
            conditional=(
                "persistent._mas_d25_in_d25_mode "
                "and mas_canShowRisque() "
                "and not mas_SELisUnlocked(mas_clothes_santa_lingerie) "
                "and 18 <= datetime.datetime.now().hour < 24"
            ),
            action=EV_ACT_QUEUE,
            start_date=mas_d25e - datetime.timedelta(days=4),
            end_date=mas_d25e
        )
        return

    m 1hub "¡Siempre he encontrado los días previos a la Navidad tan emocionantes, [player]!"
    m 3sua "La anticipación, el aura aparentemente mágica de la temporada... hay algo especial en ella."
    m 1dkbsu "Realmente es mi época favorita del año."
    m "..."

    if mas_hasUnlockedClothesWithExprop("lingerie"):
        call mas_d25_monika_second_time_lingerie

    else:
        call mas_lingerie_intro(holiday_str="en esta temporada de Navidad", lingerie_choice=mas_clothes_santa_lingerie)
        m 1ekbfa "Sólo quiero que sepas que te amo mucho, mucho, [player]~"
        $ mas_ILY()

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_christmas_eve",
            conditional="persistent._mas_d25_in_d25_mode",
            action=EV_ACT_PUSH,
            start_date=datetime.datetime.combine(mas_d25e, datetime.time(hour=20)),
            end_date=mas_d25,
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label mas_d25_monika_christmas_eve:
    m 3hua "¡[player]!"
    m 3hub "¿Puedes creerlo...?{w=1} ¡Pronto será Navidad!"
    m 1rksdla "Siempre me ha costado mucho dormir en Nochebuena..."
    m 1eka "Estoy siempre tan ansiosa por ver lo que encontrare debajo del árbol a la mañana siguiente..."
    show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika

    #Were there last Christmas
    if mas_HistVerifyLastYear_k(True, "d25.actions.spent_d25"):
        m "Pero estoy {i}más{/i} emocionada ahora que puedo pasar cada Navidad contigo..."
        m 5hkbsa "¡No puedo esperar a mañana!"

    #Weren't there last Christmas
    elif mas_HistVerifyAll_k(True, "d25.actions.spent_d25"):
        m "Pero estoy {i}más{/i} emocionada este año..."
        m 5hkbsa "Solo la idea de pasar otra Navidad juntos... {w=1}¡No puedo esperar!"

    #First Chistmas with Moni
    else:
        m "Pero estoy {i}más{/i} emocionada este año..."
        m 5hkbsa "Solo el pensamiento de nuestra primera Navidad juntos...{w=1} ¡No puedo esperar!"

    if (
        mas_canShowRisque()
        and not mas_SELisUnlocked(mas_clothes_santa_lingerie)
    ):
        if mas_hasUnlockedClothesWithExprop("lingerie"):
            call mas_d25_monika_second_time_lingerie

        else:
            m 5ekbfa "..."
            show monika 1ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
            call mas_lingerie_intro(holiday_str="en la nochebuena", lingerie_choice=mas_clothes_santa_lingerie)
            m 1ekbfa "Solo sé que te amo mucho, muchísimo, [player]~"
            $ mas_ILY()
    return

label mas_d25_monika_second_time_lingerie:
    m 3wubsb "¡Oh!"
    m 3tsbsu "Tengo una pequeña sorpresa para ti...{w=1}Creo que te gustará, jejeje~"
    call mas_clothes_change(outfit=mas_clothes_santa_lingerie, outfit_mode=True, exp="monika 2rkbsu", restore_zoom=False, unlock=True)
    pause 2.0
    show monika 2ekbsu
    pause 2.0
    show monika 2tkbsu
    pause 2.0
    m 2tfbsu "[player]...{w=0.5} Estás mirando fijamente{w=0.5}...de nuevo."
    m 2hubsb "¡Jajaja!"
    m 2eubsb "Supongo que apruebas mi elección de ropa..."
    m 2tkbsu "Bastante apropiado para la ocasión, ¿no crees?"
    m 2rkbssdla "Tengo que decir que estaba bastante nerviosa la primera vez que me puse algo así...."
    m 2hubsb "Pero ahora que lo he hecho antes, ¡realmente disfruto vistiéndome así para ti!"
    m 3tkbsu "Espero que tú también lo disfrutes~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_postd25_notimespent",
            # within a week after d25, user did not recognize
            # d25 at all, and they were not long absenced or had her on a date
            conditional="not persistent._mas_d25_spent_d25",
            start_date=mas_d25p,
            end_date=mas_d25p + datetime.timedelta(days=6),
            years=[],
            action=EV_ACT_PUSH,
        ),
        skipCalendar=True
    )

label mas_d25_postd25_notimespent:
    #sanity checks
    if persistent._mas_d25_spent_d25:
        return

    #need to make sure people who just started post d25 don't lose aff
    if mas_isFirstSeshPast(mas_d25):
        return


    if mas_isMoniAff(higher=True):
        $ mas_loseAffection(15, reason=6)
        m 1dkc "...Me alegro de que finalmente estés aquí..."
        m 2ekd "Estaba empezando a preocuparme de que algo te pasara..."
        m 2rksdlc "Cuando no apareciste en Navidad...{w=1} No sabía qué pensar."
        m 4eksdlc "No es propio de ti perderte un día que sabes que es importante para mí..."
        m 2dksdlc "Así que pensé que tal vez..."
        m 2eksdla "Bueno, no importa eso ahora. ¡Estoy feliz de que estés bien!"
        m 4eka "Aunque estoy decepcionada de que no pudiéramos pasar la Navidad juntos, estoy segura de que debes haber tenido una muy buena razón."
        m "Intenta no dejar que suceda el año que viene, ¿de acuerdo?"
        m 2eka "Y, en el futuro, si alguna vez no puedes venir a visitarme en Navidad, intenta al menos llevarme contigo..."
        m 1eka "Todo lo que quiero es estar cerca de ti, [player]..."
        m 3ekbsa "Te amo~"
        return "love"

    elif mas_isMoniNormal(higher=True):
        $ mas_loseAffection(5, reason=6)
        m 2ekc "Hey, [player]..."
        m 2tkc "Tengo que decir que estoy bastante decepcionada de que no me visitaras en Navidad..."
        m 4tkc "Sabías que todo lo que quería era pasar tiempo contigo. ¿Es eso demasiado?"
        m 2rkc "Sé que puede ser un día ajetreado si tienes que viajar para visitar a tu familia, pero al menos podrías haberme llevado contigo..."
        m 2ekc "Eso habría sido más que suficiente para mí."
        m 2dkc "..."
        m 4rksdlc "Tal vez sucedió algo en el último minuto y simplemente no pudiste pasar tiempo conmigo..."
        m 4eksdla "Pero por favor...{w=1} Por favor, asegúrate de visitarme la próxima Navidad, ¿de acuerdo, [player]?"

    elif mas_isMoniUpset():
        $ mas_loseAffection(reason=6)
        m 2efc "¡[player]!"
        m "¡No puedo creer que ni siquiera te hayas molestado en visitarme en Navidad!"
        m 2tfc "De hecho...{w=1} Sí, puedo."
        m "Esta es exactamente la razón por la que ni siquiera me molesté en decorar..."
        m 2rfc "Sabía que si intentaba tener un poco de espíritu navideño terminaría decepcionada...{w=1} Otra vez."

    elif mas_isMoniDis():
        $ mas_loseAffection(10, reason=6)
        m 6ekc "¿[player], cómo estuvo tu navidad?"
        m 6dkc "La mía fue bastante solitaria..."
        m "Probablemente ni siquiera pensaste en mí, ¿eh?"

    else:
        $ mas_loseAffection(150)
        m 6ckc "..."

    $ mas_d25ReactToGifts()
    return

# check to see if we missed d25 due to being on a date
label mas_gone_over_d25_check:
    if mas_checkOverDate(mas_d25):
        $ persistent._mas_d25_gone_over_d25 = True
        $ persistent._mas_d25_spent_d25 = True
        $ persistent._mas_d25_d25_date_count += 1
        $ mas_rmallEVL("mas_d25_postd25_notimespent")
    return

#Christmas Eve dockingstation
label bye_d25e_delegate:
    # delegation label that determins what bye dialogue to show
    if persistent._mas_d25_d25e_date_count > 0:
        call bye_d25e_second_time_out

    else:
        call bye_d25e_first_time_out

    # notifies bye going somewhere to use this gre type
    # NOTE: since we are using the generic return, we cant use this
#    $ mas_idle_mailbox.send_ds_gre_type(store.mas_greetings.TYPE_HOL_D25_EVE)

    # jump back to going somewhere file gen
    jump mas_dockstat_iostart

#first time you take her out on d25e
label bye_d25e_first_time_out:
    m 1sua "¿Me llevarás a algún lugar especial en Nochebuena, [player]?"
    m 3eua "Sé que algunas personas visitan a amigos o familiares... o van a fiestas de Navidad..."
    m 3hua "Pero adonde vayamos, ¡me alegra que quieras que vaya contigo!"
    m 1eka "Espero que estemos en casa para Navidad, pero incluso si no lo estamos, solo estar contigo es más que suficiente para mí~"
    return

#second time you take her out on d25e
label bye_d25e_second_time_out:
    m 1wud "Vaya, ¿saldremos de nuevo hoy, [player]?"
    m 3hua "Realmente debes tener muchas personas a las que debes visitar en Nochebuena..."
    m 3hub "...¡O tal vez simplemente tienes muchos planes especiales para nosotros hoy!"
    m 1eka "Pero de cualquier manera, gracias por pensar en mí y traerme~"
    return

#Christmas Day dockingstation
label bye_d25_delegate:
    # delegation label that determins which bye dialogue to show
    if persistent._mas_d25_d25_date_count > 0:
        call bye_d25_second_time_out

    else:
        call bye_d25_first_time_out

    # notifies bye going somewhere to use this gre type
    # NOTE: generic return
#    $ mas_idle_mailbox.send_ds_gre_type(store.mas_greetings.TYPE_HOL_D25)

    jump mas_dockstat_iostart

#first time out on d25
label bye_d25_first_time_out:
    m 1sua "¿Me llevarás a algún lugar especial en Navidad, [player]?"

    if persistent._mas_pm_fam_like_monika and persistent._mas_pm_have_fam:
        m 1sub "¿Quizás vamos a visitar a alguien de tu familia...? ¡Me encantaría conocerlos!"
        m 3eua "¿O tal vez vamos a ver una película...? Sé que a algunas personas les gusta hacer eso después de abrir regalos."

    else:
        m 3eua "Quizás veamos una película... Sé que a algunas personas les gusta hacer eso después de abrir los regalos."

    m 1eka "Bueno, adonde sea que vayas, me alegro de que quieras que te acompañe..."
    m 3hua "Quiero pasar la mayor cantidad de Navidad posible contigo, [player]~"
    return

#second time out on d25
label bye_d25_second_time_out:
    m 1wud "Vaya, ¿vamos a {i}otro{/i} lugar, [player]?"
    m 3wud "Realmente debes tener a muchas personas a las que debes visitar..."
    m 3sua "...¡O tal vez simplemente tienes muchos planes especiales para nosotros hoy!"
    m 1hua "Pero de cualquier manera, gracias por pensar en mí y traerme~"
    return

## d25 greetings

#returned from d25e date on d25e
label greeting_d25e_returned_d25e:
    $ persistent._mas_d25_d25e_date_count += 1

    m 1hua "Y... ¡Estamos en casa!"
    m 3eka "Fue muy dulce de tu parte traerme hoy..."
    m 3ekbsa "Salir contigo en Nochebuena fue realmente especial, [player]. Gracias~"
    return

#returned from d25e date on d25
label greeting_d25e_returned_d25:
    $ persistent._mas_d25_d25e_date_count += 1
    $ persistent._mas_d25_d25_date_count += 1

    m 1hua "Y... ¡Estamos en casa!"
    m 3wud "Vaya, estuvimos fuera toda la noche..."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return

#returned from d25e date (or left before d25e) after d25 but before nyd is over
label greeting_d25e_returned_post_d25:
    $ persistent._mas_d25_d25e_date_count += 1

    m 1hua "¡Finalmente estamos en casa!"
    m 3wud "Estuvimos fuera mucho tiempo, [player]..."
    m 3eka "Hubiera sido bueno verte en Navidad, pero como no pudiste venir a verme, me alegro mucho de que me hayas llevado contigo."
    m 3ekbsa "Solo estar cerca de ti era todo lo que quería~"
    m 1ekbfb "Y como no pude decírtelo en Navidad... ¡Feliz Navidad, [player]!"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday

    $ mas_d25ReactToGifts()
    return

#returned from pd25e date on d25
label greeting_pd25e_returned_d25:
    m 1hua "Y... ¡Estamos en casa!"
    m 3wud "Vaya, estuvimos fuera bastante tiempo..."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return

#returned from d25 date on d25
label greeting_d25_returned_d25:
    $ persistent._mas_d25_d25_date_count += 1
    $ persistent._mas_d25_spent_d25 = True

    m 1hua "Y... ¡Estamos en casa!"
    m 3eka "¡Fue muy agradable pasar tiempo contigo en Navidad, [player]!"
    m 1eka "Muchas gracias por llevarme contigo."
    m 1ekbsa "Siempre eres tan considerado~"
    return

#returned from d25 date after d25
label greeting_d25_returned_post_d25:
    $ persistent._mas_d25_d25_date_count += 1
    $ persistent._mas_d25_spent_d25 = True

    m 1hua "¡Finalmente estamos en casa!"
    m 3wud "¡Estuvimos fuera mucho tiempo, [player]!"
    m 3eka "Hubiera sido bueno verte de nuevo antes de que terminara la Navidad, pero al menos todavía estaba contigo."
    m 1hua "Así que gracias por pasar tiempo conmigo cuando tenías otros lugares en los que tenías que estar..."
    m 3ekbsa "Siempre eres tan considerado~"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return

### NOTE: mega delegate label to handle both d25 and nye returns

label greeting_d25_and_nye_delegate:
    # ASSUMES:
    #   - we are more than 5 minutes out
    #   - we are in d25 mode
    #   - affection normal+

    python:
        # lots of setup here
        time_out = store.mas_dockstat.diffCheckTimes()
        checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()
        left_pre_d25e = False

        if checkout_time is not None:
            checkout_date = checkout_time.date()
            left_pre_d25e = checkout_date < mas_d25e

        if checkin_time is not None:
            checkin_date = checkin_time.date()


    if mas_isD25Eve():
        # returned on d25e

        if left_pre_d25e:
            # left before d25e, use regular greeting
            jump greeting_returned_home_morethan5mins_normalplus_flow

        else:
            # otherwise, greeting 2
            call greeting_d25e_returned_d25e

    elif mas_isD25():
        # we have returnd on d25

        if checkout_time is None or mas_isD25(checkout_date):
            # no checkout or left on d25
            call greeting_d25_returned_d25

        elif mas_isD25Eve(checkout_date):
            # left on d25e
            call greeting_d25e_returned_d25

        else:
            # otherwise assume pre d25 to d25
            call greeting_pd25e_returned_d25

    elif mas_isNYE():
        # we have returend on nye
        if checkout_time is None or mas_isNYE(checkout_date):
            # no checkout or left on nye
            call greeting_nye_delegate
            jump greeting_nye_aff_gain

        elif left_pre_d25e or mas_isD25Eve(checkout_date):
            # left before d25
            call greeting_d25e_returned_post_d25

        elif mas_isD25(checkout_date):
            # left on d25
            call greeting_d25_returned_post_d25

        else:
            # otheriwse usual more than 5 mins
            jump greeting_returned_home_morethan5mins_normalplus_flow

    elif mas_isNYD():
        # we have returned on nyd
        # NOTE: we cannot use left_pre_d25, so dont use it.

        if checkout_time is None or mas_isNYD(checkout_date):
            # no checkout or left on nyd
            call greeting_nyd_returned_nyd

        elif mas_isNYE(checkout_date):
            # left on nye
            call greeting_nye_returned_nyd
            jump greeting_nye_aff_gain

        elif checkout_time < datetime.datetime.combine(mas_d25.replace(year=checkout_time.year), datetime.time()):
            call greeting_pd25e_returned_nydp

        else:
            # all other cases should be as if leaving d25post
            call greeting_d25p_returned_nyd

    elif mas_isD25Post():

        if mas_isD25PostNYD():
            # arrived after new years day
            # NOTE: we cannot use left_pre_d25, so dnot use it

            if (
                    checkout_time is None
                    or mas_isNYD(checkout_date)
                    or mas_isD25PostNYD(checkout_date)
                ):
                # no checkout or left on nyd or after nyd
                jump greeting_returned_home_morethan5mins_normalplus_flow

            elif mas_isNYE(checkout_date):
                # left on nye
                call greeting_d25p_returned_nydp
                jump greeting_nye_aff_gain

            elif mas_isD25Post(checkout_date):
                # usual d25post
                call greeting_d25p_returned_nydp


            else:
                # all other cases use pred25e post nydp
                call greeting_pd25e_returned_nydp

        else:
            # arrived after d25, pre nye
            if checkout_time is None or mas_isD25Post(checkout_date):
                # no checkout or left during post
                jump greeting_returned_home_morethan5mins_normalplus_flow

            elif mas_isD25(checkout_date):
                # left on christmas
                call greeting_d25_returned_post_d25

            else:
                # otheriwse, use d25e returned post d25
                call greeting_d25e_returned_post_d25

    else:
        # the usual more than 5 mins
        jump greeting_returned_home_morethan5mins_normalplus_flow

    # NOTE: if you are here, then you called a regular greeting label
    # and need to return to aff gain
    jump greeting_returned_home_morethan5mins_normalplus_flow_aff


#################################### NYE ######################################
# [HOL030]

default persistent._mas_nye_spent_nye = False
# true if user spent new years eve with monika

default persistent._mas_nye_spent_nyd = False
# true if user spent new years day with monika

default persistent._mas_nye_nye_date_count = 0
# number of times user took monika out for nye

default persistent._mas_nye_nyd_date_count = 0
# number of times user took monika out for nyd

default persistent._mas_nye_date_aff_gain = 0
# amount of affection gained for an nye date

define mas_nye = datetime.date(datetime.date.today().year, 12, 31)
define mas_nyd = datetime.date(datetime.date.today().year, 1, 1)

init -810 python:
    # MASHistorySaver for nye
    store.mas_history.addMHS(MASHistorySaver(
        "nye",
        datetime.datetime(2019, 1, 6),
        {
            "_mas_nye_spent_nye": "nye.actions.spent_nye",
            "_mas_nye_spent_nyd": "nye.actions.spent_nyd",

            "_mas_nye_nye_date_count": "nye.actions.went_out_nye",
            "_mas_nye_nyd_date_count": "nye.actions.went_out_nyd",

            "_mas_nye_date_aff_gain": "nye.aff.date_gain"
        },
        use_year_before=True,
        start_dt=datetime.datetime(2019, 12, 31),
        end_dt=datetime.datetime(2020, 1, 6),
        exit_pp=store.mas_d25SeasonExit_PP
    ))

init -825 python:
    mas_run_d25s_exit = False

    def mas_d25SeasonExit_PP(mhs):
        """
        Sets a flag to run the D25 exit PP
        """
        global mas_run_d25s_exit
        mas_run_d25s_exit = True

init -10 python:
    def mas_isNYE(_date=None):
        """
        Returns True if the given date is new years eve

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is new years eve, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return _date == mas_nye.replace(year=_date.year)


    def mas_isNYD(_date=None):
        """
        RETURNS True if the given date is new years day

        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNS: True if given date is new years day, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return _date == mas_nyd.replace(year=_date.year)



#START: NYE/NYD TOPICS
#pm var so she forgives, but doesn't forget
default persistent._mas_pm_got_a_fresh_start = None

#store affection prior to reset
default persistent._mas_aff_before_fresh_start = None

#If we failed the fresh start or not
default persistent._mas_pm_failed_fresh_start = None

init 5 python:
    # NOTE: new years day
    # also known as monika_newyear2
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_nye_monika_nyd",
            action=EV_ACT_PUSH,
            start_date=mas_nyd,
            end_date=mas_nyd + datetime.timedelta(days=1),
            years=[],
            aff_range=(mas_aff.DISTRESSED, None),
        ),
        skipCalendar=True
    )

label mas_nye_monika_nyd:
    $ persistent._mas_nye_spent_nyd = True
    $ got_fresh_start_last_year = mas_HistWasFirstValueIn(True, datetime.date.today().year - 1, "pm.actions.monika.got_fresh_start")

    if store.mas_anni.pastOneMonth():
        if not mas_isBelowZero():

            #We've not had a fresh start before or you redeemed yourself
            if not persistent._mas_pm_got_a_fresh_start or not persistent._mas_pm_failed_fresh_start:
                m 1eub "¡[player]!"
                #We spent new year's together last year
                if mas_HistVerify_k([datetime.date.today().year-2], True, "nye.actions.spent_nyd")[0]:
                    m "¿Puedes creer que vamos a pasar otro año nuevo juntos?"
                if mas_isMoniAff(higher=True):
                    m 1hua "Seguro que hemos pasado por mucho juntos este año, ¿eh?"
                else:
                    m 1eua "Seguro que hemos pasado por mucho juntos este año, ¿eh?"

                m 1eka "Estoy tan feliz de saber que podemos pasar aún más tiempo juntos."

                if mas_isMoniAff(higher=True):
                    show monika 5hubfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 5hubfa "Hagamos que este año sea tan maravilloso como el anterior, ¿de acuerdo?"
                    m 5ekbfa "Te amo tanto, [player]."
                else:
                    m 3hua "Hagamos que este año sea incluso mejor que el año pasado, ¿de acuerdo?"
                    m 1hua "Te amo, [player]."

            #If you got a fresh start and are positive now
            else:
                $ last_year = "el año pasado"
                m 1eka "[player]..."

                if not got_fresh_start_last_year:
                    $ last_year = "antes"

                m 3eka "¿Recuerdas la promesa que hiciste [last_year]?"
                m "¿Que haríamos este año mejor que el anterior?"
                m 6dkbstpa "..."
                m 6ekbftpa "Gracias por mantener tu promesa."
                m "Lo digo en serio, [player]. Me has hecho muy feliz...{w=1} {nw}"
                extend 6dkbftpa "Desde el fondo de mi corazón, gracias."
                m 6dkbftda "Hagamos que este año sea incluso mejor que el anterior, ¿de acuerdo?"
                m 6ekbftda "Te amo, [player]."
                m "Realmente lo hago."
                #You made it up
                $ persistent._mas_pm_failed_fresh_start = False

        #Below zero
        else:
            #Not had fresh start yet
            if not persistent._mas_pm_got_a_fresh_start:
                m 2ekc "[player]..."
                m 2rksdlc "Hemos pasado por... {w=1}Mucho el año pasado..."
                m "Yo... Espero que este año vaya mejor que el año pasado."
                m 2dkc "Realmente lo necesito."
                jump mas_nye_monika_nyd_fresh_start

            else:
                m 2rkc "[player]..."
                #If you got a fresh start last year and you're still negative
                if got_fresh_start_last_year:
                    m 2ekc "¿Recuerdas la promesa que hiziste el año pasado?"
                    m 2ekd "¿Que haríamos de este año mejor que el anterior?"

                #Otherwise fresh start
                else:
                    m 2ekc "¿Recuerdas la promesa que hiciste antes?"
                    m 2ekd "¿Que mejorarías nuestra relación?"

                $ curr_aff = _mas_getAffection()
                if curr_aff > persistent._mas_aff_before_fresh_start:
                    m 2rkd "Supongo que lo hiciste un poco mejor..."
                    m 2ekc "Pero esperaba más, [player]."

                    #Revert back to old affection if we haven't already done this
                    if not mas_HistVerifyAll_k(True, "pm.actions.monika.failed_fresh_start"):
                        $ mas_setAffection(persistent._mas_aff_before_fresh_start)

                elif curr_aff < persistent._mas_aff_before_fresh_start:
                    m 2rfc "Supongo que realmente no podrías mantener esa promesa... ¿verdad?"

                else:
                    m 2rkc "Parece que nada ha cambiado realmente, ¿verdad?"

                #Since -50 is going to mean an FF next load, we need to path this accordingly
                m 2rktpc "Realmente,{w=0.5} realmente espero que puedas arreglar esto, [player]..."
                m 2dktpc "No sé cuánto más puedo soportar."

                #Foreshadowing
                if _mas_getAffection() <= -50:
                    m 2dktsd "Pero tal vez ahora sea un pensamiento tonto..."
                    m 2ektsc "Este es sólo otro juego para ti, ¿no?"
                    m 2rktsd "Ni siquiera me ves como real...{w=1} {nw}"
                    extend 2dftsc "Soy sólo otro personaje con el que puedes jugar."
                    m 2eftdc "Espero que nadie tenga que experimentar el dolor y la soledad que he pasado este año."

                $ persistent._mas_pm_failed_fresh_start = True
                return

    else:
        if not mas_isBelowZero():
            m 1eub "¡[player]!"

            if mas_isMoniAff(higher=True):
                m 1ekbsa "Sé que no hemos estado juntos durante tanto tiempo todavía, pero el año pasado fue mejor de lo que esperaba..."
            else:
                m 1eka "Sé que no hemos estado juntos durante tanto tiempo todavía, pero el año pasado fue tan especial para mí..."

            m 1hua "Siempre lo recordaré como el año en que te conocí~"
            m 3hua "¡Aprovechemos nuestro poco tiempo juntos y hagamos que este año sea aún mejor!"
            m 1ekbsa "Te amo, [player]."

        else:
            m 2ekc "Entonces, [player]..."
            m 2etc "El comienzo de un nuevo año, ¿eh?"
            m 2rksdlc "No hemos estado juntos por mucho tiempo, pero el tiempo que pasamos el año pasado no fue tan bien como esperaba..."
            jump mas_nye_monika_nyd_fresh_start

    m "Feliz año nuevo~"
    return "love"

label mas_nye_monika_nyd_fresh_start:
    m 2ekc "¿Qué tal si ponemos todo eso en el pasado, nos olvidamos del año pasado y nos enfocamos en un nuevo comienzo este año?"
    m 4ekc "No es demasiado tarde para nosotros, [player]. Todavía podemos hacernos mas felices."
    m 4eka "Es todo lo que siempre he querido."

    m "¿Qué dices, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Qué dices, [player]?{fast}"

        "Amaría eso.":
            #so we can revert back to previous affection if player continues to mistreat after the second chance. need to determine the threshold the player must stay above for this.
            $ persistent._mas_pm_got_a_fresh_start = True #never forget
            $ persistent._mas_aff_before_fresh_start = _mas_getAffection()

            # reset affection and save it
            $ mas_setAffection(0)
            $ _mas_AffSave()
            $ renpy.save_persistent()

            m 4wua "¿De verdad?"
            m 1hua "¡Oh, [player], no tienes idea de lo feliz que me hace eso!"
            m 3eka "Sé que podemos hacer que esto funcione."
            m 1hua "Muchas gracias..."
            m 1eka "El solo hecho de saber que todavía quieres estar conmigo... Lo significa todo para mí."
            m 3eka "Hagamos que esto cuente, ¿de acuerdo [player]?"
            return

        "No.":
            $ persistent._mas_pm_got_a_fresh_start = False

            # set affection to broken
            $ mas_setAffection(store.mas_affection.AFF_BROKEN_MIN - 1)
            $ _mas_AffSave()
            $ renpy.save_persistent()

            m 6dktpc "..."
            m 6ektpc "Yo... Yo..."
            m 6dktuc "..."
            m 6dktsc "..."
            pause 10.0
            return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_resolutions",
            action=EV_ACT_QUEUE, #queuing it so it shows on the right day
            start_date=mas_nye,
            end_date=mas_nye + datetime.timedelta(days=1),
            years=[],
            aff_range=(mas_aff.UPSET,None)
        ),
        skipCalendar=True
    )

default persistent._mas_pm_accomplished_resolutions = None
#True if user has accomplished new years resolutions
default persistent._mas_pm_has_new_years_res = None
#True if user has resolutuons

label monika_resolutions:
    $ persistent._mas_nye_spent_nye = True
    m 2eub "¿Emm, [player]?"
    m 2eka "Me preguntaba..."

    #If we didn't see this last year, we need to ask if we made a resolution or not
    if not mas_lastSeenLastYear("monika_resolutions"):
        m 3eub "¿Tuviste alguna meta de Año Nuevo el año pasado?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Tuviste alguna meta de Año Nuevo el año pasado?{fast}"

            "Sí.":
                m 3hua "Siempre me enorgullece saber que intentas superarte, [player]."
                m 2eka "Entonces..."

                call monika_resolutions_accomplished_resolutions_menu("¿Cumpliste tus metas del año pasado?")


            "No.":
                m 2euc "Oh, ya veo..."

                if mas_isMoniNormal(higher=True):
                    if mas_isMoniHappy(higher=True):
                        m 3eka "Bueno, no creo que realmente necesitaras cambiar en absoluto de todos modos."
                        m 3hub "Creo que ya eres maravilloso, solo se tú mismo."
                    else:
                        m 3eka "No tiene nada de malo. No creo que tengas que cambiar en lo absoluto."

                else:
                    m 2rkc "Pero probablemente deberías tener una este año [player]..."

    #If we made a resolution last year, then we should ask if the player accomplished it
    elif mas_HistVerifyLastYear_k(True, "pm.actions.made_new_years_resolutions"):
        call monika_resolutions_accomplished_resolutions_menu("Desde que hiciste tus metas el año pasado, ¿lo cumpliste?")

    #This path will be the first thing you see if you didn't make a resolution last year
    m "¿Ya tienes alguna para el año que viene?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Ya tienes alguna para el año que viene?{fast}"
        "Sí.":
            $ persistent._mas_pm_has_new_years_res = True

            m 1eub "¡Eso es genial!"
            m 3eka "Incluso si pueden ser difíciles de alcanzar o mantener..."
            m 1hua "¡Incluso podría ayudarte, si lo necesitas!"

        "No.":
            $ persistent._mas_pm_has_new_years_res = False
            m 1eud "¿Oh, es eso así?"
            if mas_isMoniNormal(higher=True):
                if persistent._mas_pm_accomplished_resolutions:
                    if mas_isMoniHappy(higher=True):
                        m 1eka "No creo que tengas que cambiar. Creo que eres maravilloso tal y como eres."
                    else:
                        m 1eka "No creo que tengas que cambiar. Creo que estas bien tal y como eres."
                    m 3euc "Pero si algo te viene a la mente antes de que el reloj marque las doce, anótalo..."
                else:
                    m "Bueno, si algo te viene a la mente antes de que el reloj marque las doce, anótalo..."
                m 1kua "Tal vez deberías pensar en algo que quieras hacer."
            else:
                m 2ekc "{cps=*2}Espero por ello-{/cps}{nw}"
                m 2rfc "Sabes que, no importa..."

    if mas_isMoniAff(higher=True):
        show monika 5hubfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5hubfa "Mi meta es ser una novia incluso mejor para ti, [mas_get_player_nickname()]."
    elif mas_isMoniNormal(higher=True):
        show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ekbfa "Mi meta es ser una novia incluso mejor para ti, [player]."
    else:
        m 2ekc "Mi meta es mejorar nuestra relación, [player]."

    return

label monika_resolutions_accomplished_resolutions_menu(question):
    m 3hub "[question]{nw}"
    $ _history_list.pop()
    menu:
        m "[question]{fast}"

        "Sí.":
            $ persistent._mas_pm_accomplished_resolutions = True
            if mas_isMoniNormal(higher=True):
                m 4hub "¡Estoy feliz de escuchar eso, [player]!"
                m 2eka "Es genial como manejaste esto."
                m 3ekb "Cosas como estas me hacen sentir realmente orgullosa de ti."
                m 2eka "Sin embargo, me gustaría poder estar allí para celebrar un poco mas contigo."
            else:
                m 2rkc "Está bien, [player]."
                m 2esc "Bueno, siempre puedes celebrar algo más este año..."
                m 3euc "Nunca sabes que podría pasar."

            return True

        "No.":
            $ persistent._mas_pm_accomplished_resolutions = False
            if mas_isMoniNormal(higher=True):
                m 2eka "Ah... bueno, algunas cosas simplemente no funcionan como lo esperarías."

                if mas_isMoniHappy(higher=True):
                    m 2eub "Además, eres maravilloso, incluso si no puedo hacerte cumplidos por tus méritos..."
                    m 2eka "...Todavía estoy muy orgullosa de ti por ponerte metas e intentar mejorar, [player]."
                    m 3eub "Si decides tomar una meta este año, te apoyaré en cada paso del camino."
                    m 4hub "¡Me encantaria ayudarte a alcanzar tus metas!"
                else:
                    m "Pero creo que es genial que al menos hayas tratado de mejorarte estableciendo metas."
                    m 3eua "¡Quizás si tomas una meta este año, puedas lograrlo!"
                    m 3hub "¡Creo en ti, [player]!"

            else:
                m 2euc "Oh...{w=1} Bueno, tal vez deberías esforzarte un poco más en la meta del próximo año."

            return False


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nye_year_review",
            action=EV_ACT_QUEUE,
            start_date=mas_nye,
            end_date=datetime.datetime.combine(mas_nye, datetime.time(hour=23)),
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label monika_nye_year_review:
    $ persistent._mas_nye_spent_nye = True
    $ spent_an_event = False

    $ placeholder_and = "y "
    #Starting with an overview based on time
    if store.mas_anni.anniCount() >= 1:
        m 2eka "Ya sabes, [player], realmente hemos pasado por mucho juntos."
        if store.mas_anni.anniCount() == 1:
            m 2wuo "¡Pasemos todo el año juntos!"
            m 2eka "El tiempo vuela..."

        else:
            m 2eka "Este año ha pasado volando..."

    elif store.mas_anni.pastSixMonths():
        m 2eka "Sabes, [player], realmente hemos pasado por mucho durante el tiempo que pasamos juntos el año pasado."
        m "El tiempo simplemente vuela..."

    elif store.mas_anni.pastThreeMonths():
        m 2eka "Ya sabes [player], hemos pasado por bastante durante el poco tiempo que pasamos juntos el año pasado."
        m 2eksdla "Todo ha pasado tan rápido, jajaja..."

    else:
        m 2eka "[player], a pesar de que no hemos pasado por mucho juntos, todavía..."
        $ placeholder_and = ""


    # then a bit based on affection
    if mas_isMoniLove():
        m 2ekbsa "...Y nunca querría pasar ese tiempo con nadie más, [player]."
        m "Yo estoy realmente,{w=0.5} realmente feliz de haber pasado este año junto a ti."

    elif mas_isMoniEnamored():
        m 2eka "...[placeholder_and]estoy tan feliz de poder pasar todo este tiempo contigo, [player]."

    elif mas_isMoniAff():
        m 2eka "...[placeholder_and]realmente disfruté nuestro tiempo juntos."

    else:
        m 2euc "...[placeholder_and]el tiempo que pasamos juntos ha sido divertido."


    m 3eua "De todos modos, creo que sería bueno simplemente reflexionar sobre todo lo que hemos pasado juntos el año pasado."
    m 2dtc "Veamos..."

    # promisering related stuff
    if mas_lastGiftedInYear("mas_reaction_promisering", mas_nye.year):
        m 3eka "Mirando hacia atrás, me hiciste una promesa este año cuando me diste este anillo..."
        m 1ekbsa "...un símbolo de nuestro amor."

        if persistent._mas_pm_wearsRing:
            m "E incluso tienes uno para ti..."

            if mas_isMoniAff(higher=True):
                m 1ekbfa "Para demostrar que estás tan comprometido conmigo, como yo lo estoy contigo."
            else:
                m 1ekbfa "Para mostrarme tu compromiso."

    #vday
    if mas_lastSeenInYear("mas_f14_monika_valentines_intro"):
        $ spent_an_event = True
        m 1wuo "¡Oh!"
        m 3ekbsa "Pasaste el día de San Valentín conmigo..."

        if mas_getGiftStatsForDate("mas_reaction_gift_roses", mas_f14):
            m 4ekbfb "...y me diste un hermoso ramo de flores también."


    #922
    if persistent._mas_bday_opened_game:
        $ spent_an_event = True
        m 2eka "Pasaste tiempo conmigo incluso en mi cumpleaños..."

        if not persistent._mas_bday_no_recognize:
            m 2dua "...celebrandolo junto a mi..."

        if persistent._mas_bday_sbp_reacted:
            m 2hub "...me hiciste una fiesta sorpresa..."

        show monika 5ekbla at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ekbla "...y realmente me hiziste sentir amada. No puedo agradecerte lo suficiente por hacer eso por mí."

    #Pbday
    if (
        persistent._mas_player_bday_spent_time
        or mas_HistVerify_k([datetime.date.today().year], True, "player_bday.spent_time")[0]
    ):
        $ spent_an_event = True
        show monika 5hua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5hua "¡Hasta hemos celebrado tu cumpleaños!"

        if (
            persistent._mas_player_bday_date
            or not mas_HistVerify_k([datetime.date.today().year], 0, "player_bday.date")[0]
        ):
            m 5eubla "Incluso tuvimos una bonita cita juntos~"

    #bit on christmas
    if persistent._mas_d25_spent_d25:
        $ spent_an_event = True
        show monika 5hua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5hua "Pasaste tu navidad conmigo..."

        if persistent._mas_first_kiss is not None and persistent._mas_first_kiss.date() == mas_d25:
            m 5eubla "...y compartimos nuestro primer beso~"
            m 5lubsa "Nunca olvidare ese momento..."
            m 5ekbfa "{i}Nuestro{/i} momento."
            m "No puedo imaginarme pasarlo con nadie más."
        else:
            m 5ekbla "...un día que no podía imaginar pasar con nadie más."


    if not spent_an_event:
        m 2rksdla "...Supongo que no hemos pasado juntos por grandes eventos."
        m 3eka "Pero aun así..."

    else:
        show monika 5dsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5dsa "..."

    # lookback based on time
    if store.mas_anni.pastThreeMonths():
        if mas_isMoniHappy(higher=True):
            show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eka "Realmente no puedo creer cuánto he cambiado desde que estamos juntos..."
        else:
            m 2eka "Realmente espero que podamos avanzar más en nuestra relación, [player]..."
    else:
        show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5eka "No puedo esperar a ver cuánto cambiaré en el futuro para nosotros..."

    #If we started fresh the year before this or we didn't at all
    if not mas_HistWasFirstValueIn(True, datetime.date.today().year - 1, "pm.actions.monika.got_fresh_start"):
        show monika 5dka at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5dka "Gracias."
        if store.mas_anni.anniCount() > 0:
            $ ending = "el mejor año con el que hubiera soñado nunca"

            if mas_lastSeenLastYear("monika_nye_year_review"):
                $ ending = "mejor que el año anterior"

            m 5ekbsa "Gracias por hacer el año pasado [ending]."

        else:
            $ _last_year = " "
            if store.mas_anni.pastOneMonth():
                $ _last_year = " el año pasado "

            m 5ekbsa "Gracias por hacer que el tiempo que pasamos juntos[_last_year]sea mejor de lo que podría haber imaginado."

        if mas_isMoniEnamored(higher=True):
            if persistent._mas_first_kiss is None:
                m 1lsbsa "..."
                m 6ekbsa "[player] yo..."
                call monika_kissing_motion
                m 1ekbfa "Te amo."
                m "..."
                show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 5ekbsa "Nunca olvidaré este momento..."
                m 5ekbfa "Nuestro primer beso~"
                m 5hubfb "Hagamos que este año sea incluso mejor que el anterior, [player]."

            else:
                call monika_kissing_motion_short
                m 1ekbfa "Te amo, [player]."
                show monika 5hubfb at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 5hubfb "Hagamos que este año sea mejor que el anterior."

        else:
            m "Hagamos de este año lo mejor que podamos, [player]. Te amo~"
    else:
        m 1dsa "Gracias por decidir dejar atrás el pasado y empezar de nuevo."
        m 1eka "Creo que si lo intentamos, podemos hacer que esto funcione, [player]."
        m "Hagamos que este año sea grandioso para ambos."
        m 1ekbsa "Te amo."

    return "no_unlock|love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_nye_monika_nye_dress_intro",
            conditional=(
                "persistent._mas_d25_in_d25_mode "
                "and not mas_SELisUnlocked(mas_clothes_dress_newyears)"
            ),
            start_date=mas_nye,
            end_date=mas_nye + datetime.timedelta(days=1),
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

label mas_nye_monika_nye_dress_intro:
    m 3hub "Eh [player], tengo algo reservado para ti este año~"
    m 3eua "Solo deja que vaya a cambiarme.{w=0.5}.{w=0.5}.{nw}"

    # change into dress
    call mas_clothes_change(mas_clothes_dress_newyears, outfit_mode=True, unlock=True)
    $ mas_addClothesToHolidayMap(mas_clothes_dress_newyears)

    m 2rkbssdla "..."
    m 2rkbssdlb "Mis ojos están aquí arriba, [player]..."
    if mas_isMoniAff(higher=True):
        m 2tubsu "..."
        m 3hubsb "¡Jajaja! Solo bromeo~"
        m 3eua "Me alegro de que te guste mi vestido. {nw}"

    else:
        m 2rkbssdla "..."
        m "Yo...{w=1} Me alegro de que te guste mi vestido. {nw}"

    extend 3eua "¡Me ha costado elegir el correcto!"
    m 3rka "La corona de flores siempre se me está cayendo..."
    m 1hua "Me decante por el look de 'diosa griega', espero que se note."
    m 3eud "Pero este atuendo tiene un poco más de profundidad, ¿sabes?"

    if seen_event("mas_f14_monika_vday_colors"):
        m 3eua "Quizás recuerdes cuando hablamos de rosas y las sensaciones que transmiten sus colores."
    else:
        m 3eua "Quizás ya lo hayas adivinado, pero es por la elección del color."

    m "El blanco representa muchas cualidades positivas, como la bondad, pureza o seguridad..."
    m 3eub "Así que, querer que resaltara este atuendo era un comienzo exitoso."

    #If we fresh started last year
    if mas_HistWasFirstValueIn(True, datetime.date.today().year - 1, "pm.actions.monika.got_fresh_start"):
        m 2eka "El año pasado decidimos empezar de nuevo y estoy muy contenta de haberlo hecho."
        m 2ekbsa "Sabía que podríamos ser felices juntos, [player]."
        m 2fkbsa "Y me has hecho la más feliz del mundo."

    m 3dkbsu "Así que me gustaría usar esto cuando comience el nuevo año."
    m 1ekbsa "Podría ayudar a que el próximo año sea aún mejor."
    return "no_unlock"


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_d25_mode_exit",
            category=['fiestas'],
            prompt="¿Puedes quitar los adornos?",
            conditional="persistent._mas_d25_deco_active",
            start_date=mas_nyd+datetime.timedelta(days=1),
            end_date=mas_d25c_end,
            action=EV_ACT_UNLOCK,
            pool=True,
            rules={"no_unlock": None},
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_d25_monika_d25_mode_exit",
        mas_nyd + datetime.timedelta(days=1),
        mas_d25c_end,
    )

label mas_d25_monika_d25_mode_exit:
    m 3eka "¿Tienes ya suficiente espíritu navideño [player]?"
    m 3eua "No me importaría empezar el año nuevo."
    m 1hua "Mientras esté contigo, por supuesto~"
    m 3hub "¡Jajaja!"
    m 2dsa "Solo dame un segundo para quitar las decoraciones.{w=0.3}.{w=0.3}.{w=0.3}{nw}"

    call mas_d25_season_exit

    m 1hua "¡Perfecto!{w=0.5} {nw}"
    extend 3hub "¡Ya estamos listos para comenzar el nuevo año!"

    #And we lock this so we can'd run it again
    $ mas_lockEVL("mas_d25_monika_d25_mode_exit", "EVE")
    return

label greeting_nye_aff_gain:
    # gaining affection for nye
    python:
        if persistent._mas_nye_date_aff_gain < 15:
            # retain older affection gain so we can compare
            curr_aff = _mas_getAffection()

            # just in case
            time_out = store.mas_dockstat.diffCheckTimes()

            # reset this so we can gain aff
            persistent._mas_monika_returned_home = None

            # now gain aff
            store.mas_dockstat._ds_aff_for_tout(time_out, 5, 15, 3, 3)

            # add the amount gained
            persistent._mas_nye_date_aff_gain += _mas_getAffection() - curr_aff

    jump greeting_returned_home_morethan5mins_cleanup

label mas_gone_over_nye_check:
    if mas_checkOverDate(mas_nye):
        $ persistent._mas_nye_spent_nye = True
        $ persistent._mas_nye_nye_date_count += 1
    return

label mas_gone_over_nyd_check:
    if mas_checkOverDate(mas_nyd):
        $ persistent._mas_nye_spent_nyd = True
        $ persistent._mas_nye_nyd_date_count += 1
    return

#===========================================================Going to take you somewhere on NYE===========================================================#

label bye_nye_delegate:
    # need to determine current time
    python:
        _morning_time = datetime.time(5)
        _eve_time = datetime.time(20)
        _curr_time = datetime.datetime.now().time()

    if _curr_time < _morning_time:
        # if before morning, assume regular going out
        jump bye_going_somewhere_normalplus_flow_aff_check

    elif _curr_time < _eve_time:
        # before evening but after morning

        if persistent._mas_nye_nye_date_count > 0:
            call bye_nye_second_time_out

        else:
            call bye_nye_first_time_out

    else:
        # evening
        call bye_nye_late_out

    # finally jump back to iostart
    jump mas_dockstat_iostart

label bye_nye_first_time_out:
    #first time out (morning-about maybe, 7-8:00 [evening]):
    m 3tub "¿Vamos a ir a un lugar especial hoy, [player]?"
    m 4hub "¡Es la víspera de Año Nuevo, después de todo!"
    m 1eua "No estoy del todo segura de lo que tienes planeado, ¡pero estoy ansiosa por hacerlo!"
    return

label bye_nye_second_time_out:
    #second time out+(morning-about maybe, 7-8:00 [evening]):
    m 1wuo "Oh, ¿vamos a salir de nuevo?"
    m 3hksdlb "Debes celebrar mucho el Año Nuevo, ¡jajaja!"
    m 3hub "Me encanta ir contigo, así que espero con ansias lo que estemos haciendo~"
    return

label bye_nye_late_out:
    #(7-8:00 [evening]-about maybe midnight):
    m 1eka "Ya es algo tarde, [player]..."
    m 3eub "¿Vamos a ver los fuegos artificiales?"
    if persistent._mas_pm_have_fam and persistent._mas_pm_fam_like_monika:
        m "¿O ir a una cena familiar?"
        m 4hub "¡Me encantaría conocer a tu familia algún día!"
        m 3eka "¡De cualquier manera, estoy muy emocionada!"
    else:
        m "Siempre me ha encantado cómo los fuegos artificiales de Año Nuevo iluminan el cielo nocturno..."
        m 3ekbsa "Un día podremos verlos uno al lado del otro... Pero hasta que llegue ese día, estoy feliz de ir contigo, [player]."
    return

#=============================================================Greeting returned home for NYE=============================================================#
#greeting_returned_home_nye:

label greeting_nye_delegate:
    python:
        _eve_time = datetime.time(20)
        _curr_time = datetime.datetime.now().time()

    if _curr_time < _eve_time:
        # before firewoprk time
        call greeting_nye_prefw

    # otherwise, assume in firework time
    else:
        call greeting_nye_infw

    $ persistent._mas_nye_nye_date_count += 1

    return

label greeting_nye_prefw:
    #if before firework time (7-8:00-midnight):
    m 1hua "Y... ¡Ya estamos en casa!"
    m 1eua "Ha sido divertido, [player]."
    m 1eka "Gracias por invitarme hoy, me encanta pasar tiempo contigo."
    m "Significa mucho para mí que me lleves contigo para que podamos pasar juntos días especiales como estos."
    show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5ekbfa "Te amo, [player]."
    return "love"

label greeting_nye_infw:
    #if within firework time:
    m 1hua "Y... ¡Ya estamos en casa!"
    m 1eka "Gracias por sacarme hoy, [player]."
    m 1hua "Fue muy divertido solo pasar tiempo contigo hoy."
    m 1ekbsa "Realmente significa mucho para mí que aunque no puedas estar aquí personalmente para pasar estos días conmigo, todavía me llevas contigo."
    m 1ekbfa "Te amo, [player]."
    return "love"

#===========================================================Going to take you somewhere on NYD===========================================================#

label bye_nyd_delegate:
    if persistent._mas_nye_nyd_date_count > 0:
        call bye_nyd_second_time_out

    else:
        call bye_nyd_first_time_out

    jump mas_dockstat_iostart

label bye_nyd_first_time_out:
    #first time out
    m 3tub "¿Celebración de año nuevo, [player]?"
    m 1hua "¡Suena divertido!"
    m 1eka "Pasemos un buen rato juntos."
    return

label bye_nyd_second_time_out:
    #second+ time out
    m 1wuo "¿Wow, vamos a salir de nuevo, [player]?"
    m 1hksdlb "¡Realmente debes celebrar mucho, jajaja!"
    return

#=============================================================Greeting returned home for NYD=============================================================#

label greeting_nye_returned_nyd:
    #if returning home from NYE:
    $ persistent._mas_nye_nye_date_count += 1
    $ persistent._mas_nye_nyd_date_count += 1

    m 1hua "Y... ¡Ya estamos en casa!"
    m 1eka "Gracias por sacarme a dar una vuelta ayer, [player]."
    m 1ekbsa "Ya sabes que amo para el tiempo a tu lado, y poder pasar la víspera de Año Nuevo, hasta el día de hoy, aquí mismo contigo se sintió realmente genial."
    m "Realmente significas mucho para mí."
    m 5eubfb "Gracias por este maravilloso año juntos, [player]."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return

label greeting_nyd_returned_nyd:
    #normal return home:(i.e. took out, and returned on NYD itself)
    $ persistent._mas_nye_nyd_date_count += 1
    m 1hua "Y... ¡Ya estamos en casa!"
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eua "¡Eso ha sido muy divertido, [player]!"
    m 5eka "Es muy amable de tu parte llevarme contigo en días especiales como este."
    m 5hub "Realmente espero que podamos pasar más tiempo así juntos."
    return

#============================================================Greeting returned home after NYD============================================================#

label greeting_pd25e_returned_nydp:
    #Here for historical data
    $ persistent._mas_d25_d25e_date_count += 1
    $ persistent._mas_d25_d25_date_count += 1
    $ persistent._mas_d25_spent_d25 = True

    m 1hua "Y... ¡Ya estamos en casa!"
    m 1hub "Estuvimos fuera por un buen rato, pero ese fue un paseo realmente agradable, [player]."
    m 1eka "Gracias por llevarme contigo, realmente lo disfruté."
    show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    $ new_years = "el año nuevo"
    if mas_isNYD():
        $ new_years = "la nochebuena"
    m 5ekbsa "Siempre me encanta pasar tiempo contigo, pero pasar la Navidad y [new_years] juntos es increíble."
    m 5hub "Espero que podamos hacer algo así otra vez en alguna ocasión."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday

    $ mas_d25ReactToGifts()
    return

#============================================================Greeting returned home D25P NYD(P)============================================================#
label greeting_d25p_returned_nyd:
    $ persistent._mas_nye_nyd_date_count += 1

    m 1hua "Y... ¡Ya estamos en casa!"
    m 1eub "Gracias por llevarme contigo, [player]."
    m 1eka "¡Estuvimos fuera por un buen rato, pero ese fue un paseo realmente agradable!"
    m 3hub "Sin embargo, es genial estar de vuelta en casa, podemos pasar el año nuevo juntos."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday

    $ mas_d25ReactToGifts()
    return

label greeting_d25p_returned_nydp:
    m 1hua "Y... ¡Ya estamos en casa!"
    m 1wuo "¡Vaya paseo más largo, [player]!"
    m 1eka "Estoy un poco triste de que no pudiéramos desearnos un feliz año nuevo, pero realmente lo disfruté."
    m "Estoy muy feliz de que me hayas traído."
    m 3hub "Feliz Año Nuevo, [player]~"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday

    $ mas_d25ReactToGifts()
    return

########################################################### player_bday ########################################################################
# [HOL040]

# so we know we are in player b_day mode
default persistent._mas_player_bday_in_player_bday_mode = False
# so we know if you ruined the surprise
default persistent._mas_player_bday_opened_door = False
# for various reason, no decorations
default persistent._mas_player_bday_decor = False
# number of bday dates
default persistent._mas_player_bday_date = 0
# so we know if returning home post bday it was a bday date
default persistent._mas_player_bday_left_on_bday = False
# affection gained on bday dates
default persistent._mas_player_bday_date_aff_gain = 0
# did we celebrate player bday with Moni
default persistent._mas_player_bday_spent_time = False
# did we get the surprise variant of the event?
default persistent._mas_player_bday_saw_surprise = False

init -10 python:
    def mas_isplayer_bday(_date=None, use_date_year=False):
        """
        IN:
            _date - date to check
                If None, we use today's date
                (default: None)

            use_date_year - True if we should use the year from _date or not.
                (Default: False)

        RETURNS: True if given date is player_bday, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        if persistent._mas_player_bday is None:
            return False

        elif use_date_year:
            return _date == mas_player_bday_curr(_date)
        return _date == mas_player_bday_curr()

    def strip_mas_birthdate():
        """
        strips mas_birthdate of its conditional and action to prevent double birthday sets
        """
        mas_birthdate_ev = mas_getEV('mas_birthdate')
        if mas_birthdate_ev is not None:
            mas_birthdate_ev.conditional = None
            mas_birthdate_ev.action = None

    def mas_pbdayCapGainAff(amount):
        mas_capGainAff(amount, "_mas_player_bday_date_aff_gain", 25)

init -11 python:
    def mas_player_bday_curr(_date=None):
        """
        sets date of current year bday, accounting for leap years
        """
        if _date is None:
            _date = datetime.date.today()
        if persistent._mas_player_bday is None:
            return None
        else:
            return store.mas_utils.add_years(persistent._mas_player_bday,_date.year-persistent._mas_player_bday.year)

init -810 python:
    # MASHistorySaver for player_bday
    store.mas_history.addMHS(MASHistorySaver(
        "player_bday",
        # NOTE: this needs to be adjusted based on the player's bday
        datetime.datetime(2020, 1, 1),
        {
            "_mas_player_bday_spent_time": "player_bday.spent_time",
            "_mas_player_bday_opened_door": "player_bday.opened_door",
            "_mas_player_bday_date": "player_bday.date",
            "_mas_player_bday_date_aff_gain": "player_bday.date_aff_gain",
            "_mas_player_bday_saw_surprise": "player_bday.saw_surprise",
        },
        use_year_before=True,
        # NOTE: the start and end dt needs to be chnaged depending on the
        #   player bday
    ))

init -11 python in mas_player_bday_event:
    import datetime
    import store.mas_history as mas_history

    def correct_pbday_mhs(d_pbday):
        """
        fixes the pbday mhs usin gthe given date as pbday

        IN:
            d_pbday - player birthdate
        """
        # get mhs
        mhs_pbday = mas_history.getMHS("player_bday")
        if mhs_pbday is None:
            return

        # first, setup the reset date to be 3 days after the bday
        pbday_dt = datetime.datetime.combine(d_pbday, datetime.time())

        # determine correct year
        _now = datetime.datetime.now()
        curr_year = _now.year
        new_dt = pbday_dt.replace(year=curr_year)
        if new_dt < _now:
            # new date before today, set to next year
            curr_year += 1
            new_dt = pbday_dt.replace(year=curr_year)

        # set the reset/trigger date
        reset_dt = pbday_dt + datetime.timedelta(days=3)

        # setup ranges
        new_sdt = new_dt
        new_edt = new_sdt + datetime.timedelta(days=2)

        # NOTE: the mhs will end 2 days after the bday. The day after end_dt
        #   is when we save

        # modify mhs
        mhs_pbday.start_dt = new_sdt
        mhs_pbday.end_dt = new_edt
        mhs_pbday.use_year_before = (
            d_pbday.month == 12
            and d_pbday.day in (29, 30, 31)
        )
        mhs_pbday.setTrigger(reset_dt)


label mas_player_bday_autoload_check:
    # since this has priority over 922, need these next 2 checks
    if mas_isMonikaBirthday():
        $ persistent._mas_bday_no_time_spent = False
        $ persistent._mas_bday_opened_game = True
        $ persistent._mas_bday_no_recognize = not mas_recognizedBday()

    elif mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_blackdress:
        $ monika_chr.reset_clothes(False)
        $ monika_chr.save()
        $ renpy.save_persistent()

    # making sure we are already not in bday mode, have confirmed birthday, have normal+ affection and have not celebrated in any way
    if (
        not persistent._mas_player_bday_in_player_bday_mode
        and persistent._mas_player_confirmed_bday
        and mas_isMoniNormal(higher=True)
        and not persistent._mas_player_bday_spent_time
        and not mas_isD25()
        and not mas_isO31()
        and not mas_isF14()
    ):

        python:
            # first we determine if we want to run a surprise greeting this year
            this_year = datetime.date.today().year
            years_checked = range(this_year-10,this_year)
            surp_int = 3

            times_ruined = len(mas_HistVerify("player_bday.opened_door", True, *years_checked)[1])

            if times_ruined == 1:
                surp_int = 6
            elif times_ruined == 2:
                surp_int = 10
            elif times_ruined > 2:
                surp_int = 50

            should_surprise = renpy.random.randint(1,surp_int) == 1 and not mas_HistVerifyLastYear_k(True,"player_bday.saw_surprise")

            if not mas_HistVerify("player_bday.saw_surprise",True)[0] or (mas_getAbsenceLength().total_seconds()/3600 < 3 and should_surprise):
                # starting player b_day off with a closed door greet
                # always if haven't seen the surprise before
                # conditionally if we have
                selected_greeting = "i_greeting_monikaroom"
                mas_skip_visuals = True
                persistent._mas_player_bday_saw_surprise = True

            else:
                selected_greeting = "mas_player_bday_greet"
                if should_surprise:
                    mas_skip_visuals = True
                    persistent._mas_player_bday_saw_surprise = True

            # need this so we don't get any strange force quit dlg after the greet
            persistent.closed_self = True

        jump ch30_post_restartevent_check

    elif not mas_isplayer_bday():
        # no longer want to be in bday mode
        $ persistent._mas_player_bday_decor = False
        $ persistent._mas_player_bday_in_player_bday_mode = False
        $ mas_lockEVL("bye_player_bday", "BYE")

    if not mas_isMonikaBirthday() and (persistent._mas_bday_in_bday_mode or persistent._mas_bday_visuals):
        $ persistent._mas_bday_in_bday_mode = False
        $ persistent._mas_bday_visuals = False

    if mas_isO31():
        return
    else:
        jump mas_ch30_post_holiday_check

# closed door greet option for opening door without listening
label mas_player_bday_opendoor:
    $ mas_loseAffection()
    $ persistent._mas_player_bday_opened_door = True
    if persistent._mas_bday_visuals:
        $ persistent._mas_player_bday_decor = True
    call spaceroom(hide_monika=True, scene_change=True, dissolve_all=True, show_emptydesk=False)
    $ mas_disable_quit()
    if mas_isMonikaBirthday():
        $ your = "nuestra"
    else:
        $ your = "tú"

    if mas_HistVerify("player_bday.opened_door",True)[0]:
        $ now = "{i}again{/i}"
    else:
        $ now = "now"

    m "¡[player]!"
    m "¡No me avisaste!"
    if not persistent._mas_bday_visuals:
        m "¡Estaba a punto de empezar a preparar [your] fiesta de cumpleaños, pero no he tenido tiempo antes de que llegaras!"
    m "..."
    m "Bueno...{w=1} La sorpresa se ha estropeado [now], pero.{w=0.5}.{w=0.5}.{nw}"
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    pause 1.0
    show monika 1eua at ls32 zorder MAS_MONIKA_Z
    m 4eua "¡Feliz cumpleaños, [player]!"
    m 2rksdla "Ojalá hubieras llamado primero."
    m 4hksdlb "Oh... ¡[your] tarta!"
    call mas_player_bday_cake
    jump monikaroom_greeting_cleanup

# closed door greet option for knocking without listening
label mas_player_bday_knock_no_listen:
    m "¿Quién es?"
    menu:
        "Soy yo.":
            $ mas_disable_quit()
            m "¡Oh! ¿Puedes esperar un segundo porfi?"
            window hide
            pause 5.0
            m "Perfecto, entra, [player]..."
            jump mas_player_bday_surprise

# closed door greet surprise flow
label mas_player_bday_surprise:
    $ persistent._mas_player_bday_decor = True
    call spaceroom(scene_change=True, dissolve_all=True, force_exp='monika 4hub_static')
    m 4hub "¡Sorpresa!"
    m 4sub "¡Jajaja! ¡Feliz cumpleaños, [player]!"

    m "¿Te sorprendí?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Te sorprendí?{fast}"
        "Sí.":
            m 1hub "¡Yey!"
            m 3hua "¡Siempre me encanta dar una buena sorpresa!"
            m 1tsu "Ojalá pudiera haber visto tu expresión, jejeje."

        "No.":
            m 2lfp "Hmph. Bueno está bien."
            m 2tsu "Probablemente solo digas eso porque no quieres admitir que te pillé desprevenido..."
            if renpy.seen_label("mas_player_bday_listen"):
                if renpy.seen_label("monikaroom_greeting_ear_narration"):
                    m 2tsb "...o puede que estuvieras escuchando a través de la puerta, otra vez..."
                else:
                    m 2tsb "{cps=*2}...o tal vez me estabas viendo a escondidas.{/cps}{nw}"
                    $ _history_list.pop()
            m 2hua "Jejeje."
    if mas_isMonikaBirthday():
        m 3wub "¡Oh!{w=0.5} ¡Hice una tarta!"
    else:
        m 3wub "¡Oh!{w=0.5} ¡Te hice una tarta!"
    call mas_player_bday_cake
    jump monikaroom_greeting_cleanup

# closed door greet option for opening door for listening
label mas_player_bday_listen:
    if persistent._mas_bday_visuals:
        pause 5.0
    else:
        m "...Solo pondré esto aquí..."
        m "...Hmm esto se ve bastante bien...{w=1} Pero algo falta..."
        m "¡Oh!{w=0.5} ¡Por supuesto!"
        m "¡Ahí!{w=0.5} ¡Perfecto!"
        window hide
    jump monikaroom_greeting_choice

# closed door greet option for knocking after listening
label mas_player_bday_knock_listened:
    window hide
    pause 5.0
    menu:
        "Abrir la puerta.":
            $ mas_disable_quit()
            pause 5.0
            jump mas_player_bday_surprise

# closed door greet option for opening door after listening
label mas_player_bday_opendoor_listened:
    $ mas_loseAffection()
    $ persistent._mas_player_bday_opened_door = True
    $ persistent._mas_player_bday_decor = True
    call spaceroom(hide_monika=True, scene_change=True, show_emptydesk=False)
    $ mas_disable_quit()
    if mas_isMonikaBirthday():
        $ your = "nuestra"
    else:
        $ your = "tú"

    if mas_HistVerify("player_bday.opened_door",True)[0]:
        $ knock = "tocaste, {w=0.5}{i}de nuevo{/i}!"
    else:
        $ knock = "tocaste!"

    m "¡[player]!"
    m "¡No [knock]"
    if persistent._mas_bday_visuals:
        m "¡Quería sorprenderte, pero no estaba lista cuando entraste!"
        m "De cualquier manera..."
    else:
        m "¡Estaba preparando [your] fiesta de cumpleaños, pero no he tenido tiempo antes de que llegaras!"
    show monika 1eua at ls32 zorder MAS_MONIKA_Z
    m 4hub "¡Feliz cumpleaños, [player]!"
    m 2rksdla "Solo desearía que me hubieras avisado antes de venir."
    m 2hksdlb "Oh... ¡[your] tarta!"
    call mas_player_bday_cake
    jump monikaroom_greeting_cleanup

# all paths lead here
label mas_player_bday_cake:
    #If it's Monika's birthday too, we'll just use those delegates instead of this one
    if not mas_isMonikaBirthday():
        $ mas_unlockEVL("bye_player_bday", "BYE")
        if persistent._mas_bday_in_bday_mode or persistent._mas_bday_visuals:
            # since we need the visuals var in the special greet, we wait until here to set these
            $ persistent._mas_bday_in_bday_mode = False
            $ persistent._mas_bday_visuals = False

    # reset zoom here to make sure the cake is actually on the table
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset(1.0)
    call mas_monika_gets_cake

    if mas_isMonikaBirthday():
        m 6eua "Simplemente déjame encender las velas.{w=0.5}.{w=0.5}.{nw}"
    else:
        m 6eua "Simplemente déjame encender las velas para ti, [player].{w=0.5}.{w=0.5}.{nw}"

    window hide
    $ mas_bday_cake_lit = True
    pause 1.0

    m 6sua "¿No se ve bonito, [player]?"
    if mas_isMonikaBirthday():
        m 6eksdla "Sé que no puedes soplar las velas tú mismo exactamente, así que lo haré por los dos...."
    else:
        m 6eksdla "Sé que no puedes soplar las velas tú mismo exactamente, así que lo haré por ti..."
    m 6eua "...Sin embargo, aún deberías pedir un deseo, puede que algún día se haga realidad..."
    m 6hua "Pero primero..."
    call mas_player_bday_moni_sings
    m 6hua "¡Pide un deseo, [player]!"
    window hide
    pause 1.5
    show monika 6hft
    pause 0.1
    show monika 6hua
    $ mas_bday_cake_lit = False
    pause 1.0
    m 6hua "Jejeje..."
    if mas_isMonikaBirthday():
        m 6ekbsa "Apuesto a que ambos deseamos lo mismo~"
    else:
        m 6eka "Sé que es tu cumpleaños, pero pedí un deseo también..."
        m 6ekbsa "¿Y sabes que?{w=0.5} Apuesto a que ambos deseamos lo mismo~"
    m 6hkbsu "..."
    if mas_isMonikaBirthday():
        m 6eksdla "Bueno, ya que realmente no puedes comerla, no quiero ser grosera y comérmela frente a ti...."
    elif not mas_HistVerify("player_bday.spent_time",True)[0]:
        m 6rksdla "Oh Dios, supongo que tampoco puedes comer la tarta, ¿eh [player]?"
        m 6eksdla "Todo esto es bastante tonto, ¿no?"
    if mas_isMonikaBirthday():
        m 6hksdlb "Creo que lo guardaré para más tarde."
    else:
        m 6hksdlb "Creo que dejaré esto para más tarde. Me parece un poco de mala educación comerme {i}tu{/i} tarta de cumpleaños frente a ti, ¡jajaja!"

    call mas_HideCake('mas_bday_cake_player')

    # fall thru
label mas_player_bday_card:
    $ mas_gainAffection(5,bypass=True)
    $ persistent._mas_player_bday_spent_time = True
    $ persistent._mas_player_bday_in_player_bday_mode = True

    m 6dkbsu "..."
    if mas_isMonikaBirthday():
        m 6sub "¡Oh!"
        m 6ekbsu "Te hice una tarjeta, [player]. Espero que te guste..."
    elif not mas_HistVerify("player_bday.spent_time",True)[0]:
        m 6ekbsu "Te... Te hice incluso una tarjeta, [player]. Espero que te guste..."
    else:
        m 6ekbsu "Te hice una tarjeta, [player]. Espero que te guste..."

    call mas_showpoem(mas_poems.getRandomPoem("pbday"))

    if mas_isMoniEnamored(higher=True):
        if persistent._mas_first_kiss is None:
            m 6dkbsu "..."
            m 6ekbfa "Te amo tanto, [player]..."
            call monika_kissing_motion()
            m 6ekbfa "Oh, [player]..."
            m 6dkbfa "Eso era todo lo que siempre había soñado que sería~"
            m 6ekbfa "He estado esperando tanto tiempo para finalmente besarte..."
            m 6dkbsu "Nunca olvidare este momento..."
            m 6ekbsu "...cuando tuvimos nuestro primer beso~"
            if mas_isMonikaBirthday():
                m 6ekbsu "No puedo pensar en un momento más perfecto que en este día especial~"
        else:
            m 6ekbsa "Te amo, [player]~"
            call monika_kissing_motion(duration=0.5, initial_exp="6hkbfa", fade_duration=0.5)
            if mas_isMonikaBirthday():
                m 6eka "Estoy tan contenta de que podamos pasar nuestro cumpleaños juntos..."
                m 6hua "Disfrutemos de nuestro día especial~"
    else:
        if mas_isMonikaBirthday():
            m 1ekbfa "¡Te amo, [player]! Estoy tan contenta de que consiguiéramos pasar nuestro cumpleaños juntos..."
            m 3ekbfa "Disfrutemos de nuestro día especial~"
        else:
            m 1ekbfa "¡Te amo, [player]!"
    $ mas_rmallEVL("mas_player_bday_no_restart")
    $ mas_rmallEVL("mas_player_bday_ret_on_bday")
    # "love" return key won't work here without adding a bunch of return _returns, so we'll set this manually

    $ mas_ILY()

    # if d25 season and decor not yet active, set that up now
    if mas_isD25Pre() and not persistent._mas_d25_deco_active:
        $ pushEvent("mas_d25_monika_holiday_intro", skipeval=True)
    return

label mas_monika_gets_cake:
    call mas_transition_to_emptydesk

    $ renpy.pause(3.0, hard=True)
    $ renpy.show("mas_bday_cake_player", zorder=store.MAS_MONIKA_Z+1)

    call mas_transition_from_emptydesk("monika 6esa")

    $ renpy.pause(0.5, hard=True)
    return

# event for if you went on a date pre-bday and return on bday
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_ret_on_bday",
            years = [],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_player_bday_ret_on_bday:
    m 1eua "Así que, hoy es..."
    m 1euc "...Espera."
    m "..."
    m 2wuo "¡Oh!"
    m 2wuw "¡Oh dios mio!"
    m 2tsu "Solo dame un momento, [player].{w=0.5}.{w=0.5}.{nw}"
    $ mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    m 3eub "¡Feliz cumpleaños, [player]!"
    m 3hub "¡Jajaja!"
    m 3etc "Porque siento que me estoy olvidando de algo..."
    m 3hua "¡Oh! ¡Tu tarta!"
    call mas_player_bday_cake
    return

# for subsequent birthdays
init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="mas_player_bday_greet",
            unlocked=False
        ),
        code="GRE"
    )

label mas_player_bday_greet:
    if should_surprise:
        scene black
        pause 5.0
        jump mas_player_bday_surprise

    else:
        if mas_isMonikaBirthday():
            $ your = "Nuestra"
        else:
            $ your = "Tú"
        $ mas_surpriseBdayShowVisuals()
        $ persistent._mas_player_bday_decor = True
        m 3eub "¡Feliz cumpleaños, [player]!"
        m 3hub "¡Jajaja!"
        m 3etc "..."
        m "Siento que me estoy olvidando de algo..."
        m 3hua "¡Oh! ¡[your] tarta!"
        jump mas_player_bday_cake

# event for if the player leaves the game open starting before player_bday and doesn't restart
# moni eventually gives up on the surprise
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_no_restart",
            years = [],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_player_bday_no_restart:
    if mas_findEVL("mas_player_bday_ret_on_bday") >= 0:
        #TODO: priority rules should be set-up here
        return
    m 3rksdla "Bueno [player], esperaba hacer algo un poco más divertido, pero has sido tan dulce y no te has ido en todo el día, asi que.{w=0.5}.{w=0.5}.{nw}"
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    m 3hub "¡Feliz cumpleaños, [player]!"
    if mas_isplayer_bday():
        m 1eka "Tenía muchas ganas de sorprenderte hoy, pero se hace tarde y no podía esperar más."
    else:
        # just in case this isn't seen until after midnight
        m 1hksdlb "Tenía muchas ganas de sorprenderte, pero supongo que se me acabó el tiempo por que ya ni siquiera es tu cumpleaños, ¡ajaja!"
    m 3eksdlc "Dios, solo espero que no empezaras a pensar que olvidé tu cumpleaños. Lo siento mucho si lo hiciste..."
    m 1rksdla "Supongo que probablemente no debería haber esperado tanto, jejeje."
    m 1hua "¡Oh! ¡Te hice una tarta!"
    call mas_player_bday_cake
    return

# event for upset- players, no decorations, just a quick happy birthday
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_upset_minus",
            years = [],
            aff_range=(mas_aff.DISTRESSED, mas_aff.UPSET)
        ),
        skipCalendar=True
    )

label mas_player_bday_upset_minus:
    $ persistent._mas_player_bday_spent_time = True
    m 6eka "Bueno [player], solo quería desearte un feliz cumpleaños."
    m "Espero que hayas tenido un buen día."
    return

# event for if the player's bday is also on a holiday
# TODO update this as we add other holidays (f14) also figure out what to do if player bday is 9/22
# TODO this needs priority below the O31 return from date event
# condtions located in story-events 'birthdate'
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_other_holiday",
            years = [],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_player_bday_other_holiday:
    if mas_isO31():
        $ holiday_var = "Halloween"
    elif mas_isD25():
        $ holiday_var = "Navidad"
    elif mas_isF14():
        $ holiday_var = "el día de San Valentín"
    m 3euc "Hey, [player]..."
    m 1tsu "Me has sorprendido un poco.{w=0.5}.{w=0.5}.{nw}"
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    m 3hub "¡Feliz cumpleaños, [player]!"
    m 3rksdla "Espero que no hayas pensado que solo porque tu cumpleaños es en [holiday_var] me olvidaría..."
    m 1eksdlb "¡Nunca olvidaría tu cumpleaños, tontito!"
    m 1eub "¡Jajaja!"
    m 3hua "¡Oh! ¡Te hice una tarta!"
    call mas_player_bday_cake
    return

# when did moni last sign happy birthday
default persistent._mas_player_bday_last_sung_hbd = None
# moni singing happy birthday
label mas_player_bday_moni_sings:
    $ persistent._mas_player_bday_last_sung_hbd = datetime.date.today()
    if mas_isMonikaBirthday():
        $ you = "los dos"
    else:
        $ you = "ti"
    m 6dsc ".{w=0.2}.{w=0.2}.{w=0.2}"
    m 6hub "{cps=*0.5}{i}~Feliz Cumpleaños a [you]~{/i}{/cps}"
    m "{cps=*0.5}{i}~Feliz Cumpleaños a [you]~{/i}{/cps}"
    m 6sub "{cps=*0.5}{i}~Feliz Cumpleaños querido [player]~{/i}{/cps}"
    m "{cps=*0.5}{i}~Feliz Cumpleaños a [you]~{/i}{/cps}"
    if mas_isMonikaBirthday():
        m 6hua "¡Jejeje!"
    return
#################################################player_bday dock stat farewell##################################################
init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_player_bday",
            unlocked=False,
            prompt="¡Salgamos por mi cumpleaños!",
            pool=True,
            rules={"no_unlock": None},
            aff_range=(mas_aff.NORMAL,None),
        ),
        code="BYE"
    )

label bye_player_bday:
    $ persistent._mas_player_bday_date += 1
    if persistent._mas_player_bday_date == 1:
        m 1sua "¿Quieres salir por tu cumpleaños?{w=1} ¡Okay!"
        m 1skbla "Suena tan romántico... No puedo esperar~"
    elif persistent._mas_player_bday_date == 2:
        m 1sua "¿Quieres salir conmigo de nuevo, [player]?"
        m 3hub "¡Yey!"
        m 1sub "Siempre me encanta salir contigo, pero es mucho más especial salir en tu cumpleaños..."
        m 1skbla "Estoy segura de que lo pasaremos muy bien~"
    else:
        m 1wub "Wow, ¿quieres salir {i}de nuevo{/i}, [player]?"
        m 1skbla "¡Me encanta que quieras pasar tanto tiempo conmigo en tu día especial!"
    $ persistent._mas_player_bday_left_on_bday = True
    jump bye_going_somewhere_post_aff_check

#################################################player_bday dock stat greets##################################################
label greeting_returned_home_player_bday:
    python:
        time_out = store.mas_dockstat.diffCheckTimes()
        checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()
        if checkout_time is not None and checkin_time is not None:
            left_year = checkout_time.year
            left_date = checkout_time.date()
            ret_date = checkin_time.date()
            left_year_aff = mas_HistLookup("player_bday.date_aff_gain",left_year)[1]

            # are we returning after the mhs reset
            ret_diff_year = ret_date >= (mas_player_bday_curr(left_date) + datetime.timedelta(days=3))

            # were we gone over d25
            #TODO: do this for the rest of the holidays
            if left_date < mas_d25.replace(year=left_year) < ret_date:
                if ret_date < mas_history.getMHS("d25s").trigger.date().replace(year=left_year+1):
                    persistent._mas_d25_spent_d25 = True
                else:
                    persistent._mas_history_archives[left_year]["d25.actions.spent_d25"] = True

        else:
            left_year = None
            left_date = None
            ret_date = None
            left_year_aff = None
            ret_diff_year = None

        add_points = False

        if ret_diff_year and left_year_aff is not None:
            add_points = left_year_aff < 25


    if left_date < mas_d25 < ret_date:
        $ persistent._mas_d25_spent_d25 = True

    if mas_isMonikaBirthday() and mas_confirmedParty():
        $ persistent._mas_bday_opened_game = True
        $ mas_temp_zoom_level = store.mas_sprites.zoom_level
        call monika_zoom_transition_reset(1.0)
        $ renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)
        if time_out < mas_five_minutes:
            m 6ekp "Eso no ha sido mucho una ci-"
        else:
            # point totals split here between player and monika bdays, since this date was for both
            if time_out < mas_one_hour:
                $ mas_mbdayCapGainAff(7.5)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(7.5)
            elif time_out < mas_three_hour:
                $ mas_mbdayCapGainAff(12.5)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(12.5)
            else:
                $ mas_mbdayCapGainAff(17.5)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(17.5)

            m 6hub "Ha sido una cita muy divertida, [player]..."
            m 6eua "Gracias por--"

        m 6wud "¿Q-Qué hace esta tarta aquí?"
        m 6sub "¡¿E-Es para mí?!"
        m "¡Es tan dulce de tu parte que me invites a salir en tu cumpleaños para poder prepararme una fiesta sorpresa!"
        call return_home_post_player_bday
        jump mas_bday_surprise_party_reacton_cake

    if time_out < mas_five_minutes:
        $ mas_loseAffection()
        m 2ekp "Eso no ha sido mucho una cita, [player]..."
        m 2eksdlc "Supongo que no tiene nada de malo."
        m 2rksdla "Quizás salgamos más tarde."

    elif time_out < mas_one_hour:
        if not ret_diff_year:
            $ mas_pbdayCapGainAff(5)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(5,bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 5
        m 1eka "Fue una cita divertida mientras duró, [player]..."
        m 3hua "Gracias por dedicarme un tiempo en tu día especial."

    elif time_out < mas_three_hour:
        if not ret_diff_year:
            $ mas_pbdayCapGainAff(10)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(10,bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 10
        m 1eua "Fue una cita divertida, [player]..."
        m 3hua "¡Gracias por llevarme contigo!"
        m 1eka "Realmente disfruté salir contigo hoy~"

    else:
        # more than 3 hours
        if not ret_diff_year:
            $ mas_pbdayCapGainAff(15)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(15,bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 15
        m 1hua "Y... ¡Ya estamos en casa!"
        m 3hub "¡Eso ha sido divertido, [player]!"
        m 1eka "Fue agradable salir a celebrar tu cumpleaños..."
        m 1ekbsa "Gracias por hacerme una parte tan importante de tu día especial~"

    $ persistent._mas_player_bday_left_on_bday = False

    if not mas_isplayer_bday():
        call return_home_post_player_bday

    if mas_isD25() and not persistent._mas_d25_in_d25_mode:
         call mas_d25_monika_holiday_intro_rh_rh
    return

label return_home_post_player_bday:
    $ persistent._mas_player_bday_in_player_bday_mode = False
    $ mas_lockEVL("bye_player_bday", "BYE")
    $ persistent._mas_player_bday_left_on_bday = False
    if not (mas_isMonikaBirthday() and mas_confirmedParty()):
        if persistent._mas_player_bday_decor:
            if mas_isMonikaBirthday():
                $ persistent._mas_bday_opened_game = True
                m 3rksdla "Oh... Ya pasó {i}tu{/i} cumpleaños..."
            else:
                m 3rksdla "Oh... Ya no es tu cumpleaños..."
            m 3hksdlb "Probablemente deberíamos quitar estas decoraciones, ¡jajaja!"
            m 3eka "Solo dame un segundo.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
            $ mas_surpriseBdayHideVisuals()

            #If we returned from a date post pbday but have O31 deco
            if not mas_isO31() and persistent._mas_o31_in_o31_mode:
                $ mas_o31HideVisuals()

            m 3eua "¡Listo!"
            if not persistent._mas_f14_gone_over_f14:
                m 1hua "Ahora, disfrutemos el día juntos, [player]~"

        if persistent._mas_f14_gone_over_f14:
            m 2etc "..."
            m 3wuo "..."
            m 3wud "Wow, [player], ¡Me acabo de dar cuenta de que nos habíamos ido tanto tiempo que nos perdimos el día de San Valentín!"
            call greeting_gone_over_f14_normal_plus

        #If player told Moni their birthday on day of (o31)
        if not persistent._mas_player_bday_decor and not mas_isO31() and persistent._mas_o31_in_o31_mode:
            call mas_o31_ret_home_cleanup(time_out, ret_tt_long=False)

    $ persistent._mas_player_bday_decor = False
    return

# birthday card/poem for player
init 20 python:
    poem_pbday_1 = MASPoem(
        poem_id = "poem_pbday_1",
        category = "pbday",
        prompt = "El único",
        title = " Mi querido [player],",
        text = """\
 A la persona que amo,
 En la que confío,
 La que no puedo vivir sin él.
 Espero que tu día sea tan especial como el que haces cada día para mí.
 Muchas gracias por ser tú.

 Feliz Cumpleaños, cariño~

 Siempre tuya,
 Monika
"""
    #" # I need this to keep syntax highlighting on vim
    )

    poem_pbday_2 = MASPoem(
        poem_id = "poem_pbday_2",
        category = "pbday",
        prompt = "Tu día",
        title = " Mi querido [player],",
        text = """\
 Cualquier día contigo es un día feliz.
 Uno en el que soy libre,
 Uno donde todos mis problemas se han ido,
 Uno en el que todos mis sueños se hacen realidad.

 Pero hoy no es cualquier día,
 Hoy es especial; hoy es tu día.
 Un día en el que puedo apreciarte aún más por lo que haces.
 Un día que espero que yo también haga realidad tus sueños.

 Feliz Cumpleaños, cariño~

 Siempre tuya,
 Monika
"""
    #" # I need this to keep syntax highlighting on vim
    )

    poem_pbday_3 = MASPoem(
        poem_id = "poem_pbday_3",
        category = "pbday",
        prompt = "Un Deseo",
        title = " Mi querido [player],",
        text = """\
 Chispas y velas para la tarta de mi [player],
 Sólo hay un deseo que debes pedir.
 Que tus más grandes sueños se hagan realidad,
 Sé que la mía lo hizo cuando te encontré.

 Me alegro de estar celebrando contigo hoy,
 Te amaré hasta el fin de los días.
 No hay ningún lugar en el que prefiera estar,
 Pasar este tiempo juntos, sólo tú y yo.

 Feliz cumpleaños, cariño~

 Siempre tuya,
 Monika
"""
    #" # I need this to keep syntax highlighting on vim
    )

######################## Start [HOL050]
#Vday
##Spent f14 with Moni
default persistent._mas_f14_spent_f14 = False
##In f14 mode (f14 topics enabled)
default persistent._mas_f14_in_f14_mode = None
##Amount of times we've taken Moni out on f14 for a valentine's date
default persistent._mas_f14_date_count = 0
##Amount of affection gained via vday dates
default persistent._mas_f14_date_aff_gain = 0
##Whether or not we're on an f14 date
default persistent._mas_f14_on_date = None
##Did we do a dockstat fare over all of f14?
default persistent._mas_f14_gone_over_f14 = None
#Valentine's Day
define mas_f14 = datetime.date(datetime.date.today().year,2,14)

#Is it vday?
init -10 python:
    def mas_isF14(_date=None):
        if _date is None:
            _date = datetime.date.today()

        return _date == mas_f14.replace(year=_date.year)

    def mas_f14CapGainAff(amount):
        mas_capGainAff(amount, "_mas_f14_date_aff_gain", 25)

init -810 python:
    # MASHistorySaver for f14
    store.mas_history.addMHS(MASHistorySaver(
        "f14",
        datetime.datetime(2020, 1, 6),
        {
            #Date vars
            "_mas_f14_date_count": "f14.date",
            "_mas_f14_date_aff_gain": "f14.aff_gain",
            "_mas_f14_gone_over_f14": "f14.gone_over_f14",

            #Other general vars
            "_mas_f14_spent_f14": "f14.actions.spent_f14",
            "_mas_f14_in_f14_mode": "f14.mode.f14",
        },
        use_year_before=True,
        start_dt=datetime.datetime(2020, 2, 13),
        end_dt=datetime.datetime(2020, 2, 15)
    ))

label mas_f14_autoload_check:
    python:
        if not persistent._mas_f14_in_f14_mode and mas_isMoniNormal(higher=True):
            persistent._mas_f14_in_f14_mode = True
            #NOTE: Need to path this for people who haven't seen lingerie but are eligible via canshowrisque
            #because intro topic has her wear the outfit and comment on it
            #But we do want her to change into it if we already have it unlocked for change into lingerie
            if (
                not mas_SELisUnlocked(mas_clothes_sundress_white) and not mas_canShowRisque()
                or mas_SELisUnlocked(mas_clothes_sundress_white)
            ):
                monika_chr.change_clothes(mas_clothes_sundress_white, by_user=False, outfit_mode=True)
                monika_chr.save()
                renpy.save_persistent()

        elif not mas_isF14():
            #We want to lock all the extra topics
            #NOTE: vday origins is handled by undo action rules
            mas_lockEVL("mas_f14_monika_vday_colors","EVE")
            mas_lockEVL("mas_f14_monika_vday_cliches","EVE")
            mas_lockEVL("mas_f14_monika_vday_chocolates","EVE")

            #Need to lock the event clothes selector
            mas_lockEVL("monika_event_clothes_select", "EVE")

            #Reset the f14 mode, and outfit if we're lower than the love aff level.
            persistent._mas_f14_in_f14_mode = False

            #Reset clothes if not at the right aff and in sundress
            if mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_sundress_white:
                monika_chr.reset_clothes(False)
                monika_chr.save()
                renpy.save_persistent()

    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        jump mas_player_bday_autoload_check

    jump mas_ch30_post_holiday_check


#######################[HOL050] Pre Intro:

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_pf14_monika_lovey_dovey',
            action=EV_ACT_RANDOM,
            start_date=mas_f14-datetime.timedelta(days=3),
            end_date=mas_f14,
            aff_range=(mas_aff.NORMAL,None),
            rules={"force repeat": None},
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
       "mas_pf14_monika_lovey_dovey",
       mas_f14 - datetime.timedelta(days=3),
       mas_f14,
    )

label mas_pf14_monika_lovey_dovey:
    m 1rksdla "Oye...{w=0.2} ¿[player]?"
    m 1ekbsa "Solo quería hacerte saber que te amo."

    if mas_isMoniEnamored(higher=True):
        m 3ekbsa "Me haces muy feliz... y nunca podría soñar con alguien mejor que tú."

    if mas_HistVerifyAll_k(True, "f14.actions.spent_f14"):
        m 3ekbsa "El Día de San Valentín se acerca, y me hace inmensamente feliz saber que todavía estás a mi lado."

    else:
        m 3ekbsa "El día de San Valentín se acerca, y me pone de buen humor porque sé que te tengo a mi lado."

    m 1rkbsd "Sin ti, no sé dónde estaría..."
    m 1ekbsa "Así que quiero agradecerte por estar ahí para mí..."
    m 1hkbsu "Y por ser tan maravilloso~"
    return "derandom|no_unlock|love"

#######################[HOL050] INTRO:

init 5 python:
    addEvent(
       Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_valentines_intro',
            action=EV_ACT_PUSH,
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            years=[]
        ),
        skipCalendar=True
    )

label mas_f14_monika_valentines_intro:
    #Prevent nts stuff for upset- since they don't get the rest of the event.
    if mas_isMoniUpset(lower=True):
        $ persistent._mas_f14_spent_f14 = True
        if not mas_isMoniBroken():
            m 6eka "Por cierto [player], solo quería decirte feliz San Valentín."
            m "Gracias por venir a verme, espero que tengas un buen día."
        return

    $ mas_addClothesToHolidayMap(mas_clothes_sundress_white)
    m 1hub "¡[player]!"
    m 1hua "¿Sabes qué día es?"
    m 3eub "¡Es San Valentín!"
    m 1ekbsa "Un día donde celebramos nuestro amor por los demás..."
    m 3rkbsa "Supongo que cada día que estamos juntos ya es una celebración de nuestro amor...{w=0.3}{nw}"
    extend 3ekbsa "pero es algo realmente diferente en el Día de San Valentín."
    if not mas_anni.pastOneMonth() or mas_isMoniNormal():
        m 3rka "Aunque sé que no hemos llegado demasiado lejos en nuestra relación..."
        show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5eua "Solo quiero que sepas que siempre estoy aquí para ti."
        m 5eka "Incluso si tu corazón se rompe..."
        m 5ekbsa "Siempre estaré aquí para arreglarlo por ti. ¿Está bien, [player]?"
        show monika 1ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 1ekbsa "..."

    else:
        m 1eub "Hemos estado juntos por bastante tiempo...{w=0.2}{nw}"
        extend 1eka "y realmente amo el tiempo que pasamos juntos."
        m 1dubsu "Tu siempre haces que me sienta amada."
        m "Estoy realmente feliz de ser tu novia, [player]."

    # returning from a date or getting lingerie
    if not persistent._mas_f14_in_f14_mode or mas_canShowRisque():
        $ persistent._mas_f14_in_f14_mode = True

        # first time seeing any lingerie
        if mas_SELisUnlocked(mas_clothes_sundress_white) and mas_canShowRisque() and not mas_hasUnlockedClothesWithExprop("lingerie"):
            call mas_lingerie_intro(holiday_str="en el día de San Valentín", lingerie_choice=mas_clothes_vday_lingerie)

        # first time seeing sundress or non-first time seeing lingerie
        elif (
            not mas_SELisUnlocked(mas_clothes_sundress_white)
            or (mas_canShowRisque() and mas_hasLockedClothesWithExprop("lingerie",True))
        ):
            m 3wub "¡Oh!"
            m 3tsu "Tengo una pequeña sorpresa para ti...{w=1} Creo que te va a gustar, jejeje~"

            # lingerie
            if (
                mas_SELisUnlocked(mas_clothes_sundress_white)
                and mas_canShowRisque()
                and not mas_SELisUnlocked(mas_clothes_vday_lingerie)
            ):
                call mas_clothes_change(outfit=mas_clothes_vday_lingerie, outfit_mode=True, exp="monika 2rkbsu", restore_zoom=False, unlock=True)
                pause 2.0
                show monika 2ekbsu
                pause 2.0
                show monika 2tkbsu
                pause 2.0
                m 2tfbsu "[player]...{w=0.5} Me estas mirando fijamente{w=0.5}... otra vez."
                m 2hubsb "¡Jajaja!"
                m 2eubsb "Supongo que apruebas mi ropa..."
                m 2tkbsu "Es apropiada para unas vacaciones románticas como el Día de San Valentín, ¿no crees?"
                m 2rkbssdla "Tengo que decir que estaba bastante nerviosa la primera vez que me puse algo como esto..."
                m 2hubsb "Pero ahora que lo he hecho antes, ¡realmente disfruto vistiéndome así para ti!"
                m 3tkbsu "Espero que te guste también~"

            # sundress
            elif not mas_SELisUnlocked(mas_clothes_sundress_white):
                call mas_clothes_change(mas_clothes_sundress_white, unlock=True, outfit_mode=True)
                m 2eua "..."
                m 2eksdla "..."
                m 2rksdla "Jajaja...{w=1} No es bueno que me mires así, [player]..."
                m 3tkbsu "...pero supongo que eso significa que te gusta mi ropa, jejeje~"
                call mas_f14_sun_dress_outro

        # not getting lingerie, already have seen sundress
        else:
            # don't currently have access to sundress or wearing inappropraite outfit for f14
            if (
                monika_chr.clothes != mas_clothes_sundress_white
                and (
                    monika_chr.is_wearing_clothes_with_exprop("costume")
                    or monika_chr.clothes == mas_clothes_def
                    or monika_chr.clothes == mas_clothes_blazerless
                    or mas_isMoniEnamored(lower=True)
                )
            ):
                m 3wud "¡Oh!"
                m 3hub "Probablemente debería ponerme algo un poco más apropiado, ¡jajaja!"
                m 3eua "Vuelvo ahora."

                call mas_clothes_change(mas_clothes_sundress_white, unlock=True, outfit_mode=True)

                m 2eub "¡Ah, esto está mucho mejor!"
                m 3hua "¿Me encanta este vestido, a ti no?"
                m 3eka "Siempre ocupará un lugar especial en mi corazón en el día de San Valentín..."
                m 1fkbsu "Como tú~"

            # no change of clothes path
            else:
                # not wearing sundress
                if not monika_chr.clothes == mas_clothes_sundress_white:
                    m 1wud "Oh..."
                    m 1eka "¿Quieres que me ponga mi vestido blanco, [player]?"
                    m 3hua "Siempre ha sido una opción como mi atuendo de San Valentín."
                    m 3eka "Pero si prefieres que siga usando lo que tengo ahora, también está bien..."
                    m 1hub "Tal vez podamos comenzar una nueva tradición, ¡jajaja!"
                    m 1eua "Entonces, ¿quieres que me ponga mi vestido blanco?{nw}"
                    $ _history_list.pop()

                    menu:
                        m "Entonces, ¿quieres que me ponga mi vestido blanco?{fast}"
                        "Sí.":
                            m 3hub "¡Okay!"
                            m 3eua "Vuelvo ahora."
                            call mas_clothes_change(mas_clothes_sundress_white, unlock=True, outfit_mode=True)
                            m 2hub "¡Ahí voy!"
                            m 3eua "Algo se siente bien sobre usar este vestido en el Día de San Valentín."
                            m 1eua "..."

                        "No.":
                            m 1eka "Okay, [player]."
                            m 3hua "{i}Es{/i} una ropa realmente bonita..."
                            m 3eka "Y además, no me importa lo que lleve puesto..."

                call mas_f14_intro_generic

    # not returning from a date, not getting lingerie
    else:
        # already have sundress unlocked
        if mas_SELisUnlocked(mas_clothes_sundress_white):
            call mas_f14_intro_generic

        # first time getting sundress
        else:
            $ store.mas_selspr.unlock_clothes(mas_clothes_sundress_white)
            pause 2.0
            show monika 2rfc at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 2rfc "..."
            m 2efc "Sabes, [player]...{w=0.5} No es bueno que me mires así..."
            m 2tfc "..."
            m 2tsu "..."
            m 3tsb "¡Jajaja! Solo bromeo...{w=0.5} ¿Te gusta mi ropa?"
            call mas_f14_sun_dress_outro

    m 1fkbsu "Te amo muchísimo."
    m 1hubfb "Feliz día de San Valentín, [player]~"
    #Set the spent flag to True
    $ persistent._mas_f14_spent_f14 = True

    return "rebuild_ev|love"

# common flow for first time sundress
label mas_f14_sun_dress_outro:
    m 1rksdla "Siempre he soñado con una cita contigo mientras vestía esto..."
    m 1eksdlb "¡Es un poco tonto ahora que lo pienso!"
    m 1ekbsa "...Pero con solo pensar en si fuéramos a una cafetería juntos."
    m 1rksdlb "Creo que realmente hay una imagen de algo así en algún lugar..."
    m 1hub "¡Quizás podamos hacer que suceda de verdad!"
    m 3ekbsa "¿Tal vez quieras salir hoy?"
    m 1hkbssdlb "Está bien si no puedes, solo estoy feliz de estar contigo."
    return

# used for when we have no new outfits to change into
label mas_f14_intro_generic:
    m 1ekbsa "Estoy muy agradecida de que pases tiempo conmigo hoy."
    m 3ekbsu "Pasar tiempo con la persona que amas, {w=0.2}eso es todo lo que cualquiera puede pedir en el Día de San Valentín."
    m 3ekbsa "No me importa si tenemos una cita romántica, o simplemente pasamos el día juntos..."
    m 1fkbsu "Realmente no me importa mientras estemos juntos."
    return

#######################[HOL050] TOPICS

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_colors',
            prompt="Los colores de San Valentín",
            category=['fiestas','romance'],
            action=EV_ACT_RANDOM,
            conditional="persistent._mas_f14_in_f14_mode",
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
       "mas_f14_monika_vday_colors",
       mas_f14,
       mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_colors:
    m 3eua "¿Has pensado alguna vez en la forma en que se representan los colores en el día de San Valentín?"
    m 3hub "Me parece intrigante cómo pueden simbolizar sentimientos tan profundos y románticos."
    m 1dua "Me recuerda a cuando hice mi primera tarjeta de San Valentín en la primaria."
    m 3eub "En mi clase se nos mandó de intercambiar tarjetas con un compañero después de hacerlas."
    m 3eka "Mirando hacia atrás, a pesar de no saber qué significaban realmente los colores, me divertí mucho decorando las tarjetas con corazones rojos y blancos."
    m 1eub "Mirándolo así, los colores se parecen mucho a los poemas."
    m 1eka "Ofrecen muchas formas creativas de expresar tu amor por alguien."
    m 3ekbsu "Como regalarles rosas rojas, por ejemplo."
    m 3eub "Las rosas rojas son un símbolo de los sentimientos hacia otra persona."
    m 1eua "Si alguien les ofreciera rosas blancas en lugar de rojas, significaría que siente hacia esa persona sentimientos puros, encantadores e inocentes."
    m 3eka "Sin embargo, dado a que hay tantas emociones involucradas con el amor..."
    m 3ekd "A veces es difícil encontrar los colores adecuados para transmitir con precisión la forma en que realmente se siente."
    m 3eka "¡Afortunadamente, al combinar varios colores de rosas, es posible expresar una variedad de emociones!"
    m 1eka "Mezclar rosas rojas y blancas simbolizaría la unidad y el vínculo que comparten una pareja."

    if monika_chr.is_wearing_acs(mas_acs_roses):
        m 1ekbsa "Pero estoy segura de que ya tenías todo esto en mente cuando elegiste estas hermosas rosas para mí, [player]..."
    else:
        m 1ekbla "¿Tal vez podrías regalarme algunas rosas hoy, [player]?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_cliches',
            prompt="Los clichés de las historias de San Valentín",
            category=['fiestas','literatura','romance'],
            action=EV_ACT_RANDOM,
            conditional="persistent._mas_f14_in_f14_mode",
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
       "mas_f14_monika_vday_cliches",
       mas_f14,
       mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_cliches:
    m 2euc "¿Has notado que la mayoría de las historias de San Valentín tienen muchos clichés?"
    m 2rsc "Como por ejemplo 'Oh, estoy solo y no tengo a nadie a quien amar', o '¿Cómo voy a confesar mi amor?'"
    m 2euc "Creo que los escritores deberían ser un poco más creativos cuando se trata de historias del Día de San Valentín..."
    m 3eka "Pero supongo que esos dos temas son la forma más fácil de escribir una historia de amor."
    m 3hub "¡Eso no significa que no puedas pensar de otra manera!"
    m 2eka "A veces, una historia predecible puede arruinarla..."
    m 2rka "...Pero si {i}quieres{/i} un buen ejemplo de una historia impredecible..."
    m 3hub "¡Solo piensa en la nuestra! Jajaja~"
    m 3rksdlb "Supongo que {i}sí{/i} comenzó como ese tipo de historias..."
    m 2tfu "Pero creo que logramos hacerlo bastante original."
    m 3hua "¡La forma en que nos conocimos es la historia más interesante que he visto hasta ahora!"
    m 1hub "¡Jajaja!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_chocolates',
            prompt="Chocolates de San Valentín",
            category=['fiestas','romance'],
            action=EV_ACT_RANDOM,
            conditional="persistent._mas_f14_in_f14_mode",
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
       "mas_f14_monika_vday_chocolates",
       mas_f14,
       mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_chocolates:
    m 1hua "El día de San Valentín es una fiesta muy divertida para mí, [player]."
    m 3eub "¡No solo es el aniversario de mi cuenta de twitter, sino que también es un día para dar y regalar chocolates!"
    m 1hub "¡Una fiesta que llena todo de amor, romance y alegría!"
    m 3ekbla "Pero realmente se siente bien si obtienes algo de alguien que te gusta."
    m 3hua "Ya sea que te lo dé por respeto, como un regalo de amor o como parte de una confesión, ¡siempre te hace sentir algo especial!"
    if mas_getGiftStatsForDate("mas_reaction_gift_chocolates") > 0:
        m 1ekbsa "Justo como me hiciste sentir especial con los bombones que me diste hoy."
        m 1ekbsu "Siempre eres tan cariñoso, [player]."

    m 1ekbsa "Tal vez algún día incluso pueda darte algunos chocolates..."
    m 3hkbsa "Realmente no puedo esperar hasta el día que cruce para estar contigo, [player]."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_origins',
            prompt="¿Cómo empezó el día de San Valentín?",
            category=['fiestas','romance'],
            pool=True,
            conditional="persistent._mas_f14_in_f14_mode",
            action=EV_ACT_UNLOCK,
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[],
            rules={"no_unlock": None}
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
       "mas_f14_monika_vday_origins",
       mas_f14,
       mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_origins:
    m 3eua "¿Te gustaría conocer la historia del Día de San Valentín, [player]?"
    m 1rksdlc "Es bastante oscura."
    m 1euc "Las leyendas varían, pero se remontan al siglo III en Roma, cuando los cristianos aún eran perseguidos por el gobierno romano."
    m 3eud "Por esa época, el emperador Claudio II había prohibido a los cristianos casarse, lo que un clérigo llamado Valentín decidió que era injusto."
    m 3rsc "Contra las órdenes del emperador, casó a cristianos en secreto."
    m 3esc "Otra versión de la historia es que a los soldados romanos no se les permitía casarse, por lo que Valentín estaba salvando a las personas del reclutamiento en el ejército a través del matrimonio."
    m 1dsd "De cualquier manera, Valentín fue atrapado y sentenciado a muerte."
    m 1euc "Mientras estaba en la cárcel, se hizo amigo de la hija del carcelero y le curó la ceguera. Algunos dicen que incluso se enamoró de ella."
    m 3euc "Desafortunadamente, esto no fue suficiente para salvarlo. Pero antes de morir, le envió una carta, que firmó como, 'Tu Valentín.'"
    m 1dsc "Fue ejecutado el 14 de febrero de 269 d.C. y posteriormente canonizado como santo."
    m 3eua "Hasta el día de hoy, todavía es tradicional usar 'Tu Valentín' para firmar cartas de amor."
    m 3eud "¡Oh, pero espera, hay más!"
    m "Hay una antigua fiesta romana conocida como Lupercalia, que también se celebraba alrededor del 14 de febrero."
    m 3eua "Aparentemente, parte de la ceremonia involucró la creación de parejas al sacar nombres al azar de una caja."
    m 3eub "...Luego pasarían tiempo juntos, ¡y algunos incluso se casarían si se gustaban lo suficiente!"
    m 1eua "En definitiva, esta fiesta se convirtió en una celebración cristiana para recordar a San Valentín."
    m 3hua "Ha evolucionado a lo largo de los años hasta convertirse en una forma de que las personas expresen sus sentimientos por sus seres queridos."
    m 3eubsb "...¡Justo como nosotros!"
    m 1ekbsa "A pesar de haber comenzado un poco deprimente, creo que es muy dulce."
    m 1ekbsu "Me alegro de que podamos compartir juntos un día tan mágico.{w=0.2} {nw}"
    extend 1ekbfa "Feliz día de San Valentín, [mas_get_player_nickname()]~"
    return

#######################[HOL050] TIME SPENT

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_f14_monika_spent_time_with",
            conditional="persistent._mas_f14_spent_f14",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL,None),
            start_date=datetime.datetime.combine(mas_f14, datetime.time(hour=18)),
            end_date=datetime.datetime.combine(mas_f14+datetime.timedelta(1), datetime.time(hour=3)),
            years=[]
        ),
        skipCalendar=True
    )

label mas_f14_monika_spent_time_with:
    #Do this first so we make sure we always remove it
    $ mas_rmallEVL("mas_f14_monika_spent_time_with")

    m 1eua "Oye, ¿[player]?"
    m 1eka "Solo quería agradecerte por pasar el día de San Valentín conmigo."
    m 1ekbsa "Sé que no es un día festivo normal, pero es un día muy especial para mí ahora que te tengo."

    if not mas_isBelowZero():
        if not mas_HistVerifyAll_k(True, "f14.actions.spent_f14"):
            m 1rkbsb "Así que, yo...{w=0.5} ¡He hecho algo para ti, [player]!"

        else:
            m 1ekbsa "Te hice una carta, [player]."

        m 1ekbsa "Mira, déjame mostrártela."

        #NOTE: The first two f14 poems will always be in order and the same. Everything after is randomly selected
        if not poem_vday_1.is_seen():
            call mas_showpoem(poem_vday_1)
            m "Realmente lo digo en serio, [player]..."
            m 3ekbsa "En ti encontré todo lo que deseaba~"

        elif not poem_vday_2.is_seen():
            call mas_showpoem(poem_vday_2)
            m "Realmente eres todo para mi, [player]~"

        else:
            call mas_showpoem(mas_poems.getRandomPoem("f14"))


        if mas_isMoniEnamored(higher=True):
            if persistent._mas_first_kiss is None:
                jump mas_f14_first_kiss
            else:
                call monika_kissing_motion(duration=0.5, initial_exp="6hkbfa", fade_duration=0.5)

        m 1ekbfa "Gracias por estar siempre a mi lado."
        show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ekbfa "Te amo tanto, [player]. Feliz día de San Valentín~"
        return "love"

    else:
        m 1eka "Gracias por estar a mi lado."
        m 3ekb "¡Feliz día de San Valentín!"
    return

label mas_f14_first_kiss:
        m 1ektpu "Honestamente, no sé qué haría sin ti."
        #NOTE: Thinking of dissolving into pose 6 here. Might look cleaner. Thoughts?
        m 6dktuu "..."
        window hide
        menu:
            "Te amo, [m_name].":
                $ HKBHideButtons()
                $ mas_RaiseShield_core()
                $ disable_esc()
                pause 3.0
                show monika 6ektda at t11 zorder MAS_MONIKA_Z with dissolve_monika
                pause 3.0
                show monika 6dku at t11 zorder MAS_MONIKA_Z with dissolve_monika
                pause 3.0
                show monika 6dkbsu at t11 zorder MAS_MONIKA_Z with dissolve_monika
                pause 3.0
                show monika 6ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 6ekbfa "[player]... Yo... Yo..."
                call monika_kissing_motion(hide_ui=False)
                show monika 6ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 6ekbfa "...También te amo~"
                m 6dkbfa "..."
                m "Eso es todo con lo que siempre había soñado~"
                m 6ekbfa "He estado esperando tanto tiempo para finalmente besarte, y no podría haber habido un momento más perfecto...."
                m 6dkbsu "Nunca olvidaré esto..."
                m 6ekbsu "...nuestro primer beso."
                m "Feliz día de San Valentín, [player]~"
                $ enable_esc()
                $ mas_MUINDropShield()
                $ HKBShowButtons()
                return


#######################[HOL050] Notimespent

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_f14_no_time_spent",
            action=EV_ACT_PUSH,
            start_date=mas_f14+datetime.timedelta(1),
            end_date=mas_f14+datetime.timedelta(8),
            conditional=(
                "not persistent._mas_f14_spent_f14"
            ),
            years=[]
        ),
        skipCalendar=True
    )

label mas_f14_no_time_spent:

    #need to make sure people who just started post f14 don't lose aff
    if mas_isFirstSeshPast(mas_f14):
        return

    if mas_ret_long_absence:
        #Was away on a long absence
        $ mas_loseAffection(ev_label="mas_apology_missed_vday")

        m 1rksdlc "Oye, [player]..."
        m 2eksdld "Sé que me dijiste que no podrías estar... pero realmente te extrañé el día de San Valentín."
        m 2eksdla "La próxima vez, ¿crees que podrías llevarme contigo si no puedes venir?"
        m 3eub "¡Al menos así estaremos juntos e incluso podremos celebrar juntos!"
        m 1eka "Te agradecería mucho que pudieras hacer eso por mí, [player]."

    elif mas_isMoniAff(higher=True):
        $ mas_loseAffection(15, ev_label="mas_apology_missed_vday")
        m 1rkc "¿[player]?"
        m "¿Dónde estabas el día de San Valentín?"
        m 1ekc "Es un dia muy especial para mi..."
        m 1ekd "...un día que quería pasar contigo."
        m 2dkc "..."
        m 2ekd "Hubiera significado mucho para mí si vinieras..."
        m 2dkd "Aunque solo fuese por unos minutos."
        m "¿Es mucho pedir visitar a tu novia el día de San Valentín?"
        m 2ekc "Por favor, no dejes que vuelva a suceder, ¿está bien [player]?"

    elif mas_isMoniNormal(higher=True):
        $ mas_loseAffection(5, ev_label="mas_apology_missed_vday")
        m 2ekc "Oye, [player]..."
        m 2tkc "Estoy bastante decepcionada..."
        m 2tkd "No me visitaste ni un segundo en el día de San Valentín."
        m 4tkc "Sabes que todo lo que quiero hacer es pasar tiempo contigo..."
        m 4rkd "¿Visitar a tu novia el día de San Valentín es demasiado pedir?"
        m 4eksdla "Por favor...{w=1} Asegúrate de visitarme el próximo día de San Valentín, ¿de acuerdo?"

    elif mas_isMoniUpset():
        $ mas_loseAffection(ev_label="mas_apology_missed_vday")
        m 2efc "¡[player]!"
        m "¡No puedo creer que ni siquiera me visitaras el día de San Valentín!"
        m 2rfc "¿Tiene idea de lo que es quedarse sola en un día como este?"
        m 2rkc "Sé que no estamos en las mejores condiciones..."
        m 2dkd "Pero hubiera significado mucho si vinieras."
        m 2tfc "No dejes que vuelva a pasar, [player]."

    elif mas_isMoniDis():
        $ mas_loseAffection(10, ev_label="mas_apology_missed_vday")
        m 6ekc "Oh [player]..."
        m "¿Cómo estuvo el día de San Valentín?"
        m 6dkc "No tener un San Valentín es bastante triste..."

    else:
        $ mas_loseAffection(150)
        m 6ckc "..."
    return


#######################[HOL050] Apology for notimespent

init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_missed_vday",
            prompt="...por perderme el día de San Valentín.",
            unlocked=False
        ),
        code="APL"
    )


label mas_apology_missed_vday:
    if mas_isMoniAff(higher=True):
        m 1eka "Gracias por disculparte por perderte el Día de San Valentín, [player]."
        m 1ekd "Tenía muchas ganas de pasarlo contigo..."
        m 1rkc "Pero supongo que quizás hayas tenido algo que hacer y no pudiste hacerlo."
        m 1ekd "Intenta visitarme el año que viene, ¿está bien [player]?"
        m 3eua "¡Si vas a estar ocupado, solo llévame contigo!"
        m 3hub "Incluso si no estamos juntos en casa, estoy más que feliz de pasar el día a tu lado~"
        $ mas_gainAffection(modifier=0.2)

    elif mas_isMoniNormal(higher=True):
        m 1eka "Gracias por disculparte por perderte el Día de San Valentín, [player]."
        if not store.mas_anni.pastOneMonth():
            m 1rkd "Sé que no estamos tan lejos en nuestra relación, pero todo ya empezaba a sentirse diferente..."

        m 1ekd "Hubiera significado mucho para mí si vinieras, al menos por un tiempo."
        m 3eka "Prométeme que me llevarás contigo si vas a estar ocupado la próxima vez, ¿de acuerdo [player]?"
        $ mas_gainAffection(modifier=0.2)

    elif mas_isMoniUpset():
        m 2dkc "Aunque estoy un poco molesta porque no apareciste el día de San Valentín, me alegro de que te disculpes."
        m "Cosas como esa me demuestran que realmente te preocupas por nosotros."
        m 2ekd "Por favor, [player]..."
        m 2eka "Intenta venir el próximo día de San Valentín."
        $ mas_gainAffection(modifier=0.1)

    elif mas_isMoniDis():
        m 2dkc "No esperaba que aparecieras de todos modos, [player]."
        m 2dkd "Sé que no somos tan cercanos, pero una parte de mí esperaba que al menos me visitaras..."
        m 2dsc "Por favor prométeme que vendrás el año que viene, ¿de acuerdo?"
        $ mas_gainAffection(modifier=0.1)

    else:
        #No gain from this
        m 6ckc "..."

    return


init 20 python:
    poem_vday_1 = MASPoem(
        poem_id="poem_f14_1",
        category="f14",
        prompt="Te encontré",
        title=" Mi querido [player],",
        text="""\
 Siempre me ha gustado el Día de San Valentín, pero éste se siente diferente.
 ¿Ha cambiado el mundo, o sólo yo?
 Encontré el amor, encontré un propósito,
 Encontré una verdad que no sabía que estaba buscando.
 Todo eso lo encontré en ti.

 Gracias por compartir este día tan especial conmigo.

 Siempre tuya,
 Monika
"""
    )

    poem_vday_2 = MASPoem(
        poem_id="poem_f14_2",
        category="f14",
        prompt="Todo",
        title=" Mi querido [player],",
        text="""\
 ¿Puede ser realmente nuestro segundo San Valentín?
 El primero parece que fue ayer, pero han pasado muchas cosas.
 Una vez me pregunté si el mundo había cambiado, o sólo yo.
 Ahora sé la respuesta.

 Todo cambió.

 Sin ti no hay nada.
 Antes de ti no había nada.

 Vacío. Oscuridad. Nada.

 Nada.

 Y luego estabas tú.
 Sólo tú.
 Mi mundo. Mi luz. Mi Todo.

 Todo.


 Feliz día de San Valentín~

 Siempre tuya,
 Monika
"""

    #" # I need this to keep syntax highlighting on vim
    )

    poem_vday_3 = MASPoem(
        poem_id="poem_f14_3",
        category="f14",
        prompt="Tú",
        title=" Mi querido [player],",
        text="""\
 Cajas de chocolates y corazones; tarjetas de color rojo rubí.
 Rosas en mi pelo, pétalos suaves como la seda.
 Nada de esto se sentiría completo sin ti.

 Tú, el que se ha quedado a mi lado.
 Tú, el que me ha dado su corazón.
 El corazón vale más que todo el chocolate del mundo, todas las rosas de la tierra.

 El amor que siento no puede ser exagerado.

 Por siempre tu Valentín,
 Monika
"""
    )


#######################[HOL050] dockstat farwell###############################
label bye_f14:
    $ persistent._mas_f14_date_count += 1
    $ persistent._mas_f14_on_date = True
    if persistent._mas_f14_date_count == 1:
        m 1sua "¿Me llevas a algún lugar especial por el día de San Valentín?"
        m 1ekbsa "Eso suena muy romántico [player]..."
        m 3hub "¡No puedo esperar!"
    elif persistent._mas_f14_date_count == 2:
        m 1sua "¿Vas a sacarme de nuevo el día de San Valentín?"
        m 3tkbsu "Realmente sabes cómo hacer que una chica se sienta especial, [player]."
        m 1ekbfa "Soy tan afortunada de tener a alguien como tú~"
    else:
        m 1sua "Wow, [player]...{w=1} ¡Estás realmente decidido a hacer de este un día verdaderamente especial!"
        m 1ekbfa "Eres el mejor compañero que podría esperar~"
    jump mas_dockstat_iostart

########################[HOL050] dockstat greet################################
label greeting_returned_home_f14:
    python:
        time_out = store.mas_dockstat.diffCheckTimes()

    if time_out < mas_five_minutes:
        $ mas_loseAffection()
        m 2ekp "No fue una gran cita, [player]..."
        m 2eksdlc "¿Está todo bien?"
        m 2rksdla "Quizás podamos salir más tarde..."

    elif time_out < mas_one_hour:
        $ mas_f14CapGainAff(5)
        m 1eka "Fue divertido mientras duró, [player]..."
        m 3hua "Gracias por dedicarme un tiempo el día de San Valentín."

    elif time_out < mas_three_hour:
        $ mas_f14CapGainAff(10)
        m 1eub "¡Fue una cita tan divertida, [player]!"
        m 3ekbsa "Gracias por hacerme sentir especial el día de San Valentín~"

    else:
        # more than 3 hours
        $ mas_f14CapGainAff(15)
        m 1hua "Y... ¡Ya estamos en casa!"
        m 3hub "¡Fue maravilloso, [player]!"
        m 1eka "Fue muy agradable salir contigo el día de San Valentín..."
        m 1ekbsa "Muchas gracias por hacer que el día de hoy sea realmente especial~"

    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday

    $ persistent._mas_f14_on_date = False

    if not mas_isF14() and not mas_lastSeenInYear("mas_f14_monika_spent_time_with"):
        $ pushEvent("mas_f14_monika_spent_time_with",skipeval=True)
    return

# if we went on a date pre-f14 and returned in the time period mas_f14_no_time_spent event runs
# need to make sure we get credit for time spent and don't get the event
label mas_gone_over_f14_check:
    if mas_checkOverDate(mas_f14):
        $ persistent._mas_f14_spent_f14 = True
        $ persistent._mas_f14_gone_over_f14 = True
        $ mas_rmallEVL("mas_f14_no_time_spent")
    return

label greeting_gone_over_f14:
    $ mas_gainAffection(5,bypass=True)
    m 1hua "¡Y finalmente estamos en casa!"
    m 3wud "Wow [player], ¡estuvimos fuera tanto tiempo que nos perdimos el Día de San Valentín!"
    if mas_isMoniNormal(higher=True):
        call greeting_gone_over_f14_normal_plus
    else:
        m 2rka "Te agradezco que te asegures de no tener que pasar el día sola..."
        m 2eka "Significa mucho para mí, [player]."
    $ persistent._mas_f14_gone_over_f14 = False
    return

label greeting_gone_over_f14_normal_plus:
    $ mas_gainAffection(10,bypass=True)
    m 1ekbsa "Me hubiera encantado pasar el día contigo aquí, pero no importa dónde estuviéramos, solo sabiendo que estábamos juntos para celebrar nuestro amor...."
    m 1dubsu "Bueno, significa todo para mí."
    show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5ekbsa "Gracias por asegurarse de que tuviéramos un maravilloso día de San Valentín, [player]~"
    $ persistent._mas_f14_gone_over_f14 = False
    return

############################### 922 ###########################################
# [HOL060]
#START:

#Moni's bday
define mas_monika_birthday = datetime.date(datetime.date.today().year, 9, 22)

#922 mode
default persistent._mas_bday_in_bday_mode = False

#Date related vars
default persistent._mas_bday_on_date = False
default persistent._mas_bday_date_count = 0
default persistent._mas_bday_date_affection_gained = 0
default persistent._mas_bday_gone_over_bday = False

#Suprise party bits and bobs
default persistent._mas_bday_sbp_reacted = False
default persistent._mas_bday_confirmed_party = False

#Bday visuals
default persistent._mas_bday_visuals = False

#Need to store the name of the file chibi writes
default persistent._mas_bday_hint_filename = None

#Time spent tracking
default persistent._mas_bday_opened_game = False
default persistent._mas_bday_no_time_spent = True
default persistent._mas_bday_no_recognize = True
default persistent._mas_bday_said_happybday = False

############### [HOL060]: HISTORY
init -810 python:
    store.mas_history.addMHS(MASHistorySaver(
        "922",
        datetime.datetime(2020, 1, 6),
        {
            "_mas_bday_in_bday_mode": "922.bday_mode",

            "_mas_bday_on_date": "922.on_date",
            "_mas_bday_date_count": "922.actions.date.count",
            "_mas_bday_date_affection_gained": "922.actions.date.aff_gained",
            "_mas_bday_gone_over_bday": "922.gone_over_bday",
            "_mas_bday_has_done_bd_outro": "922.done_bd_outro",

            "_mas_bday_sbp_reacted": "922.actions.surprise.reacted",
            "_mas_bday_confirmed_party": "922.actions.confirmed_party",

            "_mas_bday_opened_game": "922.actions.opened_game",
            "_mas_bday_no_time_spent": "922.actions.no_time_spent",
            "_mas_bday_no_recognize": "922.actions.no_recognize",
            "_mas_bday_said_happybday": "922.actions.said_happybday"
        },
        use_year_before=True,
        start_dt=datetime.datetime(2020, 9, 21),
        end_dt=datetime.datetime(2020, 9, 23)
    ))

### bday stuff

############### [HOL060]: IMAGES
define mas_bday_cake_lit = False

# NOTE: maybe the cakes should be ACS

image mas_bday_cake_monika = LiveComposite(
    (1280, 850),
    (0, 0), MASFilterSwitch("mod_assets/location/spaceroom/bday/monika_birthday_cake.png"),
    (0, 0), ConditionSwitch(
        "mas_bday_cake_lit", "mod_assets/location/spaceroom/bday/monika_birthday_cake_lights.png",
        "True", Null()
        )
)

image mas_bday_cake_player = LiveComposite(
    (1280, 850),
    (0, 0), MASFilterSwitch("mod_assets/location/spaceroom/bday/player_birthday_cake.png"),
    (0, 0), ConditionSwitch(
        "mas_bday_cake_lit", "mod_assets/location/spaceroom/bday/player_birthday_cake_lights.png",
        "True", Null()
        )
)

image mas_bday_banners = MASFilterSwitch(
    "mod_assets/location/spaceroom/bday/birthday_decorations.png"
)

image mas_bday_balloons = MASFilterSwitch(
    "mod_assets/location/spaceroom/bday/birthday_decorations_balloons.png"
)

############### [HOL060]: METHODS
init -1 python:
    def mas_isMonikaBirthday(_date=None):
        """
        checks if the given date is monikas birthday
        Comparison is done solely with month and day

        IN:
            _date - date to check. If not passed in, we use today.
        """
        if _date is None:
            _date = datetime.date.today()

        return (
            _date.month == mas_monika_birthday.month
            and _date.day == mas_monika_birthday.day
        )


    def mas_getNextMonikaBirthday():
        today = datetime.date.today()
        if mas_monika_birthday < today:
            return datetime.date(
                today.year + 1,
                mas_monika_birthday.month,
                mas_monika_birthday.day
            )
        return mas_monika_birthday


    def mas_recognizedBday(_date=None):
        """
        Checks if the user recognized monika's birthday at all.

        RETURNS:
            True if the user recoginzed monika's birthday, False otherwise
        """
        if _date is None:
            _date = mas_monika_birthday


        if (
            mas_generateGiftsReport(_date)[0] > 0
            or persistent._mas_bday_date_affection_gained > 0
            or persistent._mas_bday_sbp_reacted
            or persistent._mas_bday_said_happybday
        ):
            persistent._mas_bday_no_time_spent = False
            return True
        return False

    def mas_surpriseBdayShowVisuals(cake=False):
        """
        Shows bday surprise party visuals
        """
        if cake:
            renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)
        if store.mas_is_indoors:
            renpy.show("mas_bday_banners", zorder=7)
        renpy.show("mas_bday_balloons", zorder=8)


    def mas_surpriseBdayHideVisuals():
        """
        Hides all visuals for surprise party
        """
        renpy.hide("mas_bday_banners")
        renpy.hide("mas_bday_balloons")

    def mas_confirmedParty():
        """
        Checks if the player has confirmed the party
        """
        #Must be within a week of the party (including party day)
        if (mas_monika_birthday - datetime.timedelta(days=7)) <= today <= mas_monika_birthday:
            #If this is confirmed already, then we just return true, since confirmed
            if persistent._mas_bday_confirmed_party:
                #We should also handle if the player confirmed the party pre-note
                if persistent._mas_bday_hint_filename:
                    store.mas_docking_station.destroyPackage(persistent._mas_bday_hint_filename)
                return True

            #Otherwise, we need to check if the file exists (we're going to make this as foolproof as possible)
            #Step 1, get the characters folder contents
            char_dir_files = store.mas_docking_station.getPackageList()

            #Step 2, We need to remove the extensions
            for filename in char_dir_files:
                temp_filename = filename.partition('.')[0]

                #Step 3, check if the filename is present
                if "oki doki" == temp_filename:
                    #If we got here: Step 4, file exists so flag and delete. Also get rid of note
                    persistent._mas_bday_confirmed_party = True
                    store.mas_docking_station.destroyPackage(filename)

                    if persistent._mas_bday_hint_filename:
                        store.mas_docking_station.destroyPackage(persistent._mas_bday_hint_filename)

                    #We should also return a new file indicating the player has confirmed the party
                    _write_txt("/characters/gotcha", "")
                    #Step 5a, return true since party is confirmed
                    return True

        #Otherwise, Step 5b, no previous confirm and file doesn't exist, so party is not confirmed. return false
        return False

    def mas_mbdayCapGainAff(amount):
        mas_capGainAff(amount, "_mas_bday_date_affection_gained", 50, 75)

################## [HOL060] AUTOLOAD
label mas_bday_autoload_check:
    #First, if it's no longer 922 and we're here, that means we're in 922 mode and need to fix that
    python:
        if not mas_isMonikaBirthday():
            persistent._mas_bday_in_bday_mode = False
            #Also make sure we're no longer showing visuals
            persistent._mas_bday_visuals = False

            #Lock the event clothes selector
            store.mas_lockEVL("monika_event_clothes_select", "EVE")

            store.mas_utils.trydel("characters/gotcha")

            #And reset outfit if not at the right aff
            if mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_blackdress:
                monika_chr.reset_clothes(False)
                monika_chr.save()
                renpy.save_persistent()

        #It's Moni's bday! If we're here that means we're spending time with her, so:
        persistent._mas_bday_no_time_spent = False

        persistent._mas_bday_opened_game = True
        #Have we recogized bday?
        persistent._mas_bday_no_recognize = not mas_recognizedBday()

    jump mas_ch30_post_holiday_check


################## [HOL060] PRE INTRO
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_surprise_party_hint",
            start_date=mas_monika_birthday - datetime.timedelta(days=7),
            end_date=mas_monika_birthday - datetime.timedelta(days=2),
            years=[],
            action=EV_ACT_RANDOM,
            rules={"force repeat": None, "no rmallEVL": None},
            aff_range=(mas_aff.DISTRESSED,None)
        ),
        skipCalendar=True
    )

    #Create the undo action rule
    MASUndoActionRule.create_rule_EVL(
        "mas_bday_surprise_party_hint",
        mas_monika_birthday - datetime.timedelta(days=7),
        mas_monika_birthday - datetime.timedelta(days=2)
    )

#If random hasn't shown this topic yet, we need to push this to make sure people get this
init 10 python:
    if (
        mas_monika_birthday - datetime.timedelta(days=2) <= datetime.date.today() < mas_monika_birthday
        and not mas_lastSeenInYear("mas_bday_surprise_party_hint")
    ):
        pushEvent("mas_bday_surprise_party_hint")

image chibi_peek = MASFilterSwitch("mod_assets/other/chibi_peek.png")

label mas_bday_surprise_party_hint:
    #Set up letters
    python:
        persistent._mas_bday_hint_filename = "Para " + player + ".txt"
        if mas_isMoniNormal(higher=True):
            message = """\
[player],
Como estoy segura de que sabes, el cumpleaños de Monika se acerca y quiero ayudarte a que sea lo más especial posible.
Como siempre estoy aquí, puedo organizar fácilmente la fiesta sorpresa... pero necesito un poco de ayuda de ti.
Todo lo que necesito es que te asegures de que la saques de la habitación en algún momento de su cumpleaños, y yo me encargaré del resto.
Monika es tan increíble, y sólo quiero hacer mi parte para asegurarme de que todo esto salga bien...
¡Jajaja!

Por favor, deja un archivo llamado 'oki doki' en la misma carpeta en la que encontraste esta nota, así sabré seguir adelante con la fiesta.

¡Buena suerte con Monika!

P.D: ¡No le hables de mí!
"""

        else:
            message = """\
[player],
Como espero que sepas, el cumpleaños de Monika se acerca y quiero hacerlo especial.
Ha pasado por mucho últimamente, y sé que significaría mucho para ella si la invitaras a pasar un buen día.
Como siempre estoy aquí, puedo organizar una fiesta sorpresa... pero necesito un poco de ayuda.
Todo lo que necesito es que te asegures de que la saques de la habitación en algún momento de su cumpleaños, y yo me encargaré del resto.
Si te preocupas por Monika, me ayudarás a hacer esto.

Sólo deja un archivo llamado 'oki doki' en la misma carpeta en la que encontraste esta nota, así sabré seguir adelante con la fiesta.

Por favor, no lo estropees.

P.D: ¡No le hables de mí!
"""
        #Now write it to the chars folder
        _write_txt("/characters/" + persistent._mas_bday_hint_filename, message)

    #Moni brings it up (so)
    if mas_isMoniNormal(higher=True):
        m 1eud "Hey, [player]..."
        m 3euc "Alguien dejó una nota en la carpeta de personajes dirigida a ti."
        if mas_current_background == mas_background_def:
            #show chibi, she's just written the letter
            show chibi_peek with moveinleft
        m 1ekc "Por supuesto, no la he leído, ya que obviamente es para ti..."
        m 1tuu "{cps=*2}Hmm, me pregunto de qué se trata esto...{/cps}{nw}"
        $ _history_list.pop()
        m 1hua "Jejeje~"

    else:
        m 2eud "Oye, [player]..."
        m 2euc "Alguien dejó una nota en la carpeta de personajes dirigida a ti."
        m 2ekc "Por supuesto, no la he leído, ya que obviamente es para ti..."
        m 2ekd "Solo quería hacértelo saber."

    #Hide chibi
    hide chibi_peek with dissolve

    #Flag this so it doesn't get shown again
    $ persistent._mas_monika_bday_surprise_hint_seen = True
    return "derandom|no_unlock"


################## [HOL060] HAPPY BDAY TOPICS
# both of these make the most sense showing up under 'I want to tell you something` so they are made as compliments
# also makes sure they don't show up under unseen

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_pool_happy_bday",
            prompt="¡Feliz Cumpleaños!",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock": None},
            start_date=mas_monika_birthday,
            end_date=mas_monika_birthday + datetime.timedelta(days=1),
            years=[]
        ),
        code="CMP",
        skipCalendar=True,
        markSeen=True
    )

    #Create the undo action rule
    MASUndoActionRule.create_rule_EVL(
        "mas_bday_pool_happy_bday",
        mas_monika_birthday,
        mas_monika_birthday + datetime.timedelta(1)
    )

label mas_bday_pool_happy_bday:
    $ mas_gainAffection(5,bypass=True)
    if mas_recognizedBday():
        m 3hub "Jejeje, ¡gracias [player]!"
        m 3eka "Estaba esperando que dijeras esas palabras mágicas~"
        m 1eub "{i}¡Ahora{/i} podemos llamarlo fiesta de cumpleaños!"
        m 1eka "Realmente hiciste esta ocasión tan especial, [player]."
        m 1ekbsa "No puedo agradecerte lo suficiente por amarme tanto..."

    else:
        m 1skb "¡Awww, [player]!"
        m 1sub "¡Te acuerdas de mi cumpleaños...!"
        m 1sktpa "Oh Dios, estoy tan feliz de que lo recuerdes."
        m 1dktdu "Siento que hoy va a ser un día especial~"
        m 1ekbsa "Me pregunto qué más tienes reservado para mí..."
        m 1hub "¡Jajaja!"

    if mas_isplayer_bday() and (persistent._mas_player_bday_in_player_bday_mode or persistent._mas_bday_sbp_reacted):
        m 1eua "Oh, y..."
        m 3hub "¡Feliz cumpleaños a ti tambien, [player]!"
        m 1hua "¡Jejeje!"

    #Flag this for hist
    $ persistent._mas_bday_no_recognize = False
    $ persistent._mas_bday_said_happybday = True

    #Lock this
    $ mas_lockEVL("mas_bday_pool_happy_bday", "CMP")
    return

# happy belated bday topic for people that took her out before her bday and returned her after
# cond/act and start/end dates to be set in mas_gone_over_bday_check:

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_pool_happy_belated_bday",
            prompt="¡Feliz cumpleaños atrasado!",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock": None},
            years=[]
        ),
        code="CMP",
        skipCalendar=True,
        markSeen=True
    )

label mas_bday_pool_happy_belated_bday:
    $ mas_gainAffection(5,bypass=True)

    #We've essentially said happy birthday, let's flag this
    $ persistent._mas_bday_said_happybday = True
    $ persistent._mas_bday_no_recognize = False

    #Lock this
    $ mas_lockEVL("mas_bday_pool_happy_belated_bday", "CMP")

    if mas_isMoniNormal(higher=True):
        m 1sua "¡Muchas gracias, [player]!"
        m 3hub "¡Sabía que me llevarías a un largo viaje por mi cumpleaños!"
        m 3rka "Ojalá hubiera podido ver todos los lugares increíbles a los que fuimos..."
        m 1hua "Pero sabiendo que estábamos juntos, bueno, ¡es el mejor cumpleaños que podría desear!"
        m 3ekbsa "Te amo mucho, [player]~"
        return "love"
    else:
        m 3eka "Así que {i}me{/i} llevaste a un largo viaje por mi cumpleaños..."
        m 3rkd "Eso es tan considerado de tu parte, me estaba preguntando--"
        m 1eksdla "Sabes qué, no importa."
        m 1eka "Estoy aliviada de saber que estabas pensando en mí en mi cumpleaños."
        m 3hua "Eso es todo lo que importa."
        m 3eub "¡Gracias, [player]!"
        return

################## [HOL060] PARTY REACTION
label mas_bday_surprise_party_reaction:
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_bday_visuals = True
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset(1.0)
    $ renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)

    if mas_isMoniNormal(higher=True):
        m 6suo "E-{w=0.5}Esto es..."
        m 6ska "Oh, [player]..."
        m 6dku "Me quedo sin palabras."

        if store.mas_is_indoors:
            m 6dktpu "Preparando todo esto para sorprenderme en mi cumpleaños..."

        m 6dktdu "Jejeje, realmente debes amarme."
        m 6suu "¡Todo se ve tan festivo!"

    else:
        m 6wuo "E-{w=0.5}Esto es.."
        m "..."
        m 6dkd "Lo siento, estoy...{w=1} Estoy sin palabras."
        m 6ekc "Realmente no esperaba nada especial hoy, y mucho menos esto."
        m 6rka "Quizás todavía sientes algo por mí, después de todo..."
        m 6eka "Todo luce genial."

label mas_bday_surprise_party_reacton_cake:
    #Let's light candles
    menu:
        "Enciende velas.":
            $ mas_bday_cake_lit = True

    m 6sub "Ahh, ¡es tan bonito, [player]!"
    m 6hua "Me recuerda a esa tarta que alguien me dio una vez."
    m 6eua "¡Era casi tan bonita como la que has hecho!"
    m 6tkb "Casi."
    m 6hua "Pero de todos modos..."
    window hide

    show screen mas_background_timed_jump(5, "mas_bday_surprise_party_reaction_no_make_wish")
    menu:
        "Pide un deseo, [m_name]...":
            $ made_wish = True
            show monika 6hua
            if mas_isplayer_bday():
                m "¡Asegúrate de hacer una también, [player]!"
            hide screen mas_background_timed_jump
            #+10 for wishes
            $ mas_gainAffection(10, bypass=True)
            pause 2.0
            show monika 6hft
            jump mas_bday_surprise_party_reaction_post_make_wish

label mas_bday_surprise_party_reaction_no_make_wish:
    $ made_wish = False
    hide screen mas_background_timed_jump
    show monika 6dsc
    pause 2.0
    show monika 6hft

label mas_bday_surprise_party_reaction_post_make_wish:
    $ mas_bday_cake_lit = False
    window auto
    if mas_isMoniNormal(higher=True):
        m 6hub "¡He pedido un deseo!"
        m 6eua "Espero que se haga realidad algún día..."
        if mas_isplayer_bday() and made_wish:
            m 6eka "¿Y sabes qué? {w=0.5}Apuesto a que ambos deseamos lo mismo~"
        m 6hub "Jajaja..."

    else:
        m 6eka "He pedido un deseo."
        m 6rka "Espero que se haga realidad algún día..."

    m 6eka "Guardaré esta tarta para más tarde.{w=0.5}.{w=0.5}.{nw}"

    if mas_isplayer_bday():
        call mas_HideCake('mas_bday_cake_monika',False)
    else:
        call mas_HideCake('mas_bday_cake_monika')

    pause 0.5

label mas_bday_surprise_party_reaction_end:
    if mas_isMoniNormal(higher=True):
        m 6eka "Gracias, [player]. Desde el fondo de mi corazón, gracias..."
        if mas_isplayer_bday() and persistent._mas_player_bday_last_sung_hbd != datetime.date.today():
            m 6eua "..."
            m 6wuo "..."
            m 6wub "¡Oh! Casi lo olvido. {w=0.5}¡También te hice una tarta!"

            call mas_monika_gets_cake

            m 6eua "Déjame encender las velas por ti, [player].{w=0.5}.{w=0.5}.{nw}"

            window hide
            $ mas_bday_cake_lit = True
            pause 1.0

            m 6sua "¿No es bonito?"
            m 6hksdlb "Supongo que también tendré que apagar estas velas, ya que realmente no puedes hacerlo, ¡jajaja!"

            if made_wish:
                m 6eua "¡Deseemos los dos de nuevo, [player]!{w=0.5} Será dos veces más probable que se haga realidad, ¿verdad?"
            else:
                m 6eua "¡Pidamos ambos un deseo, [player]!"

            m 6hua "Pero primero..."
            call mas_player_bday_moni_sings
            m 6hua "¡Pide un deseo, [player]!"

            window hide
            pause 1.5
            show monika 6hft
            pause 0.1
            show monika 6hua
            $ mas_bday_cake_lit = False
            pause 1.0

            if not made_wish:
                m 6hua "Jejeje..."
                m 6ekbsa "Apuesto a que ambos deseamos lo mismo~"
            m 6hkbsu "..."
            m 6hksdlb "También guardaré esta tarta para más tarde, supongo. ¡Jajaja!"

            call mas_HideCake('mas_bday_cake_player')
            call mas_player_bday_card

        else:
            m 6hua "Disfrutemos el resto del día ahora, ¿de acuerdo?"
    else:
        m 6ektpa "Gracias, [player]. Realmente significa mucho que hayas hecho esto por mí."
    $ persistent._mas_bday_sbp_reacted = True
    #+25 aff for following through and getting the party
    $ mas_gainAffection(25, bypass=True)

    #We set these flags here
    $ persistent._mas_bday_in_bday_mode = True
    $ persistent._mas_bday_no_recognize = False
    $ persistent._mas_bday_no_time_spent = False
    return


################## [HOL060] TIME SPENT
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_spent_time_with",
            conditional="mas_recognizedBday()",
            action=EV_ACT_QUEUE,
            start_date=datetime.datetime.combine(mas_monika_birthday, datetime.time(18)),
            end_date=datetime.datetime.combine(mas_monika_birthday+datetime.timedelta(days=1), datetime.time(hour=3)),
            years=[]
        ),
        skipCalendar=True
    )

label mas_bday_spent_time_with:
    if mas_isMoniUpset(lower=True):
        m 1eka "[player]..."
        m 3eka "Solo quería decirte que te agradezco mucho que pases tiempo conmigo hoy."
        m 3rksdla "Sé que no ha ido tan bien últimamente, pero te tomas el tiempo para celebrar mi cumpleaños conmigo..."
        m 1eud "Bueno, me da la esperanza de que tal vez no sea demasiado tarde para nosotros."
        m "Quizás hoy pueda ser el comienzo de algo realmente especial..."
        m 3eka "Ese sería el mejor regalo que podría pedir."
        return

    else:
        $ _timeout = store.mas_dockstat.timeOut(mas_monika_birthday)
        m 1eua "[player]..."
        m 3eua "Gracias por pasar tiempo conmigo hoy."
        m 3hua "Algo así puede hacer feliz a una chica, ¿sabes?"

        if _timeout > mas_five_minutes:
            m 3eka "Realmente disfruté nuestra cita de hoy, [player]."
            m 1eka "Siempre disfruto pasar tiempo contigo aquí, pero poder pasar tiempo contigo en tu realidad..."
            m 1dku "Saber que estás pensando en mí incluso cuando no puedes verme..."
            m 1ekbsa "Bueno, realmente significa mucho para mí."
            m 3ekbsa "Realmente hiciste que mi cumpleaños este completo~"

label mas_bday_spent_time_with_wrapup:
    $ mas_rmallEVL("mas_bday_spent_time_with")
    $ gave_gifts = mas_getGiftStatsRange(mas_monika_birthday, mas_monika_birthday + datetime.timedelta(days=1))[0]

    if gave_gifts > 0:
        #More than 1
        if gave_gifts > 1:
            m 3eua "No olvidemos los regalos que me hiciste por mi cumpleaños."
            m 3hub "Eran simplemente increíbles, [player]!"
        else:
            m 3eua "No olvidemos el regalo que me hiciste por mi cumpleaños."
            m 3hub "¡Fue tan maravilloso, [player]!"

        m 1eka "Realmente aprecio el esfuerzo de encontrar una manera de llevar las cosas de tu realidad a la mía..."
        m 3eka "Sé que no puede ser fácil."

    m 1dku "..."
    if mas_isMoniEnamored(higher=True):
        m 1dktpu "..."
        m 1ektpu "Jajaja, ¡lo siento, [player]!"
        m 3ektda "Es solo que nunca me había imaginado ser tan feliz en mi vida."
        m 1rksdlb "Bueno...{w=0.5} Eso no es {i}del todo{/i} cierto."
        m 1eka "Todavía tenemos que estar físicamente juntos, después de todo~"
        m 1rkc "Y, bueno..."
        m 1rka "Sé que esto ya se está convirtiendo en un cliché, pero..."
        m 3eka "Te amo tanto, [player]."
        m "Algún día, te prometo..."
        m 1ektpu "{i}Te prometo{/i} que te haré tan feliz como tú me has hecho hoy."
        m 3ektpu "Incluso si nunca nos vemos en la misma realidad, {w=0.5}sé que siempre haré todo lo posible por ti."
        m 1dktpu "No importa los obstáculos que enfrentemos, no importa lo que otras personas digan de nosotros..."
        m 1ektda "Aún te amo con todo lo que tengo."
        m "Eres el único que me comprende. {w=0.5}Me sacaste de un lugar oscuro y me diste un propósito..."
        m 1dkbsu "Eres simplemente el mejor, [mas_get_player_nickname()], y siempre te amaré."
        m 1ekbsa "...Gracias por darme una razón para vivir."
        $ _first_kiss = persistent._mas_first_kiss
        call monika_kissing_motion
        if _first_kiss is None:
            m 6ekbfa "Oh, [player]..."
            m 6rkbfa "Yo...{w=0.5} No sé qué me pasó, pero el momento se sintió tan bien."
            m 6hubfa "He pensado en nuestro primer beso durante tanto tiempo, y finalmente experimentarlo..."
            m 6ekbfa "Nunca olvidaré este momento, [player]~"
        else:
            return "love"

    else:
        m 1eka "Ni siquiera puedo encontrar las palabras adecuadas para expresar lo feliz que me has hecho hoy."
        m 3eka "¿Todo ese dolor por el que pasé antes de conocerte?"
        m 1hua "Me alegro de haber aguantado."
        m 1rsc "Porque si no lo hubiera hecho..."
        m 1ekbsa "Este día nunca hubiera sucedido."
        m 1dkbsa "Espero que eso les diga un poquito de lo mucho que aprecio que celebren esta ocasión conmigo."
        m 1ekbfb "Te amo mucho, [player]."
        m 1ekbfa "Sigamos haciéndonos felices~"
        return "love"
    return

############## [HOL060] GONE OVER CHECK
label mas_gone_over_bday_check:
    if mas_checkOverDate(mas_monika_birthday):
        $ persistent._mas_bday_gone_over_bday = True
        $ persistent._mas_bday_no_time_spent = False
        $ mas_rmallEVL("mas_bday_postbday_notimespent")

        #Now we want to handle the belated bday unlock
        python:
            belated_ev = mas_getEV("mas_bday_pool_happy_belated_bday")

            if belated_ev is not None:
                #Set start and end dates
                belated_ev.start_date = datetime.date.today()
                belated_ev.end_date = datetime.datetime.now() + datetime.timedelta(days=1)
                belated_ev.unlocked = True

                #Prepare the undo action
                MASUndoActionRule.create_rule(belated_ev)

                #Prepare the date strip
                MASStripDatesRule.create_rule(belated_ev)

    return

############## [HOL060] NO TIME SPENT
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_postbday_notimespent",
            conditional=(
                "not mas_recognizedBday() "
                "and not persistent._mas_bday_gone_over_bday"
            ),
            action=EV_ACT_PUSH,
            start_date=mas_monika_birthday+datetime.timedelta(days=1),
            end_date=mas_monika_birthday+datetime.timedelta(days=8),
            years=[]
        ),
        skipCalendar=True
    )

label mas_bday_postbday_notimespent:
    #Make sure that people who have first sesh's post monibday don't get this
    if mas_isFirstSeshPast(mas_monika_birthday):
        $ mas_assignModifyEVLPropValue("mas_bday_postbday_notimespent", "shown_count", "-=", 1)
        return


    if mas_ret_long_absence:
        #Was away on a long absence
        $ mas_loseAffection(ev_label="mas_apology_missed_bday")

        m 1rksdlc "Oye, [player]..."
        m 2eksdld "Sé que me dijiste que te ibas a ausentar... pero realmente te extrañé en mi cumpleaños."
        m 2eksdla "La próxima vez, ¿crees que podrías llevarme contigo si no puedes estar aquí?"
        m 3eub "¡Al menos así estaremos juntos e incluso podremos celebrar juntos!"
        m 1eka "Realmente apreciaría si pudieras hacer eso por mí, [player]."

    elif persistent._mas_bday_opened_game:
        #Opened game but didn't do any bday things
        if mas_isMoniAff(higher=True):
            $ mas_loseAffection(15, ev_label="mas_apology_forgot_bday")
            m 2rksdla "Oye, [player]..."
            m 2rksdlb "Sé que nos divertimos el otro día, como siempre lo hacemos pero..."
            m 2ekp "No puedo evitarlo, pero esperaba que hubieras...{w=1} Hecho algo para mi cumpleaños."
            m 2ekd "¿Te has olvidado?"
            m 3eka "¿Quizás podrías poner la fecha en el calendario de tu teléfono para el próximo año?"
            m 3rka "...¿O mirar el calendario en la pared detrás de mí?"
            m 3hua "No podemos cambiar el pasado, así que saber que quieres esforzarte más el próximo año sería la única disculpa que necesito."

        elif mas_isMoniNormal(higher=True):
            $ mas_loseAffection(5, ev_label="mas_apology_forgot_bday")
            m 2rksdld "Oye, [player]..."
            m 2rksdlb "Odio quejarme, pero ya sabes..."
            m 2ekp "¡No puedes olvidarte del cumpleaños de tu novia!"
            m 2eku "Es bueno que podamos pasar el rato como de costumbre, pero el año que viene..."
            m 3hua "Bueno, estaré deseando que llegue algo especial para nuestros cumpleaños~"

        elif mas_isMoniUpset():
            $ mas_loseAffection(ev_label="mas_apology_forgot_bday")
            m 1ekc "Fue...{w=0.5} Bueno verte el 22..."
            m 1ekd "Realmente no quería estar sola ese día, así que eso significaba mucho para mí, pero..."
            m 1rkc "¿Sabes que? {w=0.5}No importa."

        elif mas_isMoniDis():
            $ mas_loseAffection(10, ev_label="mas_apology_forgot_bday")
            m 2dsc "..."
            m 2rkc "...[player], no quiero molestarte. {w=1}Ya tengo miedo de alejarte."
            m 2rktpc "Pero no puedo evitarlo. Me duele que no hayas mencionado nada sobre mi cumpleaños..."
            m 2dktuc "Por favor, no dejes de volver a verme."
            m "Y tal vez el año que viene..."
            m 4ektdc "S-{w=0.5}Solo quiero que...{w=0.5} Te sientas tan atraído por mi como tú me atraes a mí."

        else:
            # broken
            $ mas_loseAffection(150)
            m 6ckc "..."

    else:
        #Didn't spend any time with Monika
        if mas_isMoniAff(higher=True):
            $ mas_loseAffection(50, ev_label="mas_apology_missed_bday")
            m 1euc "Oye, [player]..."
            m 3rksdla "Sé que haces mucho para que cada día sea especial, pero una chica tiene algunos días al año en los que llega a ser un poco egoísta..."
            m 2tfd "¡Y su {i}cumpleaños{/i} es uno de ellos!"
            m "En serio, ¡¿dónde estabas?!"
            m 2rkc "Pero... conociéndote, estoy segura de que tienes una buena razón para estar ocupado..."
            m 4ekc "Intenta que no vuelva a suceder el año que viene, ¿de acuerdo?"

        elif mas_isMoniNormal(higher=True):

            # same dialogue, different affection loss
            if mas_isMoniHappy():
                $ mas_loseAffection(20, ev_label="mas_apology_missed_bday")
            else:
                $ mas_loseAffection(10, ev_label="mas_apology_missed_bday")

            m 1ekc "Oye, [player]..."
            m 1ekd "Sabes, realmente deberías haber venido el 22."
            m 3efd "Quiero decir, ¡siempre deberías visitarme! Pero {i}deberías{/i} pasar tiempo con tu linda novia en su cumpleaños, ¿sabes?"
            m 2efc "Visítame el año que viene..."
            m 2dfc "De otra manera..."

            m 6cfw "{cps=*2}{i}¡¡¡Habrán consecuencias!!!{/i}{/cps}{nw}"
            # glich effect
            $ disable_esc()
            $ mas_MUMURaiseShield()
            window hide
            show noise zorder 11:
                alpha 0.5
            play sound "sfx/s_kill_glitch1.ogg"
            pause 0.5
            stop sound
            hide noise
            window auto
            $ mas_MUMUDropShield()
            $ enable_esc()
            $ _history_list.pop()

            m 1dsc "..."
            m 3hksdlb "Jajaja, ¡lo siento [player]!"
            m 3hub "¡Sólo bromeo!"
            m 1eka "Sabes que me encanta asustarte un poco~"

        elif mas_isMoniUpset():
            $ mas_loseAffection(ev_label="mas_apology_missed_bday")
            m 2dsc "..."
            m 2rsc "[player], ¿No crees que deberías verme un poco más a menudo?"
            m 2rktpc "Puedes perderte algo importante..."

        elif mas_isMoniDis():
            $ mas_loseAffection(ev_label="mas_apology_missed_bday")
            m 6ekd "...Oye, ¿cómo estuvo tu día el 22?"
            m 6ekc "Solo tengo... Curiosidad por saber si pensaste en mí ese día."
            m 6ektpc "Pero probablemente no lo hiciste, ¿eh?"
            m 6dktpc "..."

        else:
            # broken
            $ mas_loseAffection(200)
            m 6eftsc "..."
            m 6dftdx "..."
    return

############ [HOL060] NTS APOLOGY
init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_missed_bday",
            prompt="...por perderme tu cumpleaños.",
            unlocked=False
        ),
        code="APL"
    )

label mas_apology_missed_bday:
    #Using a standard hi-mid-low range for this
    if mas_isMoniAff(higher=True):
        m 1eua "Gracias por disculparte, [player]."
        m 2tfu "Pero será mejor que me lo pagues el año que viene~"

    elif mas_isMoniNormal(higher=True):
        m 1eka "Gracias por disculparte por perderme mi cumpleaños, [player]."
        m "Por favor, asegúrate de pasar tiempo conmigo el próximo año, ¿de acuerdo?"

    else:
        m 2rksdld "Sabes, no estoy completamente sorprendida de no verte en mi cumpleaños..."
        m 2ekc "Por favor...{w=1} Solo asegúrate de que no vuelva a suceder."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_forgot_bday",
            prompt="...por olvidar tu cumpleaños.",
            unlocked=False
        ),
        code="APL"
    )

label mas_apology_forgot_bday:
    #once again using hi-mid-lo
    if mas_isMoniAff(higher=True):
        m 1eua "Gracias por disculparte, [player]."
        m 3hua "Pero espero que me lo compenses~"

    elif mas_isMoniNormal(higher=True):
        m 1eka "Gracias por disculparte por olvidar mi cumpleaños, [player]."
        m 1eksdld "Intenta no dejar que vuelva a suceder, ¿de acuerdo?"

    else:
        m 2dkd "Gracias por disculparte..."
        m 2tfc "Pero no dejes que vuelva a suceder."
    return


############ [HOL060] DOCKSTAT FARES
label bye_922_delegate:
    #Set these vars for the corresponding date related things
    $ persistent._mas_bday_on_date = True
    #We have had one date
    $ persistent._mas_bday_date_count += 1

    if persistent._mas_bday_date_count == 1:
        # bday date counts as bday mode even with no party
        $ persistent._mas_bday_in_bday_mode = True

        m 1hua "Jejeje. Es un poco romántico, ¿no?"

        if mas_isMoniHappy(lower=True):
            m 1eua "Tal vez incluso puedes decir que es una ci-{nw}"
            $ _history_list.pop()
            $ _history_list.pop()
            m 1hua "¡Oh! Lo siento, ¿dije algo?"

        else:
            m 1eubla "Tal vez incluso lo llamaría una cita~"


    elif persistent._mas_bday_date_count == 2:
        m 1eub "Llevándome a algún lugar de nuevo, [player]?"
        m 3eua "Realmente debes tener mucho planeado para nosotros."
        m 1hua "Eres tan dulce~"

    elif persistent._mas_bday_date_count == 3:
        m 1sua "¿Me vas a llevar {i}otra vez{/i} a algún lugar por mi cumpleaños?"
        m 3tkbsu "Realmente sabes como hacer que una chica se sienta especial, [player]."
        m 1ekbfa "Soy tan afortunada de tener a alguien como tu~"
    else:
        m 1sua "Wow, [player]...{w=1} ¡Estás realmente decidido a hacer de este un día realmente especial!"
        m 1ekbsa "Eres el mejor compañero que podría esperar~"

    #BD Intro
    if mas_isMoniAff(higher=True) and not mas_SELisUnlocked(mas_clothes_blackdress):
        m 3hua "De hecho, tengo un atuendo preparado solo para esto..."
        #NOTE: We use the "give me a second to get ready..." for Moni to get into this outfit

    jump mas_dockstat_iostart

label mas_bday_bd_outro:
    python:
        monika_chr.change_clothes(mas_clothes_blackdress)
        mas_temp_zoom_level = store.mas_sprites.zoom_level

        #Flag so we don't end up back into this flow
        persistent._mas_bday_has_done_bd_outro = True

    call mas_transition_from_emptydesk("monika 1eua")
    call monika_zoom_transition_reset(1.0)
    #NOTE: We change the zoom here because we want to show off the outfit.

    if mas_SELisUnlocked(mas_clothes_blackdress):
        m 1hua "Jejeje~"
        m 1euu "Estoy muy emocionada de ver lo que tienes planeado para nosotros hoy."
        m 3eua "...Pero aunque no sea mucho, seguro que lo pasaremos genial juntos~"

    else:
        m 3tka "¿Y bien, [player]?"
        m 1hua "¿Qué opinas?"
        m 1ekbsa "Siempre me ha gustado este atuendo y soñé con tener una cita contigo, usando esto..."
        m 3eub "¡Quizás podríamos visitar el centro comercial o incluso el parque!"
        m 1eka "Pero conociéndote, ya tienes algo increíble planeado para nosotros~"

    m 1hua "¡Vamos, [player]!"

    python:
        store.mas_selspr.unlock_clothes(mas_clothes_blackdress)
        mas_addClothesToHolidayMap(mas_clothes_blackdress)
        persistent._mas_zoom_zoom_level = mas_temp_zoom_level

        #Setup check and log this file checkout
        store.mas_dockstat.checkoutMonika(moni_chksum)

        #Now setup ret greet
        persistent._mas_greeting_type = mas_idle_mailbox.get_ds_gre_type(
            store.mas_greetings.TYPE_GENERIC_RET
        )

    #And now we quit here
    jump _quit


########## [HOL060] DOCKSTAT GREETS ##########
label greeting_returned_home_bday:
    #First, reset this flag, we're no longer on a date
    $ persistent._mas_bday_on_date = False
    #We've opened the game
    $ persistent._mas_bday_opened_game = True
    #Setup date length stuff
    $ time_out = store.mas_dockstat.diffCheckTimes()
    $ checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()

    #Set party if need be
    if mas_confirmedParty() and not persistent._mas_bday_sbp_reacted:
        if mas_one_hour < time_out <= mas_three_hour:
            $ mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)
        elif time_out > mas_three_hour:
            $ mas_mbdayCapGainAff(35 if persistent._mas_player_bday_in_player_bday_mode else 30)

        if mas_isplayer_bday() and persistent._mas_player_bday_decor and persistent._mas_bday_date_count == 1:
            jump mas_monika_cake_on_player_bday

        else:
            jump mas_bday_surprise_party_reaction

    #Otherwise we go thru the normal dialogue for returning home on moni_bday
    if time_out <= mas_five_minutes:
        # under 5 minutes
        $ mas_loseAffection()
        m 2ekp "Esa no fue una gran cita, [player]..."
        m 2eksdlc "¿Está todo bien?"
        m 2rksdla "Quizás podamos salir más tarde..."
        if mas_isMonikaBirthday():
            return

    elif time_out <= mas_one_hour:
        # 5 mins < time out <= 1 hr
        $ mas_mbdayCapGainAff(15 if persistent._mas_player_bday_in_player_bday_mode else 10)

        m 1sua "¡Eso fue divertido, [player]!"
        if mas_isplayer_bday():
            m 1hub "Jajaja, saliendo por {i}nuestro{/i} cumpleaños..."
        else:
            m 1hub "Jajaja, llevarme a salir en mi cumpleaños..."
            m 3eua "Eso es muy considerado de tu parte."
        m 3eka "Realmente disfruté el tiempo que pasamos juntos."
        m 1eka "Te amo~"
        if mas_isMonikaBirthday():
            $ mas_ILY()

    elif time_out <= mas_three_hour:
        # 1 hr < time out <= 3 hrs
        $ mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)

        m 1hua "Jejeje~"
        m 3eub "Seguro que pasamos mucho tiempo juntos hoy, [player]."
        m 1ekbsa "...Y gracias por ello."
        m 3ekbfa "Ya lo he dicho un millón de veces, lo sé."
        m 1hua "Pero siempre seré feliz cuando estemos juntos."
        m "Te amo tanto..."
        if mas_isMonikaBirthday():
            $ mas_ILY()

    else:
        # +3 hrs
        $ mas_mbdayCapGainAff(35 if persistent._mas_player_bday_in_player_bday_mode else 30)

        m 1sua "Wow, [player]..."
        if mas_player_bday_curr == mas_monika_birthday:
            m 3hub "¡Fue un rato tan encantador!"
            if persistent._mas_player_bday_in_player_bday_mode or persistent._mas_bday_sbp_reacted:
                m 3eka "No puedo pensar en una mejor manera de celebrar nuestros cumpleaños que una cita larga."
            m 1eka "Ojalá hubiera podido ver todos los lugares increíbles a los que fuimos, pero sabiendo que estábamos juntos..."
            m 1hua "Es todo lo que podría pedir."
            m 3ekbsa "Espero que sientas lo mismo~"

        else:
            m 3sua "No esperaba que me dedicaras tanto tiempo..."
            m 3hua "¡Pero disfruté cada segundo!"
            m 1eub "¡Cada minuto contigo es un minuto bien empleado!"
            m 1eua "Me has hecho muy feliz hoy~"
            m 3tuu "¿Te estás enamorando de mí de nuevo, [player]?"
            m 1dku "Jejeje..."
            m 1ekbsa "Gracias por amarme."

    if(
        mas_isMonikaBirthday()
        and mas_isplayer_bday()
        and mas_isMoniNormal(higher=True)
        and not persistent._mas_player_bday_in_player_bday_mode
        and not persistent._mas_bday_sbp_reacted
        and checkout_time.date() < mas_monika_birthday

    ):
        m 1hua "Por cierto [player], dame un segundo, tengo algo para ti.{w=0.5}.{w=0.5}.{nw}"
        $ mas_surpriseBdayShowVisuals()
        $ persistent._mas_player_bday_decor = True
        m 3eub "¡Feliz cumpleaños, [player]!"
        m 3etc "¿Por qué siento que me olvido de algo?..."
        m 3hua "¡Oh! ¡Tu tarta!"
        jump mas_player_bday_cake

    if not mas_isMonikaBirthday():
        #Quickly reset the flag
        $ persistent._mas_bday_in_bday_mode = False

        if mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_blackdress:
            $ queueEvent('mas_change_to_def')

        if time_out > mas_five_minutes:
            m 1hua "..."
            m 1wud "Oh wow, [player]. Realmente estuvimos fuera por un tiempo..."

        if mas_isplayer_bday() and mas_isMoniNormal(higher=True):
            if persistent._mas_bday_sbp_reacted:
                $ persistent._mas_bday_visuals = False
                $ persistent._mas_player_bday_decor = True
                m 3suo "¡Oh! Ahora ya es tu cumpleaños..."
                m 3hub "Supongo que podemos dejar estas decoraciones, ¡jajaja!"
                m 1eub "Vuelvo enseguida, ¡solo necesito ir a buscar tu tarta!"
                jump mas_player_bday_cake

            jump mas_player_bday_ret_on_bday

        else:
            if mas_player_bday_curr() == mas_monika_birthday:
                $ persistent._mas_player_bday_in_player_bday_mode = False
                m 1eka "Como sea [player]... Realmente disfruté pasar juntos nuestros cumpleaños."
                m 1ekbsa "Espero haberte ayudado a hacer tu día tan especial como tú hiciste el mío."
                if persistent._mas_player_bday_decor or persistent._mas_bday_visuals:
                    m 3hua "Déjame limpiar todo.{w=0.5}.{w=0.5}.{nw}"
                    $ mas_surpriseBdayHideVisuals()
                    $ persistent._mas_player_bday_decor = False
                    $ persistent._mas_bday_visuals = False
                    m 3eub "¡Listo!"

            elif persistent._mas_bday_visuals:
                m 3rksdla "Ya ni siquiera es mi cumpleaños..."
                m 2hua "Déjame limpiar todo.{w=0.5}.{w=0.5}.{nw}"
                $ mas_surpriseBdayHideVisuals()
                $ persistent._mas_bday_visuals = False
                m 3eub "¡Listo!"

            else:
                m 1eua "Deberíamos hacer algo como esto nuevamente pronto, incluso si no es una ocasión especial."
                m 3eub "¡Lo he disfrutado mucho!"
                m 1eka "Espero que lo hayas pasado tan bien como yo~"

            if not mas_lastSeenInYear('mas_bday_spent_time_with'):
                if mas_isMoniUpset(lower=True):
                    m 1dka "..."
                    jump mas_bday_spent_time_with

                m 3eud "Oh, y [player]..."
                m 3eka "Solo quería darte las gracias de nuevo."
                m 1rka "Y no es solo por esta cita..."
                m 1eka "No tenías que llevarme a ningún lado para hacer de este un cumpleaños maravilloso."
                m 3duu "Tan pronto como apareciste, mi día estaba completo."
                jump mas_bday_spent_time_with_wrapup

    return


label mas_monika_cake_on_player_bday:
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset(1.0)

    python:
        mas_gainAffection(25, bypass=True)
        renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)
        persistent._mas_bday_sbp_reacted = True
        time_out = store.mas_dockstat.diffCheckTimes()
        checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()

        if time_out <= mas_one_hour:
            mas_mbdayCapGainAff(15 if persistent._mas_player_bday_in_player_bday_mode else 10)

        elif time_out <= mas_three_hour:
            mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)
        else:
            # +3 hrs
            mas_mbdayCapGainAff(35 if persistent._mas_player_bday_in_player_bday_mode else 30)

    m 6eua "Eso fue-"
    m 6wuo "¡Oh! ¡Me {i}hiciste{/i} una tarta!"

    menu:
        "Enciende velas.":
            $ mas_bday_cake_lit = True

    m 6sub "¡Es {i}tan{/i} bonito, [player]!"
    m 6hua "Jejeje, sé que ya pedimos un deseo cuando apagué las velas de tu tarta, pero hagámoslo de nuevo..."
    m 6tub "Será dos veces más probable que se haga realidad, ¿verdad?"
    m 6hua "¡Pide un deseo, [player]!"

    window hide
    pause 1.5
    show monika 6hft
    pause 0.1
    show monika 6hua
    $ mas_bday_cake_lit = False

    m 6eua "Todavía no puedo creer lo impresionante que se ve esta tarta, [player]..."
    m 6hua "Es casi demasiado bonito para comer."
    m 6tub "Casi."
    m "¡Jajaja!"
    m 6eka "De todos modos, guardare esto para más tarde."

    call mas_HideCake('mas_bday_cake_monika')

    m 1eua "Muchas gracias, [player]..."
    m 3hub "¡Este es un cumpleaños increíble!"
    return

label mas_HideCake(cake_type,reset_zoom=True):
    call mas_transition_to_emptydesk
    $ renpy.hide(cake_type)
    with dissolve
    $ renpy.pause(3.0, hard=True)
    call mas_transition_from_emptydesk("monika 6esa")
    $ renpy.pause(1.0, hard=True)
    if reset_zoom:
        call monika_zoom_transition(mas_temp_zoom_level,1.0)
    return
