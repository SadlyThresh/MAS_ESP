


init python:
    def dumpPersistentToFile(dumped_persistent,dumppath):
        """
        Prints a file containing each dictionary element of a persistent variable

        IN:
            dumped_persistent - a renpy persistent variable
            dumppath - a file path to the text file to be created. Must be a valid write location
        """
        dumped_persistent = vars(dumped_persistent)
        
        fo = open(dumppath, "w")
        
        for key in sorted(dumped_persistent.iterkeys()):
            fo.write(str(key) + ' - ' + str(type(dumped_persistent[key])) + ' >>> '+ str(dumped_persistent[key]) + '\n\n')
        
        fo.close()

label import_ddlc_persistent_in_settings:
    $ mas_RaiseShield_core()

    call import_ddlc_persistent from _call_import_ddlc_persistent_1

    if store.mas_globals.dlg_workflow:


        $ enable_esc()
        $ mas_MUINDropShield()
    else:


        $ mas_DropShield_core()
    return

label import_ddlc_persistent:
    python:

        from glob import glob


        if renpy.macintosh:
            rv = "~/Library/RenPy/"
            check_path = os.path.expanduser(rv)

        elif renpy.windows:
            if 'APPDATA' in os.environ:
                check_path =  os.environ['APPDATA'] + "/RenPy/"
            else:
                rv = "~/RenPy/"
                check_path = os.path.expanduser(rv)

        else:
            rv = "~/.renpy/"
            check_path = os.path.expanduser(rv)

        ddlc_save_path = glob(check_path + 'DDLC/persistent')
        if not ddlc_save_path:
            ddlc_save_path = glob(check_path + 'DDLC-*/persistent')

    $ quick_menu = False
    scene black
    with Dissolve(1.0)


    if ddlc_save_path:
        $ ddlc_save_path = ddlc_save_path[0]
        "Se encontraron datos guardados para Doki Doki Literature Club en [ddlc save_path]."
        menu:
            "¿Te gustaría importar los datos guardados del Doki Doki Literature Club en [config.name]?\n(DDLC no se verá afectado)"
            "Sí, importar datos guardados DDLC.":
                pause 0.3
                pass
            "No, no importar.":
                pause 0.3
                return
    else:


        "No se pudieron encontrar los datos guardados del Doki Doki Literature Club."
        menu:
            "Los datos guardados no se importarán en este momento."
            "Okay":
                pause 0.3
                return


    python:

        ddlc_pfile = file(ddlc_save_path, "rb")
        ddlc_persistent = mas_dockstat.cPickle.loads(ddlc_pfile.read().decode("zlib"))
        ddlc_pfile.close()


        renpy.call_in_new_context("vv_updates_topics") 
        ddlc_persistent = updateTopicIDs("v030", ddlc_persistent)
        ddlc_persistent = updateTopicIDs("v031", ddlc_persistent)
        ddlc_persistent = updateTopicIDs("v032", ddlc_persistent)
        ddlc_persistent = updateTopicIDs("v033", ddlc_persistent)
        clearUpdateStructs()


    if persistent.first_run:
        label import_ddlc_persistent.save_merge_or_replace:
        menu:
            "También se han encontrado los datos guardados de Monika After Story.\n¿Te gustaría fusionarlos con los datos guardados de DDLC?"
            "Fusionar datos guardados.":
                pass
            "Cancelar.":

                "Los datos DDLC se pueden importar más tarde en el menú de Ajustes."
                return


    python:
















































        def _updatePersistentDict(key, old_persistent, new_persistent):
            """
            Merges the old persistent dict at the key provided into the new persistent

            IN:
                key - key to update
                old_persistent - persistent to copy data from
                new_persistent - persistent to copy data to

            NOTE: Should only be used to update dicts
            """
            
            if old_persistent.__dict__[key] is not None:
                if new_persistent.__dict__[key] is not None:
                    new_persistent.__dict__[key].update(old_persistent.__dict__[key])
                
                else:
                    new_persistent.__dict__[key] = old_persistent.__dict__[key]

        def _updatePersistentBool(key, old_persistent, new_persistent):
            """
            Merges bools from the old persistent at the key provided into the new persistent

            IN:
                key - key to update
                old_persistent - persistent to copy data from
                new_persistent - persistent to copy data to

            NOTE: Should only be used to update bools
            """
            if old_persistent.__dict__[key] is not None:
                if new_persistent.__dict__[key] is not None:
                    new_persistent.__dict__[key] = new_persistent.__dict__[key] or old_persistent.__dict__[key]
                
                else:
                    new_persistent.__dict__[key] = old_persistent.__dict__[key]




        _updatePersistentDict("_seen_ever", ddlc_persistent, persistent)


        _updatePersistentDict("_seen_audio", ddlc_persistent, persistent)


        _updatePersistentDict("_seen_images", ddlc_persistent, persistent)


        _updatePersistentBool("clearall", ddlc_persistent, persistent)


        _updatePersistentBool("monika_kill", ddlc_persistent, persistent)


        _updatePersistentBool("tried_skip", ddlc_persistent, persistent)


        if ddlc_persistent.monika_reload is not None:
            if persistent.monika_reload is not None:
                persistent._mas_ddlc_reload_count = persistent.monika_reload + ddlc_persistent.monika_reload
            
            else:
                persistent._mas_ddlc_reload_count = ddlc_persistent.monika_reload


        if ddlc_persistent.clear is not None:
            if persistent.clear is not None:
                for index in range(len(persistent.clear)-1):
                    persistent.clear[index] = persistent.clear[index] or ddlc_persistent.clear[index]
            
            else:
                persistent.clear = ddlc_persistent.clear


        if ddlc_persistent.playername:
            if persistent.playername and persistent.playername != ddlc_persistent.playername:
                renpy.call_in_new_context("merge_unmatched_names")
            
            else:
                persistent.playername = ddlc_persistent.playername

        player = persistent.playername



        if ddlc_persistent.playthrough is not None:
            if (
                persistent.playthrough is not None
                and persistent.playthrough < ddlc_persistent.playthrough
            ):
                persistent.playthrough = ddlc_persistent.playthrough
            
            else:
                persistent.playthrough = ddlc_persistent.playthrough


        __mas__memoryCleanup()


        persistent.has_merged = True
    return

label merge_unmatched_names:
    menu:
        "Los nombres de los protagonistas no coinciden. ¿Cuál te gustaría conservar?"
        "[ddlc_persistent.playername]":
            $ persistent.playername = ddlc_persistent.playername
        "[persistent.playername]":
            $ persistent.playername
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
