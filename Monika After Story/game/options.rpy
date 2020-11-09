define config.default_language = "Spanish"
define config.language ="Spanish"






init -999:




    define config.name = "Monika After Story"


    define config.version = "0.11.6"




define gui.show_name = False




define gui.about = _("")






define build.name = "Monika_After_Story"






define config.has_sound = True
define config.has_music = True
define config.has_voice = False













define config.main_menu_music = audio.t1










define config.enter_transition = Dissolve(.2)
define config.exit_transition = Dissolve(.2)




define config.after_load_transition = None




define config.end_game_transition = Dissolve(.5)
















define config.window = "auto"




define config.window_show_transition = dissolve_textbox
define config.window_hide_transition = dissolve_textbox







default preferences.text_cps = 50





default preferences.afm_time = 15

default preferences.music_volume = 0.75
default preferences.sfx_volume = 0.75
















define config.save_directory = "Monika After Story"







define config.window_icon = "gui/window_icon.png"



define config.allow_skipping = True
define config.has_autosave = False
define config.autosave_on_quit = False
define config.autosave_slots = 0
define config.layers = [ 'master', 'transient', 'screens', 'overlay', 'front' ]
define config.image_cache_size = 64
define config.debug_image_cache = config.developer
define config.predict_statements = 5
define config.rollback_enabled = config.developer
define config.menu_clear_layers = ["front"]
define config.gl_test_image = "white"
define config.label_overrides = {
    "_choose_renderer": "mas_choose_renderer_override"
}


init python:
    if len(renpy.loadsave.location.locations) > 1: del(renpy.loadsave.location.locations[1])
    renpy.game.preferences.pad_enabled = False
    def replace_text(s):
        s = s.replace('--', u'\u2014') 
        s = s.replace(' - ', u'\u2014') 
        return s
    config.replace_text = replace_text

    def game_menu_check():
        if quick_menu: renpy.call_in_new_context('_game_menu')

    config.game_menu_action = game_menu_check

    def force_integer_multiplier(width, height):
        if float(width) / float(height) < float(config.screen_width) / float(config.screen_height):
            return (width, float(width) / (float(config.screen_width) / float(config.screen_height)))
        else:
            return (float(height) * (float(config.screen_width) / float(config.screen_height)), height)







init python:



























    build.include_update = True





    build.classify("game/gui/**",build.name)


    build.classify("game/mod_assets/**",build.name)

    build.classify("game/*.rpyc",build.name) 
    build.classify("game/dev/*.*",None) 
    build.classify("README.html",build.name) 
    build.classify("game/python-packages/**",build.name)
    build.classify("CustomIcon**.**",build.name)


    build.package(build.directory_name + "Mod",'zip',build.name,description='DDLC Compatible Mod')

    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)
    build.classify('**.rpy', None)
    build.classify('**.psd', None)
    build.classify('**.sublime-project', None)
    build.classify('**.sublime-workspace', None)
    build.classify('/music/*.*', None)
    build.classify('script-regex.txt', None)
    build.classify('/game/10', None)
    build.classify('/game/cache/*.*', None)
    build.classify('**.rpa',None)




    build.documentation('*.html')
    build.documentation('*.txt')
    build.documentation('*.md')

    build.include_old_themes = False
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
