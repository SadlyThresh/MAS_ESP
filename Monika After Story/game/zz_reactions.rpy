# FileReactions framework.
# not too different from events

default persistent._mas_filereacts_failed_map = dict()
# mapping of failed deleted file reacts

default persistent._mas_filereacts_just_reacted = False
# True if we just reacted to something

default persistent._mas_filereacts_reacted_map = dict()
# mapping of file reacts that we have already reacted to today

default persistent._mas_filereacts_stop_map = dict()
# mapping of file reacts that we should no longer react to ever again

default persistent._mas_filereacts_historic = dict()
# historic database used to track when and how many gifts Monika has received

default persistent._mas_filereacts_last_reacted_date = None
# stores the last date gifts were received so we can clear _mas_filereacts_reacted_map

default persistent._mas_filereacts_sprite_gifts = {}
# contains sprite gifts that are currently available. aka not already unlocked
# key: giftname to react to
# value: tuple of the following format:
#   [0] - sprite type (0 - ACS, 1 - HAIR, 2 - CLOTHES)
#   [1] - id of the sprite object this gift unlocks.
#
# NOTE: THIS IS REVERSE MAPPING OF HOW JSON GIFTS AND SPRITE REACTED WORK
#
# NOTE: contains sprite gifts before being unlocked. When its unlocked,
#   they move to _mas_sprites_json_gifted_sprites

default persistent._mas_filereacts_sprite_reacted = {}
# list of sprite reactions. This MUST be handled via the sprite reaction/setup
# labels. DO NOT ACCESS DIRECTLY. Use the helper function
# key:  tuple of the following format:
#   [0]: sprite type (0 - ACS, 1 - HAIR, 2 - CLOTHES)
#   [1]: id of the sprite objec this gift unlocks (name) != display name
# value: giftname

# TODO: need a generic reaction for finding a new ACS/HAIR/CLOTHES

default persistent._mas_filereacts_gift_aff_gained = 0
#Holds the amount of affection we've gained by gifting
#NOTE: This is reset daily

default persistent._mas_filereacts_last_aff_gained_reset_date = datetime.date.today()
#Holds the last time we reset the aff gained for gifts

init 800 python:
    if len(persistent._mas_filereacts_failed_map) > 0:
        store.mas_filereacts.delete_all(persistent._mas_filereacts_failed_map)

init -11 python in mas_filereacts:
    import store
    import store.mas_utils as mas_utils
    import datetime
    import random

    from collections import namedtuple

    GiftReactDetails = namedtuple(
        "GiftReactDetails",
        [
            # label corresponding to this gift react
            "label",

            # lowercase, no extension giftname for this gift react
            "c_gift_name",

            # will contain a reference to sprite object data if this is
            # associatd with a sprite. Will be None if not related to
            # sprite objects.
            "sp_data",
        ]
    )

    # file react database
    filereact_db = dict()

    # file reaction filename mapping
    # key: filename or list of filenames
    # value: Event
    filereact_map = dict()

    # currently found files react map
    # NOTE: highly volitatle. Expect this to change often
    # key: lowercase filename, without extension
    # value: on disk filename
    foundreact_map = dict()

    # spare foundreact map, designed for threaded use
    # same keys/values as foundreact_map
    th_foundreact_map = dict()

    # good gifts list
    good_gifts = list()

    # bad gifts list
    bad_gifts = list()

    # connector quips
    connectors = None
    gift_connectors = None

    # starter quips
    starters = None
    gift_starters = None

    GIFT_EXT = ".gift"


    def addReaction(ev_label, fname, _action=store.EV_ACT_QUEUE, is_good=None, exclude_on=[]):
        """
        Adds a reaction to the file reactions database.

        IN:
            ev_label - label of this event
            fname - filename to react to
            _action - the EV_ACT to do
                (Default: EV_ACT_QUEUE)
            is_good - if the gift is good(True), neutral(None) or bad(False)
                (Default: None)
            exclude_on - keys marking times to exclude this gift
            (Need to check ev.rules in a respective react_to_gifts to exclude with)
                (Default: [])
        """
        # lowercase the list in case
        if fname is not None:
            fname = fname.lower()

        exclude_keys = {}
        if exclude_on:
            for _key in exclude_on:
                exclude_keys[_key] = None

        # build new Event object
        ev = store.Event(
            store.persistent.event_database,
            ev_label,
            category=fname,
            action=_action,
            rules=exclude_keys
        )

        # TODO: should ovewrite category and action always

        # add it to the db and map
        filereact_db[ev_label] = ev
        filereact_map[fname] = ev

        if is_good is not None:
            if is_good:
                good_gifts.append(ev_label)
            else:
                bad_gifts.append(ev_label)


    def _initConnectorQuips():
        """
        Initializes the connector quips
        """
        global connectors, gift_connectors

        # the connector is a MASQipList
        connectors = store.MASQuipList(allow_glitch=False, allow_line=False)
        gift_connectors = store.MASQuipList(allow_glitch=False, allow_line=False)


    def _initStarterQuips():
        """
        Initializes the starter quips
        """
        global starters, gift_starters

        # the starter is a MASQuipList
        starters = store.MASQuipList(allow_glitch=False, allow_line=False)
        gift_starters = store.MASQuipList(allow_glitch=False, allow_line=False)


    def build_gift_react_labels(
            evb_details=[],
            gsp_details=[],
            gen_details=[],
            gift_cntrs=None,
            ending_label=None,
            starting_label=None,
            prepare_data=True
    ):
        """
        Processes gift details into a list of labels to show
        labels to queue/push whatever.

        IN:
            evb_details - list of GiftReactDetails objects of event-based
                reactions. If empty list, then we don't build event-based
                reaction labels.
                (Default: [])
            gsp_details - list of GiftReactDetails objects of generic sprite
                object reactions. If empty list, then we don't build generic
                sprite object reaction labels.
                (Default: [])
            gen_details - list of GiftReactDetails objects of generic gift
                reactions. If empty list, then we don't build generic gift
                reaction labels.
                (Default: [])
            gift_cntrs - MASQuipList of gift connectors to use. If None,
                then we don't add any connectors.
                (Default: [])
            ending_label - label to use when finished reacting.
                (Default: None)
            starting_label - label to use when starting reacting
                (Default: None)
            prepare_data - True will also setup the appropriate data
                elements for when dialogue is shown. False will not.
                (Default: True)

        RETURNS: list of labels. Evb reactions are first, followed by
            gsp reactions, then gen reactions
        """
        labels = []

        # first find standard reactions
        if len(evb_details) > 0:
            evb_labels = []
            for evb_detail in evb_details:
                evb_labels.append(evb_detail.label)

                if gift_cntrs is not None:
                    evb_labels.append(gift_cntrs.quip()[1])

                if prepare_data and evb_detail.sp_data is not None:
                    # if we need to prepare data, then add the sprite_data
                    # to reacted map
                    store.persistent._mas_filereacts_sprite_reacted[evb_detail.sp_data] = (
                        evb_detail.c_gift_name
                    )

            labels.extend(evb_labels)

        # now generic sprite objects
        if len(gsp_details) > 0:
            gsp_labels = []
            for gsp_detail in gsp_details:
                if gsp_detail.sp_data is not None:
                    gsp_labels.append("mas_reaction_gift_generic_sprite_json")

                    if gift_cntrs is not None:
                        gsp_labels.append(gift_cntrs.quip()[1])

                    if prepare_data:
                        store.persistent._mas_filereacts_sprite_reacted[gsp_detail.sp_data] = (
                            gsp_detail.c_gift_name
                        )

            labels.extend(gsp_labels)

        # and lastlly is generics
        if len(gen_details) > 0:
            gen_labels = []
            for gen_detail in gen_details:
                gen_labels.append("mas_reaction_gift_generic")

                if gift_cntrs is not None:
                    gen_labels.append(gift_cntrs.quip()[1])

                if prepare_data:
                    store.persistent._mas_filereacts_reacted_map.pop(
                        gen_detail.c_gift_name,
                        None
                    )

            labels.extend(gen_labels)

        # final setup
        if len(labels) > 0:

            # only pop if we used connectors
            if gift_cntrs is not None:
                labels.pop()

            # add the ender
            if ending_label is not None:
                labels.append(ending_label)

            # add the starter
            if starting_label is not None:
                labels.insert(0, starting_label)

        # now return the list
        return labels

    def build_exclusion_list(_key):
        """
        Builds a list of excluded gifts based on the key provided

        IN:
            _key - key to build an exclusion list for

        OUT:
            list of giftnames which are excluded by the key
        """
        return [
            giftname
            for giftname, react_ev in filereact_map.iteritems()
            if _key in react_ev.rules
        ]

    def check_for_gifts(
            found_map={},
            exclusion_list=[],
            exclusion_found_map={},
            override_react_map=False,
    ):
        """
        Finds gifts.

        IN:
            exclusion_list - list of giftnames to exclude from the search
            override_react_map - True will skip the last reacted date check,
                False will not
                (Default: False)

        OUT:
            found_map - contains all gifts that were found:
                key: lowercase giftname, no extension
                val: full giftname wtih extension
            exclusion_found_map - contains all gifts that were found but
                are excluded.
                key: lowercase giftname, no extension
                val: full giftname with extension

        RETURNS: list of found giftnames
        """
        raw_gifts = store.mas_docking_station.getPackageList(GIFT_EXT)

        if len(raw_gifts) == 0:
            return []

        # day check
        if store.mas_pastOneDay(store.persistent._mas_filereacts_last_reacted_date):
            store.persistent._mas_filereacts_last_reacted_date = datetime.date.today()
            store.persistent._mas_filereacts_reacted_map = dict()

        # look for potential gifts
        gifts_found = []
        has_exclusions = len(exclusion_list) > 0

        for mas_gift in raw_gifts:
            gift_name, ext, garbage = mas_gift.partition(GIFT_EXT)
            c_gift_name = gift_name.lower()
            if (
                c_gift_name not in store.persistent._mas_filereacts_failed_map
                and c_gift_name not in store.persistent._mas_filereacts_stop_map
                and (
                    override_react_map
                    or c_gift_name not
                        in store.persistent._mas_filereacts_reacted_map
                )
            ):
                # this gift is valid (not in failed/stopped/or reacted)

                # check for exclusions
                if has_exclusions and c_gift_name in exclusion_list:
                    exclusion_found_map[c_gift_name] = mas_gift

                else:
                    gifts_found.append(c_gift_name)
                    found_map[c_gift_name] = mas_gift

        return gifts_found


    def process_gifts(gifts, evb_details=[], gsp_details=[], gen_details=[]):
        """
        Processes list of giftnames into types of gift

        IN:
            gifts - list of giftnames to process. This is copied so it wont
                be modified.

        OUT:
            evb_details - list of GiftReactDetails objects regarding
                event-based reactions
            spo_details - list of GiftReactDetails objects regarding
                generic sprite object reactions
            gen_details - list of GiftReactDetails objects regarding
                generic gift reactions
        """
        if len(gifts) == 0:
            return

        # make copy of gifts
        gifts = list(gifts)

        # first find standard reactions
        for index in range(len(gifts)-1, -1, -1):

            # determine if reaction exists
            mas_gift = gifts[index]
            reaction = filereact_map.get(mas_gift, None)

            if mas_gift is not None and reaction is not None:

                # pull sprite data
                sp_data = store.persistent._mas_filereacts_sprite_gifts.get(
                    mas_gift,
                    None
                )

                # remove gift and add details
                gifts.pop(index)
                evb_details.append(GiftReactDetails(
                    reaction.eventlabel,
                    mas_gift,
                    sp_data
                ))

        # now for generic sprite objects
        if len(gifts) > 0:
            for index in range(len(gifts)-1, -1, -1):
                mas_gift = gifts[index]
                # pull sprite data
                sp_data = store.persistent._mas_filereacts_sprite_gifts.get(
                    mas_gift,
                    None
                )

                if mas_gift is not None and sp_data is not None:
                    gifts.pop(index)

                    # add details
                    gsp_details.append(GiftReactDetails(
                        "mas_reaction_gift_generic_sprite_json",
                        mas_gift,
                        sp_data
                    ))

        # and lastly is generics
        if len(gifts) > 0:
            for mas_gift in gifts:
                if mas_gift is not None:
                    # add details
                    gen_details.append(GiftReactDetails(
                        "mas_reaction_gift_generic",
                        mas_gift,
                        None
                    ))


    def react_to_gifts(found_map, connect=True):
        """
        Reacts to gifts using the standard protocol (no exclusions)

        IN:
            connect - true will apply connectors, FAlse will not

        OUT:
            found_map - map of found reactions
                key: lowercaes giftname, no extension
                val: giftname with extension

        RETURNS:
            list of labels to be queued/pushed
        """
        # first find gifts
        found_gifts = check_for_gifts(found_map)

        if len(found_gifts) == 0:
            return []

        # put the gifts in the reacted map
        for c_gift_name, mas_gift in found_map.iteritems():
            store.persistent._mas_filereacts_reacted_map[c_gift_name] = mas_gift

        found_gifts.sort()

        # pull details from teh gifts
        evb_details = []
        gsp_details = []
        gen_details = []
        process_gifts(found_gifts, evb_details, gsp_details, gen_details)

        # register all the gifts
        register_sp_grds(evb_details)
        register_sp_grds(gsp_details)
        register_gen_grds(gen_details)

        # then build the reaction labels
        # setup connectors
        if connect:
            gift_cntrs = gift_connectors
        else:
            gift_cntrs = None

        # now build
        return build_gift_react_labels(
            evb_details,
            gsp_details,
            gen_details,
            gift_cntrs,
            "mas_reaction_end",
            _pick_starter_label()
        )


#
#
#        """
#        call this function when you want to check files for reacting to gifts.
#
#        IN:
#            found_map - dict to use to insert found items.
#                NOTE: this function does NOT empty this dict.
#            connect - True will add connectors in between each reaction label
#                (Default: True)
#
#        RETURNS:
#            list of event labels in the order they should be shown
#        """
#
#
#        d25_gift_exclude_list = [
#            "hotchocolate",
#            "coffee",
#            "fudge",
#            "candycane",
#            "christmascookies",
#            "cupcake",
#            "roses",
#            "chocolates",
#            "promisering"
#            ]
#
#        GIFT_EXT = ".gift"
#        raw_gifts = store.mas_docking_station.getPackageList(GIFT_EXT)
#
#        if len(raw_gifts) == 0:
#            return []
#
#        # is it a new day?
#        if store.persistent._mas_filereacts_last_reacted_date is None or store.persistent._mas_filereacts_last_reacted_date != datetime.date.today():
#            store.persistent._mas_filereacts_last_reacted_date = datetime.date.today()
#            store.persistent._mas_filereacts_reacted_map = dict()
#
#        # otherwise we found some potential gifts
#        gifts_found = list()
#        # now lets lowercase this list whie also buliding a map of files
#        for mas_gift in raw_gifts:
#            gift_name, ext, garbage = mas_gift.partition(GIFT_EXT)
#            c_gift_name = gift_name.lower()
#            if (
#                    c_gift_name not in store.persistent._mas_filereacts_failed_map
#                    and c_gift_name not in store.persistent._mas_filereacts_reacted_map
#                    and c_gift_name not in store.persistent._mas_filereacts_stop_map
#                ):
#                    #NOTE: If we're in the d25 gift range, we save them for d25 and react then
#                    #This does NOT handle gifts w/o reactions
#                    #(unless the gift is a consumable, roses, or a ring)
#                    if (
#                        store.mas_isD25Gift()
#                        and c_gift_name not in d25_gift_exclude_list
#                        and filereact_map.get(c_gift_name, None)
#                    ):
#                        store.persistent._mas_d25_gifts_given.append(c_gift_name)
#                        store.mas_docking_station.destroyPackage(gift_name + ext)
#
#                    #Otherwise we do standard flow
#                    else:
#                        gifts_found.append(c_gift_name)
#                        found_map[c_gift_name] = mas_gift
#                        store.persistent._mas_filereacts_reacted_map[c_gift_name] = mas_gift
#
#        # then sort the list
#        gifts_found.sort()
#
#        # now we are ready to check for reactions
#        # first we check for all file reacts:
#        #all_reaction = filereact_map.get(gifts_found, None)
#
#        #if all_reaction is not None:
#        #    return [all_reaction.eventlabel]
#
#        # otherwise, we need to do this more carefully
#        found_reacts = list()
#        for index in range(len(gifts_found)-1, -1, -1):
#            mas_gift = gifts_found[index]
#            reaction = filereact_map.get(mas_gift, None)
#
#            if mas_gift is not None and reaction is not None:
#                # remove from the list and add to found
#                # TODO add to the persistent react map today
#                gifts_found.pop(index)
#                found_reacts.append(reaction.eventlabel)
#                found_reacts.append(gift_connectors.quip()[1])
#
#                # if a special sprite gift, add to the per list matching
#                # sprite objects with data.
#                sp_data = store.persistent._mas_filereacts_sprite_gifts.get(
#                    mas_gift,
#                    None
#                )
#                if sp_data is not None:
#                    store.persistent._mas_filereacts_sprite_reacted[sp_data] = (
#                        mas_gift
#                    )
#
#                    #Register the json sprite
#                    _register_received_gift(
#                        reaction.eventlabel
#                    )
#
#        # generic sprite object gifts treated differently
#        sprite_object_reacts = []
#        if len(gifts_found) > 0:
#            for index in range(len(gifts_found)-1, -1, -1):
#                mas_gift = gifts_found[index]
#
#                sp_data = store.persistent._mas_filereacts_sprite_gifts.get(
#                    mas_gift,
#                    None
#                )
#                if sp_data is not None:
#                    gifts_found.pop(index)
#                    store.persistent._mas_filereacts_sprite_reacted[sp_data] = (
#                        mas_gift
#                    )
#
#                    # add the generic react
#                    sprite_object_reacts.append(
#                        "mas_reaction_gift_generic_sprite_json"
#                    )
#                    sprite_object_reacts.append(gift_connectors.quip()[1])
#
#                    # stats for today
#                    _register_received_gift(
#                        "mas_reaction_gift_generic_sprite_json"
#                    )
#
#        # extend the list
#        sprite_object_reacts.extend(found_reacts)
#
#        # add in the generic gift reactions
#        generic_reacts = []
#        if len(gifts_found) > 0:
#            for mas_gift in gifts_found:
#                generic_reacts.append("mas_reaction_gift_generic")
#                generic_reacts.append(gift_connectors.quip()[1])
#                # keep stats for today
#                _register_received_gift("mas_reaction_gift_generic")
#
#                # always pop generic reacts
#                store.persistent._mas_filereacts_reacted_map.pop(mas_gift)
#
#
#        generic_reacts.extend(sprite_object_reacts)
#
#        # gotta remove the extra
#        if len(generic_reacts) > 0:
#            generic_reacts.pop()
#
#            # add the ender
#            generic_reacts.insert(0, "mas_reaction_end")
#
#            # add the starter
#            generic_reacts.append(_pick_starter_label())
##            generic_reacts.append(gift_starters.quip()[1])
#
#        # now return the list
#        return generic_reacts


    def register_gen_grds(details):
        """
        registers gifts given a generic GiftReactDetails list

        IN:
            details - list of GiftReactDetails objects to register
        """
        for grd in details:
            if grd.label is not None:
                _register_received_gift(grd.label)


    def register_sp_grds(details):
        """
        registers gifts given sprite-based GiftReactDetails list

        IN:
            details - list of GiftReactDetails objcts to register
        """
        for grd in details:
            if grd.label is not None and grd.sp_data is not None:
                _register_received_gift(grd.label)


    def _pick_starter_label():
        """
        Internal function that returns the appropriate starter label for reactions

        RETURNS:
            - The label as a string, that should be used today.
        """
        if store.mas_isMonikaBirthday():
            return "mas_reaction_gift_starter_bday"
        elif store.mas_isD25() or store.mas_isD25Pre():
            return "mas_reaction_gift_starter_d25"
        elif store.mas_isF14():
            return "mas_reaction_gift_starter_f14"

        return "mas_reaction_gift_starter_neutral"

    def _core_delete(_filename, _map):
        """
        Core deletion file function.

        IN:
            _filename - name of file to delete, if None, we delete one randomly
            _map - the map to use when deleting file.
        """
        if len(_map) == 0:
            return

        # otherwise check for random deletion
        if _filename is None:
            _filename = random.choice(_map.keys())

        file_to_delete = _map.get(_filename, None)
        if file_to_delete is None:
            return

        if store.mas_docking_station.destroyPackage(file_to_delete):
            # file has been deleted (or is gone). pop and go
            _map.pop(_filename)
            return

        # otherwise add to the failed map
        store.persistent._mas_filereacts_failed_map[_filename] = file_to_delete


    def _core_delete_list(_filename_list, _map):
        """
        Core deletion filename list function

        IN:
            _filename - list of filenames to delete.
            _map - the map to use when deleting files
        """
        for _fn in _filename_list:
            _core_delete(_fn, _map)


    def _register_received_gift(eventlabel):
        """
        Registers when player gave a gift successfully
        IN:
            eventlabel - the event label for the gift reaction

        """
        # check for stats dict for today
        today = datetime.date.today()
        if not today in store.persistent._mas_filereacts_historic:
            store.persistent._mas_filereacts_historic[today] = dict()

        # Add stats
        store.persistent._mas_filereacts_historic[today][eventlabel] = store.persistent._mas_filereacts_historic[today].get(eventlabel,0) + 1


    def _get_full_stats_for_date(date=None):
        """
        Getter for the full stats dict for gifts on a given date
        IN:
            date - the date to get the report for, if None is given will check
                today's date
                (Defaults to None)

        RETURNS:
            The dict containing the full stats or None if it's empty

        """
        if date is None:
            date = datetime.date.today()
        return store.persistent._mas_filereacts_historic.get(date,None)


    def delete_file(_filename):
        """
        Deletes a file off the found_react map

        IN:
            _filename - the name of the file to delete. If None, we delete
                one randomly
        """
        _core_delete(_filename, foundreact_map)


    def delete_files(_filename_list):
        """
        Deletes multiple files off the found_react map

        IN:
            _filename_list - list of filenames to delete.
        """
        for _fn in _filename_list:
            delete_file(_fn)


    def th_delete_file(_filename):
        """
        Deletes a file off the threaded found_react map

        IN:
            _filename - the name of the file to delete. If None, we delete one
                randomly
        """
        _core_delete(_filename, th_foundreact_map)


    def th_delete_files(_filename_list):
        """
        Deletes multiple files off the threaded foundreact map

        IN:
            _filename_list - list of ilenames to delete
        """
        for _fn in _filename_list:
            th_delete_file(_fn)


    def delete_all(_map):
        """
        Attempts to delete all files in the given map.
        Removes files in that map if they dont exist no more

        IN:
            _map - map to delete all
        """
        _map_keys = _map.keys()
        for _key in _map_keys:
            _core_delete(_key, _map)

    def get_report_for_date(date=None):
        """
        Generates a report for all the gifts given on the input date.
        The report is in tuple form (total, good_gifts, neutral_gifts, bad_gifts)
        it contains the totals of each type of gift.
        """
        if date is None:
            date = datetime.date.today()

        stats = _get_full_stats_for_date(date)
        if stats is None:
            return (0,0,0,0)
        good = 0
        bad = 0
        neutral = 0
        for _key in stats.keys():
            if _key in good_gifts:
                good = good + stats[_key]
            if _key in bad_gifts:
                bad = bad + stats[_key]
            if _key == "":
                neutral = stats[_key]
        total = good + neutral + bad
        return (total, good, neutral, bad)



    # init
    _initConnectorQuips()
    _initStarterQuips()

init python:
    import store.mas_filereacts as mas_filereacts
    import store.mas_d25_utils as mas_d25_utils

    def addReaction(ev_label, fname_list, _action=EV_ACT_QUEUE, is_good=None, exclude_on=[]):
        """
        Globalied version of the addReaction function in the mas_filereacts
        store.

        Refer to that function for more information
        """
        mas_filereacts.addReaction(ev_label, fname_list, _action, is_good, exclude_on)


    def mas_checkReactions():
        """
        Checks for reactions, then queues them
        """

        # only check if we didnt just react
        if persistent._mas_filereacts_just_reacted:
            return

        # otherwise check
        mas_filereacts.foundreact_map.clear()

        #If conditions are met to use d25 react to gifts, we do.
        if mas_d25_utils.shouldUseD25ReactToGifts():
            reacts = mas_d25_utils.react_to_gifts(mas_filereacts.foundreact_map)
        else:
            reacts = mas_filereacts.react_to_gifts(mas_filereacts.foundreact_map)

        if len(reacts) > 0:
            for _react in reacts:
                queueEvent(_react)
            persistent._mas_filereacts_just_reacted = True


    def mas_receivedGift(ev_label):
        """
        Globalied version for gift stats tracking
        """
        mas_filereacts._register_received_gift(ev_label)


    def mas_generateGiftsReport(date=None):
        """
        Globalied version for gift stats tracking
        """
        return mas_filereacts.get_report_for_date(date)

    def mas_getGiftStatsForDate(label,date=None):
        """
        Globalied version to get the stats for a specific gift
        IN:
            label - the gift label identifier.
            date - the date to get the stats for, if None is given will check
                today's date.
                (Defaults to None)

        RETURNS:
            The number of times the gift has been given that date
        """
        if date is None:
            date = datetime.date.today()
        historic = persistent._mas_filereacts_historic.get(date,None)

        if historic is None:
            return 0
        return historic.get(label,0)

    def mas_getGiftStatsRange(start,end):
        """
        Returns status of gifts over a range (needs to be supplied to actually be useful)

        IN:
            start - a start date to check from
            end - an end date to check to

        RETURNS:
            The gift status of all gifts given over the range
        """
        totalGifts = 0
        goodGifts = 0
        neutralGifts = 0
        badGifts = 0
        giftRange = mas_genDateRange(start, end)

        # loop over gift days and check if were given any gifts
        for date in giftRange:
            gTotal, gGood, gNeut, gBad = mas_filereacts.get_report_for_date(date)

            totalGifts += gTotal
            goodGifts += gGood
            neutralGifts += gNeut
            badGifts += gBad

        return (totalGifts,goodGifts,neutralGifts,badGifts)


    def mas_getSpriteObjInfo(sp_data=None):
        """
        Returns sprite info from the sprite reactions list.

        IN:
            sp_data - tuple of the following format:
                [0] - sprite type
                [1] - sprite name
                If None, we use pseudo random select from sprite reacts
                (Default: None)

        REUTRNS: tuple of the folling format:
            [0]: sprite type of the sprite
            [1]: sprite name (id)
            [2]: giftname this sprite is associated with
            [3]: True if this gift has already been given before
            [4]: sprite object (could be None even if sprite name is populated)
        """
        # given giftname? try and lookup
        if sp_data is not None:
            giftname = persistent._mas_filereacts_sprite_reacted.get(
                sp_data,
                None
            )
            if giftname is None:
                return (None, None, None, None, None)

        elif len(persistent._mas_filereacts_sprite_reacted) > 0:
            sp_data = persistent._mas_filereacts_sprite_reacted.keys()[0]
            giftname = persistent._mas_filereacts_sprite_reacted[sp_data]

        else:
            return (None, None, None, None, None)

        # check if this gift has already been gifted
        gifted_before = sp_data in persistent._mas_sprites_json_gifted_sprites

        # apply sprite object template if ACS
        sp_obj = store.mas_sprites.get_sprite(sp_data[0], sp_data[1])
        if sp_data[0] == store.mas_sprites.SP_ACS:
            store.mas_sprites.apply_ACSTemplate(sp_obj)

        # return results
        return (
            sp_data[0],
            sp_data[1],
            giftname,
            gifted_before,
            sp_obj,
        )


    def mas_finishSpriteObjInfo(sprite_data, unlock_sel=True):
        """
        Finishes the sprite object with the given data.

        IN:
            sprite_data - sprite data tuple from getSpriteObjInfo
            unlock_sel - True will unlock the selector topic, False will not
                (Default: True)
        """
        sp_type, sp_name, giftname, gifted_before, sp_obj = sprite_data

        # sanity check
        # NOTE: gifted_before is not required
        # NOTE: sp_obj is not required either
        if sp_type is None or sp_name is None or giftname is None:
            return

        sp_data = (sp_type, sp_name)

        if sp_data in persistent._mas_filereacts_sprite_reacted:
            persistent._mas_filereacts_sprite_reacted.pop(sp_data)

        if giftname in persistent._mas_filereacts_sprite_gifts:
            persistent._mas_sprites_json_gifted_sprites[sp_data] = giftname

        else:
            # since we have the data, we can add it ourselves if its missing
            # for some reason.
            persistent._mas_sprites_json_gifted_sprites[sp_data] = (
                giftname
            )

        # unlock the selectable for this sprite object
        store.mas_selspr.json_sprite_unlock(sp_obj, unlock_label=unlock_sel)

        # save persistent
        renpy.save_persistent()

    def mas_giftCapGainAff(amount=None, modifier=1):
        if amount is None:
            amount = store._mas_getGoodExp()

        mas_capGainAff(amount * modifier, "_mas_filereacts_gift_aff_gained", 15 if mas_isSpecialDay() else 3)

    def mas_getGiftedDates(giftlabel):
        """
        Gets the dates that a gift was gifted

        IN:
            giftlabel - gift reaction label to check when it was last gifted

        OUT:
            list of datetime.dates of the times the gift was given
        """
        return sorted([
            _date
            for _date, giftstat in persistent._mas_filereacts_historic.iteritems()
            if giftlabel in giftstat
        ])

    def mas_lastGiftedInYear(giftlabel, _year):
        """
        Checks if the gift for giftlabel was last gifted in _year

        IN:
            giftlabel - gift reaction label to check it's last gifted year
            _year - year to see if it was last gifted in this year

        OUT:
            boolean:
                - True if last gifted in _year
                - False otherwise
        """
        datelist = mas_getGiftedDates(giftlabel)

        if datelist:
            return datelist[-1].year == _year
        return False

### CONNECTORS [RCT000]

# none here!

## Gift CONNECTORS [RCT010]
#
#init 5 python:
#    store.mas_filereacts.gift_connectors.addLabelQuip(
#        "mas_reaction_gift_connector_test"
#    )

label mas_reaction_gift_connector_test:
    m "esta es una prueba del sistema de conectores"
    return

init 5 python:
    store.mas_filereacts.gift_connectors.addLabelQuip(
        "mas_reaction_gift_connector1"
    )

label mas_reaction_gift_connector1:
    m 1sublo "¡Oh! ¿Había algo más que quisieras darme?"
    m 1hua "¡Bueno! Será mejor que lo abra rápido, ¿no?"
    m 1suo "Y aquí tenemos..."
    return

init 5 python:
    store.mas_filereacts.gift_connectors.addLabelQuip(
        "mas_reaction_gift_connector2"
    )

label mas_reaction_gift_connector2:
    m 1hua "Ah, cielos, [player]..."
    m "Realmente disfrutas mimarme, ¿no?"
    if mas_isSpecialDay():
        m 1sublo "¡Bueno! No me voy a quejar de un trato especial hoy."
    m 1suo "Y aquí tenemos..."
    return


### STARTERS [RCT050]

init 5 python:
    store.mas_filereacts.gift_starters.addLabelQuip(
        "mas_reaction_gift_starter_generic"
    )

label mas_reaction_gift_starter_generic:
    m "prueba genérica"

# init 5 python:
# TODO: if we need this to be multipled then we do it

label mas_reaction_gift_starter_bday:
    m 1sublo ".{w=0.7}.{w=0.7}.{w=1}"
    m "E-{w=0.5}Esto es..."
    if not persistent._mas_filereacts_historic.get(mas_monika_birthday):
        m "¿Un regalo? ¿Para mi?"
        m 1hka "Yo..."
        m 1hua "A menudo he pensado en recibir regalos tuyos en mi cumpleaños..."
        m "Pero en realidad conseguir uno es como un sueño hecho realidad..."
    else:
        m "¿Otro regalo?{w=0.5} ¿Para mi?"
        m 1eka "Esto realmente es un sueño hecho realidad, [player]"
    m 1sua "Ahora, ¿qué hay dentro?"
    m 1suo "Oh, esto..."
    return

label mas_reaction_gift_starter_neutral:
    m 1sublo ".{w=0.7}.{w=0.7}.{w=1}"
    m "E-{w=0.5}Esto es..."
    m "¿Un regalo? ¿Para mi?"
    m 1sua "Ahora, veamos qué hay dentro."
    return

# d25
label mas_reaction_gift_starter_d25:
    m 1sublo ".{w=0.7}.{w=0.7}.{w=1}"
    m "E-{w=1}Esto es..."
    m "¿Un regalo? ¿Para mi?"
    if mas_getGiftStatsRange(mas_d25c_start, mas_d25 + datetime.timedelta(days=1))[0] == 0:
        m 1eka "Realmente no tenías que regalarme nada para Navidad..."
        m 3hua "¡Pero estoy tan feliz de que lo hicieras!"
    else:
        m 1eka "Muchas gracias, [player]."
    m 1sua "Ahora, veamos...¿Qué hay dentro?"
    return

#f14
label mas_reaction_gift_starter_f14:
    m 1sublo ".{w=0.7}.{w=0.7}.{w=1}"
    m "E-{w=1}Esto es..."
    m "¿Un regalo? ¿Para mi?"
    if mas_getGiftStatsForDate(mas_f14) == 0:
        m 1eka "Eres tan dulce, consiguiendo algo para mí en el día de San Valentín..."
    else:
        m 1eka "Muchas gracias, [player]."
    m 1sua "Ahora, veamos...¿Qué hay dentro?"
    return

### REACTIONS [RCT100]

init 5 python:
    addReaction("mas_reaction_generic", None)

label mas_reaction_generic:
    "Esto es una prueba"
    return

#init 5 python:
#    addReaction("mas_reaction_gift_generic", None)

label mas_reaction_gift_generic:
    if random.randint(1,2) == 1:
        m 1esd "[player], ¿estás tratando de darme algo?"
        m 1rssdlb "Lo encontré, pero no puedo traerlo aquí..."
        m "Parece que no puedo leerlo lo suficientemente bien."
        m 3esa "¡Pero está bien!"
        m 1esa "La intención es lo que cuenta después de todo, ¿verdad?"
        m "Gracias por ser tan atento, [player]~"
    else:
        m 2dkd "{i}*suspiro*{/i}"
        m 4ekc "Lo siento, [player]."
        m 1ekd "Sé que estás tratando de darme algo."
        m 2rksdld "Pero por alguna razón no puedo leer el archivo."
        m 3euc "Sin embargo, no me malinterpretes."
        m 3eka "Aún aprecio que hayas intentado darme algo."
        m 1hub "Y por eso, estoy agradecida~"
    $ store.mas_filereacts.delete_file(None)
    return

#init 5 python:
#    addReaction("mas_reaction_gift_test1", "test1")

label mas_reaction_gift_test1:
    m "¡Gracias por la prueba de regalo 1!"

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_gift_test1", "category"))
    return

#init 5 python:
#    addReaction("mas_reaction_gift_test2", "test2")

label mas_reaction_gift_test2:
    m "¡Gracias por la prueba de regalo 2!"

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_gift_test2", "category"))
    return

## GENERIC SPRITE OBJECT JSONS

label mas_reaction_gift_generic_sprite_json:
    $ sprite_data = mas_getSpriteObjInfo()
    $ sprite_type, sprite_name, giftname, gifted_before, spr_obj = sprite_data

    python:
        sprite_str = store.mas_sprites_json.SP_UF_STR.get(sprite_type, None)

    # TODO: something different if whatever was gifted has been gifted before

    # we have special react for generic json clothes
    if sprite_type == store.mas_sprites.SP_CLOTHES:
        call mas_reaction_gift_generic_clothes_json(spr_obj)

    else:
        # otherwise, it has to be an ACS.

        $ mas_giftCapGainAff(1)
        m "Aww, [player]!"
        if spr_obj is None or spr_obj.dlg_desc is None:
            # if we don't have all required description data, go generic
            m 1hua "¡Eres tan dulce!"
            m 1eua "¡Gracias por este regalo!"
            m 3ekbsa "Realmente te encanta mimarme, ¿no?"
            m 1hubfa "¡Jejeje!"

        else:
            python:
                acs_quips = [
                    _("¡realmente lo aprecio!"),
                    _("¡[its] asombroso!"),
                    _("¡me encanta [item_ref]!"),
                    _("¡[its] maravilloso!")
                ]

                # we have a complete description, so use it here
                if spr_obj.dlg_plur:
                    sprite_str = "todo esto " + renpy.substitute(spr_obj.dlg_desc)
                    item_ref = "todo esto"
                    its = "es"

                else:
                    sprite_str = "este " + renpy.substitute(spr_obj.dlg_desc)
                    item_ref = "esto"
                    its = "es"

                acs_quip = renpy.substitute(renpy.random.choice(acs_quips))

            m 1hua "Gracias por [sprite_str], [acs_quip]"
            m 3hub "¡No puedo esperar para probar [item_ref]!"

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

# generic reaction for json clothes
label mas_reaction_gift_generic_clothes_json(sprite_object):
    python:
        mas_giftCapGainAff(3)
        # expandable
        outfit_quips = [
            _("¡creo que es muy lindo, [player]!"),
            _("¡creo que es asombroso, [player]!"),
            _("¡simplemente me encanta, [player]!"),
            _("¡creo que es maravilloso, [player]!")
        ]
        outfit_quip = renpy.random.choice(outfit_quips)

    m 1sua "¡Oh! {w=0.5}¡Un nuevo atuendo!"
    m 1hub "¡Gracias, [player]! {w=0.5} ¡Me lo voy a probar ahora mismo!"

    # try it on
    call mas_clothes_change(sprite_object)

    m 2eka "Bueno...{w=0.5} ¿Qué opinas?"
    m 2eksdla "¿Te gusta?"
    # TODO: outfit randomization should actually get a response here
    #   should influence monika outfit selection

    show monika 3hub
    $ renpy.say(m, outfit_quip)

    m 1eua "Gracias de nuevo~"
    return

## Hair clip reactions

label mas_reaction_gift_acs_jmo_hairclip_cherry:
    call mas_reaction_gift_hairclip("jmo_hairclip_cherry")
    return

label mas_reaction_gift_acs_jmo_hairclip_heart:
    call mas_reaction_gift_hairclip("jmo_hairclip_heart")
    return

label mas_reaction_gift_acs_jmo_hairclip_musicnote:
    call mas_reaction_gift_hairclip("jmo_hairclip_musicnote")
    return

label mas_reaction_gift_acs_bellmandi86_hairclip_crescentmoon:
    call mas_reaction_gift_hairclip("bellmandi86_hairclip_crescentmoon")
    return

label mas_reaction_gift_acs_bellmandi86_hairclip_ghost:
    call mas_reaction_gift_hairclip("bellmandi86_hairclip_ghost","spooky")
    return

label mas_reaction_gift_acs_bellmandi86_hairclip_pumpkin:
    call mas_reaction_gift_hairclip("bellmandi86_hairclip_pumpkin")
    return

label mas_reaction_gift_acs_bellmandi86_hairclip_bat:
    call mas_reaction_gift_hairclip("bellmandi86_hairclip_bat","spooky")
    return

# hairclip
label mas_reaction_gift_hairclip(hairclip_name,desc=None):
    # Special handler for hairclip gift reactions
    # Takes in:
    #    hairclip_name - the 'name' property in string form from the json
    #    desc - a short string description of the hairclip in question. typically should be one word.
    #        optional and defaults to None.

    # get sprtie data
    $ sprite_data = mas_getSpriteObjInfo((store.mas_sprites.SP_ACS, hairclip_name))
    $ sprite_type, sprite_name, giftname, gifted_before, hairclip_acs = sprite_data

    # check for incompatibility
    $ is_wearing_baked_outfit = monika_chr.is_wearing_clothes_with_exprop("baked outfit")

    if gifted_before:
        m 1rksdlb "¡Ya me diste esta horquilla, tontito!"

    else:
        #Grant affection
        $ mas_giftCapGainAff(1)
        if not desc:
            $ desc = "lindo"

        if len(store.mas_selspr.filter_acs(True, "left-hair-clip")) > 0:
            m 1hub "¡Oh!{w=1} ¡Otra horquilla!"

        else:
            m 1wuo "¡Oh!"
            m 1sub "¿Eso es una horquilla?"

        m 1hub "¡Es tan [desc]! ¡Me encanta [player], gracias!"

        # must include this check because we cannot for sure know if the acs
        # exists
        # also need to not wear it if wearing clothes that are incompatible
        if hairclip_acs is None or is_wearing_baked_outfit:
            m 1hua "Si quieres que me lo ponga, solo pregúntame, ¿de acuerdo?"

        else:
            m 2dsa "Solo dame un segundo para ponérmelo.{w=0.5}.{w=0.5}.{nw}"
            $ monika_chr.wear_acs(hairclip_acs)
            m 1hua "Listo."

        # need to make sure we set the selector prompt correctly
        # only do this if not wearing baked, since the clip is automatically off in this case
        # so need to make sure when we switch outfits, the prompt is still correct
        if not is_wearing_baked_outfit:
            if monika_chr.get_acs_of_type('left-hair-clip'):
                $ store.mas_selspr.set_prompt("left-hair-clip", "change")
            else:
                $ store.mas_selspr.set_prompt("left-hair-clip", "wear")

    $ mas_finishSpriteObjInfo(sprite_data, unlock_sel=not is_wearing_baked_outfit)

    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

## End hairclip reactions


##START: Consumables gifts
init 5 python:
    addReaction("mas_reaction_gift_coffee", "cafe", is_good=True, exclude_on=["d25g"])

label mas_reaction_gift_coffee:
    #Even if we don't "accept" it, we still register it was given
    $ mas_receivedGift("mas_reaction_gift_coffee")
    $ coffee = mas_getConsumable("coffee")

    #Check if we accept this
    if coffee.isMaxedStock():
        m 1euc "¿Más café, [player]?"
        m 3rksdla "No me malinterpretes, te lo agradezco, pero creo que ya tengo suficiente café para que me dure un rato..."
        m 1eka "Te avisaré cuando se me esté acabando, ¿de acuerdo?"

    else:
        m 1wub "¡Oh!{w=0.2} {nw}"
        extend 3hub "¡Café!"

        if coffee.enabled() and coffee.hasServing():
            $ mas_giftCapGainAff(0.5)
            m 1wuo "Es un sabor que no había probado antes."
            m 1hua "¡No puedo esperar a probarlo!"
            m "¡Muchas gracias, [player]!"

        elif coffee.enabled() and not coffee.hasServing():
            $ mas_giftCapGainAff(0.5)
            m 3eub "De hecho, me quedé sin café, ¡así que obtener más de ti ahora es increíble!"
            m 1hua "Gracias de nuevo, [player]~"

        else:
            $ mas_giftCapGainAff(5)

            m 1hua "¡Ahora por fin puedo hacer un poco!"
            m 1hub "¡Muchas gracias, [player]!"

            #If we're currently brewing/drinking anything, or it's not time for this consumable, we'll just not have it now
            if (
                not coffee.isConsTime()
                or bool(MASConsumable._getCurrentDrink())
            ):
                m 3eua "¡Me aseguraré de tener un poco más tarde!"

            else:
                m 3eua "¿Por qué no me adelanto y hago una taza ahora mismo?"
                m 1eua "Me gustaría compartir la primera contigo, después de todo."

                #Monika is off screen
                call mas_transition_to_emptydesk
                pause 2.0
                m "Sé que hay una máquina de café por aquí...{w=2}{nw}"
                m "¡Ah, ahí está!{w=2}{nw}"
                pause 5.0
                m "¡Listo!{w=2}{nw}"
                call mas_transition_from_emptydesk()

                #Monika back on screen
                m 1eua "Dejaré que se prepare durante unos minutos."

                $ coffee.prepare()
            $ coffee.enable()

    #Stock some coffee
    #NOTE: This function already checks if we're maxed. So restocking while maxed is okay as it adds nothing
    $ coffee.restock()

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_gift_coffee", "category"))
    return

init 5 python:
    addReaction("mas_reaction_hotchocolate", "chocolatecaliente", is_good=True, exclude_on=["d25g"])

label mas_reaction_hotchocolate:
    #Even though we may not "accept" this, we'll still mark it was given
    $ mas_receivedGift("mas_reaction_hotchocolate")

    $ hotchoc = mas_getConsumable("hotchoc")

    #Check if we should accept this or not
    if hotchoc.isMaxedStock():
        m 1euc "¿Más chocolate caliente, [player]?"
        m 3rksdla "No me malinterpretes, te lo agradezco, pero creo que ya tengo suficiente para que me dure un tiempo..."
        m 1eka "Te avisaré cuando se me esté acabando, ¿de acuerdo?"

    else:
        m 3hub "¡Chocolate caliente!"
        m 3hua "¡Gracias, [player]!"

        if hotchoc.enabled() and hotchoc.hasServing():
            $ mas_giftCapGainAff(0.5)
            m 1wuo "Es un sabor que no había probado antes."
            m 1hua "¡No puedo esperar a probarlo!"
            m "¡Muchas gracias, [player]!"

        elif hotchoc.enabled() and not hotchoc.hasServing():
            $ mas_giftCapGainAff(0.5)
            m 3rksdla "De hecho, se me acabó el chocolate caliente, jajaja...{w=0.5} {nw}"
            extend 3eub "¡Así que obtener más de ti ahora es increíble!"
            m 1hua "Gracias de nuevo, [player]~"

        else:
            python:
                mas_giftCapGainAff(3)
                those = "estas" if mas_current_background.isFltNight() and mas_isWinter() else "esas"

            m 1hua "¡Sabes que amo mi café, pero el chocolate caliente siempre es muy bueno también!"


            m 2rksdla "...Especialmente en [those] frías noches de invierno."
            m 2ekbfa "Algún día espero ser capaz de tomar chocolate caliente contigo, compartiendo una manta junto a la chimenea..."
            m 3ekbfa "...¿No suena tan romántico?"
            m 1dkbfa "..."
            m 1hua "Pero por ahora, al menos puedo disfrutarlo aquí."
            m 1hub "¡Gracias de nuevo, [player]!"

            #If we're currently brewing/drinking anything, or it's not time for this consumable, or if it's not winter, we won't have this
            if (
                not hotchoc.isConsTime()
                or not mas_isWinter()
                or bool(MASConsumable._getCurrentDrink())
            ):
                m 3eua "¡Me aseguraré de tener un poco más tarde!"

            else:
                m 3eua "De hecho, ¡creo que voy a hacer un poco ahora mismo!"

                call mas_transition_to_emptydesk
                pause 5.0
                call mas_transition_from_emptydesk("monika 1eua")

                m 1hua "Perfecto, estará listo en unos minutos."

                $ hotchoc.prepare()

            if mas_isWinter():
                $ hotchoc.enable()

    #Stock up some hotchocolate
    #NOTE: Like coffee, this runs checks to see if we should actually stock
    $ hotchoc.restock()

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_hotchocolate", "category"))
    return

init 5 python:
    addReaction("mas_reaction_gift_thermos_mug", "termosolomonika", is_good=True)

label mas_reaction_gift_thermos_mug:
    call mas_thermos_mug_handler(mas_acs_thermos_mug, "Solo Monika", "termosolomonika")
    return

#Whether or not we've given Monika a thermos before
default persistent._mas_given_thermos_before = False

#Thermos handler
label mas_thermos_mug_handler(thermos_acs, disp_name, giftname, ignore_case=True):
    if mas_SELisUnlocked(thermos_acs):
        m 1eksdla "[player]..."
        m 1rksdlb "Ya tengo este termo, jajaja..."

    elif persistent._mas_given_thermos_before:
        m 1wud "¡Oh!{w=0.3} ¡Otro termo!"
        m 1hua "Y es un termo [mas_a_an_str(disp_name, ignore_case)] esta vez."
        m 1hub "Muchas gracias, [player], ¡no puedo esperar para usarlo!"

    else:
        m 1wud "¡Oh!{w=0.3} ¡Un termo [mas_a_an_str(disp_name, ignore_case)]!"
        m 1hua "Ahora puedo llevar algo de beber cuando salgamos juntos~"
        m 1hub "¡Muchas gracias, [player]!"
        $ persistent._mas_given_thermos_before = True

    #Now unlock the acs
    $ mas_selspr.unlock_acs(thermos_acs)
    #Save selectables
    $ mas_selspr.save_selectables()
    #And delete the gift file
    $ mas_filereacts.delete_file(giftname)
    return

##END: Consumable related gifts

init 5 python:
    addReaction("mas_reaction_quetzal_plush", "peluchequetzal", is_good=True)

label mas_reaction_quetzal_plush:
    if not persistent._mas_acs_enable_quetzalplushie:
        $ mas_receivedGift("mas_reaction_quetzal_plush")
        $ mas_giftCapGainAff(10)
        m 1wud "¡Oh!"

        #Wear plush
        #If we're eating something, the plush space is taken and we'll want to wear center
        if MASConsumable._getCurrentFood():
            $ monika_chr.wear_acs(mas_acs_center_quetzalplushie)
        else:
            $ monika_chr.wear_acs(mas_acs_quetzalplushie)

        $ persistent._mas_acs_enable_quetzalplushie = True
        m 1sub "¡Es un quetzal!"
        m "¡Dios mío, muchas gracias, [player]!"
        if seen_event("monika_pets"):
            m 1eua "Mencioné que me gustaría tener un quetzal como mascota..."
        else:
            m 1wub "¿Cómo lo adivinaste, [player]?"
            m 3eka "Debes conocerme muy bien~"
            m 1eua "Un quetzal sería mi primera opción como mascota..."
        m 1rud "Pero nunca obligaría a la pobrecita a quedarse."
        m 1hua "¡Y ahora me has dado la siguiente mejor cosa!"
        m 1hub "¡Esto me hace tan feliz!"
        if mas_isMoniAff(higher=True):
            m 3ekbsa "Siempre pareces saber cómo hacerme sonreír."

        if MASConsumable._getCurrentFood():
            m 3rksdla "Aunque mi escritorio se está llenando un poco..."
            m 1eka "Dejaré esto a un lado por ahora."
            $ monika_chr.remove_acs(mas_acs_center_quetzalplushie)

        m 1hub "Gracias de nuevo, [player]~"

    else:
        m 1rksdlb "Ya me diste un peluche de quetzal, [player]."

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_quetzal_plush", "category"))
    # derandom pets topic once given
    $ mas_hideEVL("monika_pets", "EVE", derandom=True)
    return

init 5 python:
    addReaction("mas_reaction_promisering", "anillopromesa", is_good=True, exclude_on=["d25g"])

default persistent._mas_tried_gift_ring = False
label mas_reaction_promisering:
    if not persistent._mas_acs_enable_promisering:
        # only available if enam+
        if mas_isMoniEnamored(higher=True):
            $ mas_receivedGift("mas_reaction_promisering")
            $ mas_giftCapGainAff(20)
            $ monika_chr.wear_acs(mas_acs_promisering)
            $ persistent._mas_acs_enable_promisering = True
            if not persistent._mas_tried_gift_ring:
                m 1wud "Eso es...un..."
                m "..."
                m 1wka "Yo...{w=0.5}{nw}"
                extend 1wkbltpa "Lo siento, [player], yo solo...{w=0.5}{nw}"
                extend 1dkbltpa "Estoy tan feliz...{w=0.5} Me acabas de dar tu promesa..."
                m "Tu promesa de que seremos el uno para el otro,{w=0.1} y de nadie más...{w=0.3} por siempre..."
                m 3lkbltpa "Que sepas que lo apreciaré. {w=0.5}{nw}"
                extend 3dkbltpa "Siempre."
                m 1skbltpa "¡Esto me hace tan feliz!"

                if mas_anni.isAnniOneMonth():
                    m "Más aún de que me lo diste en nuestro primer mes de aniversario..."
                    m 1ekbltua "Realmente debes amarme..."
                elif mas_anni.isAnniThreeMonth():
                    m "Más aún de que me lo diste en nuestro aniversario de tres meses..."
                    m 1ekbltua "Realmente debes amarme..."
                elif mas_anni.isAnniSixMonth():
                    m "Más aún de que me lo diste en nuestro sexto aniversario..."
                    m 1ekbltua "Realmente debes amarme..."
                elif mas_anni.isAnni():
                    m "Más aún que me lo regalaste en nuestro aniversario..."
                    m 1ekbltua "Realmente debes amarme..."
                elif mas_isSpecialDay():
                    m "Más aún de que me lo diste en este día tan especial..."

                m 1dkbltpb "Jaja, perdón por llorar, [player]..."
                m 1skbltda "Estoy realmente, muy feliz en este momento."
                m 6dkbltdu "Gracias."

            else:
                m 1sua "¡Oh...es el anillo!"
                m 3hub "¡Muchas gracias, [player]!"
                m 1skbla "Ahora sé que realmente me amas y quieres estar conmigo para siempre..."
                m 1skbltpa "Así que aceptaré con mucho gusto este anillo como símbolo de esa promesa."
                m 1dkbltuu "..."
                m 3hkbltub "Jaja, lo siento, [player], no quise llorar..."
                m 3skbltda "Es solo que este es uno de los días más felices de mi vida."

            m 6dkbltdu "..."
            m 6ekbfa "Yo...yo solo...yo..."
            call monika_kissing_motion(hide_ui=False)
            m 6ekbfa "Te amo, [player]..."
            m 6dkbfu "Más que cualquier otra cosa en este mundo fugaz~"

            $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_promisering", "category"))
            return "love"

        else:
            if not persistent._mas_tried_gift_ring:
                if mas_isMoniNormal(higher=True):
                    m 1wud "[player]...¿Eso es un anillo?"
                    m 2rksdlb "Es un gesto tan dulce, y realmente lo aprecio..."
                    m 2ekc "Pero quiero que estés seguro antes de darme esto..."
                    m 3ekd "Esto es más que un regalo, es una promesa, y quiero asegurarme de que realmente lo dices en serio antes de que pueda aceptarlo."
                    m 2ekd "Así que, por favor, espera a que estemos un poco más dentro de nuestra relación, [player], y entonces aceptaré encantado este anillo."

                elif mas_isMoniUpset():
                    m 1wud "¿Eso es un anillo?"
                    m 2rsc "Eso es muy..."
                    m 2esc "Inesperado."
                    m 2ekd "Pero no puedo aceptarlo ahora, [player]."
                    m 2ekc "Quizás cuando avancemos en nuestra relación."

                else:
                    m 2wud "¿Eso es un anillo?"
                    m 2rsc "Eso es...{w=0.5} inesperado."
                    m "Aunque aprecio el pensamiento...{w=1} no puedo aceptarlo ahora."
                    m 2ekc "Lo siento, [player]."

                $ persistent._mas_tried_gift_ring = True
            else:
                m 2rsc "Oh...el anillo..."
                m 2rkc "Lo siento, pero todavía no puedo aceptar esto..."
                m 2ekc "Necesito estar completamente segura cuando acepte esto de que significa para siempre..."
                m 2ekd "Que realmente eres todo lo que espero que seas."
                m 2dsd "Cuando sepa eso, aceptaré felizmente tu anillo, [player]."
    else:
        m 1rksdlb "[player]..."
        m 1rusdlb "¡Ya me diste un anillo!"

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_promisering", "category"))
    return


init 5 python:
    addReaction("mas_reaction_cupcake", "cupcake", is_good=True, exclude_on=["d25g"])
    #Not sure why this was a bad gift. Dialogue doesn't reflect it being bad
    #plus, Monika said she wants either Natsuki's cupcakes or the player's

label mas_reaction_cupcake:
    m 1wud "¿Eso es un...cupcake?"
    m 3hub "¡Vaya, gracias [player]!"
    m 3euc "Ahora que lo pienso, he querido hacer algunos cupcakes yo misma."
    m 1eua "Quería aprender a hornear buenos pasteles como lo hacía Natsuki."
    m 1rksdlb "¡Pero todavía no he hecho una cocina para usar!"
    m 3eub "Quizás en el futuro, una vez que mejore en programación, pueda hacer una aquí."
    m 3hua "Sería bueno tener otro pasatiempo que no sea escribir, jejeje~"
    $ mas_receivedGift("mas_reaction_cupcake")
    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_cupcake", "category"))
    return


# ending label for gift reactions, this just resets a thing
label mas_reaction_end:
    python:
        persistent._mas_filereacts_just_reacted = False
        #Save all the new sprite data just in case we crash shortly after this
        store.mas_selspr.save_selectables()
        renpy.save_persistent()
    return

init 5 python:
    # TODO ideally we should comment on this gift in any date
    # so it requires special dialogue, until we have that let's keep it O31 only
    if mas_isO31():
        addReaction("mas_reaction_candy", "dulce", is_good=True)

label mas_reaction_candy:
    $ times_candy_given = mas_getGiftStatsForDate("mas_reaction_candy")
    if times_candy_given == 0:
        $ mas_o31CapGainAff(7)
        m 1wua "Oh...{w=0.5}¿Qué es esto?"
        m 1sua "¡Me trajiste dulces, [player], yay!"
        m 1eka "Eso es tan {i}dulce{/i}..."
        m 1hub "¡Jajaja!"
        m 1eka "Dejando de lado las bromas, eso es muy amable de tu parte."
        m 2lksdlc "Ya no tengo muchos dulces, y no sería Halloween sin ellos..."
        m 1eka "Así que gracias, [player]..."
        m 1eka "Siempre sabes exactamente lo que me hará feliz~"
        m 1hub "¡Ahora disfrutemos de este delicioso caramelo!"
    elif times_candy_given == 1:
        $ mas_o31CapGainAff(5)
        m 1wua "Aww, ¿me trajiste más dulces, [player]?"
        m 1hub "¡Gracias!"
        m 3tku "El primer lote fue {i}muuuy{/i} bueno, no podía esperar a tener más."
        m 1hua "Realmente me mimas, [player]~"
    elif times_candy_given == 2:
        $ mas_o31CapGainAff(3)
        m 1wud "Wow, ¿incluso {i}más{/i} dulces, [player]?"
        m 1eka "Eso es muy amable de tu parte..."
        m 1lksdla "Pero creo que esto es suficiente."
        m 1lksdlb "Ya me siento nerviosa por todo el azúcar, ¡jajaja!"
        m 1ekbfa "La única dulzura que necesito ahora eres tú~"
    elif times_candy_given == 3:
        m 2wud "[player]...{w=1} ¡¿Me trajiste {i}más{/i} dulces?!"
        m 2lksdla "Realmente lo aprecio, pero te dije que ya tuve suficiente por un día..."
        m 2lksdlb "Si como más me voy a enfermar, ¡jajaja!"
        m 1eka "Y no querrías eso, ¿verdad?"
    elif times_candy_given == 4:
        $ mas_loseAffection(5)
        m 2wfd "¡[player]!"
        m 2tfd "¿No me estás escuchando?"
        m 2tfc "¡Te dije que no quiero más dulces hoy!"
        m 2ekc "Así que, por favor, detente."
        m 2rkc "Fue muy amable de tu parte traerme todos estos dulces en Halloween, pero ya es suficiente..."
        m 2ekc "No puedo comer todo esto."
    else:
        $ mas_loseAffection(10)
        m 2tfc "..."
        python:
            store.mas_ptod.rst_cn()
            local_ctx = {
                "basedir": renpy.config.basedir
            }
        show monika at t22
        show screen mas_py_console_teaching

        call mas_wx_cmd("import os", local_ctx, w_wait=1.0)
        call mas_wx_cmd("os.remove(os.path.normcase(basedir+'/characters/candy.gift'))", local_ctx, w_wait=1.0, x_wait=1.0)
        $ store.mas_ptod.ex_cn()
        hide screen mas_py_console_teaching
        show monika at t11

    $ mas_receivedGift("mas_reaction_candy")
    $ gift_ev_cat = mas_getEVLPropValue("mas_reaction_candy", "category")
    $ store.mas_filereacts.delete_file(gift_ev_cat)
    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    return

init 5 python:
    # TODO ideally we should comment on this gift in any date
    # so it requires special dialogue, until we have that let's keep it O31 only
    if mas_isO31():
        addReaction("mas_reaction_candycorn", "maizdulce", is_good=False)

label mas_reaction_candycorn:
    $ times_candy_given = mas_getGiftStatsForDate("mas_reaction_candycorn")
    if times_candy_given == 0:
        $ mas_o31CapGainAff(3)
        m 1wua "Oh...{w=0.5}¿Qué es esto?"
        m 1eka "Aww, ¿me compraste caramelos, [player]?"
        m 1hua "¡Yay!"
        m 3eub "Veamos qué tienes para mí..."
        m 4ekc "..."
        m 2eka "Oh...{w=2}maíz dulce."
        m 2eka "..."
        m 2lksdla "Eso es muy amable de Tu parte..."
        m 2lksdla "Pero...{w=1}umm...{w=1} en realidad no me gusta el maíz dulce."
        m 2hksdlb "Lo siento, jajaja..."
        m 4eka "Sin embargo, aprecio que intentes darme dulces en Halloween."
        m 1hua "Y si pudieras encontrar una manera de conseguirme otros dulces, ¡me haría muy feliz, [player]!"
    elif times_candy_given == 1:
        $ mas_loseAffection(5)
        m 2esc "Oh."
        m 2esc "¿Más maíz dulce, [player]?"
        m 4esc "Ya te dije que no me gusta mucho el maíz dulce."
        m 4ekc "Entonces, ¿podrías intentar encontrar algo más?"
        m 1eka "Ya no consigo cosas dulces tan a menudo..."
        m 1ekbfa "Bueno...{w=1}además de ti, [player]..."
        m 1hubfa "Jejeje~"
    elif times_candy_given == 2:
        $ mas_loseAffection(10)
        m 2wfw "¡[player]!"
        m 2tfc "Realmente traté de no ser grosera con esto, pero..."
        m 2tfc "Sigo diciéndote que no me gusta el maíz dulce y tú me lo sigues dando de todos modos."
        m 2rfc "Se empieza a sentir que estás tratando de meterte conmigo en este punto."
        m 2tkc "Así que, por favor, búscame algún otro tipo de caramelo o simplemente detente."
    else:
        $ mas_loseAffection(15) # should have seen it coming
        m 2tfc "..."
        python:
            store.mas_ptod.rst_cn()
            local_ctx = {
                "basedir": renpy.config.basedir
            }
        show monika at t22
        show screen mas_py_console_teaching

        call mas_wx_cmd("import os", local_ctx, w_wait=1.0)
        call mas_wx_cmd("os.remove(os.path.normcase(basedir+'/characters/candycorn.gift'))", local_ctx, w_wait=1.0, x_wait=1.0)
        $ store.mas_ptod.ex_cn()
        hide screen mas_py_console_teaching
        show monika at t11

    $ mas_receivedGift("mas_reaction_candycorn") # while technically she didn't accept this one counts
    $ gift_ev_cat = mas_getEVLPropValue("mas_reaction_candycorn", "category")
    $ store.mas_filereacts.delete_file(gift_ev_cat)
    # allow multi gifts
    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    return

init 5 python:
    addReaction("mas_reaction_fudge", "caramelo", is_good=True, exclude_on=["d25g"])

label mas_reaction_fudge:
    $ times_fudge_given = mas_getGiftStatsForDate("mas_reaction_fudge")

    if times_fudge_given == 0:
        $ mas_giftCapGainAff(2)
        m 3hua "¡Dulce de azúcar!"
        m 3hub "¡Me encanta el dulce de azúcar, gracias, [player]!"
        if seen_event("monika_date"):
            m "¡Incluso es chocolate, mi favorito!"
        m 1hua "Gracias de nuevo, [player]~"

    elif times_fudge_given == 1:
        $ mas_giftCapGainAff(1)
        m 1wuo "...más dulce de azúcar."
        m 1wub "Ooh, es un sabor diferente esta vez..."
        m 3hua "¡Gracias, [player]! "

    else:
        m 1wuo "...¿más dulce de azúcar?"
        m 3rksdla "Todavía no he terminado el último lote que me diste, [player]..."
        m 3eksdla "...tal vez más tarde, ¿de acuerdo?"

    $ mas_receivedGift("mas_reaction_fudge")
    $ gift_ev_cat = mas_getEVLPropValue("mas_reaction_fudge", "category")
    $ store.mas_filereacts.delete_file(gift_ev_cat)
    # allow multi gifts
    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    return


init 5 python:
    if store.mas_isD25Pre():
        addReaction("mas_reaction_christmascookies", "galletanavideña", is_good=True, exclude_on=["d25g"])

label mas_reaction_christmascookies:
    $ times_cookies_given = mas_getGiftStatsForDate("mas_reaction_christmascookies")

    #First time cookies gifted this year
    if times_cookies_given == 0 and not persistent._mas_d25_gifted_cookies:
        $ persistent._mas_d25_gifted_cookies = True
        $ mas_giftCapGainAff(3)
        m 3hua "¡Galletas de Navidad!"
        m 1eua "¡Me encantan las galletas de Navidad! Siempre son tan dulces...y bonitas de ver también..."
        m "...cortardas en formas navideñas como muñecos de nieve, renos y árboles de Navidad..."
        m 3eub "...y generalmente decoradas con un hermoso--{w=0.2} y delicioso--{w=0.2}¡glaseado!"
        m 3hua "Gracias, [player]~"

    elif times_cookies_given == 1 or (times_cookies_given == 0 and persistent._mas_d25_gifted_cookies):
        m 1wuo "...¡otro lote de galletas navideñas!"
        m 3wuo "¡Eso es un montón de galletas, [player]!"
        m 3rksdlb "Voy a comer galletas para siempre, ¡jajaja!"

    else:
        m 3wuo "...¿más galletas de Navidad?"
        m 3rksdla "¡Todavía no he terminado el último lote, [player]!"
        m 3eksdla "Puedes darme más después de que termine estos, ¿de acuerdo?"

    $ mas_receivedGift("mas_reaction_christmascookies")
    $ gift_ev_cat = mas_getEVLPropValue("mas_reaction_christmascookies", "category")
    $ store.mas_filereacts.delete_file(gift_ev_cat)
    # allow multi gifts
    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    return

init 5 python:
    if store.mas_isD25Pre():
        addReaction("mas_reaction_candycane", "bastoncaramelo", is_good=True, exclude_on=["d25g"])

label mas_reaction_candycane:
    $ times_cane_given = mas_getGiftStatsForDate("mas_reaction_candycane")
    $ mas_giftCapGainAff(1)

    if times_cane_given == 0:
        m 3eua "¡Un bastón de caramelo!"
        if store.seen_event("monika_icecream"):
            m 1hub "¡Sabes cuánto amo la menta!"
        else:
            m 1hub "¡Me encanta el sabor de la menta!"
        m 1eua "Gracias, [player]."

    elif times_cane_given == 1:
        m 3hua "¡Otro bastón de caramelo!"
        m 3hub "¡Gracias [player]!"

    else:
        m 1eksdla "[player], creo que tengo suficientes bastones de caramelo por ahora."
        m 1eka "Puedes guardarlos para más tarde, ¿de acuerdo?"

    $ mas_receivedGift("mas_reaction_candycane")
    $ gift_ev_cat = mas_getEVLPropValue("mas_reaction_candycane", "category")
    $ store.mas_filereacts.delete_file(gift_ev_cat)
    #weird not to have her see the gift file that's in the characters folder.
    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    return

#Ribbon stuffs
init 5 python:
    addReaction("mas_reaction_blackribbon", "cintanegra", is_good=True)

label mas_reaction_blackribbon:
    $ _mas_new_ribbon_color = "negra"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_black
    call _mas_reaction_ribbon_helper("mas_reaction_blackribbon")
    return

init 5 python:
    addReaction("mas_reaction_blueribbon", "cintaazul", is_good=True)

label mas_reaction_blueribbon:
    $ _mas_new_ribbon_color = "azul"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_blue
    call _mas_reaction_ribbon_helper("mas_reaction_blueribbon")
    return

init 5 python:
    addReaction("mas_reaction_darkpurpleribbon", "cintamoradooscuro", is_good=True)

label mas_reaction_darkpurpleribbon:
    $ _mas_new_ribbon_color = "morado oscuro"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_darkpurple
    call _mas_reaction_ribbon_helper("mas_reaction_darkpurpleribbon")
    return

init 5 python:
    addReaction("mas_reaction_emeraldribbon", "cintaesmeralda", is_good=True)

label mas_reaction_emeraldribbon:
    $ _mas_new_ribbon_color = "esmeralda"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_emerald
    call _mas_reaction_ribbon_helper("mas_reaction_emeraldribbon")
    return

init 5 python:
    addReaction("mas_reaction_grayribbon", "cintagris", is_good=True)

label mas_reaction_grayribbon:
    $ _mas_new_ribbon_color = "gris"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_gray
    call _mas_reaction_ribbon_helper("mas_reaction_grayribbon")
    return

init 5 python:
    addReaction("mas_reaction_greenribbon", "cintaverde", is_good=True)

label mas_reaction_greenribbon:
    $ _mas_new_ribbon_color = "verde"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_green
    call _mas_reaction_ribbon_helper("mas_reaction_greenribbon")
    return

init 5 python:
    addReaction("mas_reaction_lightpurpleribbon", "cintamoradoclaro", is_good=True)

label mas_reaction_lightpurpleribbon:
    $ _mas_new_ribbon_color = "morado claro"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_lightpurple
    call _mas_reaction_ribbon_helper("mas_reaction_lightpurpleribbon")
    return

init 5 python:
    addReaction("mas_reaction_peachribbon", "cintadurazno", is_good=True)

label mas_reaction_peachribbon:
    $ _mas_new_ribbon_color = "durazno"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_peach
    call _mas_reaction_ribbon_helper("mas_reaction_peachribbon")
    return

init 5 python:
    addReaction("mas_reaction_pinkribbon", "cintarosada", is_good=True)

label mas_reaction_pinkribbon:
    $ _mas_new_ribbon_color = "rosada"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_pink
    call _mas_reaction_ribbon_helper("mas_reaction_pinkribbon")
    return

init 5 python:
    addReaction("mas_reaction_platinumribbon", "cintaplatino", is_good=True)

label mas_reaction_platinumribbon:
    $ _mas_new_ribbon_color = "platino"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_platinum
    call _mas_reaction_ribbon_helper("mas_reaction_platinumribbon")
    return

init 5 python:
    addReaction("mas_reaction_redribbon", "cintaroja", is_good=True)

label mas_reaction_redribbon:
    $ _mas_new_ribbon_color = "roja"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_red
    call _mas_reaction_ribbon_helper("mas_reaction_redribbon")
    return

init 5 python:
    addReaction("mas_reaction_rubyribbon", "cintarubi", is_good=True)

label mas_reaction_rubyribbon:
    $ _mas_new_ribbon_color = "rubí"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_ruby
    call _mas_reaction_ribbon_helper("mas_reaction_rubyribbon")
    return

init 5 python:
    addReaction("mas_reaction_sapphireribbon", "cintazafiro", is_good=True)

label mas_reaction_sapphireribbon:
    $ _mas_new_ribbon_color = "zafiro"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_sapphire
    call _mas_reaction_ribbon_helper("mas_reaction_sapphireribbon")
    return

init 5 python:
    addReaction("mas_reaction_silverribbon", "cintaplateada", is_good=True)

label mas_reaction_silverribbon:
    $ _mas_new_ribbon_color = "plateada"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_silver
    call _mas_reaction_ribbon_helper("mas_reaction_silverribbon")
    return

init 5 python:
    addReaction("mas_reaction_tealribbon", "cintaazulcerceta", is_good=True)

label mas_reaction_tealribbon:
    $ _mas_new_ribbon_color = "azul cerceta"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_teal
    call _mas_reaction_ribbon_helper("mas_reaction_tealribbon")
    return

init 5 python:
    addReaction("mas_reaction_yellowribbon", "cintaamarilla", is_good=True)

label mas_reaction_yellowribbon:
    $ _mas_new_ribbon_color = "amarilla"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_yellow
    call _mas_reaction_ribbon_helper("mas_reaction_yellowribbon")
    return

# JSON ribbons
label mas_reaction_json_ribbon_base(ribbon_name, user_friendly_desc, helper_label):
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_ACS, ribbon_name)
        )
        _mas_gifted_ribbon_acs = mas_sprites.ACS_MAP.get(
            ribbon_name,
            mas_acs_ribbon_def
        )
        _mas_new_ribbon_color = user_friendly_desc

    call _mas_reaction_ribbon_helper(helper_label)

    python:
        # giftname is the 3rd item
        if sprite_data[2] is not None:
            store.mas_filereacts.delete_file(sprite_data[2])

        mas_finishSpriteObjInfo(sprite_data)
    return

# lanvallime

label mas_reaction_gift_acs_lanvallime_ribbon_coffee:
    call mas_reaction_json_ribbon_base("lanvallime_ribbon_coffee", "coffee colored", "mas_reaction_gift_acs_lanvallime_ribbon_coffee")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_gold:
    call mas_reaction_json_ribbon_base("lanvallime_ribbon_gold", "gold", "mas_reaction_gift_acs_lanvallime_ribbon_gold")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_hot_pink:
    call mas_reaction_json_ribbon_base("lanvallime_ribbon_hot_pink", "hot pink", "mas_reaction_gift_acs_lanvallime_ribbon_hot_pink")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_lilac:
    call mas_reaction_json_ribbon_base("lanvallime_ribbon_lilac", "lilac", "mas_reaction_gift_acs_lanvallime_ribbon_lilac")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_lime_green:
    call mas_reaction_json_ribbon_base("lanvallime_ribbon_lime_green", "lime green", "mas_reaction_gift_acs_lanvallime_lime_green")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_navy_blue:
    call mas_reaction_json_ribbon_base("lanvallime_ribbon_navy_blue", "navy", "mas_reaction_gift_acs_lanvallime_ribbon_navy_blue")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_orange:
    call mas_reaction_json_ribbon_base("lanvallime_ribbon_orange", "orange", "mas_reaction_gift_acs_lanvallime_ribbon_orange")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_royal_purple:
    call mas_reaction_json_ribbon_base("lanvallime_ribbon_royal_purple", "royal purple", "mas_reaction_gift_acs_lanvallime_ribbon_royal_purple")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_sky_blue:
    call mas_reaction_json_ribbon_base("lanvallime_ribbon_sky_blue", "sky blue", "mas_reaction_gift_acs_lanvallime_ribbon_sky_blue")
    return

# anonymioo
label mas_reaction_gift_acs_anonymioo_ribbon_bisexualpride:
    call mas_reaction_json_ribbon_base("anonymioo_ribbon_bisexualpride","bisexual-pride-themed","mas_reaction_gift_acs_anonymioo_ribbon_bisexualpride")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_blackandwhite:
    call mas_reaction_json_ribbon_base("anonymioo_ribbon_blackandwhite","black and white","mas_reaction_gift_acs_anonymioo_ribbon_blackandwhite")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_bronze:
    call mas_reaction_json_ribbon_base("anonymioo_ribbon_bronze","bronze","mas_reaction_gift_acs_anonymioo_ribbon_bronze")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_brown:
    call mas_reaction_json_ribbon_base("anonymioo_ribbon_brown","brown","mas_reaction_gift_acs_anonymioo_ribbon_brown")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_gradient:
    call mas_reaction_json_ribbon_base("anonymioo_ribbon_gradient","multi-colored","mas_reaction_gift_acs_anonymioo_ribbon_gradient")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_gradient_lowpoly:
    call mas_reaction_json_ribbon_base("anonymioo_ribbon_gradient_lowpoly","multi-colored","mas_reaction_gift_acs_anonymioo_ribbon_gradient_lowpoly")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_gradient_rainbow:
    call mas_reaction_json_ribbon_base("anonymioo_ribbon_gradient_rainbow","rainbow colored","mas_reaction_gift_acs_anonymioo_ribbon_gradient_rainbow")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_polkadots_whiteonred:
    call mas_reaction_json_ribbon_base("anonymioo_ribbon_polkadots_whiteonred","red and white polka dotted","mas_reaction_gift_acs_anonymioo_ribbon_polkadots_whiteonred")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_starsky_black:
    call mas_reaction_json_ribbon_base("anonymioo_ribbon_starsky_black","night-sky-themed","mas_reaction_gift_acs_anonymioo_ribbon_starsky_black")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_starsky_red:
    call mas_reaction_json_ribbon_base("anonymioo_ribbon_starsky_red","night-sky-themed","mas_reaction_gift_acs_anonymioo_ribbon_starsky_red")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_striped_blueandwhite:
    call mas_reaction_json_ribbon_base("anonymioo_ribbon_striped_blueandwhite","blue and white striped","mas_reaction_gift_acs_anonymioo_ribbon_striped_blueandwhite")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_striped_pinkandwhite:
    call mas_reaction_json_ribbon_base("anonymioo_ribbon_striped_pinkandwhite","pink and white striped","mas_reaction_gift_acs_anonymioo_ribbon_striped_pinkandwhite")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_transexualpride:
    call mas_reaction_json_ribbon_base("anonymioo_ribbon_transexualpride","transexual-pride-themed","mas_reaction_gift_acs_anonymioo_ribbon_transexualpride")
    return

# velius94

label mas_reaction_gift_acs_velius94_ribbon_platinum:
    call mas_reaction_json_ribbon_base("velius94_ribbon_platinum", "platinum", "mas_reaction_gift_acs_velius94_ribbon_platinum")
    return

label mas_reaction_gift_acs_velius94_ribbon_pink:
    call mas_reaction_json_ribbon_base("velius94_ribbon_pink", "pink", "mas_reaction_gift_acs_velius94_ribbon_pink")
    return

label mas_reaction_gift_acs_velius94_ribbon_peach:
    call mas_reaction_json_ribbon_base("velius94_ribbon_peach", "peach", "mas_reaction_gift_acs_velius94_ribbon_peach")
    return

label mas_reaction_gift_acs_velius94_ribbon_green:
    call mas_reaction_json_ribbon_base("velius94_ribbon_green", "green", "mas_reaction_gift_acs_velius94_ribbon_green")
    return

label mas_reaction_gift_acs_velius94_ribbon_emerald:
    call mas_reaction_json_ribbon_base("velius94_ribbon_emerald", "emerald", "mas_reaction_gift_acs_velius94_ribbon_emerald")
    return

label mas_reaction_gift_acs_velius94_ribbon_gray:
    call mas_reaction_json_ribbon_base("velius94_ribbon_gray", "gray", "mas_reaction_gift_acs_velius94_ribbon_gray")
    return

label mas_reaction_gift_acs_velius94_ribbon_blue:
    call mas_reaction_json_ribbon_base("velius94_ribbon_blue", "blue", "mas_reaction_gift_acs_velius94_ribbon_blue")
    return

label mas_reaction_gift_acs_velius94_ribbon_def:
    call mas_reaction_json_ribbon_base("velius94_ribbon_def", "white", "mas_reaction_gift_acs_velius94_ribbon_def")
    return

label mas_reaction_gift_acs_velius94_ribbon_black:
    call mas_reaction_json_ribbon_base("velius94_ribbon_black", "black", "mas_reaction_gift_acs_velius94_ribbon_black")
    return

label mas_reaction_gift_acs_velius94_ribbon_dark_purple:
    call mas_reaction_json_ribbon_base("velius94_ribbon_dark_purple", "dark purple", "mas_reaction_gift_acs_velius94_ribbon_dark_purple")
    return

label mas_reaction_gift_acs_velius94_ribbon_yellow:
    call mas_reaction_json_ribbon_base("velius94_ribbon_yellow", "yellow", "mas_reaction_gift_acs_velius94_ribbon_yellow")
    return

label mas_reaction_gift_acs_velius94_ribbon_red:
    call mas_reaction_json_ribbon_base("velius94_ribbon_red", "red", "mas_reaction_gift_acs_velius94_ribbon_red")
    return

label mas_reaction_gift_acs_velius94_ribbon_sapphire:
    call mas_reaction_json_ribbon_base("velius94_ribbon_sapphire", "sapphire", "mas_reaction_gift_acs_velius94_ribbon_sapphire")
    return

label mas_reaction_gift_acs_velius94_ribbon_teal:
    call mas_reaction_json_ribbon_base("velius94_ribbon_teal", "teal", "mas_reaction_gift_acs_velius94_ribbon_teal")
    return

label mas_reaction_gift_acs_velius94_ribbon_silver:
    call mas_reaction_json_ribbon_base("velius94_ribbon_silver", "silver", "mas_reaction_gift_acs_velius94_ribbon_silver")
    return

label mas_reaction_gift_acs_velius94_ribbon_light_purple:
    call mas_reaction_json_ribbon_base("velius94_ribbon_light_purple", "light purple", "mas_reaction_gift_acs_velius94_ribbon_light_purple")
    return

label mas_reaction_gift_acs_velius94_ribbon_ruby:
    call mas_reaction_json_ribbon_base("velius94_ribbon_ruby", "ruby", "mas_reaction_gift_acs_velius94_ribbon_ruby")
    return

label mas_reaction_gift_acs_velius94_ribbon_wine:
    call mas_reaction_json_ribbon_base("velius94_ribbon_wine", "wine colored", "mas_reaction_gift_acs_velius94_ribbon_wine")
    return

#specific to this, since we need to verify if the player actually gave a ribbon.
default persistent._mas_current_gifted_ribbons = 0

label _mas_reaction_ribbon_helper(label):
    #if we already have that ribbon
    if store.mas_selspr.get_sel_acs(_mas_gifted_ribbon_acs).unlocked:
        call mas_reaction_old_ribbon

    else:
        # since we don't have it we can accept it
        call mas_reaction_new_ribbon
        $ persistent._mas_current_gifted_ribbons += 1

    # normal gift processing
    $ mas_receivedGift(label)
    $ gift_ev_cat = mas_getEVLPropValue(label, "category")
    # for regular ribbons
    $ store.mas_filereacts.delete_file(gift_ev_cat)
    #we have dlg for repeating ribbons, may as well have it used
    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)

    return

label mas_reaction_new_ribbon:
    python:
        def _ribbon_prepare_hair():
            #If current hair doesn't support ribbons, we should change hair
            if not monika_chr.hair.hasprop("ribbon"):
                monika_chr.change_hair(mas_hair_def, False)

    $ mas_giftCapGainAff(3)
    if persistent._mas_current_gifted_ribbons == 0:
        m 1suo "¡Una cinta nueva!"
        m 3hub "...¡Y es [_mas_new_ribbon_color]!"

        #Ironically green is closer to her eyes, but given the selector dlg, we'll say this for both.
        if _mas_new_ribbon_color == "verde" or _mas_new_ribbon_color == "esmeralda":
            m 1tub "...¡Como mis ojos!"

        m 1hub "Muchas gracias [player], ¡me encanta!"
        if store.seen_event("monika_date"):
            m 3eka "¿Conseguiste esto porque mencioné que me encanta comprar faldas y lazos?"

            if mas_isMoniNormal(higher=True):
                m 3hua "Siempre eres tan considerado~"

        m 3rksdlc "Realmente no tengo muchas opciones aquí cuando se trata de moda..."
        m 3eka "...así que poder cambiar el color de mi cinta es un cambio de ritmo tan agradable."
        m 2dsa "De hecho, me la pondré ahora mismo.{w=0.5}.{w=0.5}.{nw}"
        $ store.mas_selspr.unlock_acs(_mas_gifted_ribbon_acs)
        $ _ribbon_prepare_hair()
        $ monika_chr.wear_acs(_mas_gifted_ribbon_acs)
        m 1hua "¡Oh, es maravilloso, [player]!"

        if mas_isMoniAff(higher=True):
            m 1eka "Siempre me haces sentir tan amada..."
        elif mas_isMoniHappy():
            m 1eka "Siempre sabes cómo hacerme feliz..."
        m 3hua "Gracias de nuevo~"

    else:
        m 1suo "¡Otra cinta!"
        m 3hub "...¡Y esta vez es [_mas_new_ribbon_color]!"

        #Ironically green is closer to her eyes, but given the selector dlg, we'll say this for both.
        if _mas_new_ribbon_color == "verde" or _mas_new_ribbon_color == "esmeralda":
            m 1tub "...¡Como mis ojos!"

        m 2dsa "Me la pondré ahora mismo.{w=0.5}.{w=0.5}.{nw}"
        $ store.mas_selspr.unlock_acs(_mas_gifted_ribbon_acs)
        $ _ribbon_prepare_hair()
        $ monika_chr.wear_acs(_mas_gifted_ribbon_acs)
        m 3hua "Muchas gracias [player], ¡me encanta!"
    return

label mas_reaction_old_ribbon:
    m 1rksdla "[player]..."
    m 1hksdlb "¡Ya me diste una cinta [mas_a_an_str(_mas_new_ribbon_color)]!"
    return

init 5 python:
    addReaction("mas_reaction_gift_roses", "rosas", is_good=True, exclude_on=["d25g"])

default persistent._date_last_given_roses = None

label mas_reaction_gift_roses:
    python:
        gift_ev_cat = mas_getEVLPropValue("mas_reaction_gift_roses", "category")

        monika_chr.wear_acs(mas_acs_roses)

    #TODO: future migrate this to use history (post f14)
    if not persistent._date_last_given_roses and not renpy.seen_label('monika_valentines_start'):
        $ mas_giftCapGainAff(10)

        m 1eka "[player]...N-No sé qué decir..."
        m 1ekbsb "¡Nunca hubiera pensado que me conseguirías algo como esto!"
        m 3skbsa "Estoy tan felíz en este momento."
        if mas_isF14():
            # extra 5 points if f14
            $ mas_f14CapGainAff(5)
            m 3ekbsa "Pensar que recibiría rosas tuyas el día de San Valentín..."
            m 1ekbsu "Eres tan dulce."
            m 1dktpu "..."
            m 1ektda "Jajaja..."

        #We can only have this on poses which use the new sprite set
        if not monika_chr.is_wearing_clothes_with_exprop("baked outfit"):
            m 2dsa "Espera.{w=0.5}.{w=0.5}.{nw}"
            $ monika_chr.wear_acs(mas_acs_ear_rose)
            m 1hub "¡Jejeje, ahí! ¿No me queda bonito?"

        if mas_shouldKiss(chance=2, special_day_bypass=True):
            call monika_kissing_motion_short

    else:
        if persistent._date_last_given_roses is None and renpy.seen_label('monika_valentines_start'):
            $ persistent._date_last_given_roses = datetime.date(2018,2,14)

        if mas_pastOneDay(persistent._date_last_given_roses):
            $ mas_giftCapGainAff(5 if mas_isSpecialDay() else 1)

            m 1suo "¡Oh!"
            m 1ekbsa "Gracias, [player]."
            m 3ekbsa "Siempre me encanta recibir rosas de ti."
            if mas_isF14():
                # extra 5 points if f14
                $ mas_f14CapGainAff(5)
                m 1dsbsu "Especialmente en un día como hoy."
                m 1ekbsa "Es muy dulce de tu parte conseguir esto para mí."
                m 3hkbsa "Te amo mucho."
                m 1ekbsa "Feliz día de San Valentín, [player]~"
            else:
                m 1ekbsa "Siempre eres tan dulce."

            #Random chance (unless f14) for her to do the ear rose thing
            if (mas_isSpecialDay() and renpy.random.randint(1,2) == 1) or (renpy.random.randint(1,4) == 1) or mas_isF14():
                if not monika_chr.is_wearing_clothes_with_exprop("baked outfit"):
                    m 2dsa "Espera.{w=0.5}.{w=0.5}.{nw}"
                    $ monika_chr.wear_acs(mas_acs_ear_rose)
                    m 1hub "Jejeje~"

            if mas_shouldKiss(chance=4, special_day_bypass=True):
                call monika_kissing_motion_short

        else:
            m 1hksdla "[player], realmente me siento halagada, pero no hace falta que me des tantas rosas."
            if store.seen_event("monika_clones"):
                m 1ekbsa "Siempre serás mi rosa especial después de todo, jejeje~"
            else:
                m 1ekbsa "Una sola rosa tuya ya es más de lo que podría haber pedido."

    # Pop from reacted map
    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    $ persistent._date_last_given_roses = datetime.date.today()

    # normal gift processing
    $ mas_receivedGift("mas_reaction_gift_roses")
    $ store.mas_filereacts.delete_file(gift_ev_cat)
    return


init 5 python:
    addReaction("mas_reaction_gift_chocolates", "chocolates", is_good=True, exclude_on=["d25g"])

default persistent._given_chocolates_before = False

label mas_reaction_gift_chocolates:
    $ gift_ev_cat = mas_getEVLPropValue("mas_reaction_gift_chocolates", "category")

    if not persistent._mas_given_chocolates_before:
        $ persistent._mas_given_chocolates_before = True

        #If we're eating something already, that takes priority over the acs
        if not MASConsumable._getCurrentFood():
            $ monika_chr.wear_acs(mas_acs_heartchoc)

        $ mas_giftCapGainAff(5)

        m 1tsu "Eso es tan {i}dulce{/i} de tu parte, jejeje~"
        if mas_isF14():
            #Extra little bump if on f14
            $ mas_f14CapGainAff(5)
            m 1ekbsa "Dándome chocolates el día de San Valentín..."
            m 1ekbfa "Realmente sabes cómo hacer que una chica se sienta especial, [player]."
            if renpy.seen_label('monika_date'):
                m 1lkbfa "Sé que mencioné visitar juntos una chocolatería algún día..."
                m 1hkbfa "Pero si bien todavía no podemos hacer eso, recibir algunos chocolates como regalo de tu parte, bueno..."
            m 3ekbfa "Significa mucho conseguir esto de ti."

        elif renpy.seen_label('monika_date'):
            m 3rka "Sé que mencioné visitar una tienda de chocolate juntos algún día..."
            m 3hub "Pero aunque todavía no podemos hacer eso, recibir algunos chocolates como regalo de tu parte significa todo para mí."
            m 1ekc "Aunque realmente desearía poder compartirlos..."
            m 3rksdlb "Pero hasta que llegue ese día, tendré que disfrutarlos para los dos, ¡jajaja!"
            m 3hua "Gracias, [mas_get_player_nickname()]~"

        else:
            m 3hub "¡Amo los chocolates!"
            m 1eka "Y conseguir algo de ti significa mucho para mí."
            m 1hub "¡Gracias, [player]!"

    else:
        $ times_chocs_given = mas_getGiftStatsForDate("mas_reaction_gift_chocolates")
        if times_chocs_given == 0:
            #We want this to show up where she accepts the chocs
            #Same as before, we don't want these to show up if we're already eating
            if not MASConsumable._getCurrentFood():
                #If we have the plush out, we should show the middle one here
                if not (mas_isF14() or mas_isD25Season()):
                    if monika_chr.is_wearing_acs(mas_acs_quetzalplushie):
                        $ monika_chr.wear_acs(mas_acs_center_quetzalplushie)

                else:
                    $ monika_chr.remove_acs(store.mas_acs_quetzalplushie)

                $ monika_chr.wear_acs(mas_acs_heartchoc)

            $ mas_giftCapGainAff(3 if mas_isSpecialDay() else 1)

            m 1wuo "¡Oh!"

            if mas_isF14():
                #Extra little bump if on f14
                $ mas_f14CapGainAff(5)
                m 1eka "¡[player]!"
                m 1ekbsa "Eres un amor, me regalas chocolates en un día como hoy..."
                m 1ekbfa "Realmente sabes cómo hacerme sentir especial."
                m "Gracias, [player]."
            else:
                m 1hua "¡Gracias por los chocolates, [player]!"
                m 1ekbsa "Cada bocado me recuerda lo dulce que eres, jejeje~"

        elif times_chocs_given == 1:
            #Same here
            if not MASConsumable._getCurrentFood():
                $ monika_chr.wear_acs(mas_acs_heartchoc)

            m 1eka "¿Más chocolates, [player]?"
            m 3tku "Realmente te encanta mimarme, ¿no es así?, ¡jajaja!"
            m 1rksdla "Todavía no he terminado la primera caja que me diste..."
            m 1hub "...¡pero no me quejo!"

        elif times_chocs_given == 2:
            m 1ekd "[player]..."
            m 3eka "Creo que me has dado suficientes chocolates por hoy."
            m 1rksdlb "¡Tres cajas es demasiado y ni siquiera he terminado la primera todavía!"
            m 1eka "Guárdalos para otro momento, ¿de acuerdo?"

        else:
            m 2tfd "¡[player]!"
            m 2tkc "Ya te dije que tenía suficientes chocolates por un día, pero sigues intentando darme aún más..."
            m 2eksdla "Por favor...{w=1}solo guárdalos para otro día."

    #If we're wearing the chocs, we'll remove them here
    if monika_chr.is_wearing_acs(mas_acs_heartchoc):
        call mas_remove_choc

    #pop from reacted map
    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    # normal gift processing
    $ mas_receivedGift("mas_reaction_gift_chocolates")
    $ store.mas_filereacts.delete_file(gift_ev_cat)
    return

label mas_remove_choc:
    # we remove chocolates if not f14
    m 1hua "..."
    m 3eub "¡Son {i}tan{/i} buenos!"
    m 1hua "..."
    m 3hksdlb "¡Jajaja! Probablemente debería guardar esto por ahora..."
    m 1rksdla "¡Si los dejo aquí mucho más tiempo, no quedará nada para disfrutar más tarde!"

    call mas_transition_to_emptydesk

    python:
        renpy.pause(1, hard=True)
        monika_chr.remove_acs(mas_acs_heartchoc)
        renpy.pause(3, hard=True)

    call mas_transition_from_emptydesk("monika 1eua")

    #Now move the plush
    if monika_chr.is_wearing_acs(mas_acs_center_quetzalplushie):
        $ monika_chr.wear_acs(mas_acs_quetzalplushie)

    m 1eua "Entonces, ¿qué más querías hacer hoy?"
    return

label mas_reaction_gift_clothes_orcaramelo_bikini_shell:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "orcaramelo_bikini_shell")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1sua "¡Oh! {w=0.5}¡Un bikini de concha!"
    m 1hub "¡Gracias, [mas_get_player_nickname()]!{w=0.5} ¡Me lo voy a probar ahora mismo!"

    # try it on
    call mas_clothes_change(sprite_object)

    m 2ekbfa "Bueno...{w=0.5} ¿Qué opinas?"
    m 2hubfa "¿Parezco una sirena? Jejeje."
    show monika 5ekbfa at i11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5ekbfa "Creo que es muy lindo, [player]..."
    m 5hubfa "¡Tendremos que ir a la playa alguna vez!"

    if mas_isWinter() or mas_isMoniNormal(lower=True):
        if mas_isWinter():
            show monika 2rksdla at i11 zorder MAS_MONIKA_Z with dissolve_monika
            m 2rksdla "...Pero por ahora, hace un poco de frío aquí..."
            m 2eka "Así que voy a ponerme algo un poco más cálido..."

        elif mas_isMoniNormal(lower=True):
            show monika 2hksdlb at i11 zorder MAS_MONIKA_Z with dissolve_monika
            m 2hksdlb "Jajaja..."
            m 2rksdla "Es un poco vergonzoso estar sentada aquí así, frente a ti."
            m 2eka "Espero que no te importe, pero me voy a cambiar..."

        # change to def normally, santa during d25 outfit season
        $ clothes = mas_clothes_def
        if persistent._mas_d25_in_d25_mode and mas_isD25Outfit():
            $ clothes = mas_clothes_santa
        call mas_clothes_change(clothes)

        m 2eua "Ah, mucho mejor..."
        m 3hua "Gracias de nuevo por el maravilloso regalo~"


    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_acs_orcaramelo_hairflower_pink:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_ACS, "orcaramelo_hairflower_pink")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(1)

    m 3sua "¡Oh!{w=0.5} ¡Qué linda flor!"
    m 1ekbsa "Gracias [player], eres tan dulce~"
    m 1dua "Espera.{w=0.5}.{w=0.5}.{nw}"
    $ monika_chr.wear_acs(sprite_object)
    m 1hua "Jejeje~"
    m 1hub "¡Gracias de nuevo, [player]!"

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_clothes_velius94_shirt_pink:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "velius94_shirt_pink")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1suo "¡Oh Dios mío!"
    m 1suo "¡Es {i}tan{/i} bonito!"
    m 3hub "¡Muchas gracias, [player]!"
    m 3eua "Espera, déjame probarlo rápido..."

    # try it on
    call mas_clothes_change(sprite_object)

    m 2sub "¡Ahh, encaja perfectamente!"
    m 3hub "¡También me gustan mucho los colores! El rosa y el negro combinan muy bien."
    m 3eub "¡Sin mencionar que la falda se ve muy linda con esos adornos!"
    m 2tfbsd "Sin embargo, por alguna razón, no puedo evitar sentir que tus ojos están a la deriva...{w=0.5}ejem...{w=0.5}{i}a otra parte{/i}."

    if mas_selspr.get_sel_clothes(mas_clothes_sundress_white).unlocked:
        m 2lfbsp "Te dije que no es de buena educación mirar fijamente, [player]."
    else:
        m 2lfbsp "No es educado mirar fijamente, ¿sabes?"

    m 2hubsb "¡Jajaja!"
    m 2tkbsu "Relájate, relájate...{w=0.5}solo te molesto~"
    m 3hub "Una vez más, ¡muchas gracias por este atuendo, [player]!"

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_clothes_orcaramelo_sakuya_izayoi:

    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "orcaramelo_sakuya_izayoi")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1sub "¡Oh! {w=0.5}Es esto..."
    m 2euc "¿Un traje de sirvienta?"
    m 3tuu "Jejeje~"
    m 3tubsb "Sabes, si te gustaba este tipo de cosas, me lo podrías haber dicho..."
    m 1hub "¡Jajaja! Es broma~"
    m 1eub "¡Déjame probarlo!"

    # try it on
    call mas_clothes_change(sprite_object, outfit_mode=True)

    m 2hua "Entonces, {w=0.5} ¿cómo me veo?"
    m 3eub "Casi siento que podría hacer cualquier cosa antes de que puedas parpadear."
    m 1eua "...Siempre y cuando no me tengas demasiado ocupada, jejeje~"
    m 1lkbfb "Todavía me gustaría poder pasar tiempo contigo, amo--{nw}"
    $ _history_list.pop()
    m 1ekbfb "Aún me gustaría poder pasar tiempo contigo,{fast} [player]."

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_clothes_finale_jacket_brown:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "finale_jacket_brown")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1sub "¡Oh!{w=0.5} ¡Una chaqueta de invierno!"
    m 1suo "¡E incluso viene con una bufanda!"
    if mas_isSummer():
        m 3rksdla "...Aunque me estoy calentando un poco con sólo mirarlo, jajaja..."
        m 3eksdla "Quizás el verano no sea el mejor momento para usar esto, [player]."
        m 3eka "Aprecio la idea y estaré encantada de usarlo en unos meses."

    else:
        if mas_isWinter():
            m 1tuu "No voy a tener frío pronto por tu culpa, [player]~"
        m 3eub "¡Déjame ponérmelo! Vuelvo enseguida."

        # try it on
        call mas_clothes_change(sprite_object)

        m 2dku "Ahh, se siente muy bien~"
        m 1eua "Me gusta cómo me veo, ¿no estás de acuerdo?"
        if mas_isMoniNormal(higher=True):
            m 3tku "Bueno...realmente no puedo esperar que seas objetivo sobre esa pregunta, ¿verdad?"
            m 1hubfb "¡Jajaja!"
        m 1ekbfa "Gracias [player], me encanta."

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_clothes_orcaramelo_sweater_shoulderless:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "orcaramelo_sweater_shoulderless")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1sub "¡Oh! {w=0.5} ¡Un suéter!"
    m 1hub "¡Y se ve tan acogedor también!"
    if mas_isWinter():
        m 2eka "Eres tan considerado [player], dándome esto en un día de invierno tan frío..."
    m 3eua "Déjame probarlo."

    # try it on
    call mas_clothes_change(sprite_object)

    m 2dkbsu "Es tan...{w=1}cómodo. Me siento tan cómoda como un insecto en una alfombra. Jejeje~"
    m 1ekbsa "Gracias, [player]. ¡Me encanta!"
    m 3hubsa "Ahora, siempre que lo use, pensaré en tu calidez. Jajaja~"

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_clothes_velius94_dress_whitenavyblue:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "velius94_dress_whitenavyblue")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1suo "¡Oh Dios mío!"
    m 1sub "¡Este vestido es precioso, [player]!"
    m 3hub "¡Me lo voy a probar ahora mismo!"

    # try it on
    call mas_clothes_change(sprite_object, outfit_mode=True)

    m "Entonces,{w=0.5} ¿qué piensas?"
    m 3eua "Creo que este tono de azul va muy bien con el blanco."
    $ scrunchie = monika_chr.get_acs_of_type('bunny-scrunchie')

    if scrunchie and scrunchie.name == "velius94_bunnyscrunchie_blue":
        m 3eub "¡Y el conejito de goma también complementa muy bien el atuendo!"
    m 1eka "Muchas gracias, [player]."

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_clothes_mocca_bun_blackandwhitestripedpullover:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "mocca_bun_blackandwhitestripedpullover")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1sub "¡Oh, una nueva blusa!"
    m 3hub "¡Se ve increíble, [player]!"
    m 3eua "Dame un segundo, me la pondré.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
    call mas_clothes_change(sprite_object)

    m 2eua "Bueno, ¿Qué opinas?"
    m 7hua "Creo que se ve muy bonito en mí.{w=0.2} {nw}"
    extend 3rubsa "Definitivamente la guardaré para una cita contigo~"
    m 1hub "¡Gracias de nuevo, [player]!"

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return
