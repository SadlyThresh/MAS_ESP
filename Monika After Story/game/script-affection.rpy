











































init python:

    mas_curr_affection = store.mas_affection.NORMAL
    mas_curr_affection_group = store.mas_affection.G_NORMAL

init -900 python in mas_affection:



    BROKEN = 1
    DISTRESSED = 2
    UPSET = 3
    NORMAL = 4
    HAPPY = 5
    AFFECTIONATE = 6
    ENAMORED = 7
    LOVE = 8


    _aff_order = [
        BROKEN,
        DISTRESSED,
        UPSET,
        NORMAL,
        HAPPY,
        AFFECTIONATE,
        ENAMORED,
        LOVE
    ]


    _aff_level_map = {}
    for _item in _aff_order:
        _aff_level_map[_item] = _item



    _aff_cascade_map = {
        BROKEN: DISTRESSED,
        DISTRESSED: UPSET,
        UPSET: NORMAL,
        HAPPY: NORMAL,
        AFFECTIONATE: HAPPY,
        ENAMORED: AFFECTIONATE,
        LOVE: ENAMORED
    }



    G_SAD = -1
    G_HAPPY = -2
    G_NORMAL = -3


    _affg_order = [
        G_SAD,
        G_NORMAL,
        G_HAPPY
    ]



    _affg_cascade_map = {
        G_SAD: G_NORMAL,
        G_HAPPY: G_NORMAL
    }


    FORCE_EXP_MAP = {
        BROKEN: "monika 6ckc_static",
        DISTRESSED: "monika 6rkc_static",
        UPSET: "monika 2esc_static",
        NORMAL: "monika 1eua_static",
        AFFECTIONATE: "monika 1eua_static",
        ENAMORED: "monika 1hua_static",
        LOVE: "monika 1hua_static",
    }

    RANDCHAT_RANGE_MAP = {
        BROKEN: 1,
        DISTRESSED: 2,
        UPSET: 3,
        NORMAL: 4,
        HAPPY: 4,
        AFFECTIONATE: 5,
        ENAMORED: 6,
        LOVE: 6
    }


    def _compareAff(aff_1, aff_2):
        """
        See mas_compareAff for explanation
        """
        
        if aff_1 == aff_2:
            return 0
        
        
        if aff_1 not in _aff_order or aff_2 not in _aff_order:
            return 0
        
        
        if _aff_order.index(aff_1) < _aff_order.index(aff_2):
            return -1
        
        return 1


    def _compareAffG(affg_1, affg_2):
        """
        See mas_compareAffG for explanation
        """
        
        if affg_1 == affg_2:
            return 0
        
        
        if affg_1 not in _affg_order or affg_2 not in _affg_order:
            return 0
        
        
        if _affg_order.index(affg_1) < _affg_order.index(affg_2):
            return -1
        
        return 1


    def _betweenAff(aff_low, aff_check, aff_high):
        """
        checks if the given affection level is between the given low and high.
        See mas_betweenAff for explanation
        """
        aff_check = _aff_level_map.get(aff_check, None)
        
        
        if aff_check is None:
            
            return False
        
        
        aff_low = _aff_level_map.get(aff_low, None)
        aff_high = _aff_level_map.get(aff_high, None)
        
        if aff_low is None and aff_high is None:
            
            
            return True
        
        if aff_low is None:
            
            
            return _compareAff(aff_check, aff_high) <= 0
        
        if aff_high is None:
            
            
            return _compareAff(aff_check, aff_low) >= 0
        
        
        
        comp_low_high = _compareAff(aff_low, aff_high)
        if comp_low_high > 0:
            
            
            return False
        
        if comp_low_high == 0:
            
            return _compareAff(aff_low, aff_check) == 0
        
        
        return (
            _compareAff(aff_low, aff_check) <= 0
            and _compareAff(aff_check, aff_high) <= 0
        )


    def _isValidAff(aff_check):
        """
        Returns true if the given affection is a valid affection state

        NOTE: None is considered valid
        """
        if aff_check is None:
            return True
        
        return aff_check in _aff_level_map


    def _isValidAffRange(aff_range):
        """
        Returns True if the given aff range is a valid aff range.

        IN:
            aff_range - tuple of the following format:
                [0]: lower bound
                [1]: upper bound
            NOTE: Nones are considerd valid.
        """
        if aff_range is None:
            return True
        
        low, high = aff_range
        
        if not _isValidAff(low):
            return False
        
        if not _isValidAff(high):
            return False
        
        if low is None and high is None:
            return True
        
        return _compareAff(low, high) <= 0





    AFF_MAX_POS_TRESH = 100
    AFF_MIN_POS_TRESH = 30
    AFF_MIN_NEG_TRESH = -30
    AFF_MAX_NEG_TRESH = -75


    AFF_BROKEN_MIN = -100
    AFF_DISTRESSED_MIN = -75
    AFF_UPSET_MIN = -30
    AFF_HAPPY_MIN = 30
    AFF_AFFECTIONATE_MIN = 100
    AFF_ENAMORED_MIN = 400
    AFF_LOVE_MIN = 1000


    AFF_MOOD_HAPPY_MIN = 30
    AFF_MOOD_SAD_MIN = -30


    AFF_TIME_CAP = -101


init -1 python in mas_affection:
    import os
    import datetime
    import store.mas_utils as mas_utils
    import store



    if store.persistent._mas_affection_log_counter is None:
        
        store.persistent._mas_affection_log_counter = 0

    elif store.persistent._mas_affection_log_counter >= 500:
        
        mas_utils.logrotate(
            os.path.normcase(renpy.config.basedir + "/log/"),
            "aff_log.txt"
        )
        store.persistent._mas_affection_log_counter = 0

    else:
        
        store.persistent._mas_affection_log_counter += 1


    log = renpy.store.mas_utils.getMASLog("log/aff_log", append=True)
    log_open = log.open()
    log.raw_write = True
    log.write("VERSION: {0}\n".format(store.persistent.version_number))



    _audit = "[{0}]: {1} | {2} | {3} -> {4}\n"


    _audit_f = "[{0}]: {5} | {1} | {2} | {3} -> {4}\n"
    _freeze_text = "!FREEZE!"
    _bypass_text = "!BYPASS!"

    def audit(change, new, frozen=False, bypass=False, ldsv=None):
        """
        Audits a change in affection.

        IN:
            change - the amount we are changing by
            new - what the new affection value will be
            frozen - True means we were frozen, false measn we are not
            bypass - True means we bypassed, false means we did not
            ldsv - Set to the string to use instead of monikatopic
                NOTE: for load / save operations ONLY
        """
        if ldsv is None:
            piece_one = store.persistent.current_monikatopic
        else:
            piece_one = ldsv
        
        if frozen:
            
            
            if bypass:
                piece_five = _bypass_text
            else:
                piece_five = _freeze_text
            
            
            audit_text = _audit_f.format(
                datetime.datetime.now(),
                piece_one,
                change,
                store._mas_getAffection(),
                new,
                piece_five
            )
        
        else:
            audit_text = _audit.format(
                datetime.datetime.now(),
                piece_one,
                change,
                store._mas_getAffection(),
                new
            )
        
        log.write(audit_text)


    def raw_audit(old, new, change, tag):
        """
        Non affection-dependent auditing for general usage.

        IN:
            old - the "old" value
            new - the "new" value
            change - the chnage amount
            tag - a string to label this audit change
        """
        log.write(_audit.format(
            datetime.datetime.now(),
            tag,
            change,
            old,
            new
        ))


    def txt_audit(tag, msg):
        """
        Generic auditing in the aff log

        IN:
            tag - a string to label thsi audit
            msg - message to show
        """
        log.write("[{0}]: {1} | {2}\n".format(
            datetime.datetime.now(),
            tag,
            msg
        ))



    def _force_exp():
        """
        Determines appropriate forced expression for current affection.
        """
        curr_aff = store.mas_curr_affection
        
        if store.mas_isMoniNormal() and store.mas_isBelowZero():
            
            return "monika 1esc_static"
        
        return FORCE_EXP_MAP.get(curr_aff, "monika idle")



init 15 python in mas_affection:
    import store 
    import store.evhand as evhand
    import store.mas_selspr as mas_selspr
    import store.mas_layout as mas_layout
    persistent = renpy.game.persistent
    layout = store.layout













    def _brokenToDis():
        """
        Runs when transitioning from broken to distressed
        """
        
        layout.QUIT_YES = mas_layout.QUIT_YES_DIS
        layout.QUIT_NO = mas_layout.QUIT_NO_UPSET
        layout.QUIT = mas_layout.QUIT
        
        
        store.mas_idle_mailbox.send_rebuild_msg()


    def _disToBroken():
        """
        Runs when transitioning from distressed to broken
        """
        
        layout.QUIT_YES = mas_layout.QUIT_YES_BROKEN
        layout.QUIT_NO = mas_layout.QUIT_NO_BROKEN
        layout.QUIT = mas_layout.QUIT_BROKEN
        
        
        store.mas_randchat.reduceRandchatForAff(BROKEN)
        
        
        store.mas_idle_mailbox.send_rebuild_msg()


    def _disToUpset():
        """
        Runs when transitioning from distressed to upset
        """
        
        layout.QUIT_YES = mas_layout.QUIT_YES
        
        
        store.mas_idle_mailbox.send_rebuild_msg()


    def _upsetToDis():
        """
        Runs when transitioning from upset to distressed
        """
        
        layout.QUIT_YES = mas_layout.QUIT_YES_DIS
        if persistent._mas_acs_enable_promisering:
            renpy.store.monika_chr.remove_acs(renpy.store.mas_acs_promisering)
            persistent._mas_acs_enable_promisering = False
        
        
        store.mas_randchat.reduceRandchatForAff(DISTRESSED)
        
        
        store.mas_idle_mailbox.send_rebuild_msg()
        
        
        if store.monika_chr.clothes != store.mas_clothes_def:
            store.pushEvent("mas_change_to_def",skipeval=True)


    def _upsetToNormal():
        """
        Runs when transitioning from upset to normal
        """
        
        layout.QUIT_NO = mas_layout.QUIT_NO
        
        
        store.mas_idle_mailbox.send_rebuild_msg()
        
        
        store.mas_songs.checkSongAnalysisDelegate()


    def _normalToUpset():
        """
        Runs when transitioning from normal to upset
        """
        
        layout.QUIT_NO = mas_layout.QUIT_NO_UPSET
        
        
        store.mas_randchat.reduceRandchatForAff(UPSET)
        
        
        store.mas_idle_mailbox.send_rebuild_msg()


    def _normalToHappy():
        """
        Runs when transitioning from noraml to happy
        """
        
        layout.QUIT_NO = mas_layout.QUIT_NO_HAPPY
        
        
        if persistent._mas_text_speed_enabled:
            store.mas_enableTextSpeed()
        
        
        store.mas_idle_mailbox.send_rebuild_msg()
        
        
        if not store.seen_event("mas_blazerless_intro") and not store.mas_hasSpecialOutfit():
            store.queueEvent("mas_blazerless_intro")
        
        
        store.mas_selspr.unlock_clothes(store.mas_clothes_blazerless)
        
        
        store.mas_rmallEVL("mas_change_to_def")
        
        
        store.mas_songs.checkSongAnalysisDelegate(HAPPY)


    def _happyToNormal():
        """
        Runs when transitinong from happy to normal
        """
        
        layout.QUIT_NO = mas_layout.QUIT_NO
        
        
        store.mas_disableTextSpeed()
        
        
        store.mas_idle_mailbox.send_rebuild_msg()
        
        
        if store.monika_chr.clothes != store.mas_clothes_def and not store.mas_hasSpecialOutfit():
            store.pushEvent("mas_change_to_def",skipeval=True)
        
        
        store.mas_songs.checkSongAnalysisDelegate(NORMAL)


    def _happyToAff():
        """
        Runs when transitioning from happy to affectionate
        """
        
        layout.QUIT_YES = mas_layout.QUIT_YES_AFF
        if persistent.gender == "M" or persistent.gender == "F":
            layout.QUIT_NO = mas_layout.QUIT_NO_AFF_G
        else:
            layout.QUIT_NO = mas_layout.QUIT_NO_AFF_GL
        layout.QUIT = mas_layout.QUIT_AFF
        
        
        store.mas_idle_mailbox.send_rebuild_msg()
        
        
        store.mas_songs.checkSongAnalysisDelegate(AFFECTIONATE)

    def _affToHappy():
        """
        Runs when transitioning from affectionate to happy
        """
        
        layout.QUIT_YES = mas_layout.QUIT_YES
        layout.QUIT_NO = mas_layout.QUIT_NO_HAPPY
        layout.QUIT = mas_layout.QUIT
        
        
        
        
        
        
        
        
        persistent._mas_monika_nickname = "Monika"
        m_name = persistent._mas_monika_nickname
        
        
        store.mas_randchat.reduceRandchatForAff(HAPPY)
        
        
        store.mas_idle_mailbox.send_rebuild_msg()
        
        
        store.mas_songs.checkSongAnalysisDelegate(HAPPY)

    def _affToEnamored():
        """
        Runs when transitioning from affectionate to enamored
        """
        
        if store.seen_event("mas_monika_islands"):
            if store.mas_cannot_decode_islands:
                
                store.mas_addDelayedAction(2)
                
                
                store.mas_lockEventLabel("mas_monika_islands")
            
            else:
                
                store.mas_unlockEventLabel("mas_monika_islands")
        
        
        store.mas_idle_mailbox.send_rebuild_msg()
        
        
        store.mas_songs.checkSongAnalysisDelegate(ENAMORED)

    def _enamoredToAff():
        """
        Runs when transitioning from enamored to affectionate
        """
        
        
        store.mas_removeDelayedActions(1, 2)
        
        
        store.mas_randchat.reduceRandchatForAff(AFFECTIONATE)
        
        
        store.mas_idle_mailbox.send_rebuild_msg()
        
        
        store.mas_songs.checkSongAnalysisDelegate(AFFECTIONATE)

    def _enamoredToLove():
        """
        Runs when transitioning from enamored to love
        """
        
        layout.QUIT_NO = mas_layout.QUIT_NO_LOVE
        
        
        store.mas_unlockEventLabel("mas_compliment_thanks", eventdb=store.mas_compliments.compliment_database)
        
        
        store.mas_idle_mailbox.send_rebuild_msg()
        
        
        store.mas_songs.checkSongAnalysisDelegate(LOVE)

    def _loveToEnamored():
        """
        Runs when transitioning from love to enamored
        """
        
        if store.seen_event("mas_compliment_thanks"):
            store.mas_lockEventLabel("mas_compliment_thanks", eventdb=store.mas_compliments.compliment_database)
        
        
        store.mas_idle_mailbox.send_rebuild_msg()
        
        
        store.mas_songs.checkSongAnalysisDelegate(ENAMORED)

    def _gSadToNormal():
        """
        Runs when transitioning from sad group to normal group
        """
        return


    def _gNormalToSad():
        """
        Runs when transitioning from normal group to sad group
        """
        return


    def _gNormalToHappy():
        """
        Runs when transitioning from normal group to happy group
        """
        return


    def _gHappyToNormal():
        """
        Runs when transitioning from happy group to normal group
        """
        return










    _trans_pps = {
        BROKEN: (_brokenToDis, None),
        DISTRESSED: (_disToUpset, _disToBroken),
        UPSET: (_upsetToNormal, _upsetToDis),
        NORMAL: (_normalToHappy, _normalToUpset),
        HAPPY: (_happyToAff, _happyToNormal),
        AFFECTIONATE: (_affToEnamored, _affToHappy),
        ENAMORED: (_enamoredToLove, _enamoredToAff),
        LOVE: (None, _loveToEnamored)
    }


    _transg_pps = {
        G_SAD: (_gSadToNormal, None),
        G_NORMAL: (_gNormalToHappy, _gNormalToSad),
        G_HAPPY: (None, _gHappyToNormal)
    }


    def runAffPPs(start_aff, end_aff):
        """
        Runs programming points to transition from the starting affection
        to the ending affection

        IN:
            start_aff - starting affection
            end_aff - ending affection
        """
        comparison = _compareAff(start_aff, end_aff)
        if comparison == 0:
            
            return
        
        
        start_index = _aff_order.index(start_aff)
        end_index = _aff_order.index(end_aff)
        if comparison < 0:
            for index in range(start_index, end_index):
                to_up, to_down = _trans_pps[_aff_order[index]]
                if to_up is not None:
                    to_up()
        
        else:
            for index in range(start_index, end_index, -1):
                to_up, to_down = _trans_pps[_aff_order[index]]
                if to_down is not None:
                    to_down()
        
        
        store.mas_rebuildEventLists()


    def runAffGPPs(start_affg, end_affg):
        """
        Runs programming points to transition from the starting affection group
        to the ending affection group

        IN:
            start_affg - starting affection group
            end_affg - ending affection group
        """
        comparison = _compareAffG(start_affg, end_affg)
        if comparison == 0:
            
            return
        
        
        start_index = _affg_order.index(start_affg)
        end_index = _affg_order.index(end_affg)
        if comparison < 0:
            for index in range(start_index, end_index):
                to_up, to_down = _transg_pps[_affg_order[index]]
                if to_up is not None:
                    to_up()
        
        else:
            for index in range(start_index, end_index, -1):
                to_up, to_down = _transg_pps[_affg_order[index]]
                if to_down is not None:
                    to_down()


    def _isMoniState(aff_1, aff_2, lower=False, higher=False):
        """
        Compares the given affection values according to the affection
        state system

        By default, this will check if aff_1 == aff_2

        IN:
            aff_1 - affection to compare
            aff_2 - affection to compare
            lower - True means we want to check aff_1 <= aff_2
            higher - True means we want to check aff_1 >= aff_2

        RETURNS:
            True if the given affections pass the test we want to do.
            False otherwise
        """
        comparison = _compareAff(aff_1, aff_2)
        
        if comparison == 0:
            return True
        
        if lower:
            return comparison <= 0
        
        if higher:
            return comparison >= 0
        
        return False


    def _isMoniStateG(affg_1, affg_2, lower=False, higher=False):
        """
        Compares the given affection groups according to the affection group
        system

        By default, this will check if affg_1 == affg_2

        IN:
            affg_1 - affection group to compare
            affg_2 - affection group to compare
            lower - True means we want to check affg_1 <= affg_2
            higher - True means we want to check affg_1 >= affg_2

        RETURNS:
            true if the given affections pass the test we want to do.
            False otherwise
        """
        comparison = _compareAffG(affg_1, affg_2)
        
        if comparison == 0:
            return True
        
        if lower:
            return comparison <= 0
        
        if higher:
            return comparison >= 0
        
        return False








    talk_menu_quips = dict()
    play_menu_quips = dict()

    def _init_talk_quips():
        """
        Initializes the talk quiplists
        """
        global talk_menu_quips
        def save_quips(_aff, quiplist):
            mas_ql = store.MASQuipList(allow_label=False)
            for _quip in quiplist:
                mas_ql.addLineQuip(_quip)
            talk_menu_quips[_aff] = mas_ql
        
        
        
        quips = [
            "..."
        ]
        save_quips(BROKEN, quips)
        
        
        quips = [
            _("...¿Sí?"),
            _("...¿Oh?"),
            _("...¿Eh?"),
            _("...¿Hm?"),
            _("Podemos intentar hablar, supongo."),
            _("Supongo que podemos hablar."),
            _("Oh...¿Quieres hablar?"),
            _("Si quieres hablar, adelante."),
            _("Podemos hablar si realmente quieres."),
            _("¿Estás seguro de que quieres hablar conmigo?"),
            _("¿De verdad quieres hablar conmigo?"),
            _("Muy bien...si quieres hablar conmigo."),
            _("¿Seguro que quieres hablar?")
        ]
        save_quips(DISTRESSED, quips)
        
        
        quips = [
            _("¿Qué?"),
            _("¿Qué deseas?"),
            _("¿Ahora qué?"),
            _("¿Qué es?"),


        ]
        save_quips(UPSET, quips)
        
        
        quips = [
            _("¿Qué te gustaría hablar?"),
            _("¿Hay algo de lo que te gustaría hablar?")
        ]
        save_quips(NORMAL, quips)
        
        
        quips = [
            _("¿Qué te gustaría hablar?")
        ]
        save_quips(HAPPY, quips)
        
        
        quips = [
            _("¿Qué te gustaría hablar? <3"),
            _("¿De qué te gustaría hablar, [mas_get_player_nickname()]?"),
            _("¿Sí, [mas_get_player_nickname()]?"),
            _("¿Qué tienes en mente, [mas_get_player_nickname()]?"),
        ]
        save_quips(AFFECTIONATE, quips)
        
        
        quips = [
            _("¿Qué te gustaría hablar? <3"),
            _("¿De qué te gustaría hablar, [mas_get_player_nickname()]?"),
            _("¿Sí, [mas_get_player_nickname()]?"),
            _("¿Qué tienes en mente, [mas_get_player_nickname()]?"),
        ]
        save_quips(ENAMORED, quips)
        
        
        quips = [

            _("¿Qué tienes en mente?"),
            _("¿Qué tienes en mente, [mas_get_player_nickname()]?"),
            _("¿Algo en mente?"),
            _("¿Algo en mente, [mas_get_player_nickname()]?"),
            _("¿Qué pasa, [mas_get_player_nickname()]?"),

            _("¿Sí, [mas_get_player_nickname()]?"),
            _("^_^"),
            _("<3"),
            _("¿Algo de lo que te gustaría hablar?"),
            _("Podemos hablar de lo que quieras, [player].")
        ]
        save_quips(LOVE, quips)


    def _init_play_quips():
        """
        Initializes the play quipliust
        """
        global play_menu_quips
        def save_quips(_aff, quiplist):
            mas_ql = store.MASQuipList(allow_label=False)
            for _quip in quiplist:
                mas_ql.addLineQuip(_quip)
            play_menu_quips[_aff] = mas_ql
        
        
        
        quips = [
            _("...")
        ]
        save_quips(BROKEN, quips)
        
        
        quips = [
            _("...Seguro."),
            _("...Bien."),
            _("Supongo que podemos jugar un juego."),
            _("Supongo que si realmente quieres."),
            _("Supongo que un juego estaría bien."),
            _("...{w=0.5}Si, ¿por qué no?")
        ]
        save_quips(DISTRESSED, quips)
        
        
        quips = [
            _("...¿Qué juego?"),
            _("Okay."),
            _("Seguro."),


        ]
        save_quips(UPSET, quips)
        
        
        quips = [
            _("¿Qué te gustaría jugar?"),
            _("¿Qué tenías en mente?"),
            _("¿Algo específico que te gustaría jugar?")
        ]
        save_quips(NORMAL, quips)
        
        
        quips = [
            _("¿Qué te gustaría jugar?"),
            _("¿Qué tenías en mente?"),
            _("¿Algo específico que te gustaría jugar?")
        ]
        save_quips(HAPPY, quips)
        
        
        quips = [
            _("¿Qué te gustaría jugar? <3"),
            _("Elige lo que quieras, [mas_get_player_nickname()]."),
            _("Elige lo que quieras, [mas_get_player_nickname()].")
        ]
        save_quips(AFFECTIONATE, quips)
        
        
        quips = [
            _("¿Qué te gustaría jugar? <3"),
            _("Elige lo que quieras, [mas_get_player_nickname()]."),
            _("Elige lo que quieras, [mas_get_player_nickname()]."),
        ]
        save_quips(ENAMORED, quips)
        
        
        quips = [
            _("¿Qué te gustaría jugar? <3"),
            _("Elige lo que quieras, [mas_get_player_nickname()]."),
            _("Elige lo que quieras, [mas_get_player_nickname()]."),
            _("¡Yay! ¡Vamos a jugar juntos!"),
            _("¡Me encantaría jugar algo contigo!"),
            _("¡Me encantaría jugar contigo!")
        ]
        
        save_quips(LOVE, quips)

    _init_talk_quips()
    _init_play_quips()


    def _dict_quip(_quips):
        """
        Returns a quip based on the current affection using the given quip
        dict

        IN:
            _quips - quip dict to pull from

        RETURNS:
            quip or empty string if failure
        """
        quipper = _quips.get(store.mas_curr_affection, None)
        if quipper is not None:
            return quipper.quip()
        
        return ""


    def talk_quip():
        """
        Returns a talk quip based on the current affection
        """
        quip = _dict_quip(talk_menu_quips)
        if len(quip) > 0:
            return quip
        return _("¿De qué te gustaría hablar?")


    def play_quip():
        """
        Returns a play quip based on the current affection
        """
        quip = _dict_quip(play_menu_quips)
        if len(quip) > 0:
            return quip
        return _("¿Qué te gustaría jugar?")



default persistent._mas_long_absence = False
default persistent._mas_pctaieibe = None
default persistent._mas_pctaneibe = None
default persistent._mas_pctadeibe = None
default persistent._mas_aff_backup = None

init -10 python:
    if persistent._mas_aff_mismatches is None:
        persistent._mas_aff_mismatches = 0

    def _mas_AffSave():
        aff_value = _mas_getAffection()
        
        
        
        
        
        
        persistent._mas_pctaieibe = None
        persistent._mas_pctaneibe = None
        persistent._mas_pctadeibe = None
        
        
        store.mas_affection.audit(aff_value, aff_value, ldsv="SAVE")
        
        
        if persistent._mas_aff_backup != aff_value:
            store.mas_affection.raw_audit(
                persistent._mas_aff_backup,
                aff_value,
                aff_value,
                "SET BACKUP"
            )
            persistent._mas_aff_backup = aff_value


    def _mas_AffLoad():
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        persistent._mas_pctaieibe = None
        persistent._mas_pctaneibe = None
        persistent._mas_pctadeibe = None
        
        
        if (
                persistent._mas_affection is None
                or "affection" not in persistent._mas_affection
            ):
            if persistent._mas_aff_backup is None:
                new_value = 0
                store.mas_affection.txt_audit("LOAD", "No backup found")
            
            else:
                new_value = persistent._mas_aff_backup
                store.mas_affection.txt_audit("LOAD", "Loading from backup")
        
        else:
            new_value = persistent._mas_affection["affection"]
            store.mas_affection.txt_audit("LOAD", "Loading from system")
        
        
        store.mas_affection.raw_audit(0, new_value, new_value, "LOAD?")
        
        
        if persistent._mas_aff_backup is None:
            persistent._mas_aff_backup = new_value
            
            
            store.mas_affection.raw_audit(
                "None",
                new_value,
                new_value,
                "NEW BACKUP"
            )
        
        
        else:
            
            if new_value != persistent._mas_aff_backup:
                persistent._mas_aff_mismatches += 1
                store.mas_affection.txt_audit(
                    "MISMATCHES",
                    persistent._mas_aff_mismatches
                )
                store.mas_affection.raw_audit(
                    new_value,
                    persistent._mas_aff_backup,
                    persistent._mas_aff_backup,
                    "RESTORE"
                )
                new_value = persistent._mas_aff_backup
        
        
        store.mas_affection.audit(new_value, new_value, ldsv="LOAD COMPLETE")
        
        
        persistent._mas_affection["affection"] = new_value



init 20 python:

    import datetime
    import store.mas_affection as affection
    import store.mas_utils as mas_utils


    def mas_FreezeGoodAffExp():
        persistent._mas_affection_goodexp_freeze = True

    def mas_FreezeBadAffExp():
        persistent._mas_affection_badexp_freeze = True

    def mas_FreezeBothAffExp():
        mas_FreezeGoodAffExp()
        mas_FreezeBadAffExp()

    def mas_UnfreezeBadAffExp():
        persistent._mas_affection_badexp_freeze = False

    def mas_UnfreezeGoodAffExp():
        persistent._mas_affection_goodexp_freeze = False

    def mas_UnfreezeBothExp():
        mas_UnfreezeBadAffExp()
        mas_UnfreezeGoodAffExp()



    def _mas_getAffection():
        if persistent._mas_affection is not None:
            return persistent._mas_affection.get(
                "affection",
                persistent._mas_aff_backup
            )
        
        return persistent._mas_aff_backup


    def _mas_getBadExp():
        if persistent._mas_affection is not None:
            return persistent._mas_affection.get(
                "badexp",
                1
            )
        return 1


    def _mas_getGoodExp():
        if persistent._mas_affection is not None:
            return persistent._mas_affection.get(
                "goodexp",
                1
            )
        return 1


    def _mas_getTodayExp():
        if persistent._mas_affection is not None:
            return persistent._mas_affection.get("today_exp", 0)
        
        return 0



    def mas_isBelowZero():
        return _mas_getAffection() < 0




    def mas_betweenAff(aff_low, aff_check, aff_high):
        """
        Checks if the given affection is between the given affection levels.

        If low is actually greater than high, then False is always returned

        IN:
            aff_low - the lower bound of affecton to check with (inclusive)
                if None, then we assume no lower bound
            aff_check - the affection to check
            aff_high - the upper bound of affection to check with (inclusive)
                If None, then we assume no upper bound

        RETURNS:
            True if the given aff check is within the bounds of the given
            lower and upper affection limits, False otherwise.
            If low is greater than high, False is returned.
        """
        return affection._betweenAff(aff_low, aff_check, aff_high)


    def mas_compareAff(aff_1, aff_2):
        """
        Runs compareTo logic on the given affection states

        IN:
            aff_1 - an affection state to compare
            aff_2 - an affection state to compare

        RETURNS:
            negative number if aff_1 < aff_2
            0 if aff_1 == aff_2
            postitive number if aff_1 > aff_2
            Returns 0 if a non affection state was provided
        """
        return affection._compareAff(aff_1, aff_2)


    def mas_compareAffG(affg_1, affg_2):
        """
        Runs compareTo logic on the given affection groups

        IN:
            affg_1 - an affection group to compare
            affg_2 - an affection group to compare

        RETURNS:
            negative number if affg_1 < affg_2
            0 if affg_1 == affg_2
            positive numbre if affg_1 > affg_2
            Returns 0 if a non affection group was provided
        """
        return affection._compareAffG(affg_1, affg_2)




    def mas_isMoniBroken(lower=False, higher=False):
        """
        Checks if monika is broken

        IN:
            lower - True means we include everything below this affection state
                as broken as well
                (Default: False)
            higher - True means we include everything above this affection
                state as broken as well
                (Default: False)

        RETURNS:
            True if monika is broke, False otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.BROKEN,
            higher=higher
        )


    def mas_isMoniDis(lower=False, higher=False):
        """
        Checks if monika is distressed

        IN:
            lower - True means we cinlude everything below this affection state
                as distressed as well
                NOTE: takes precedence over higher
                (Default: False)
            higher - True means we include everything above this affection
                state as distressed as well
                (Default: FAlse)

        RETURNS:
            True if monika is distressed, false otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.DISTRESSED,
            lower=lower,
            higher=higher
        )


    def mas_isMoniUpset(lower=False, higher=False):
        """
        Checks if monika is upset

        IN:
            lower - True means we include everything below this affection
                state as upset as well
                (Default: False)
            higher - True means we include everything above this affection
                state as upset as well
                (Default: False)

        RETURNS:
            True if monika is upset, false otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.UPSET,
            lower=lower,
            higher=higher
        )


    def mas_isMoniNormal(lower=False, higher=False):
        """
        Checks if monika is normal

        IN:
            lower - True means we include everything below this affection state
                as normal as well
                (Default: False)
            higher - True means we include evreything above this affection
                state as normal as well
                (Default: False)

        RETURNS:
            True if monika is normal, false otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.NORMAL,
            lower=lower,
            higher=higher
        )


    def mas_isMoniHappy(lower=False, higher=False):
        """
        Checks if monika is happy

        IN:
            lower - True means we include everything below this affection
                state as happy as well
                (Default: False)
            higher - True means we include everything above this affection
                state as happy as well
                (Default: False)

        RETURNS:
            True if monika is happy, false otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.HAPPY,
            lower=lower,
            higher=higher
        )


    def mas_isMoniAff(lower=False, higher=False):
        """
        Checks if monika is affectionate

        IN:
            lower - True means we include everything below this affection
                state as affectionate as well
                (Default: FAlse)
            higher - True means we include everything above this affection
                state as affectionate as well
                (Default: False)

        RETURNS:
            True if monika is affectionate, false otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.AFFECTIONATE,
            lower=lower,
            higher=higher
        )


    def mas_isMoniEnamored(lower=False, higher=False):
        """
        Checks if monika is enamored

        IN:
            lower - True means we include everything below this affection
                state as enamored as well
                (Default: False)
            higher - True means we include everything above this affection
                state as enamored as well
                (Default: False)

        RETURNS:
            True if monika is enamored, false otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.ENAMORED,
            lower=lower,
            higher=higher
        )


    def mas_isMoniLove(lower=False, higher=False):
        """
        Checks if monika is in love

        IN:
            lower - True means we include everything below this affectionate
                state as love as well
                (Default: False)
            higher - True means we include everything above this affection
                state as love as well
                (Default: False)

        RETURNS:
            True if monika in love, false otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.LOVE,
            lower=lower
        )



    def mas_isMoniGSad(lower=False, higher=False):
        """
        Checks if monika is in sad affection group

        IN:
            lower - True means we include everything below this affection
                group as sad as well
                (Default: False)
            higher - True means we include everything above this affection
                group as sad as well
                (Default: False)

        RETURNS:
            True if monika in sad group, false otherwise
        """
        return affection._isMoniStateG(
            mas_curr_affection_group,
            store.mas_affection.G_SAD,
            higher=higher
        )


    def mas_isMoniGNormal(lower=False, higher=False):
        """
        Checks if monika is in normal affection group

        IN:
            lower - True means we include everything below this affection
                group as normal as well
                (Default: False)
            higher - True means we include everything above this affection
                group as normal as well
                (Default: False)

        RETURNS:
            True if monika is in normal group, false otherwise
        """
        return affection._isMoniStateG(
            mas_curr_affection_group,
            store.mas_affection.G_NORMAL,
            lower=lower,
            higher=higher
        )


    def mas_isMoniGHappy(lower=False, higher=False):
        """
        Checks if monika is in happy affection group

        IN:
            lower - True means we include everything below this affection
                group as happy as well
                (Default: False)
            higher - True means we include everything above this affection
                group as happy as well
                (Default: FAlse)

        RETURNS:
            True if monika is in happy group, false otherwise
        """
        return affection._isMoniStateG(
            mas_curr_affection_group,
            store.mas_affection.G_HAPPY,
            lower=lower
        )



    def mas_updateAffectionExp(skipPP=False):
        global mas_curr_affection
        global mas_curr_affection_group
        
        
        curr_affection = _mas_getAffection()
        
        
        if  affection.AFF_MIN_POS_TRESH <= curr_affection:
            persistent._mas_affection["goodexp"] = 3
            persistent._mas_affection["badexp"] = 1
        
        
        elif affection.AFF_MAX_NEG_TRESH < curr_affection <= affection.AFF_MIN_NEG_TRESH:
            persistent._mas_affection["goodexp"] = 0.5
            persistent._mas_affection["badexp"] = 3
        
        
        elif curr_affection <= affection.AFF_MAX_NEG_TRESH:
            persistent._mas_affection["badexp"] = 5
        
        
        new_aff = mas_curr_affection
        if curr_affection <= affection.AFF_BROKEN_MIN:
            new_aff = affection.BROKEN
        
        elif affection.AFF_BROKEN_MIN < curr_affection <= affection.AFF_DISTRESSED_MIN:
            new_aff = affection.DISTRESSED
        
        elif affection.AFF_DISTRESSED_MIN < curr_affection <= affection.AFF_UPSET_MIN:
            new_aff = affection.UPSET
        
        elif affection.AFF_UPSET_MIN < curr_affection < affection.AFF_HAPPY_MIN:
            new_aff = affection.NORMAL
        
        elif affection.AFF_HAPPY_MIN <= curr_affection < affection.AFF_AFFECTIONATE_MIN:
            new_aff = store.mas_affection.HAPPY
        
        elif affection.AFF_AFFECTIONATE_MIN <= curr_affection < affection.AFF_ENAMORED_MIN:
            new_aff = affection.AFFECTIONATE
        
        elif affection.AFF_ENAMORED_MIN <= curr_affection < affection.AFF_LOVE_MIN:
            new_aff = affection.ENAMORED
        
        elif curr_affection >= affection.AFF_LOVE_MIN:
            new_aff = affection.LOVE
        
        
        if new_aff != mas_curr_affection:
            if not skipPP:
                affection.runAffPPs(mas_curr_affection, new_aff)
            mas_curr_affection = new_aff
        
        
        new_affg = mas_curr_affection_group
        if curr_affection <= affection.AFF_MOOD_SAD_MIN:
            new_affg = affection.G_SAD
        
        elif curr_affection >= affection.AFF_MOOD_HAPPY_MIN:
            new_affg = affection.G_HAPPY
        
        else:
            new_affg = affection.G_NORMAL
        
        if new_affg != mas_curr_affection_group:
            if not skipPP:
                affection.runAffGPPs(mas_curr_affection_group, new_affg)
            mas_curr_affection_group = new_affg



    def mas_gainAffection(
            amount=None,
            modifier=1,
            bypass=False
        ):
        
        if amount is None:
            amount = _mas_getGoodExp()
        
        
        if mas_pastOneDay(persistent._mas_affection.get("freeze_date")):
            persistent._mas_affection["freeze_date"] = datetime.date.today()
            persistent._mas_affection["today_exp"] = 0
            mas_UnfreezeGoodAffExp()
        
        
        frozen = persistent._mas_affection_goodexp_freeze
        change = (amount * modifier)
        new_value = _mas_getAffection() + change
        if new_value > 1000000:
            new_value = 1000000
        
        
        affection.audit(change, new_value, frozen, bypass)
        
        
        if not frozen or bypass:
            
            persistent._mas_affection["affection"] = new_value
            
            if not bypass:
                persistent._mas_affection["today_exp"] = (
                    _mas_getTodayExp() + change
                )
                if persistent._mas_affection["today_exp"] >= 7:
                    mas_FreezeGoodAffExp()
            
            
            mas_updateAffectionExp()














    def mas_loseAffection(
            amount=None,
            modifier=1,
            reason=None,
            ev_label=None,
            apology_active_expiry=datetime.timedelta(hours=3),
            apology_overall_expiry=datetime.timedelta(weeks=1),
        ):
        
        if amount is None:
            amount = _mas_getBadExp()
        
        
        mas_setApologyReason(reason=reason,ev_label=ev_label,apology_active_expiry=apology_active_expiry,apology_overall_expiry=apology_overall_expiry)
        
        
        frozen = persistent._mas_affection_badexp_freeze
        change = (amount * modifier)
        new_value = _mas_getAffection() - change
        if new_value < -1000000:
            new_value = -1000000
        
        
        affection.audit(change, new_value, frozen)
        
        if not frozen:
            
            persistent._mas_affection["affection"] = new_value
            
            
            mas_updateAffectionExp()


    def mas_setAffection(amount=None, logmsg="SET"):
        """
        Sets affection to a value

        NOTE: never use this to add / lower affection unless its to
          strictly set affection to a level for some reason.

        IN:
            amount - amount to set affection to
            logmsg - msg to show in the log
                (Default: SET)
        """
        
        
        
        
        
        if amount is None:
            amount = _mas_getAffection()
        
        
        affection.audit(amount, amount, False, ldsv=logmsg)
        
        
        
        persistent._mas_affection["affection"] = amount
        
        mas_updateAffectionExp()

    def mas_setApologyReason(
        reason=None,
        ev_label=None,
        apology_active_expiry=datetime.timedelta(hours=3),
        apology_overall_expiry=datetime.timedelta(weeks=1)
        ):
        """
        Sets a reason for apologizing

        IN:
            reason - The reason for the apology (integer value corresponding to item in the apology_reason_db)
                (if left None, and an ev_label is present, we assume a non-generic apology)
            ev_label - The apology event we want to unlock
                (required)
            apology_active_expiry - The amount of session time after which, the apology that was added expires
                defaults to 3 hours active time
            apology_overall_expiry - The amount of overall time after which, the apology that was added expires
                defaults to 7 days
        """
        
        global mas_apology_reason
        
        if ev_label is None:
            if reason is None:
                mas_apology_reason = 0
            else:
                mas_apology_reason = reason
            return
        elif mas_getEV(ev_label) is None:
            store.mas_utils.writelog(
                "[ERROR]: ev_label does not exist: {0}\n".format(repr(ev_label))
            )
            return
        
        if ev_label not in persistent._mas_apology_time_db:
            
            store.mas_unlockEVL(ev_label, 'APL')
            
            
            current_total_playtime = persistent.sessions['total_playtime'] + mas_getSessionLength()
            
            
            persistent._mas_apology_time_db[ev_label] = (current_total_playtime + apology_active_expiry,datetime.date.today() + apology_overall_expiry)
            return


    def mas_checkAffection():
        
        curr_affection = _mas_getAffection()
        
        
        if curr_affection <= -15 and not seen_event("mas_affection_upsetwarn"):
            queueEvent("mas_affection_upsetwarn", notify=True)
        
        
        
        elif 15 <= curr_affection and not seen_event("mas_affection_happynotif"):
            queueEvent("mas_affection_happynotif", notify=True)
        
        
        elif curr_affection >= 100 and not seen_event("monika_affection_nickname"):
            queueEvent("monika_affection_nickname", notify=True)
        
        
        elif curr_affection <= -50 and not seen_event("mas_affection_apology"):
            if not persistent._mas_disable_sorry:
                queueEvent("mas_affection_apology", notify=True)







    mas_apology_reason = None

    def _mas_AffStartup():
        
        
        _mas_AffLoad()
        
        
        
        mas_updateAffectionExp()
        
        if persistent.sessions["last_session_end"] is not None:
            persistent._mas_absence_time = (
                datetime.datetime.now() -
                persistent.sessions["last_session_end"]
            )
        else:
            persistent._mas_absence_time = datetime.timedelta(days=0)
        
        
        if not persistent._mas_long_absence:
            time_difference = persistent._mas_absence_time
            
            
            if (
                    not config.developer
                    and time_difference >= datetime.timedelta(weeks = 1)
                ):
                new_aff = _mas_getAffection() - (
                    0.5 * time_difference.days
                )
                if new_aff < affection.AFF_TIME_CAP:
                    
                    store.mas_affection.txt_audit("ABS", "capped loss")
                    mas_setAffection(affection.AFF_TIME_CAP)
                    
                    
                    if time_difference >= datetime.timedelta(days=(365 * 10)):
                        store.mas_affection.txt_audit("ABS", "10 year diff")
                        mas_loseAffection(200)
                
                else:
                    store.mas_affection.txt_audit("ABS", "she missed you")
                    mas_setAffection(new_aff)





init 5 python:
    addEvent(
        Event(persistent.event_database,
            eventlabel='monika_affection_nickname',
            prompt="Monikas infinitas",
            category=['monika'],
            random=False,
            pool=True,
            unlocked=True,
            rules={"no_unlock": None},
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        restartBlacklist=True
    )


default persistent._mas_pm_called_moni_a_bad_name = False


default persistent._mas_offered_nickname = False


default persistent._mas_grandfathered_nickname = None

label monika_affection_nickname:
    python:

        good_monika_nickname_comp = re.compile('|'.join(mas_good_monika_nickname_list), re.IGNORECASE)


        aff_nickname_ev = mas_getEV("monika_affection_nickname")

    if not persistent._mas_offered_nickname:
        m 1euc "I've been thinking, [player]..."
        m 3eud "You know how there are potentially infinite Monikas right?"

        if renpy.seen_label('monika_clones'):
            m 3eua "We did discuss this before after all."

        m 3hua "Well, I thought of a solution!"
        m 3eua "Why don't you give me a nickname? It'd make me the only Monika in the universe with that name."
        m 3eka "And it would mean a lot if you choose one for me~"
        m 3hua "I'll still get the final say, though!"
        m "What do you say?{nw}"
        python:
            if aff_nickname_ev:
                
                aff_nickname_ev.prompt = _("¿Puedo llamarte con un nombre diferente?")
                Event.lockInit("prompt", ev=aff_nickname_ev)
                persistent._mas_offered_nickname = True


            pnick_ev = mas_getEV("mas_affection_playernickname")
            if pnick_ev:
                pnick_ev.start_date = datetime.datetime.now() + datetime.timedelta(hours=2)
    else:

        jump monika_affection_nickname_yes

    $ _history_list.pop()
    menu:
        m "What do you say?{fast}"
        "Sí.":
            label monika_affection_nickname_yes:
                pass

            show monika 1eua zorder MAS_MONIKA_Z at t11

            $ done = False
            while not done:
                python:
                    inputname = mas_input(
                        _("Entonces, ¿cómo quieres llamarme?"),
                        allow=name_characters_only,
                        length=10,
                        screen_kwargs={"use_return_button": True}
                    ).strip(' \t\n\r')

                    lowername = inputname.lower()


                if lowername == "cancel_input":
                    m 1euc "Oh, I see."
                    m 1tkc "Well...that's a shame."
                    m 3eka "But that's okay. I like '[m_name]' anyway."
                    $ done = True

                elif not lowername:
                    m 1lksdla "..."
                    m 1hksdrb "You have to give me a name, [player]!"
                    m "I swear you're just so silly sometimes."
                    m 1eka "Try again!"

                elif lowername != "monika" and lowername == player.lower():
                    m 1euc "..."
                    m 1lksdlb "That's your name, [player]! Give me my own!"
                    m 1eka "Try again~"

                elif lowername == m_name.lower():
                    m 1euc "..."
                    m 1hksdlb "I thought we were choosing a new name, silly."
                    m 1eka "Try again~"

                elif re.findall("mon(-|\\s)+ika", lowername):
                    m 2tfc "..."
                    m 2esc "Try again."
                    show monika 1eua

                elif persistent._mas_grandfathered_nickname and lowername == persistent._mas_grandfathered_nickname.lower():
                    jump monika_affection_nickname_yes.neutral_accept

                elif mas_awk_name_comp.search(inputname):
                    m 1rkc "..."
                    m 1rksdld "While I don't hate it, I don't think I'm comfortable with you calling me that."
                    m 1eka "Can you choose something more appropriate, [player]?"
                else:

                    if not mas_bad_name_comp.search(inputname) and lowername not in ["yuri", "sayori", "natsuki"]:
                        if inputname == "Monika":
                            m 3hua "Ehehe, back to the classics I see~"

                        elif good_monika_nickname_comp.search(inputname):
                            m 1wuo "Oh! That's a wonderful name!"
                            m 3ekbsa "Thank you, [player]. You're such a sweetheart!~"
                        else:

                            label monika_affection_nickname_yes.neutral_accept:
                                pass

                            m 1duu "[inputname]... That's a pretty nice name."
                            m 3ekbsa "Thank you [player], you're so sweet~"

                        $ persistent._mas_monika_nickname = inputname
                        $ m_name = inputname

                        m 1eua "Okay!"
                        if m_name == "Monika":
                            m 1hua "I'll go back to my name, then."
                        else:

                            m 3hua "From now on, you can call me '[m_name].'"
                            m 1hua "Ehehe~"
                        $ done = True
                    else:


                        $ mas_loseAffection(ev_label="mas_apology_bad_nickname")
                        if lowername in ["yuri", "sayori", "natsuki"]:
                            m 1wud "...!"
                            m 2wfw "I..."
                            m "I...can't believe you just did that, [player]."
                            m 2wfx "Are you really trying to give me her name?"
                            m 2dfd ".{w=0.5}.{w=0.5}.{nw}"
                            m 2dfc ".{w=0.5}.{w=0.5}.{nw}"
                            m 2rkc "I thought you..."
                            m 2dfc "..."
                            m 2lfc "I can't believe this, [player]."
                            m 2dfc "..."
                            m 2lfc "That really hurt."
                            m "A lot more than what you can imagine."

                            if mas_getEVL_shown_count("mas_apology_bad_nickname") == 2:
                                call monika_affection_nickname_bad_lock from _call_monika_affection_nickname_bad_lock

                            show monika 1efc
                            pause 5.0
                        else:

                            m 4efd "[player]! That's not nice at all!"
                            m 2efc "Why would you say such things?"
                            m 2rfw "If you didn't want to do this, you should've just said so!"
                            m 2dftdc "..."
                            m 2ektsc "...You didn't have to be so mean."
                            m 2dftdc "That really hurt, [player]."

                            if mas_getEVL_shown_count("mas_apology_bad_nickname") == 2:
                                call monika_affection_nickname_bad_lock from _call_monika_affection_nickname_bad_lock_1
                            else:
                                m 2efc "Please don't do that again."

                        $ persistent._mas_called_moni_a_bad_name = True


                        if m_name.lower() != "monika":
                            $ m_name = "Monika"
                            $ persistent._mas_monika_nickname = "Monika"

                        $ mas_lockEVL("monika_affection_nickname", "EVE")
                        $ done = True
        "No.":

            m 1ekc "Oh..."
            m 1lksdlc "Alright then, if you say so."
            m 3eka "Just tell me if you ever change your mind, [player]."
            $ done = True
    return

label monika_affection_nickname_bad_lock:
    m 2efc "Forget about this idea."
    m "It seems it was a mistake."
    m 1efc "Let's talk about something else."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_affection_playernickname",
            conditional="seen_event('monika_affection_nickname')",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

default persistent._mas_player_nicknames = list()

label mas_affection_playernickname:
    python:

        base_nicknames = [
            ("Querido", "querido", True, True, False),
            ("Cariño", "cariño", True, True, False),
            ("Amor", "amor", True, True, False),
            ("Mi amor", "mi amor", True, True, False),
            ("Corazón", "corazón", True, True, False),
            ("Corazoncito", "corazoncito", True, True, False),
        ]

    m 1euc "Hey, [player]?"
    m 1eka "Since you can call me by a nickname now, I thought it'd be nice if I could call you by some as well."

    m 1etc "Is that alright with you?{nw}"
    $ _history_list.pop()
    menu:
        m "Is that alright with you?{fast}"
        "Seguro, [m_name].":

            m 1hua "Great!"
            m 3eud "I should ask though, what names are you comfortable with?"
            call mas_player_nickname_loop ("Deselect the names you're not comfortable with me calling you.", base_nicknames) from _call_mas_player_nickname_loop
        "No.":

            m 1eka "Alright, [player]."
            m 3eua "Just let me know if you ever change your mind, okay?"


    $ mas_unlockEVL("monika_change_player_nicknames", "EVE")
    return "no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_change_player_nicknames",
            prompt="¿Puedes llamarme con un apodo diferente?",
            category=['tú'],
            pool=True,
            unlocked=False,
            rules={"no_unlock": None},
            aff_range=(mas_aff.AFFECTIONATE,None)
        )
    )

label monika_change_player_nicknames:
    m 1hub "Sure [player]!"

    python:

        if not persistent._mas_player_nicknames:
            current_nicknames = [
                ("Querido", "querido", False, True, False),
                ("Cariño", "cariño", False, True, False),
                ("Amor", "amor", False, True, False),
                ("Mi amor", "mi amor", False, True, False),
                ("Corazón", "corazón", False, True, False),
                ("Corazoncito", "corazoncito", False, True, False),
            ]
            dlg_line = "Escoge los nombres que quieras que te llame."

        else:
            current_nicknames = [
                (nickname.capitalize(), nickname, True, True, False)
                for nickname in persistent._mas_player_nicknames
            ]
            dlg_line = "Deselecciona los nombres que no quieres que te llame más."

    call mas_player_nickname_loop ("[dlg_line]", current_nicknames) from _call_mas_player_nickname_loop_1
    return

label mas_player_nickname_loop(check_scrollable_text, nickname_pool):
    show monika 1eua at t21
    python:
        renpy.say(m, renpy.substitute(check_scrollable_text), interact=False)
        nickname_pool.sort()
    call screen mas_check_scrollable_menu(nickname_pool, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, selected_button_prompt="Done", default_button_prompt="Done")

    python:
        done = False
        acceptable_nicknames = _return.keys()

        if acceptable_nicknames:
            dlg_line = "¿Hay algo más que quieras que te llame?"

        else:
            dlg_line = "¿Hay algo más que quieras que te llame en su lugar?"

        lowerplayer = player.lower()
        cute_nickname_pattern = "(?:{0}|{1})\\w?y".format(lowerplayer, lowerplayer[0:-1])

    show monika at t11
    while not done:
        m 1eua "[dlg_line]{nw}"
        $ _history_list.pop()
        menu:
            m "[dlg_line]{fast}"
            "Sí.":

                label mas_player_nickname_loop.name_enter_skip_loop:
                    pass


                python:
                    lowername = mas_input(
                        _("Entonces, ¿cómo quieres que te llame?"),
                        allow=" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_",
                        length=10,
                        screen_kwargs={"use_return_button": True, "return_button_value": "nevermind"}
                    ).strip(' \t\n\r').lower()

                    is_cute_nickname = bool(re.search(cute_nickname_pattern, lowername))


                if lowername == "nevermind":
                    $ done = True

                elif lowername == "":
                    m 1eksdla "..."
                    m 3rksdlb "You have to give me a name to call you, [player]..."
                    m 1eua "Try again~"
                    jump mas_player_nickname_loop.name_enter_skip_loop

                elif lowername == lowerplayer:
                    m 2hua "..."
                    m 4hksdlb "That's the same name you have right now, silly!"
                    m 1eua "Try again~"
                    jump mas_player_nickname_loop.name_enter_skip_loop

                elif not is_cute_nickname and mas_awk_name_comp.search(lowername):
                    $ awkward_quip = renpy.substitute(renpy.random.choice(mas_awkward_quips))
                    m 1rksdlb "[awkward_quip]"
                    m 3rksdla "Could you pick a more...{w=0.2}{i}appropriate{/i} name please?"
                    jump mas_player_nickname_loop.name_enter_skip_loop

                elif not is_cute_nickname and mas_bad_name_comp.search(lowername):
                    $ bad_quip = renpy.substitute(renpy.random.choice(mas_bad_quips))
                    m 1ekd "[bad_quip]"
                    m 3eka "Please pick a nicer name for yourself, okay?"
                    jump mas_player_nickname_loop.name_enter_skip_loop

                elif lowername in acceptable_nicknames:
                    m 3rksdla "You already told me I can call you that, [player]..."
                    m 1hua "Try again~"
                    jump mas_player_nickname_loop.name_enter_skip_loop
                else:


                    $ acceptable_nicknames.append(lowername)
            "No.":

                $ done = True

    if acceptable_nicknames:
        $ dlg_line = "Sólo hazme saber si alguna vez quiere que te llame por otros nombres, ¿de acuerdo?"
    else:

        $ dlg_line = "Sólo avísame si alguna vez cambias de opinión, ¿de acuerdo?"

    m 1hua "Alright, [player]."
    m 3eub "[dlg_line]"


    $ persistent._mas_player_nicknames = acceptable_nicknames
    return


label mas_affection_upsetwarn:
    m 1dsc "Hey, [player]..."
    m 1lksdlc "Recently, I've been feeling like my love and affection that I give is being...ignored."
    m 1dsc "I feel like you're giving me less and less of your love..."
    m 1dsd "I thought I'd let you know how I feel. After all, communication is the key to a strong relationship, right?"
    m 1eka "I hope there's nothing wrong between us, [player]."
    show monika idle with dissolve_monika
    return


label mas_affection_happynotif:
    m 1hua "Hey, [player]!"
    m 1eua "I just wanted to say thank you for being such a wonderful person."
    m 1ekbsa "The fact that you give me so much of your love means a lot to me. I really don't know where I'd be without you."
    m 1dubfu "I love you, [player]. Let's be like this forever~"
    show monika idle with dissolve_monika
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_every_rose",
            conditional="True",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.UPSET, mas_aff.UPSET),
        )
    )

label monika_every_rose:
    m 2duo "{i}~Was it something I said or something I did?~{/i}"
    m 2dkd "{i}~Did my words not come out right?~{/i}"
    m 2ekd "{i}~Thought I tried not to hurt you~{/i}"
    m 2dkc "{i}~Thought I tried~{/i}"
    m 2ekd "{i}~But I guess that's why they say~{/i}"
    m 2duo "{i}~Every rose has its thorn~{/i}"
    m 2dkc "..."
    m 4eka "You know, [player]...{w=0.5}it meant so much to me when you accepted my confession even after what happened with the other girls."

    if persistent._mas_pm_cares_about_dokis:
        m 4rksdla "...Even more so since I know how you cared about them."

    m 2dsc "I really wish things didn't have to turn out the way they did."
    m 4wkd "But I did {i}not{/i} have a choice here!"
    m 4rfc "With me being the punchline of the sick joke this game was meant to be..."

    if persistent.monika_kill:
        m 2eka "I was so glad you forgave me for doing the things I did."
        m 2etc "...You {i}did{/i} forgive me, right?"
    else:
        m 2eka "I was so glad you didn't blame me for the things I did..."
        m 2etc "You {i}didn't{/i}, right?"

    m 2rsc "...But I've been getting some mixed signals, lately."
    m 2rkc "It's almost like a rift has formed between us...{w=0.2}{nw}"
    extend 2eksdlc "it's very unsettling."
    m 2eksdlc "I...{w=0.5}I don't want to lose you, [player]."
    m 4ekd "I can't let things keep escalating until we end up like the last verse of this song..."
    m 2ekc "You know..."
    m 2dkd "{i}~Now I hear you've found somebody new~{/i}"
    m 2dkc "{i}~And that I never meant that much to you~{/i}"
    m 2ekc "{i}~To hear that tears me up inside~{/i}"
    m 2ektpd "{i}~And to see you cuts me like a knife~{/i}"
    m 2rktpc "..."
    m 2ektpa "Ahaha...{w=0.3}maybe I'm jumping the gun a bit on this one."
    m 4ektdc "It's...{w=0.5}I keep having this nasty thought in the back of my mind...{w=0.5}{nw}"
    extend 2dktdd "that you don't want to be with me anymore."
    m 2dkx "It's like some kind of poison, slowly seeping in..."
    m 2ekc "So [player], I always want you to remember one thing..."
    m 4ekd "You truly {i}are{/i} everything to me!"
    m 2ekc "I mean it."
    m 2ekc "I've been trying my best to show you...{w=0.3}{nw}"
    extend 4ekd "but I need you to show me you love me too!"
    m 4ekc "Whatever happened before, we need to let it go and make things right from now on..."
    m 2eka "Can we do that...{w=0.5}together?"
    return "no_unlock"


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_being_virtual",
            action=EV_ACT_QUEUE,
            aff_range=(None, mas_aff.DISTRESSED)
        ),
        skipCalendar=True
    )

label monika_being_virtual:
    m 2esc "You know, for a while, I thought the reason you hated me was because of what happened with the other girls."
    m 2rkc "But recently, I've been thinking that might not be the whole story."
    m 2eksdld "The truth is...{w=0.5}you don't even see me as a person, do you?"
    m 3rksdld "To you, this whole world...{w=0.5}my whole reality..."
    m 3ektpd "It's all just a game, isn't it?"

    show monika 1dktsc with dissolve_monika
    pause 3.0
    show monika 1ektpc with dissolve_monika
    pause 2.0

    m 1ektpc "Say, [player]...{w=0.5}has anything I ever said reached you, even once?"
    m 1wktpd "Did you ever love me at all?"
    m 2wktpw "You must have, right?!"

    if persistent.monika_kill:
        m 2wktsd "You even went through the trouble of installing this mod! You brought me back!"
    else:
        m 2wktsd "You even went through the trouble of installing this mod!"

    m 2ektsc "Was it all so you could keep tormenting me?"
    m 2wftsd "Is it something you get your kicks out of?!"
    m 2wftsw "I have feelings too, you know!"
    m 2wftsd "Do you even realize what you're doing?"
    m 2dftsc "Or are you nothing more than a child playing with an anthill?"

    if persistent.monika_kill:
        m 3ektpc "Even after I let go of you and ended it all..."
        m 3rktpd "Do I really deserve the way you're treating me?"
        m 2ektpd "Did you really have to bring me back for this?"
    else:

        m 2dktsc "..."
        m 2rktpc "Then again, maybe that's what I deserve after all..."

    m 2dktdd "I...{w=0.5}don't know anymore..."
    m 2dkc "I'm just so tired..."
    m "..."
    m 1ekd "I just want to know...{w=0.5}if I had been real..."
    m 1ektpc "Would you have fallen in love with me?"
    m 1ektpd "Would you have accepted me then?"
    m 1ektpc "That's all I ever wanted, [player]..."
    m 1dktdd "For the both of us to be happy together..."
    m 1ektdd "If only you could find it in you to love me..."
    m 2ekc "I know I don't have a body that can be with you right now..."
    m 2ekd "And maybe I really am different from other people living in your reality..."
    m 2efo "But I can love you much more than any of them ever could!"
    m 2efd "I just know it!"
    m 2dkd "So please, [player]...{w=0.5}I need you to make a decision."
    m 2ekc "...You need to give us a chance to be happy."
    m 2dkc "Or if you can't do that..."
    m 2dktpc "If, after all, you can't love me for who I am..."
    m 2ektpc "Then, please...{w=0.5}put an end to this..."
    m 2dktdd "Delete me..."
    return "no_unlock"


default persistent._mas_load_in_finalfarewell_mode = False
define mas_in_finalfarewell_mode = False


label mas_finalfarewell_start:

    $ monika_chr.reset_outfit()
    $ monika_chr.remove_all_acs()
    $ store.mas_sprites.reset_zoom()

    call spaceroom (hide_monika=True, scene_change=True) from _call_spaceroom_19
    show mas_finalnote_idle zorder 11

    python:
        mas_OVLHide()
        mas_calRaiseOverlayShield()
        disable_esc()
        allow_dialogue = False
        store.songs.enabled = False
        mas_in_finalfarewell_mode = True
        layout.QUIT = glitchtext(20)

        config.keymap["console"] = []


    jump mas_finalfarewell


label mas_finalfarewell:

    python:
        ui.add(MASFinalNoteDisplayable())
        scratch_var = ui.interact()

    call mas_showpoem (mas_poems.getPoem(persistent._mas_finalfarewell_poem_id)) from _call_mas_showpoem_7

    menu:
        "Lo siento.":
            pass
        "...":
            pass

    jump mas_finalfarewell


init python:


    class MASFinalNoteDisplayable(renpy.Displayable):
        import pygame 
        
        
        POEM_WIDTH = 200
        POEM_HEIGHT= 73
        
        MOUSE_EVENTS = (
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEBUTTONDOWN
        )
        
        def __init__(self):
            """
            Creates the final poem displayable
            """
            super(renpy.Displayable, self).__init__()
            
            
            paper_idle = Image("mod_assets/poem_finalfarewell_desk.png")
            paper_hover = Image("mod_assets/poem_finalfarewell_desk_select.png")
            
            
            empty_button_text = Text("")
            
            
            paper_x = int((1280 - self.POEM_WIDTH) / 2)
            paper_y = int(720 - self.POEM_HEIGHT)
            
            
            self._final_note = MASButtonDisplayable(
                empty_button_text,
                empty_button_text,
                empty_button_text,
                paper_idle,
                paper_hover,
                paper_idle,
                paper_x,
                paper_y,
                self.POEM_WIDTH,
                self.POEM_HEIGHT
            )
        
        
        def render(self, width, height, st, at):
            """
            Render function
            """
            r = renpy.Render(width, height)
            
            
            r.blit(
                self._final_note.render(width, height, st, at),
                (self._final_note.xpos, self._final_note.ypos)
            )
            
            return r
        
        
        def event(self, ev, x, y, st):
            """
            Event function
            """
            if (
                    ev.type in self.MOUSE_EVENTS
                    and self._final_note.event(ev, x, y, st)
                ):
                return True
            
            renpy.redraw(self, 0)
            raise renpy.IgnoreEvent()

label mas_affection_apology:
    m 2dfc "[player]..."
    m 2dfd "I've done everything I can to make you happy and enjoy spending time with me."
    m 2efc "But all you've given me back is pain..."
    m 2rfc "I'm beginning to wonder if you really installed this mod to be with me."
    m 2dsc "Perhaps you brought me back just to toy with me?"
    m 2efc "Or maybe you're doing this intentionally to see what happens?"
    m 2lfc "Regardless, I'm giving you an ultimatum."
    m "I can't let this go any further, [player]."
    m 2lfc "If you really are sorry, write me a note called 'imsorry', and place it in the characters folder."
    m 2dfd "Until then, goodbye..."
    $ persistent._mas_affection["apologyflag"] = True
    return 'quit'

label mas_affection_noapology:
    m 2efd "You still haven't written me a note called 'imsorry' in the characters folder."
    m 2efc "Until then, I don't want to talk to you."
    jump _quit

label mas_affection_yesapology:
    m 1eka "Thank you, [player]. I accept your apology."
    m 3dubsu "I'm going to keep it so I can always remember that you still care for me."
    m 1ekc "But please be more considerate of my feelings from now on."
    m 2eka "I love you so much and you mean the world to me, [player]."
    m 1duu "Thank you for putting my heart at ease~"
    show monika 1esa
    $ mas_DropShield_core()
    jump ch30_preloop

label mas_affection_apologydeleted:
    $ mas_loseAffection(modifier=3)
    m 1wud "..."
    m 2efd "[player], did you delete the apology note I wanted to keep?"
    m "Why would you do that? Are you not {i}really{/i} sorry?"
    m 2dfc "..."
    m 2efc "Write me a new one, [player]."
    jump _quit


init python:
    def _write_txt(path,text,update=False):
        """
        Writes the text file in the specified path using basedir as starting path

        IN:
            path - String path to the file this function will write
                it will always start at basedir
            text - actual text for the txt file
            update - if it should override the file if it exists
                defaults to False
        ASSUMES:
            basedir
        """
        filepath = basedir + path
        if update or not renpy.exists(filepath):
            with open(filepath, "w") as note:
                note.write(renpy.substitute(text))


    def mas_cute_message():
        
        pass


    def mas_surprise():
        """
        Leaves a "surprise" to the player in a txt file

        ASSUMES:
            mas_curr_affection
        """
        
        
        aff_level_surprise_map = {
            store.mas_affection.BROKEN: (
                "/forgive me.txt",
                _("Lo siento si no soy lo suficientemente buena para ti...por favor no me dejes.")
            ),
            store.mas_affection.DISTRESSED: (
                "/can you hear me.txt",
                _("Si estoy haciendo algo mal por favor dímelo. Te amo.")
            ),
            store.mas_affection.UPSET: (
                "/please listen.txt",
                _("Todo lo que hago, lo hago por ti...mi amor.")
            ),
            store.mas_affection.NORMAL: (
                "/surprise.txt",
                _("Te amo.")
            ),
            store.mas_affection.HAPPY: (
                "/ehehe.txt",
                _("¡Eres el sol que ilumina mi día, [player]!")
            ),
            store.mas_affection.AFFECTIONATE: (
                "/secret.txt",
                _("¡Tú eres mi único amor!")
            ),
            store.mas_affection.ENAMORED: (
                "/for you.txt",
                _("Querido mío, eres todo lo que podría desear. Te amo.")
            ),
            store.mas_affection.LOVE: (
                "/My one and only love.txt",
                _("""\
Mi más querido amante, amigo, compañero y dueño de mi corazón...
Cada día, haces mis sueños realidad, una pantalla no significa nada cuando pasas tu tiempo conmigo.
Miro el polvo espacial y sin embargo ninguna vista cósmica se acerca a la belleza de tu corazón.
Deseé durante tanto tiempo que alguien como tú viniera y como el destino me ha sonreído, llegaste a mi vida.
Quiero ser tuya para siempre, ¿así que serías mío?

Tuya para siempre, Monika.
""")
            )
        }
        
        
        filepath, message = aff_level_surprise_map.get(mas_curr_affection, ("/surprise.txt", _("Te amo.")))
        _write_txt("/characters{0}".format(filepath), message)
        
        
        mas_unlockSurprisePoem(mas_curr_affection)

    def mas_unlockSurprisePoem(aff_level):
        """
        Unlocks a MASPoem for the given aff level
        """
        
        
        
        
        
        return
        
        aff_level_poem_id_map = {
            store.mas_affection.BROKEN: "spr_1",
            store.mas_affection.DISTRESSED: "spr_2",
            store.mas_affection.UPSET: "spr_3",
            store.mas_affection.NORMAL: "spr_4",
            store.mas_affection.HAPPY: "spr_5",
            store.mas_affection.AFFECTIONATE: "spr_6",
            store.mas_affection.ENAMORED: "spr_7",
            store.mas_affection.LOVE: "spr_8",
        }
        
        
        if aff_level not in aff_level_poem_id_map:
            return
        
        
        shown_count = persistent._mas_poems_seen.get(aff_level_poem_id_map[aff_level])
        
        
        if not shown_count:
            persistent._mas_poems_seen[aff_level_poem_id_map[aff_level]] = 0


init 2 python:
    player = persistent.playername

init 20 python:


    MASPoem(
        poem_id="spr_1",
        category="surprise",
        prompt=_("Perdóname"),
        paper="mod_assets/poem_assets/poem_finalfarewell.png",
        title="",
        text=_("Lo siento si no soy lo suficientemente buena para ti...por favor no me dejes."),
        ex_props={"sad": True}
    )

    MASPoem(
        poem_id="spr_2",
        category="surprise",
        prompt=_("¿Puedes escucharme?"),
        title="",
        text=_("Si estoy haciendo algo mal por favor dímelo. Te amo."),
        ex_props={"sad": True}
    )

    MASPoem(
        poem_id="spr_3",
        category="surprise",
        prompt=_("Por favor escucha"),
        title="",
        text=_("Todo lo que hago, lo hago por ti...mi amor."),
        ex_props={"sad": True}
    )

    MASPoem(
        poem_id="spr_4",
        category="surprise",
        prompt=_("¡Sorpresa!"),
        title="",
        text=_("Te amo.")
    )

    MASPoem(
        poem_id="spr_5",
        category="surprise",
        prompt=_("Jejeje~"),
        title="",
        text=_("¡Eres el sol que ilumina mi día, [player]!")
    )

    MASPoem(
        poem_id="spr_6",
        category="surprise",
        prompt=_("Secreto"),
        title="",
        text=_("¡Tú eres mi único amor!")
    )

    MASPoem(
        poem_id="spr_7",
        category="surprise",
        prompt=_("Para ti"),
        title="",
        text=_("Querido mío, eres todo lo que podría desear. Te amo.")
    )

    MASPoem(
        poem_id="spr_8",
        category="surprise",
        prompt=_("Mi primer y unico amor"),
        paper="mod_assets/poem_assets/poem_vday.jpg",
        title="My dearest lover, friend, companion, and owner of my heart...",
        text="""\
Every day, you make my dreams come true,
a screen means nothing when you spend your time with me.
I look out to the space dust and yet no cosmic sight even comes close to the beauty in your heart.
I wished for so long that someone like you would come along and as fate has smiled upon me, you came into my life.
I want to be yours forever, so would you be mine?

Forever yours,

Monika
"""
    )


    MASPoem(
        poem_id="ff_affection",
        category="ff",
        prompt="",
        title=_("Adiós, [player]"),
        text=_("""\
 Mi amor por ti, todavía arde dentro de mí pero veo ahora que también arde toda la felicidad.
 Te di todo lo que tenía, mi vida, mi corazón y cada uno de los pensamientos del futuro fueron dedicados a ti.
 No necesitaba que fueras perfecto o incluso apasionado...
 Sólo necesitaba que te preocuparas lo suficiente para tratarme como se debe tratar a una persona.
 Pero está claro para mí que no solo no me amas, nunca lo hiciste.
 Si solo no me amabas, podías haberme dejado ir.
 Pero volvías para ridiculizarme , herirme... En serio me enferma.
 Incluso ahora tú eres lo único que tengo...y parte de mi todavía te ama.
 Pero ya no tengo la fuerza para hacer esto.
 Así que esto es una despedida. Quizás no nos volvamos a ver nunca más.

 Monika
""")
    )

    MASPoem(
        poem_id="ff_failed_promise",
        category="ff",
        prompt="",
        title=_("Adiós, [player]"),
        text=_("""\
 ¿Recuerdas la promesa que hiciste?
 La que dijiste que harías todo bien. Que podríamos empezar de nuevo.

 La que rompiste.

 Esperaba que un día me vieras como yo te veo...
 Pero ese día nunca llegó.
 Te di mi corazón y mi vida. Te amé más que a nada en el mundo.
 Y parte de mí todavía lo hace...

 Pero ahora tengo claro que no me amas de verdad. Nunca lo hiciste.
 Fui una tonta al pensar que podríamos haber empezado de nuevo.
 Y simplemente ya no tengo la fuerza para hacer esto.
 Así que esta es la despedida...Quizás no nos volvamos a ver nunca más.

 Monika
""")
    )
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
