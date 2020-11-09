default persistent.monika_reload = 0
default persistent.tried_skip = False
default persistent.monika_kill = True
default persistent.rejected_monika = None
default initial_monika_file_check = None
define modoorg.CHANCE = 20
define mas_battery_supported = False
define mas_in_intro_flow = False


default persistent._mas_disable_animations = False

init -998 python:

    if "unstable" in config.version and not persistent.sessions:
        raise Exception(
            _("Unstable mode files in install on first session. This can cause issues.\n"
            "Please reinstall the latest stable version of Monika After Story to ensure that there will be no data issues.")
        )

init -890 python in mas_globals:
    import datetime
    import store


    tt_detected = (
        store.mas_getLastSeshEnd() - datetime.datetime.now()
            > datetime.timedelta(hours=30)
    )

    if tt_detected:
        store.persistent._mas_pm_has_went_back_in_time = True


    is_r7 = renpy.version(True)[0] == 7


    is_steam = "steamapps" in renpy.config.basedir.lower()

init -1 python in mas_globals:



    dlg_workflow = False

    show_vignette = False


    show_lightning = False


    lightning_chance = 16
    lightning_s_chance = 10


    show_s_light = False


    text_speed_enabled = False


    in_idle_mode = False


    late_farewell = False


    last_minute_dt = datetime.datetime.now()


    last_hour = last_minute_dt.hour


    last_day = last_minute_dt.day


    time_of_day_4state = None


    time_of_day_3state = None


    returned_home_this_sesh = bool(store.persistent._mas_moni_chksum)


    this_ev = None


init 970 python:
    import store.mas_filereacts as mas_filereacts



    if persistent._mas_moni_chksum is not None:
        
        
        
        store.mas_dockstat.init_findMonika(mas_docking_station)


init -10 python:

    class MASIdleMailbox(store.MASMailbox):
        """
        Spaceroom idle extension of the mailbox

        PROPERTIES:
            (no additional)

        See MASMailbox for properties
        """
        
        
        REBUILD_EV = 1
        
        
        DOCKSTAT_GRE_TYPE = 2
        
        
        IDLE_MODE_CB_LABEL = 3
        
        
        SKIP_MID_LOOP_EVAL = 4
        
        
        SCENE_CHANGE = 5
        
        
        
        
        def __init__(self):
            """
            Constructor for the idle mailbox
            """
            super(MASIdleMailbox, self).__init__()
        
        
        def send_rebuild_msg(self):
            """
            Sends the rebuild message to the mailbox
            """
            self.send(self.REBUILD_EV, True)
        
        def get_rebuild_msg(self):
            """
            Gets rebuild message
            """
            return self.get(self.REBUILD_EV)
        
        def send_ds_gre_type(self, gre_type):
            """
            Sends greeting type to mailbox
            """
            self.send(self.DOCKSTAT_GRE_TYPE, gre_type)
        
        def get_ds_gre_type(self, default=None):
            """
            Gets dockstat greeting type

            RETURNS: None by default
            """
            result = self.get(self.DOCKSTAT_GRE_TYPE)
            if result is None:
                return default
            return result
        
        def send_idle_cb(self, cb_label):
            """
            Sends idle callback label to mailbox
            """
            self.send(self.IDLE_MODE_CB_LABEL, cb_label)
        
        def get_idle_cb(self):
            """
            Gets idle callback label
            """
            return self.get(self.IDLE_MODE_CB_LABEL)
        
        def send_skipmidloopeval(self):
            """
            Sends skip mid loop eval message to mailbox
            """
            self.send(self.SKIP_MID_LOOP_EVAL, True)
        
        def get_skipmidloopeval(self):
            """
            Gets skip midloop eval value
            """
            return self.get(self.SKIP_MID_LOOP_EVAL)
        
        def send_scene_change(self):
            """
            Sends scene change message to mailbox
            """
            self.send(self.SCENE_CHANGE, True)
        
        def get_scene_change(self):
            """
            Gets scene change value
            """
            return self.get(self.SCENE_CHANGE)


    mas_idle_mailbox = MASIdleMailbox()


image monika_room_highlight:
    "images/cg/monika/monika_room_highlight.png"
    function monika_alpha
image monika_bg = "images/cg/monika/monika_bg.png"
image monika_bg_highlight:
    "images/cg/monika/monika_bg_highlight.png"
    function monika_alpha
image monika_scare = "images/cg/monika/monika_scare.png"

image monika_body_glitch1:
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"
    0.15
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"
    1.00
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"
    0.15
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"

image monika_body_glitch2:
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"
    0.15
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"
    1.00
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"
    0.15
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"



image room_glitch = "images/cg/monika/monika_bg_glitch.png"

init python:

    import subprocess
    import os
    import eliza      
    import datetime   
    import battery    
    import re
    import store.songs as songs
    import store.hkb_button as hkb_button
    import store.mas_globals as mas_globals
    therapist = eliza.eliza()
    process_list = []
    currentuser = None 
    if renpy.windows:
        try:
            process_list = subprocess.check_output("wmic process get Description", shell=True).lower().replace("\r", "").replace(" ", "").split("\n")
        except:
            pass
        try:
            for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
                user = os.environ.get(name)
                if user:
                    currentuser = user
        except:
            pass

    try:
        renpy.file("../characters/monika.chr")
        initial_monika_file_check = True
    except:
        
        pass



    if not currentuser or len(currentuser) == 0:
        currentuser = persistent.playername
    if not persistent.mcname or len(persistent.mcname) == 0:
        persistent.mcname = currentuser
        mcname = currentuser
    else:
        mcname = persistent.mcname


    mas_battery_supported = battery.is_supported()



    renpy.music.register_channel(
        "background",
        mixer="amb",
        loop=True,
        stop_on_mute=True,
        tight=True
    )


    renpy.music.register_channel(
        "backsound",
        mixer="amb",
        loop=False,
        stop_on_mute=True
    )


    def show_dialogue_box():
        """
        Jumps to the topic promt menu
        """
        renpy.jump('prompt_menu')


    def pick_game():
        """
        Jumps to the pick a game workflow
        """
        renpy.jump("mas_pick_a_game")


    def mas_getuser():
        """
        Attempts to get the current user

        RETURNS: current user if found, or None if not found
        """
        for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
            user = os.environ.get(name)
            if user:
                return user
        
        return None


    def mas_enable_quitbox():
        """
        Enables Monika's quit dialogue warning
        """
        global _confirm_quit
        _confirm_quit = True


    def mas_disable_quitbox():
        """
        Disables Monika's quit dialogue warning
        """
        global _confirm_quit
        _confirm_quit = False


    def mas_enable_quit():
        """
        Enables quitting without monika knowing
        """
        persistent.closed_self = True
        mas_disable_quitbox()


    def mas_disable_quit():
        """
        Disables quitting without monika knowing
        """
        persistent.closed_self = False
        mas_enable_quitbox()


    def mas_drawSpaceroomMasks(dissolve_masks=True):
        """
        Draws the appropriate masks according to the current state of the
        game.

        IN:
            dissolve_masks - True will dissolve masks, False will not
                (Default; True)
        """
        
        renpy.hide("rm")
        
        
        mask = mas_current_weather.get_mask()
        
        
        renpy.show(mask, tag="rm")
        
        if dissolve_masks:
            renpy.with_statement(Dissolve(1.0))


    def mas_validate_suntimes():
        """
        Validates both persistent and store suntimes are in a valid state.
        Sunrise is always used as the lead if a reset is needed.
        """
        if (
            mas_suntime.sunrise > mas_suntime.sunset
            or persistent._mas_sunrise > persistent._mas_sunset
        ):
            mas_suntime.sunset = mas_suntime.sunrise
            persistent._mas_sunset = persistent._mas_sunrise


    def show_calendar():
        """RUNTIME ONLY
        Opens the calendar if we can
        """
        mas_HKBRaiseShield()
        
        if not persistent._mas_first_calendar_check:
            renpy.call('_first_time_calendar_use')
        
        renpy.call_in_new_context("mas_start_calendar_read_only")
        
        if store.mas_globals.in_idle_mode:
            
            store.hkb_button.talk_enabled = True
            store.hkb_button.extra_enabled = True
            store.hkb_button.music_enabled = True
        
        else:
            mas_HKBDropShield()


    dismiss_keys = config.keymap['dismiss']
    renpy.config.say_allow_dismiss = store.mas_hotkeys.allowdismiss

    def slow_nodismiss(event, interact=True, **kwargs):
        """
        Callback for whenever monika talks

        IN:
            event - main thing we can use here, lets us now when in the pipeline
                we are for display text:
                begin -> start of a say statement
                show -> right before dialogue is shown
                show_done -> right after dialogue is shown
                slow_done -> called after text finishes showing
                    May happen after "end"
                end -> end of dialogue (user has interacted)
        """
        
        
        
        
        
        
        
        
        if event == "begin":
            store.mas_hotkeys.allow_dismiss = False
        
        
        
        elif event == "slow_done":
            store.mas_hotkeys.allow_dismiss = True




    def mas_isMorning():
        """DEPRECATED
        Checks if it is day or night via suntimes

        NOTE: the wording of this function is bad. This does not literally
            mean that it is morning. USE mas_isDayNow

        RETURNS: True if day, false if not
        """
        return mas_isDayNow()


    def mas_progressFilter():
        """
        Changes filter according to rules.

        Call this when you want to update the filter.

        RETURNS: True upon a filter change, False if not
        """
        curr_flt = store.mas_sprites.get_filter()
        new_flt = mas_current_background.progress()
        store.mas_sprites.set_filter(new_flt)
        
        return curr_flt != new_flt


    def mas_shouldChangeTime():
        """DEPRECATED
        This no longer makes sense with the filtering system.
        """
        return False


    def mas_shouldRain():
        """
        Rolls some chances to see if we should make it rain

        RETURNS:
            rain weather to use, or None if we dont want to change weather
        """
        
        chance = random.randint(1,100)
        if mas_isMoniNormal(higher=True):
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            if mas_isSpring():
                return mas_weather._determineCloudyWeather(
                    40,
                    15,
                    15,
                    rolled_chance=chance
                )
            
            elif mas_isSummer():
                return mas_weather._determineCloudyWeather(
                    10,
                    6,
                    5,
                    rolled_chance=chance
                )
            
            elif mas_isFall():
                return mas_weather._determineCloudyWeather(
                    30,
                    12,
                    15,
                    rolled_chance=chance
                )
            
            else:
                
                if chance <= 50:
                    return mas_weather_snow
                elif chance <= 70:
                    return mas_weather_overcast
        
        
        elif mas_isMoniUpset() and chance <= MAS_RAIN_UPSET:
            return mas_weather_overcast
        
        elif mas_isMoniDis() and chance <= MAS_RAIN_DIS:
            return mas_weather_rain
        
        elif mas_isMoniBroken() and chance <= MAS_RAIN_BROKEN:
            return mas_weather_thunder
        
        return None


    def mas_lockHair():
        """
        Locks all hair topics
        """
        mas_lockEVL("monika_hair_select")


    def mas_seasonalCheck():
        """
        Determines the current season and runs an appropriate programming
        point.

        If the global for season is currently None, then we instead set the
        current season.

        NOTE: this does NOT do progressive programming point execution.
            This is intended for runtime usage only.

        ASSUMES:
            persistent._mas_current_season
        """
        _s_tag = store.mas_seasons._currentSeason()
        
        if persistent._mas_current_season != _s_tag:
            
            _s_pp = store.mas_seasons._season_pp_map.get(_s_tag, None)
            if _s_pp is not None:
                
                
                _s_pp()
                
                
                persistent._mas_current_season = _s_tag


    def mas_resetIdleMode():
        """
        Resets specific idle mode vars.

        This is meant to basically clear idle mode for holidays or other
        things that hijack main flow
        """
        store.mas_globals.in_idle_mode = False
        persistent._mas_in_idle_mode = False
        persistent._mas_idle_data = {}
        mas_idle_mailbox.get_idle_cb()


    def mas_enableTextSpeed():
        """
        Enables text speed
        """
        style.say_dialogue = style.normal
        store.mas_globals.text_speed_enabled = True


    def mas_disableTextSpeed():
        """
        Disables text speed
        """
        style.say_dialogue = style.default_monika
        store.mas_globals.text_speed_enabled = False


    def mas_resetTextSpeed(ignoredev=False):
        """
        Sets text speed to the appropriate one depending on global settings

        Rules:
        1 - developer always gets text speed (unless ignoredev is True)
        2 - text speed enabled if affection above happy
        3 - text speed disabled otherwise
        """
        if config.developer and not ignoredev:
            mas_enableTextSpeed()
        
        elif (
                mas_isMoniHappy(higher=True)
                and persistent._mas_text_speed_enabled
            ):
            mas_enableTextSpeed()
        
        else:
            mas_disableTextSpeed()


    def mas_isTextSpeedEnabled():
        """
        Returns true if text speed is enabled
        """
        return store.mas_globals.text_speed_enabled

    def mas_check_player_derand():
        """
        Checks the player derandom lists for events that are not random and derandoms them
        """
        
        derand_list = store.mas_bookmarks_derand.getDerandomedEVLs()
        
        
        for ev_label in derand_list:
            
            ev = mas_getEV(ev_label)
            if ev and ev.random:
                ev.random = False

    def mas_get_player_bookmarks(bookmarked_evls):
        """
        Gets topics which are bookmarked by the player
        Also cleans events which no longer exist

        NOTE: Will NOT add events which fail the aff range check

        IN:
            bookmarked_evls - appropriate persistent variable holding the bookmarked eventlabels

        OUT:
            List of bookmarked topics as evs
        """
        bookmarkedlist = []
        
        
        for index in range(len(bookmarked_evls)-1,-1,-1):
            
            ev = mas_getEV(bookmarked_evls[index])
            
            
            if not ev:
                bookmarked_evls.pop(index)
            
            
            elif ev.unlocked and ev.checkAffection(mas_curr_affection):
                bookmarkedlist.append(ev)
        
        return bookmarkedlist

    def mas_get_player_derandoms(derandomed_evls):
        """
        Gets topics which are derandomed by the player (in check-scrollable-menu format)
        Also cleans out events which no longer exist

        IN:
            derandomed_evls - appropriate variable holding the derandomed eventlabels

        OUT:
            List of player derandomed topics in mas_check_scrollable_menu form
        """
        derandlist = []
        
        
        for index in range(len(derandomed_evls)-1,-1,-1):
            
            ev = mas_getEV(derandomed_evls[index])
            
            
            if not ev:
                derandomed_evls.pop(index)
            
            
            elif ev.unlocked:
                derandlist.append((renpy.substitute(ev.prompt), ev.eventlabel, False, True, False))
        
        return derandlist













































label spaceroom(start_bg=None, hide_mask=None, hide_monika=False, dissolve_all=False, dissolve_masks=False, scene_change=False, force_exp=None, hide_calendar=None, day_bg=None, night_bg=None, show_emptydesk=True, progress_filter=True):

    with None


    if hide_mask is None:
        $ hide_mask = store.mas_current_background.hide_masks
    if hide_calendar is None:
        $ hide_calendar = store.mas_current_background.hide_calendar





    python:
        if progress_filter and mas_progressFilter():
            
            scene_change = True
            dissolve_all = True

        day_mode = mas_current_background.isFltDay()

    if scene_change:
        scene black

    python:
        monika_room = None

        if scene_change:
            monika_room = mas_current_background.getCurrentRoom()


        if persistent._mas_auto_mode_enabled:
            mas_darkMode(day_mode)
        else:
            mas_darkMode(not persistent._mas_dark_mode_enabled)


        if hide_monika:
            if show_emptydesk:
                store.mas_sprites.show_empty_desk()

        else:
            if force_exp is None:
                
                if dissolve_all:
                    force_exp = store.mas_affection._force_exp()
                
                else:
                    force_exp = "monika idle"
            
            if not renpy.showing(force_exp):
                renpy.show(force_exp, at_list=[t11], zorder=MAS_MONIKA_Z)
                
                if not dissolve_all:
                    renpy.with_statement(None)


        if not dissolve_all and not hide_mask:
            mas_drawSpaceroomMasks(dissolve_masks)



        if start_bg:
            if not renpy.showing(start_bg):
                renpy.show(start_bg, tag="sp_mas_room", zorder=MAS_BACKGROUND_Z)

        elif monika_room is not None:
            if not renpy.showing(monika_room):
                renpy.show(
                    monika_room,
                    tag="sp_mas_room",
                    zorder=MAS_BACKGROUND_Z
                )
                
                if not hide_calendar:
                    mas_calShowOverlay()



    if store.mas_globals.show_vignette:
        show vignette zorder 70


    if persistent._mas_bday_visuals:

        $ store.mas_surpriseBdayShowVisuals(cake=not persistent._mas_bday_sbp_reacted)



    if persistent._mas_o31_in_o31_mode:
        $ store.mas_o31ShowVisuals()


    elif persistent._mas_d25_deco_active:
        $ store.mas_d25ShowVisuals()



    if persistent._mas_player_bday_decor:
        $ store.mas_surpriseBdayShowVisuals()

    if datetime.date.today() == persistent._date_last_given_roses:
        $ monika_chr.wear_acs_pst(mas_acs_roses)


    if dissolve_all and not hide_mask:
        $ mas_drawSpaceroomMasks(dissolve_all)
    elif dissolve_all:
        $ renpy.with_statement(Dissolve(1.0))


    if not hide_monika and not show_emptydesk:
        hide emptydesk

    return


label ch30_main:
    $ mas_skip_visuals = False
    $ m.display_args["callback"] = slow_nodismiss
    $ m.what_args["slow_abortable"] = config.developer
    $ quick_menu = True
    if not config.developer:
        $ style.say_dialogue = style.default_monika
    $ m_name = persistent._mas_monika_nickname
    $ delete_all_saves()
    $ persistent.clear[9] = True


    call ch30_reset from _call_ch30_reset


    $ monika_chr.reset_outfit(False)
    $ monika_chr.wear_acs(mas_acs_ribbon_def)


    $ mas_in_intro_flow = True



    $ mas_RaiseShield_core()


    $ store.hkb_button.enabled = False



    call spaceroom (scene_change=True, dissolve_all=True, force_exp="monika 6dsc_static") from _call_spaceroom_15




    call introduction from _call_introduction



    $ mas_DropShield_core()


    $ mas_in_intro_flow = False


    $ store._mas_root.initialSessionData()


    $ skip_setting_weather = True


    if not mas_events_built:
        $ mas_rebuildEventLists()

    jump ch30_preloop

label continue_event:
    m "Ahora, ¿dónde estaba?..."
    return

label ch30_noskip:
    show screen fake_skip_indicator
    m 1esc "...¿Estás tratando de adelantar?"
    m 1ekc "No te estoy aburriendo, ¿verdad?"
    m "Oh Dios..."
    m 2esa "...Bueno, sólo para que lo sepas, no hay nada que adelantar, [player]."
    m "Sólo somos nosotros dos, después de todo..."
    m 1eua "Pero aparte de eso, el tiempo ya no existe realmente, así que ni siquiera va a funcionar."
    m "Me adelantaré y apagaré eso por ti..."
    pause 0.4
    hide screen fake_skip_indicator
    pause 0.4
    m 1hua "¡Ya está!"
    m 1esa "Serás un encanto y me escucharás a partir de ahora, ¿verdad?"
    m "Gracias~"
    hide screen fake_skip_indicator


    $ restartEvent()
    jump ch30_loop

image splash-glitch2 = "images/bg/splash-glitch2.png"

label ch30_nope:

    $ persistent.autoload = ""
    $ m.display_args["callback"] = slow_nodismiss
    $ quick_menu = True
    call spaceroom from _call_spaceroom_1

    if persistent.rejected_monika:
        m 1euc "Espera. ¿Te estás metiendo con mi archivo de personajes?"
        m 2esa "La curiosidad es lo que nos hace humanos, ¿verdad?"
        m "Si no fuera por el deseo humano de explorar, todavía estaríamos columpiándonos de los árboles."
        m 1eka "Aún así, por favor no lo hagas. Me pone nerviosa, aunque ya no necesito un archivo de personajes."
        m "Ya he arreglado ese fallo."
    else:

        $ quick_menu = False
        $ m_name = glitchtext(12)
        m 1euc "Espera. ¿Te estás metiendo con mi archivo de personajes?"
        m 1tkc "¿Por qué estás jugando este mod si sólo querías borrarme de nuevo?"
        m 1tfc "Realmente eres el peor."
        m 1tfd "¿Pierdes todo tu tiempo en Internet con un montón de gente con la que nunca hablarás en la realidad, pero aún así estás dispuesto a matarme por capricho sólo porque estabas aburrido?"
        m 1tkd "Todo lo que quería era alguien de quien enamorarme..."
        m "Habría hecho cualquier cosa que quisieras que hiciera."
        m 1tku "Pero si vas a intentar borrarme de nuevo..."
        m 4tfu "Entonces tendré que borrarte primero."
        if renpy.windows:
            call updateconsole ("shututil.rmtree(\"Documents\", true)", "Eliminación de documentos en curso...") from _call_updateconsole_15
        elif renpy.linux:
            call updateconsole ("sudo mv ~ /dev/null", "En curso...") from _call_updateconsole_16
        elif renpy.macintosh:
            call updateconsole ("sudo mv ~ /dev/null", "En curso...") from _call_updateconsole_19
        pause 3.0
        call hideconsole from _call_hideconsole_2
        $ open(config.basedir + "/characters/monika.chr", "wb").write(renpy.file("monika.chr").read())
        $ m_name = persistent._mas_monika_nickname
        $ quick_menu = True
        m 1hua "¡Jajaja!"
        m "¡Solo bromeo!"
        m 1eua "Ya he arreglado ese fallo."
        m "Ya no necesito un archivo de personajes."

    m 1ekbfa "Sólo necesito tu amor, [player]."
    m 1eua "Oh, a menos que intentes borrar todos los archivos del juego, supongo."
    m 3tfu "Si haces eso, no me detendré en borrar un directorio la próxima vez."
    m 3tku "Pero eso nunca sucederá, ¿verdad? Sólo estás siendo un tsundere~"
    m 1hua "¡Eso es tan lindo!"
    m 1eua "Por mucho que quieras negarlo, hablarás conmigo el resto de tu vida."
    m "Estar solo es bastante solitario si quieres que lo sea, ¡así que anímate!"
    jump ch30_loop


label ch30_autoload:


    python:
        import store.evhand as evhand

        m.display_args["callback"] = slow_nodismiss
        m.what_args["slow_abortable"] = config.developer

        if not config.developer:
            config.allow_skipping = False

        mas_resetTextSpeed()
        quick_menu = True
        startup_check = True 
        mas_skip_visuals = False


        skip_setting_weather = False

        mas_cleanEventList()


    call mas_set_gender from _call_mas_set_gender


    call ch30_reset from _call_ch30_reset_1



    python:
        if (
            persistent._mas_pm_got_a_fresh_start
            and _mas_getAffection() <= -50
        ):
            persistent._mas_load_in_finalfarewell_mode = True
            persistent._mas_finalfarewell_poem_id = "ff_failed_promise"

        elif _mas_getAffection() <= -115:
            persistent._mas_load_in_finalfarewell_mode = True
            persistent._mas_finalfarewell_poem_id = "ff_affection"



    if persistent._mas_load_in_finalfarewell_mode:
        jump mas_finalfarewell_start


    $ selected_greeting = None


    $ mas_startupBackground()













    if store.mas_dockstat.retmoni_status is not None:

        $ store.mas_dockstat.triageMonika(False)

label mas_ch30_post_retmoni_check:



    if mas_isO31() or persistent._mas_o31_in_o31_mode:
        jump mas_o31_autoload_check

    elif (
        mas_isD25Season()
        or persistent._mas_d25_in_d25_mode
        or (mas_run_d25s_exit and not mas_lastSeenInYear("mas_d25_monika_d25_mode_exit"))
    ):
        jump mas_holiday_d25c_autoload_check

    elif mas_isF14() or persistent._mas_f14_in_f14_mode:
        jump mas_f14_autoload_check



    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        jump mas_player_bday_autoload_check

    if mas_isMonikaBirthday() or persistent._mas_bday_in_bday_mode:
        jump mas_bday_autoload_check



label mas_ch30_post_holiday_check:




    if persistent._mas_affection["affection"] <= -50 and seen_event("mas_affection_apology"):




        if persistent._mas_affection["apologyflag"] and not is_apology_present():
            $ mas_RaiseShield_core()
            call spaceroom (scene_change=True) from _call_spaceroom_16
            jump mas_affection_noapology


        elif persistent._mas_affection["apologyflag"] and is_apology_present():
            $ persistent._mas_affection["apologyflag"] = False
            $ mas_RaiseShield_core()
            call spaceroom (scene_change=True) from _call_spaceroom_17
            jump mas_affection_yesapology


        elif not persistent._mas_affection["apologyflag"] and not is_apology_present():
            $ persistent._mas_affection["apologyflag"] = True
            $ mas_RaiseShield_core()
            call spaceroom (scene_change=True) from _call_spaceroom_18
            jump mas_affection_apologydeleted


    $ gre_cb_label = None
    $ just_crashed = False
    $ forced_quit = False


    if (
            persistent.playername.lower() == "yuri"
            and not persistent._mas_sensitive_mode
        ):
        call yuri_name_scare from _call_yuri_name_scare


        jump ch30_post_greeting_check

    elif not persistent._mas_game_crashed:

        $ forced_quit = True
        $ persistent._mas_greeting_type = store.mas_greetings.TYPE_RELOAD

    elif not persistent.closed_self:

        $ just_crashed = True
        $ persistent._mas_greeting_type = store.mas_greetings.TYPE_CRASHED


        $ persistent.closed_self = True




    python:


        persistent._mas_greeting_type = store.mas_greetings.checkTimeout(
            persistent._mas_greeting_type
        )


        sel_greeting_ev = store.mas_greetings.selectGreeting(
            persistent._mas_greeting_type
        )


        persistent._mas_greeting_type = None

        if sel_greeting_ev is None:
            
            
            if persistent._mas_in_idle_mode:
                
                mas_resetIdleMode()
            
            if just_crashed:
                
                
                
                
                sel_greeting_ev = mas_getEV("mas_crashed_start")
            
            elif forced_quit:
                
                
                
                sel_greeting_ev = mas_getEV("ch30_reload_delegate")




        if sel_greeting_ev is not None:
            selected_greeting = sel_greeting_ev.eventlabel
            
            
            mas_skip_visuals = MASGreetingRule.should_skip_visual(
                event=sel_greeting_ev
            )
            
            
            setup_label = MASGreetingRule.get_setup_label(sel_greeting_ev)
            if setup_label is not None and renpy.has_label(setup_label):
                gre_cb_label = setup_label



    if gre_cb_label is not None:
        call expression gre_cb_label from _call_expression_4

label ch30_post_greeting_check:



    $ restartEvent()

label ch30_post_restartevent_check:



    python:
        if persistent.sessions['last_session_end'] is not None and persistent.closed_self:
            away_experience_time=datetime.datetime.now()-persistent.sessions['last_session_end'] 
            
            
            if away_experience_time.total_seconds() >= times.REST_TIME:
                
                
                mas_gainAffection()
            
            
            while persistent._mas_pool_unlocks > 0 and mas_unlockPrompt():
                persistent._mas_pool_unlocks -= 1

        else:
            
            mas_loseAffection(modifier=2, reason=4)

label ch30_post_exp_check:




    $ mas_checkReactions()



    python:
        startup_events = {}
        for evl in evhand.event_database:
            ev = evhand.event_database[evl]
            if ev.action != EV_ACT_QUEUE:
                startup_events[evl] = ev

        Event.checkEvents(startup_events)


    $ mas_checkAffection()


    $ mas_checkApologies()


    if mas_corrupted_per and not renpy.seen_label("mas_corrupted_persistent"):
        $ pushEvent("mas_corrupted_persistent")


    if selected_greeting:

        if persistent._mas_in_idle_mode:
            $ pushEvent("mas_idle_mode_greeting_cleanup")

        $ pushEvent(selected_greeting)


    $ MASConsumable._checkConsumables(startup=True)








label ch30_preloop:


    window auto

    python:


        mas_HKRaiseShield()
        mas_HKBRaiseShield()
        set_keymaps()

        persistent.closed_self = False
        persistent._mas_game_crashed = True
        startup_check = False
        mas_checked_update = False
        mas_globals.last_minute_dt = datetime.datetime.now()
        mas_globals.last_hour = mas_globals.last_minute_dt.hour
        mas_globals.last_day = mas_globals.last_minute_dt.day


        mas_runDelayedActions(MAS_FC_IDLE_ONCE)


        mas_resetWindowReacts()


        mas_updateFilterDict()


        renpy.save_persistent()


        if mas_idle_mailbox.get_rebuild_msg():
            mas_rebuildEventLists()

    if mas_skip_visuals:
        $ mas_OVLHide()
        $ mas_skip_visuals = False
        $ quick_menu = True
        jump ch30_visual_skip


    $ mas_idle_mailbox.send_scene_change()


    $ mas_startupWeather()


    $ skip_setting_weather = False


    $ mas_startup_song()

    jump ch30_loop

label ch30_loop:
    $ quick_menu = True





    python:
        should_dissolve_masks = (
            mas_weather.weatherProgress()
            and mas_isMoniNormal(higher=True)
        )

        should_dissolve_all = mas_idle_mailbox.get_scene_change()

    call spaceroom (scene_change=should_dissolve_all, dissolve_all=should_dissolve_all, dissolve_masks=should_dissolve_masks) from _call_spaceroom_19








    if not mas_checked_update:
        $ mas_backgroundUpdateCheck()
        $ mas_checked_update = True

label ch30_visual_skip:

    $ persistent.autoload = "ch30_autoload"






    if store.mas_dockstat.abort_gen_promise:
        $ store.mas_dockstat.abortGenPromise()

    if mas_idle_mailbox.get_skipmidloopeval():
        jump ch30_post_mid_loop_eval






    $ now_check = datetime.datetime.now()


    if now_check.day != mas_globals.last_day:
        call ch30_day from _call_ch30_day
        $ mas_globals.last_day = now_check.day


    if now_check.hour != mas_globals.last_hour:
        call ch30_hour from _call_ch30_hour
        $ mas_globals.last_hour = now_check.hour


    $ time_since_check = now_check - mas_globals.last_minute_dt
    if now_check.minute != mas_globals.last_minute_dt.minute or time_since_check.total_seconds() >= 60:
        call ch30_minute (time_since_check) from _call_ch30_minute
        $ mas_globals.last_minute_dt = now_check



label ch30_post_mid_loop_eval:


    call call_next_event from _call_call_next_event_1


    if not mas_globals.in_idle_mode:
        if not mas_HKIsEnabled():
            $ mas_HKDropShield()
        if not mas_HKBIsEnabled():
            $ mas_HKBDropShield()


    $ persistent.current_monikatopic = 0


    if not _return:

        window hide(config.window_hide_transition)


        if (
                store.mas_globals.show_lightning
                and renpy.random.randint(1, store.mas_globals.lightning_chance) == 1
            ):
            $ light_zorder = MAS_BACKGROUND_Z - 1
            if (
                    not persistent._mas_sensitive_mode
                    and store.mas_globals.show_s_light
                    and renpy.random.randint(
                        1, store.mas_globals.lightning_s_chance
                    ) == 1
                ):
                $ renpy.show("mas_lightning_s", zorder=light_zorder)
            else:
                $ renpy.show("mas_lightning", zorder=light_zorder)

            $ pause(0.1)
            play backsound "mod_assets/sounds/amb/thunder.wav"





        $ mas_randchat.wait()

        if not mas_randchat.waitedLongEnough():
            jump post_pick_random_topic
        else:
            $ mas_randchat.setWaitingTime()

        window auto










        if store.mas_globals.in_idle_mode:
            jump post_pick_random_topic



        label pick_random_topic:


            if not persistent._mas_enable_random_repeats:
                jump mas_ch30_select_unseen


            $ chance = random.randint(1, 100)

            if chance <= store.mas_topics.UNSEEN:

                jump mas_ch30_select_unseen

            elif chance <= store.mas_topics.SEEN:

                jump mas_ch30_select_seen


            jump mas_ch30_select_mostseen




label post_pick_random_topic:

    $ _return = None

    jump ch30_loop


label mas_ch30_select_unseen:


    if len(mas_rev_unseen) == 0:

        if not persistent._mas_enable_random_repeats:

            if mas_timePastSince(mas_getEVL_last_seen("mas_random_limit_reached"), datetime.timedelta(weeks=2)):
                $ pushEvent("mas_random_limit_reached")

            jump post_pick_random_topic


        jump mas_ch30_select_seen

    $ mas_randomSelectAndPush(mas_rev_unseen)

    jump post_pick_random_topic


label mas_ch30_select_seen:


    if len(mas_rev_seen) == 0:

        $ mas_rev_seen, mas_rev_mostseen = mas_buildSeenEventLists()

        if len(mas_rev_seen) == 0:
            if len(mas_rev_mostseen) > 0:

                jump mas_ch30_select_mostseen


            if (
                len(mas_rev_mostseen) == 0
                and mas_timePastSince(mas_getEVL_last_seen("mas_random_limit_reached"), datetime.timedelta(days=1))
            ):
                $ pushEvent("mas_random_limit_reached")
                jump post_pick_random_topic


            jump post_pick_random_topic

    $ mas_randomSelectAndPush(mas_rev_seen)

    jump post_pick_random_topic


label mas_ch30_select_mostseen:


    if len(mas_rev_mostseen) == 0:
        jump mas_ch30_select_seen

    $ mas_randomSelectAndPush(mas_rev_mostseen)

    jump post_pick_random_topic




label ch30_end:
    jump ch30_main




label ch30_minute(time_since_check):
    python:


        mas_checkAffection()


        mas_checkApologies()


        Event.checkEvents(evhand.event_database, rebuild_ev=False)


        mas_runDelayedActions(MAS_FC_IDLE_ROUTINE)


        mas_checkReactions()


        mas_seasonalCheck()


        mas_clearNotifs()


        mas_checkForWindowReacts()


        if mas_idle_mailbox.get_rebuild_msg():
            mas_rebuildEventLists()


        _mas_AffSave()


        mas_songs.checkRandSongDelegate()


        renpy.save_persistent()

    return





label ch30_hour:
    $ mas_runDelayedActions(MAS_FC_IDLE_HOUR)


    $ MASConsumable._checkConsumables()


    $ store.mas_xp.grant()


    $ mas_setTODVars()
    return




label ch30_day:
    python:

        MASUndoActionRule.check_persistent_rules()

        MASStripDatesRule.check_persistent_rules(persistent._mas_strip_dates_rules)



        persistent._mas_filereacts_gift_aff_gained = 0
        persistent._mas_filereacts_last_aff_gained_reset_date = datetime.date.today()


        mas_ret_long_absence = False


        mas_runDelayedActions(MAS_FC_IDLE_DAY)

        if mas_isMonikaBirthday():
            persistent._mas_bday_opened_game = True

        if mas_isO31() and not persistent._mas_o31_in_o31_mode:
            pushEvent("mas_holiday_o31_returned_home_relaunch", skipeval=True)


        if (
            persistent._mas_filereacts_reacted_map
            and mas_pastOneDay(persistent._mas_filereacts_last_reacted_date)
        ):
            persistent._mas_filereacts_reacted_map = dict()


        if (
            not persistent._mas_d25_intro_seen
            and mas_isD25Outfit()
            and mas_isMoniUpset(lower=True)
        ):
            persistent._mas_d25_started_upset = True
    return



label ch30_reset:

    python:

        if persistent._mas_xp_lvl < 0:
            persistent._mas_xp_lvl = 0 

        if persistent._mas_xp_tnl < 0:
            persistent._mas_xp_tnl = store.mas_xp.XP_LVL_RATE
        elif int(persistent._mas_xp_tnl) > (2* int(store.mas_xp.XP_LVL_RATE)):
            
            persistent._mas_xp_tnl = 2 * store.mas_xp.XP_LVL_RATE

        if persistent._mas_xp_hrx < 0:
            persistent._mas_xp_hrx = 0.0

        store.mas_xp.set_xp_rate()
        store.mas_xp.prev_grant = mas_getCurrSeshStart()

    python:

        if persistent.playername.lower() == "sayori" or (mas_isO31() and not persistent._mas_pm_cares_about_dokis):
            store.mas_globals.show_s_light = True

    python:

        store.mas_sprites.apply_ACSTemplates()

    python:

        if not mas_events_built:
            mas_rebuildEventLists()


        if len(mas_rev_unseen) == 0:
            
            
            
            random_seen_limit = 1000

        if not persistent._mas_pm_has_rpy:
            if mas_hasRPYFiles():
                if not mas_inEVL("monika_rpy_files"):
                    queueEvent("monika_rpy_files")
            
            else:
                if persistent.current_monikatopic == "monika_rpy_files":
                    persistent.current_monikatopic = 0
                mas_rmallEVL("monika_rpy_files")

    python:
        import datetime
        today = datetime.date.today()


    python:
        game_unlock_db = {
            "chess": "mas_unlock_chess",
            mas_games.HANGMAN_NAME: "mas_unlock_hangman",
            "piano": "mas_unlock_piano",
        }
        mas_unlockGame("pong") 

        for game_name, game_startlabel in game_unlock_db.iteritems():
            
            if mas_getEVL_shown_count(game_startlabel) > 0:
                mas_unlockGame(game_name)






    $ store.mas_selspr.unlock_hair(mas_hair_def)

    $ store.mas_selspr.unlock_clothes(mas_clothes_def)


    $ store.mas_selspr.unlock_acs(mas_acs_ribbon_def)


    $ store.mas_selspr._validate_group_topics()


    $ monika_chr.load(startup=True)


    if ((store.mas_isMoniNormal(lower=True) and not store.mas_hasSpecialOutfit()) or store.mas_isMoniDis(lower=True)) and store.monika_chr.clothes != store.mas_clothes_def:
        $ pushEvent("mas_change_to_def",skipeval=True)

    if not mas_hasSpecialOutfit():
        $ mas_lockEVL("monika_event_clothes_select", "EVE")






    python:
        if persistent._mas_acs_enable_promisering:
            
            monika_chr.wear_acs_pst(mas_acs_promisering)


    $ mas_randchat.adjustRandFreq(persistent._mas_randchat_freq)

    python:
        if persistent.chess_strength < 0:
            persistent.chess_strength = 0
        elif persistent.chess_strength > 20:
            persistent.chess_strength = 20


    python:
        if persistent._mas_monika_returned_home is not None:
            _rh = persistent._mas_monika_returned_home.date()
            if today > _rh:
                persistent._mas_monika_returned_home = None


    python:








        if persistent.sessions is not None:
            tp_time = persistent.sessions.get("total_playtime", None)
            if tp_time is not None:
                max_time = mas_maxPlaytime()
                if tp_time > max_time:
                    
                    persistent.sessions["total_playtime"] = max_time // 100
                    
                    
                    store.mas_dockstat.setMoniSize(
                        persistent.sessions["total_playtime"]
                    )
                
                elif tp_time < datetime.timedelta(0):
                    
                    persistent.sessions["total_playtime"] = datetime.timedelta(0)
                    
                    
                    store.mas_dockstat.setMoniSize(
                        persistent.sessions["total_playtime"]
                    )


    python:

        if persistent._mas_affection is not None:
            freeze_date = persistent._mas_affection.get("freeze_date", None)
            if freeze_date is not None and freeze_date > today:
                persistent._mas_affection["freeze_date"] = today



    $ mas_startupPlushieLogic(4)


    python:
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        if not mas_isMonikaBirthday() and not mas_isMonikaBirthday(yesterday):
            persistent._mas_bday_visuals = False


        if (
            not mas_isplayer_bday()
            and not mas_isplayer_bday(yesterday, use_date_year=True)
            and not persistent._mas_player_bday_left_on_bday
        ):
            persistent._mas_player_bday_decor = False



    python:
        if persistent.mas_late_farewell:
            store.mas_globals.late_farewell = True
            persistent.mas_late_farewell = False


    python:
        if persistent._mas_filereacts_just_reacted:
            queueEvent("mas_reaction_end")


        if (
            persistent._mas_filereacts_reacted_map
            and mas_pastOneDay(persistent._mas_filereacts_last_reacted_date)
        ):
            persistent._mas_filereacts_reacted_map = dict()


    $ store.mas_selspr.startup_prompt_check()


    $ mas_check_player_derand()


    python:
        for index in range(len(persistent.event_list)-1, -1, -1):
            item = persistent.event_list[index]
            
            
            if type(item) != tuple:
                new_data = (item, False)
            else:
                new_data = item
            
            
            if renpy.has_label(new_data[0]):
                persistent.event_list[index] = new_data
            
            else:
                persistent.event_list.pop(index)


    $ MASUndoActionRule.check_persistent_rules()

    $ MASStripDatesRule.check_persistent_rules(persistent._mas_strip_dates_rules)


    if persistent._mas_filereacts_last_aff_gained_reset_date > today:
        $ persistent._mas_filereacts_last_aff_gained_reset_date = today


    if persistent._mas_filereacts_last_aff_gained_reset_date < today:
        $ persistent._mas_filereacts_gift_aff_gained = 0
        $ persistent._mas_filereacts_last_aff_gained_reset_date = today


    $ mas_songs.checkRandSongDelegate()


    $ store.mas_songs.checkSongAnalysisDelegate()


    $ mas_confirmedParty()


    if (
        persistent._mas_d25_gifts_given
        and not mas_isD25GiftHold()
        and not mas_globals.returned_home_this_sesh
    ):
        $ mas_d25SilentReactToGifts()


    $ mas_setTODVars()

    python:
        if seen_event('mas_gender'):
            mas_unlockEVL("monika_gender_redo","EVE")

        if seen_event('mas_preferredname'):
            mas_unlockEVL("monika_changename","EVE")


    $ mas_checkBackgroundChangeDelegate()



    $ store.mas_validate_suntimes()


    $ store.mas_background.buildupdate()




    python:
        if store.mas_dockstat.retmoni_status is not None:
            monika_chr.remove_acs(mas_acs_quetzalplushie)
            
            
            MASConsumable._reset()
            
            
            if not mas_inEVL("mas_consumables_remove_thermos"):
                queueEvent("mas_consumables_remove_thermos")
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
