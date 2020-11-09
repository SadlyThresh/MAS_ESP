





python early:


    def MASIslandBackground(**filter_pairs):
        """
        DynamicDisplayable for Island background images. This includes
        special handling to return None if island images could not be
        decoded.

        All Island images should use fallback handling and are built with that
        in mind.

        IN:
            **filter_pairs - filter pairs to MASFilterWeatherMap.

        RETURNS: DynamicDisplayable for Island images that respect filters and
            weather.
        """
        return MASFilterWeatherDisplayableCustom(
            _mas_islands_select,
            True,
            **filter_pairs
        )



image mas_islands_wf = MASIslandBackground(
    day=MASWeatherMap({
        mas_weather.PRECIP_TYPE_DEF: (
            "mod_assets/location/special/with_frame.png"
        ),
        mas_weather.PRECIP_TYPE_RAIN: (
            "mod_assets/location/special/rain_with_frame.png"
        ),
        mas_weather.PRECIP_TYPE_SNOW: (
            "mod_assets/location/special/snow_with_frame.png"
        ),
        mas_weather.PRECIP_TYPE_OVERCAST: (
            "mod_assets/location/special/overcast_with_frame.png"
        ),
    }),
    night=MASWeatherMap({
        mas_weather.PRECIP_TYPE_DEF: (
            "mod_assets/location/special/night_with_frame.png"
        ),
        mas_weather.PRECIP_TYPE_RAIN: (
            "mod_assets/location/special/night_rain_with_frame.png"
        ),
        mas_weather.PRECIP_TYPE_SNOW: (
            "mod_assets/location/special/night_snow_with_frame.png"
        ),
        mas_weather.PRECIP_TYPE_OVERCAST: (
            "mod_assets/location/special/night_overcast_with_frame.png"
        ),
    })
)
image mas_islands_wof = MASIslandBackground(
    day=MASWeatherMap({
        mas_weather.PRECIP_TYPE_DEF: (
            "mod_assets/location/special/without_frame.png"
        ),
        mas_weather.PRECIP_TYPE_RAIN: (
            "mod_assets/location/special/rain_without_frame.png"
        ),
        mas_weather.PRECIP_TYPE_SNOW: (
            "mod_assets/location/special/snow_without_frame.png"
        ),
        mas_weather.PRECIP_TYPE_OVERCAST: (
            "mod_assets/location/special/overcast_without_frame.png"
        ),
    }),
    night=MASWeatherMap({
        mas_weather.PRECIP_TYPE_DEF: (
            "mod_assets/location/special/night_without_frame.png"
        ),
        mas_weather.PRECIP_TYPE_RAIN: (
            "mod_assets/location/special/night_rain_without_frame.png"
        ),
        mas_weather.PRECIP_TYPE_SNOW: (
            "mod_assets/location/special/night_snow_without_frame.png"
        ),
        mas_weather.PRECIP_TYPE_OVERCAST: (
            "mod_assets/location/special/night_overcast_without_frame.png"
        ),
    })
)

init 2 python:



    mas_islands_snow_wf_mfwm = MASFilterWeatherMap(
        day=MASWeatherMap({
            mas_weather.PRECIP_TYPE_DEF: (
                "mod_assets/location/special/snow_with_frame.png"
            )
        }),
        night=MASWeatherMap({
            mas_weather.PRECIP_TYPE_DEF: (
                "mod_assets/location/special/night_snow_with_frame.png"
            )
        }),
    )
    mas_islands_snow_wof_mfwm = MASFilterWeatherMap(
        day=MASWeatherMap({
            mas_weather.PRECIP_TYPE_DEF: (
                "mod_assets/location/special/snow_without_frame.png"
            )
        }),
        night=MASWeatherMap({
            mas_weather.PRECIP_TYPE_DEF: (
                "mod_assets/location/special/night_snow_without_frame.png"
            )
        }),
    )

    mas_islands_snow_wf_mfwm.use_fb = True
    mas_islands_snow_wof_mfwm.use_fb = True



init -10 python:









    mas_cannot_decode_islands = not store.mas_island_event.decodeImages()


    def _mas_islands_select(st, at, mfwm):
        """
        Selection function to use in Island-based images

        IN:
            st - renpy related
            at - renpy related
            mfwm - MASFilterWeatherMap for this island

        RETURNS: displayable data
        """
        if mas_cannot_decode_islands:
            return "None", None
        
        
        return mas_fwm_select(st, at, mfwm)


init -11 python in mas_island_event:
    import store
    import store.mas_dockstat as mds
    import store.mas_ics as mis


    islands_station = store.MASDockingStation(mis.islands_folder)

    def decodeImages():
        """
        Attempts to decode the iamges

        Returns TRUE upon success, False otherwise
        """
        return mds.decodeImages(islands_station, mis.islands_map)


    def removeImages():
        """
        Removes the decoded images at the end of their lifecycle

        AKA quitting
        """
        mds.removeImages(islands_station, mis.islands_map)

    def isWinterWeather():
        """
        Checks if the weather on the islands is wintery

        OUT:
            boolean:
                - True if we're using snow islands
                - False otherwise
        """
        return store.mas_is_snowing or store.mas_isWinter()

    def isCloudyWeather():
        """
        Checks if the weather on the islands is cloudy

        OUT:
            boolean:
                - True if we're using overcast/rain islands
                - False otherwise
        """
        return store.mas_is_raining or store.mas_current_weather == store.mas_weather_overcast


init 4 python:

    if mas_isO31():
        
        mas_cannot_decode_islands = True
        store.mas_island_event.removeImages()


init 5 python:
    if not mas_cannot_decode_islands:
        addEvent(
            Event(
                persistent.event_database,
                eventlabel="mas_monika_islands",
                category=['monika','misc'],
                prompt="¿Puedes mostrarme las islas flotantes?",
                pool=True,
                unlocked=False,
                rules={"no_unlock": None, "bookmark_rule": store.mas_bookmarks_derand.WHITELIST},
                aff_range=(mas_aff.ENAMORED, None)
            )
        )

init -876 python in mas_delact:



    def _mas_monika_islands_unlock():
        return store.MASDelayedAction.makeWithLabel(
            2,
            "mas_monika_islands",
            (
                "not store.mas_cannot_decode_islands"
                " and mas_isMoniEnamored(higher=True)"
            ),
            store.EV_ACT_UNLOCK,
            store.MAS_FC_START
        )


label mas_monika_islands:
    m 1eub "Te dejaré admirar el paisaje por ahora."
    m 1hub "¡Espero que te guste!"


    $ mas_RaiseShield_core()
    $ mas_OVLHide()
    $ disable_esc()
    $ renpy.store.mas_hotkeys.no_window_hiding = True


    $ _mas_island_keep_going = True


    $ _mas_island_window_open = True


    $ _mas_toggle_frame_text = "Close Window"


    $ _mas_island_shimeji = False


    if renpy.random.randint(1,100) == 1:
        $ _mas_island_shimeji = True


    show screen mas_islands_background


    while _mas_island_keep_going:


        call screen mas_show_islands()

        if _return:

            call expression _return from _call_expression_1
        else:

            $ _mas_island_keep_going = False

    hide screen mas_islands_background


    $ mas_DropShield_core()
    $ mas_OVLShow()
    $ enable_esc()
    $ store.mas_hotkeys.no_window_hiding = False

    m 1eua "Espero que te haya gustado, [mas_get_player_nickname()]~"
    return

label mas_island_upsidedownisland:
    m "Oh, eso."
    m "Supongo que te estás preguntando por qué esa isla está al revés, ¿verdad?"
    m "Bueno... estaba a punto de arreglarla hasta que le di otro buen vistazo."
    m "Parece surrealista, ¿no?"
    m "Siento que hay algo especial con ella."
    m "Es simplemente...fascinante."
    return

label mas_island_glitchedmess:
    m "Oh, eso."
    m "Es algo en lo que estoy trabajando."
    m "Pero, sigue siendo un gran lío. Todavía estoy tratando de resolverlo."
    m "¡Pero a su debido tiempo, estoy segura de que mejoraré en la codificación!"
    m "Después de todo, la práctica hace al maestro, ¿verdad?"
    return

label mas_island_cherry_blossom_tree:
    python:

        if not renpy.store.seen_event("mas_island_cherry_blossom1"):
            
            renpy.call("mas_island_cherry_blossom1")

        else:
            _mas_cherry_blossom_events = [
                "mas_island_cherry_blossom1",
                "mas_island_cherry_blossom3",
                "mas_island_cherry_blossom4"
            ]
            
            if not mas_island_event.isWinterWeather():
                _mas_cherry_blossom_events.append("mas_island_cherry_blossom2")
            
            renpy.call(renpy.random.choice(_mas_cherry_blossom_events))

    return

label mas_island_cherry_blossom1:
    if mas_island_event.isWinterWeather():
        m "Este árbol puede parecer muerto ahora mismo... pero cuando florece, es hermoso."
    else:
        m "Es un árbol hermoso, ¿no?"
    m "Se llama árbol de Flor de Cerezo; son nativos de Japón."
    m "Tradicionalmente, cuando los árboles florecen, la gente va a ver las flores y hacer un picnic bajo los árboles."
    m "Bueno, no elegí este árbol por su tradición."
    m "Lo elegí porque es encantador y agradable de ver."
    m "Simplemente mirar los pétalos que caen es sobrecogedor."
    if mas_island_event.isWinterWeather():
        m "Cuando está floreciendo, claro."
        m "No puedo esperar hasta que tengamos la oportunidad de experimentar eso, [player]."
    return

label mas_island_cherry_blossom2:
    m "¿Sabías que puedes comer los pétalos de una flor de cerezo?"
    m "Yo no conozco el sabor, pero estoy segura de que no puede ser tan dulce como tú."
    m "Jejeje~"
    return

label mas_island_cherry_blossom3:
    m "Ya sabes, el árbol es simbólico como la vida misma."
    m "Hermoso, pero de corta duración."
    m "Pero contigo aquí, siempre está floreciendo."
    if mas_island_event.isWinterWeather():
        m "Incluso si está desnudo ahora, volverá a florecer pronto."
    m "Recuerda que siempre estaré agradecida contigo por estar en mi vida."
    m "Te amo, [player]~"

    $ mas_ILY()
    return

label mas_island_cherry_blossom4:
    m "¿Sabes qué sería bueno beber bajo los cerezos?"
    m "Un poco de sake~"
    m "¡Jajaja! Sólo bromeo."
    m "Prefiero tomar té o café."
    if mas_island_event.isWinterWeather():
        m "O incluso chocolate caliente. Ayudaría contra el frío."
        m "Por supuesto, incluso si eso fallara, siempre podríamos abrazarnos juntos...{w=0.5} Eso sería muy romántico~"
    else:
        m "Pero sería bueno ver cómo caen los pétalos contigo."
        m "Eso sería muy romántico~"
    return

label mas_island_sky:
    python:

        if mas_current_background.isFltDay():
            _mas_sky_events = [
                "mas_island_day1",
                "mas_island_day2",
                "mas_island_day3"
            ]

        else:
            _mas_sky_events = [
                "mas_island_night1",
                "mas_island_night2",
                "mas_island_night3"
            ]

        _mas_sky_events.append("mas_island_daynight1")
        _mas_sky_events.append("mas_island_daynight2")

        renpy.call(renpy.random.choice(_mas_sky_events))

    return

label mas_island_day1:


    if mas_island_event.isWinterWeather():
        m "Qué hermoso día es hoy."
        m "Perfecto para pasear y admirar el paisaje."
        m "...Acurrucados juntos, para evitar el frío."
        m "...Con unas buenas bebidas calientes para mantener el calor."
    elif mas_is_raining:
        m "Aww, me hubiera gustado leer un poco al aire libre."
        m "Pero prefiero evitar mojar mis libros..."
        m "Es difícil lidiar con las páginas empapadas."
        m "Tal vez en otro momento."
    elif mas_current_weather == mas_weather_overcast:
        m "Leer afuera con este clima no sería tan malo, pero podría llover en cualquier momento."
        m "Prefiero no arriesgarme."
        m "No te preocupes, [player]. Lo haremos en otro momento."
    else:
        m "Hoy es un buen día."
        m "Este clima sería bueno para leer un pequeño libro bajo los cerezos, ¿verdad, [player]?"
        m "Tumbados bajo la sombra mientras leo mi libro favorito."
        m "...Junto con un refrigerio y yu bebida favorita al lado."
        m "Ahh, sería muy bueno hacerlo~"
    return

label mas_island_day2:


    if mas_island_event.isWinterWeather():
        m "¿Alguna vez has hecho un ángel de nieve, [player]?"
        m "Lo intenté en el pasado, pero nunca tuve mucho éxito..."
        m "Es mucho más difícil de lo que parece."
        m "Apuesto a que nos divertiríamos mucho, incluso si lo que hacemos no termina pareciendo un ángel."
        m "Es solo cuestión de ser un poco tonto, ¿sabes?"
    elif mas_island_event.isCloudyWeather():
        m "Salir al aire libre con este tipo de clima no parece muy atractivo..."
        m "Quizás si tuviera un paraguas me sentiría más cómoda."
        m "Imagínanos, protegidos de la lluvia, a centímetros de distancia."
        m "Mirándonos a los ojos."
        m "Luego comenzamos a acercarnos más y más hasta que estamos casi-"
        m "Creo que puedes terminar ese pensamiento tú mismo, [player]~"
    else:
        m "El clima parece agradable."
        m "Definitivamente este sería el mejor momento para hacer un picnic."
        m "¡Incluso tenemos una gran vista para acompañarlo!"
        m "¿No sería genial?"
        m "Comer debajo de los cerezos."
        m "Admirando el paisaje que nos rodea."
        m "Disfrutando de la compañía del otro."
        m "Ahh, eso sería fantástico~"
    return

label mas_island_day3:
    if mas_is_raining and not mas_isWinter():
        m "Está lloviendo bastante..."
        m "No me gustaría estar afuera ahora."
        m "Aunque estar adentro en un momento como este se siente bastante cómodo, ¿no crees?"
    else:
        m "Es bastante tranquilo afuera."
        if mas_island_event.isWinterWeather():
            m "Podríamos tener una pelea de bolas de nieve."
            m "¡Jajaja, eso sería muy divertido!"
            m "Apuesto a que podría dispararte a unas pocas islas de distancia."
            m "Una competencia sana nunca lastimó a nadie, ¿verdad?"
        else:
            m "No me importaría holgazanear en la hierba ahora mismo..."
            m "Con tu cabeza apoyada en mi regazo..."
            m "Jejeje~"
    return

label mas_island_night1:
    m "Si bien es bueno ser productivo durante el día, hay algo tan tranquilo con la noche."
    m "El sonido del canto de los grillos mezclado con una suave brisa es muy relajante."
    m "Me abrazarías en una noche como esa, verdad~"
    return

label mas_island_night2:
    if not mas_isWinter() and mas_island_event.isCloudyWeather():
        m "Lástima que no podamos ver las estrellas esta noche..."
        m "Me hubiera encantado contemplar el cosmos contigo."
        m "Pero, está bien, lo veremos en otro momento."
    else:
        if seen_event('monika_stargazing'):
            m "¿No son las estrellas maravillosas, [player]?"
            m "Aunque, esto {i}no{/i} es lo que tenía en mente cuando mencioné sobre mirar las estrellas..."
            m "Por más agradable que sea mirarlas, la parte que más quiero experimentar es estar contigo, abrazándonos fuerte mientras estamos acostados."
            m "Algún día, [player].{w=0.3} Algún día."
        else:

            m "¿Alguna vez has ido a ver las estrellas, [mas_get_player_nickname()]?"
            m "Tomarse un tiempo de la noche para mirar el cielo nocturno y mirar la belleza del cielo..."
            m "Es sorprendentemente relajante, ¿sabías?"
            m "He descubierto que puede aliviar el estrés y despejar la mente..."
            m "Y ver todo tipo de constelaciones en el cielo te llena la mente de asombro."
            m "Por supuesto, te hace darte cuenta de lo pequeños que somos en el universo."
            m "Jajaja..."
    return

label mas_island_night3:
    if not mas_isWinter() and mas_island_event.isCloudyWeather():
        m "El cielo nublado es algo deprimente, ¿no lo crees?"
        m "Especialmente durante la noche, cuando oculta las estrellas de nuestra vista."
        m "De verdad, es una pena..."
    else:
        m "¡Qué hermosa noche!"
        if mas_island_event.isWinterWeather():
            m "Hay algo en una noche fría y fresca que me encanta."
            m "El contraste del cielo oscuro y la tierra cubierta de nieve es realmente impresionante, ¿no crees?"
        else:
            m "Si pudiera, agregaría luciérnagas."
            m "Sus luces complementan el cielo nocturno, es una hermosa vista."
            m "Mejora un poco el ambiente, ¿sabes?"
    return

label mas_island_daynight1:
    m "Quizás debería agregar más arbustos y árboles."
    m "Hacer las islas más bonitas, ¿sabes?"
    m "Solo tengo que encontrar las flores y el follaje adecuados."
    m "O tal vez cada isla debería tener su propio conjunto de plantas para que todo sea diferente y haya variedad."
    m "Me emociono pensando en eso~"
    return

label mas_island_daynight2:

    m "{i}~Molino de viento, molino de viento para la tierra~{/i}"


    m "{i}~Gira para siempre de la mano~{/i}"


    m "{i}~Toma todo con calma~{/i}"


    m "{i}~Está haciendo tictac, cayendo~{/i}"


    m "{i}~Amor por siempre, el amor es gratis~{/i}"


    m "{i}~Volvamos para siempre, tú y yo~{/i}"


    m "{i}~Molino de viento, molino de viento para la tierra~{/i}"

    m "Jejeje, no me hagas caso, solo quería cantar~"
    return

label mas_island_shimeji:
    m "¡Ah!"
    m "¿Cómo llegó allí?"
    m "Dame un segundo, [player]..."
    $ _mas_island_shimeji = False
    m "¡Todo listo!"
    m "No te preocupes, acabo de mudarlo a un lugar diferente."
    return

label mas_island_bookshelf:
    python:

        _mas_bookshelf_events = [
            "mas_island_bookshelf1",
            "mas_island_bookshelf2"
        ]

        renpy.call(renpy.random.choice(_mas_bookshelf_events))

    return

label mas_island_bookshelf1:


    if mas_island_event.isWinterWeather():
        m "Puede que esa estantería no parezca muy resistente, pero estoy segura de que puede resistir un poco de nieve."
        m "Son los libros los que me preocupan un poco."
        m "Solo espero que no se dañen demasiado..."
    elif mas_island_event.isCloudyWeather():
        m "En momentos como este, desearía haber mantenido mis libros en el interior..."
        m "Parece que tendremos que esperar a que mejore el tiempo para leerlos."
        m "Mientras tanto..."
        m "¿Qué tal abrazarnos un poco, [player]?"
        m "Jejeje~"
    else:
        m "Algunos de mis libros favoritos están ahí."
        m "{i}Fahrenheit 451{/i}, {i}El fin del mundo y un despiadado país de las maravillas{/i}, {i}1984{/i} y algunos otros."
        m "Quizás podamos leerlos juntos alguna vez~"
    return

label mas_island_bookshelf2:


    if mas_island_event.isWinterWeather():
        m "Sabes, no me importaría leer un poco afuera, incluso si hay un poco de nieve."
        m "Aunque no me aventuraría a salir sin un abrigo, una bufanda gruesa y un par de guantes."
        m "Supongo que pasar las páginas puede ser un poco difícil de esa manera, jajaja..."
        m "Pero estoy segura de que nos las arreglaremos de alguna manera."
        m "¿No es así, [player]?"
    elif mas_island_event.isCloudyWeather():
        m "Leer en interiores con la lluvia en la ventana es bastante relajante."
        m "Si tan solo no hubiera dejado los libros afuera..."
        m "Debería traer algunos aquí cuando tenga la oportunidad."
        m "Estoy segura de que podemos encontrar otras cosas que hacer mientras tanto, ¿verdad [player]?"
    else:
        m "Leer al aire libre es un buen cambio de ritmo, ¿sabes?"
        m "Tomaría una brisa fresca sobre una biblioteca cerrada cualquier día."
        m "Tal vez debería agregar una mesa debajo de los cerezos."
        m "Sería bueno disfrutar de una taza de café y algunos bocadillos para acompañar mi lectura."
        m "Eso sería maravilloso~"
    return




init 500 python in mas_island_event:
    def getBackground():
        """
        Because of the dead cherry blossom, we keep the snowy islands during all of winter

        Picks the islands bg to use based on the season.

        RETURNS: image to use as a displayable. (or image path)
        """
        if store.mas_isWinter():
            if store._mas_island_window_open:
                return store.mas_islands_snow_wof_mfwm.fw_get(
                    store.mas_sprites.get_filter()
                )
            
            return store.mas_islands_snow_wf_mfwm.fw_get(
                store.mas_sprites.get_filter()
            )
        
        if store._mas_island_window_open:
            return "mas_islands_wof"
        
        return "mas_islands_wf"


screen mas_islands_background:

    add mas_island_event.getBackground()












    if _mas_island_shimeji:
        add "gui/poemgame/m_sticker_1.png" at moni_sticker_mid:
            xpos 935
            ypos 395
            zoom 0.5

screen mas_show_islands():
    style_prefix "island"
    imagemap:

        ground mas_island_event.getBackground()


















        hotspot (11, 13, 314, 270) action Return("mas_island_upsidedownisland")
        hotspot (403, 7, 868, 158) action Return("mas_island_sky")
        hotspot (699, 347, 170, 163) action Return("mas_island_glitchedmess")
        hotspot (622, 269, 360, 78) action Return("mas_island_cherry_blossom_tree")
        hotspot (716, 164, 205, 105) action Return("mas_island_cherry_blossom_tree")
        hotspot (872, 444, 50, 30) action Return("mas_island_bookshelf")

        if _mas_island_shimeji:
            hotspot (935, 395, 30, 80) action Return("mas_island_shimeji")

    if _mas_island_shimeji:
        add "gui/poemgame/m_sticker_1.png" at moni_sticker_mid:
            xpos 935
            ypos 395
            zoom 0.5

    hbox:
        yalign 0.98
        xalign 0.96
        textbutton _mas_toggle_frame_text action [ToggleVariable("_mas_island_window_open"),ToggleVariable("_mas_toggle_frame_text","Open Window", "Close Window") ]
        textbutton "Go Back" action Return(False)





style island_button is default:
    properties gui.button_properties("island_button")
    idle_background "mod_assets/island_idle_background.png"
    hover_background "mod_assets/island_hover_background.png"
    xysize (205, None)
    ypadding 5
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style island_button_dark is default:
    properties gui.button_properties("island_button_dark")
    idle_background "mod_assets/island_idle_background_d.png"
    hover_background "mod_assets/island_hover_background_d.png"
    xysize (205, None)
    ypadding 5
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style island_button_text is default:
    properties gui.button_text_properties("island_button")
    idle_background "mod_assets/island_idle_background.png"
    hover_background "mod_assets/island_hover_background.png"
    font gui.default_font
    size gui.text_size
    xalign 0.5
    idle_color mas_ui.light_button_text_idle_color
    hover_color mas_ui.light_button_text_hover_color
    kerning 0.2
    outlines []

style island_button_text_dark is default:
    properties gui.button_text_properties("island_button_dark")
    idle_background "mod_assets/island_idle_background_d.png"
    hover_background "mod_assets/island_hover_background_d.png"
    font gui.default_font
    size gui.text_size
    xalign 0.5
    idle_color mas_ui.dark_button_text_idle_color
    hover_color mas_ui.dark_button_text_hover_color
    kerning 0.2
    outlines []


transform moni_sticker_mid:
    block:
        function randomPauseMonika
        parallel:
            sticker_move_n
        repeat
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
