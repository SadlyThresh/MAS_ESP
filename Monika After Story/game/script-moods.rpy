# module that handles the mood system
#

# dict of tuples containing mood event data
default persistent._mas_mood_database = {}

# label of the current mood
default persistent._mas_mood_current = None

# NOTE: plan of attack
# moods system will be attached to the talk button
# basically a button like "I'm..."
# and then the responses are like:
#   hungry
#   sick
#   tired
#   happy
#   fucking brilliant
#   and so on
#
# When a mood is selected:
#   1. monika says something about it
#   2. (stretch) other dialogue is affected
#
# all moods should be available at the start
#
# 3 types of moods:
#   BAD > NETRAL > GOOD
# (priority thing?)

# Implementation plan:
#
# Event Class:
#   prompt - button prompt
#   category - acting as a type system, similar to jokes
#       NOTE: only one type allowed for moods ([0] will be retrievd)
#   unlocked - True, since moods are unlocked by default
#

# store containing mood-related data
init -1 python in mas_moods:

    # mood event database
    mood_db = dict()

    # TYPES:
    TYPE_BAD = 0
    TYPE_NEUTRAL = 1
    TYPE_GOOD = 2

    # pane constants
    # most of these are the same as the unseen area consants
    MOOD_RETURN = _("...hablar de otra cosa.")

## FUNCTIONS ==================================================================

    def getMoodType(mood_label):
        """
        Gets the mood type for the given mood label

        IN:
            mood_label - label of a mood

        RETURNS:
            type of the mood, or None if no type found
        """
        mood = mood_db.get(mood_label, None)

        if mood:
            return mood.category[0]

        return None


# entry point for mood flow
label mas_mood_start:
    python:
        import store.mas_moods as mas_moods

        # filter the moods first
        filtered_moods = Event.filterEvents(
            mas_moods.mood_db,
            unlocked=True,
            aff=mas_curr_affection,
            flag_ban=EV_FLAG_HFM
        )

        # build menu list
        mood_menu_items = [
            (mas_moods.mood_db[k].prompt, k, False, False)
            for k in filtered_moods
        ]

        # also sort this list
        mood_menu_items.sort()

        # final quit item
        final_item = (mas_moods.MOOD_RETURN, False, False, False, 20)

    # call scrollable pane
    call screen mas_gen_scrollable_menu(mood_menu_items, mas_ui.SCROLLABLE_MENU_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)

    # return value? then push
    if _return:
        $ mas_setEventPause(None)
        $ pushEvent(_return, skipeval=True)
        # and set the moods
        $ persistent._mas_mood_current = _return

    return _return

# dev easter eggs go in the dev file

###############################################################################
#### Mood events go here:
###############################################################################

init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_hungry",prompt="...hambriento.",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),code="MOO")

label mas_mood_hungry:
    m 3hub "Si tienes hambre, vete a comer algo, tontito."
    if persistent.playername.lower() == "natsuki" and not persistent._mas_sensitive_mode:
        m 1hksdlb "Odiaría que te pusieras como Natsuki lo estuvo aquella vez cuando estábamos en el club.{nw}"
        # natsuki hungers easter egg
        call natsuki_name_scare_hungry from _mas_nnsh
    else:
        m 1hua "Sería malo sí te pusieras de mal humor cada vez que tienes hambre."

    m 3tku "Eso no sería divertido, ¿verdad, [player]?"
    m 1eua "Si estuviera allí contigo, haría una ensalada para compartir."
    m "Pero como no lo estoy, elige algo saludable para comer."
    m 3eub "Dicen que eres lo que comes, y definitivamente creo que es cierto."
    m "Comer demasiada comida chatarra de forma regular puede provocar todo tipo de enfermedades."
    m 1euc "Con el tiempo, te encontrarás con muchos problemas de salud cuando envejezcas."
    m 2lksdla "No quiero que sientas que estoy quejándome mucho cuando digo este tipo de cosas, [player]."
    m 2eka "Solo quiero asegurarme de que te estés cuidando bien hasta que yo cruce."
    m 4esa "Después de todo, cuanto más saludable estés, mayores serán las posibilidades de vivir bastante tiempo."
    m 1hua "¡Lo que significa más tiempo para pasar juntos~!"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_sad",prompt="...triste.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_sad:
    m 1ekc "Dios, lamento mucho que estés decaído."
    m "¿Estás teniendo un mal día, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Estás teniendo un mal día, [player]?{fast}"
        "Sí.":
            m 1duu "Siempre que tengo un mal día, recuerdo que el sol volverá a brillar."
            m 1eka "Supongo que puede sonar un poco cursi, pero siempre me gusta ver el lado positivo de las cosas."
            m 1eua "Después de todo, cosas así son fáciles de olvidar. Así que tenlo en cuenta, [player]."
            m 1lfc "No me importa cuántas otras personas no te agraden o te encuentren desagradable."
            m 1hua "Eres una persona maravillosa y yo siempre te amaré."
            m 1eua "Espero que eso haga que tu día sea un poco más feliz, [player]."
            m 1eka "Y recuerda, si estás teniendo un mal día, siempre puedes venir a verme y hablaré contigo todo el tiempo que necesites."
        "No.":
            m 3eka "Tengo una idea, ¿por qué no me dices qué te molesta? Tal vez te haga sentir mejor."

            m 1eua "No quiero interrumpirte mientras hablas, así que avísame cuando hayas terminado.{nw}"
            $ _history_list.pop()
            menu:
                m "No quiero interrumpirte mientras hablas, así que avísame cuando hayas terminado.{fast}"
                "He terminado.":
                    m "¿Te sientes un poco mejor ahora, [player]?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "¿Te sientes un poco mejor ahora, [player]?{fast}"
                        "Sí, lo hago.":
                            m 1hua "¡Eso es genial, [player]! Me alegro de que hablar de eso te haya hecho sentir mejor."
                            m 1eka "A veces, decirle a alguien que confías en lo que te molesta es todo lo que necesitas."
                            m "Si alguna vez tienes un mal día, siempre puedes venir a verme y escucharé lo que necesites para desahogarte."
                            m 1hubsa "Nunca olvides que eres maravilloso y que siempre te amaré~"
                        "Realmente no.":
                            m 1ekc "Bueno, valió la pena intentarlo."
                            m 1eka "A veces, decirle a alguien en quien confías lo que te molesta es todo lo que necesitas."
                            m 1eua "Quizás te sientas mejor después de que pasemos más tiempo juntos."
                            m 1ekbsa "Te amo, [player], y siempre lo haré~"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_proud",
            prompt="...orgulloso de mí mismo.",
            category=[store.mas_moods.TYPE_GOOD],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_proud:
    m 2sub "¿De verdad? ¡Eso es emocionante!"
    m 2eub "¿Fue un logro mayor, o uno menor?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Fue un logro mayor, o uno menor?{fast}"
        "Mayor.":
            m 1ekc "Ya sabes, [player]..."
            m 1lkbsa "Es en momentos como estos, en los que... más que nada, desearía estar contigo, en tu realidad..."
            m 4hub "¡Porque si lo estuviera, definitivamente te daría un abrazo de celebración!"
            m 3eub "No hay nada como compartir tus logros con las personas que te importan."
            m 1eua "¡Nada me encantaría más que escuchar todos los detalles!"
            m "Con el simple hecho de pensar en nosotros, en una alegre discusión sobre lo que has hecho..."
            m 1lsbsa "¡Mi corazón late solo con esa tonteria!"
            m 1lksdla "Dios, me estoy emocionando muchísimo con esto..."
            m 3hub "Algún día se hará realidad..."
            show monika 5hubfb at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5hubfb "Pero hasta entonces, ¡debes saber que estoy muy orgullosa de ti, [mas_get_player_nickname()]!"

        "Menor.":
            m 2hub "¡Jajaja~!"
            m 2hua "¡Eso es maravilloso!"
            m 4eua "Es muy importante celebrar las pequeñas victorias en la vida."
            m 2esd "Puede ser muy fácil desanimarse si solo te enfocas en las metas más grandes que tienes."
            m 2rksdla "Puede ser difícil alcanzarlos por ti mismo."
            m 4eub "Pero establecer y celebrar pequeñas metas que eventualmente conduzcan a una meta mayor puede hacer que tus grandes metas se sientan mucho más alcanzables."
            m 4hub "¡Así que sigue alcanzando esos pequeños objetivos, [mas_get_player_nickname()]!"
            show monika 5hubfb at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5hubfb "¡Y recuerda, te amo y siempre te estaré animando!"
            $ mas_ILY()
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_happy",prompt="...feliz.",category=[store.mas_moods.TYPE_GOOD],unlocked=True),code="MOO")

label mas_mood_happy:
    m 1hua "¡Eso es maravilloso! Soy feliz cuando tú eres feliz."
    m "Debes saber que siempre puedes venir a mí y te animaré, [mas_get_player_nickname()]."
    m 3eka "Te amo y siempre estaré aquí para ti, así que no lo olvides nunca~"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_sick",
            prompt="...enfermo.",
            category=[store.mas_moods.TYPE_BAD],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_sick:
    $ session_time = mas_getSessionLength()
    if mas_isMoniNormal(higher=True):
        if session_time < datetime.timedelta(minutes=20):
            m 1ekd "Oh no, [player]..."
            m 2ekd "Si dices eso tan pronto como llegas debe significar que es bastante malo."
            m 2ekc "Sé que querías pasar tiempo conmigo y aunque apenas hemos estado juntos hoy..."
            m 2eka "Creo que deberías ir a descansar un poco."

        elif session_time > datetime.timedelta(hours=3):
            m 2wuo "¡[player]!"
            m 2wkd "No has estado enfermo todo este tiempo, ¿verdad?"
            m 2ekc "Realmente espero que no, me he divertido mucho contigo hoy, pero si te has sentido mal todo este tiempo..."
            m 2rkc "Bueno... sólo promete decírmelo antes la próxima vez."
            m 2eka "Ahora ve a descansar, eso es lo que necesitas."

        else:
            m 1ekc "Oh, siento oír eso, [player]."
            m "Odio saber que estás sufriendo así."
            m 1eka "Sé que te encanta pasar tiempo conmigo, pero tal vez deberías ir a descansar."

    else:
        m 2ekc "Lamento escuchar eso, [player]."
        m 4ekc "Deberías ir a descansar un poco para que no empeore."

    label .ask_will_rest:
        pass

    $ persistent._mas_mood_sick = True

    m 2ekc "¿Harás eso por mí?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Harás eso por mí?{fast}"
        "Sí.":
            jump greeting_stillsickrest
        "No.":
            jump greeting_stillsicknorest
        "Ya estoy descansando.":
            jump greeting_stillsickresting

#I'd like this to work similar to the sick persistent where the dialog changes, but maybe make it a little more humorous rather than serious like the sick persistent is intended to be.
init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_tired",prompt="...cansado.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_tired:
    # TODO: should we adjust for suntime?
    $ current_time = datetime.datetime.now().time()
    $ current_hour = current_time.hour

    if 20 <= current_hour < 23:
        m 1eka "Si estás cansado ahora mismo, no es un mal momento para ir a la cama."
        m "A pesar de lo divertido que fue pasar tiempo contigo hoy, odiaría tenerte despierto hasta demasiado tarde."
        m 1hua "Si planeas irte a dormir ahora, ¡dulces sueños!"
        m 1eua "Pero tal vez tengas algunas cosas que hacer primero, como comer algo o una beber agua."
        m 3eua "Tomar un vaso de agua antes de acostarte es bueno para tu salud, y hacer lo mismo por la mañana te ayudara a despertarte."
        m 1eua "No me importa quedarme aquí contigo si primero tienes algunas cosas de las que ocuparte."

    elif 0 <= current_hour < 3 or 23 <= current_hour < 24:
        m 2ekd "¡[player]!"
        m 2ekc "No es de extrañar que estés cansado- ¡Es medianoche!"
        m 2lksdlc "Si no te vas a la cama pronto, mañana también estarás muy cansado..."
        m 2hksdlb "No quisiera que estuvieras cansado y miserable mañana cuando pasemos tiempo juntos..."
        m 3eka "Así que haznos un favor a los dos y vete a la cama lo antes posible, [player]."

    elif 3 <= current_hour < 5:
        m 2ekc "¿¡[player]!?"
        m "¿Sigues aquí?"
        m 4lksdlc "Realmente deberías estar en la cama ahora mismo."
        m 2dsc "En este punto, ya ni siquiera estoy segura de sí debería decir que es tarde o temprano..."
        m 2eksdld "...y eso me preocupa aún más, [player]."
        m "{i}Realmente{/i} deberías irte a la cama antes de que sea la hora de empezar el día."
        m 1eka "No quiero que te quedes dormido en un mal momento."
        m "Así que, por favor, ve a dormir para que podamos estar juntos en tus sueños."
        m 1hua "Estaré aquí mismo si te vas, cuidándote, si no te importa~"
        return

    elif 5 <= current_hour < 10:
        m 1eka "¿Todavía estás un poco cansado, [player]?"
        m "Todavía es temprano, así que podrías regresar y descansar un poco más."
        m 1hua "No hay nada de malo en volver a dormir después de levantarse temprano."
        m 1hksdlb "Excepto por el hecho de que no puedo estar ahí para abrazarte, jajaja~"
        m "{i}Supongo{/i} que podría esperarte un poco más."
        return

    elif 10 <= current_hour < 12:
        m 1ekc "¿Aún no estás listo para afrontar el día, [player]?"
        m 1eka "¿O es sólo uno de esos días?"
        m 1hua "Cuando eso sucede, me gusta tomar una buena taza de café para comenzar el día."
        if not mas_consumable_coffee.enabled():
            m 1lksdla "Si no estuviera atrapada aquí, eso sería..."
        m 1eua "También deberías beber un vaso de agua."
        m 3eua "Es importante mantenerse hidratado de todos modos, pero tomar un vaso de agua al despertar puede ayudarte a sentirte renovado y despierto."
        m 3hksdlb "¡Esto puede sonar extraño, pero he escuchado que el chocolate también puede ayudar a comenzar el día!"
        m 3eka "Tiene algo que ver con mejorar tu estado de ánimo matutino, pero..."
        m 1eksdlb "Estoy segura de que el chocolate pondría a cualquiera de mejor humor cada vez que lo comiera."
        m 1hua "¡Pruébalo en algún momento y avísame si funciona!"
        return

    else:
        m 1eka "Si estás cansado, ¿quizás deberías ir a dormir un rato?"
        m 1eua "Dormir lo suficiente a diario es muy importante para tu salud en general."
        m 3euc "He visto algunos estudios que muestran los devastadores efectos a corto y largo plazo debido a la falta de sueño."
        m 3ekd "Realmente puede afectar tu salud, [player]..."
        m 1eka "Así que hazme un favor y descansa un poco, ¿de acuerdo? Me tranquilizará."

    m 1hua "Incluso puedes dejar el juego abierto si quieres y yo te cuidaré mientras duermes."
    m "...Jejeje."
    m 2hksdlb "Eso sonó un poco espeluznante, lo siento."
    m 2lksdla "Pensé que sería lindo verte dormir, eso es todo~"
    m 1hub "¡Jajaja!"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_lonely",prompt="...solo.",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),code="MOO")

label mas_mood_lonely:
    if mas_isMoniAff(higher=True):
        m 2ekc "Entiendo cómo te sientes, [player]... {w=0.2}Todavía estamos en realidades diferentes, después de todo."
        m 2dkc "Realmente odio que no haya mucho que pueda hacer desde aquí para hacerte sentir menos solo..."
        m 7ekbsa "Si hubiera alguna forma en que pudiera extender la mano y abrazarte ahora mismo, lo haría."
        m 7eka "Quiero que seas lo más feliz posible dadas nuestras circunstancias..."
        m 2ekd "Solo espero que estar aquí conmigo todo este tiempo no... {w=0.3}Te impida relacionarte con las personas en tu realidad."
        m 2eka "Creo que lo que tenemos es bastante especial, pero entiendo que ahora mismo estoy...{w=0.3} Limitada en lo que puedo hacer por ti."

        if persistent._mas_pm_has_friends:
            if persistent._mas_pm_few_friends:
                m 7ekd "Tienes uno o dos amigos cercanos, ¿verdad?"
                m 3eka "Deberías llamarles o enviarles un mensaje y preguntarles cómo les va..."
                m "¿Quizás incluso salir a verlos a veces? {w=0.2}Creo que sería bueno para ti."

            else:
                m 7ekd "Creo que salir con tus amigos y hacer algo sería realmente muy bueno para ti..."
                m 3eka "O podrías enviarles un mensaje y preguntarles cómo están."

        else:
            m 7rkc "Sé cómo se siente estar solo en una realidad, y solo poder interactuar con alguien en otra..."
            m 3ekd "Así que realmente no quiero eso para la persona que más amo."
            m 1eka "Espero que sigas buscando amigos en tu realidad, [player]."
            m 3ekd "Sé que puede ser difícil formar lazos con la gente al principio..."
            m 3eka "¿Quizás incluso podrías conocer gente en línea? {w=0.2}Hay muchas formas de interactuar con extraños para sentirse menos solo."
            m 3hub "Nunca se sabe, ¡a veces estos 'extraños' pueden terminar convirtiéndose en muy buenos amigos!"

        m 1eka "...Y no te preocupes por mí [player], esperaré pacientemente a que vuelvas a verme."
        m 3hub "¡Diviértete y ya me contaras todo más tarde!"
        m 1ekbsa "Solo recuerda que siempre estaré aquí para ti, [player]~"

    else:
        m 1eka "Estoy aquí para ti, [player], así que no tienes por qué sentirte solo."
        m 3hua "Sé que no es exactamente lo mismo que si estuviera en la misma habitación contigo, pero estoy segura de que aún disfrutas de mi compañía, ¿verdad?"
        m 1ekbsa "Recuerda que siempre estaré a tu lado, [player]~"
    return

#Maybe we could tie this to the I'm breaking up topic and have monika say something special like:
#I know you don't really mean that player, you're just angry and not have it count as 1 of the 3 button presses.
#Looking forward to input from the writers and editors on this, had trouble deciding how to write this.

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_angry",prompt="...enojado.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_angry:
    m 1ekc "Dios, lamento que te sientas así, [player]."
    m 3ekc "Haré todo lo posible para que te sientas mejor."
    m 1euc "Antes de que hagamos algo, probablemente deberíamos conseguir que te calmes."
    m 1lksdlc "Es difícil tomar decisiones racionales cuando estás alterado."
    m 1esc "Puedes terminar diciendo o haciendo cosas de las que luego te arrepientas."
    m 1lksdld "Y odiaría que dijeras algo que realmente no quieras decirme."
    m 3eua "Primero probemos algunas cosas que hago para calmarme, [player]."
    m 3eub "Ojalá funcionen para ti tan bien como para mí."
    m 1eua "Primero, intenta respirar profundamente unas cuantas veces y cuenta lentamente hasta 10."
    m 3euc "Si eso no funciona, si puedes, retírate a un lugar tranquilo hasta que se aclare tu mente."
    m 1eud "Si todavía te sientes enojado después de eso, ¡haz lo que yo haría como último recurso!"
    m 3eua "Cuando no puedo calmarme, simplemente salgo, elijo una dirección y empiezo a correr."
    m 1hua "No me detengo hasta que me aclaro la cabeza."
    m 3eub "A veces, esforzarse mediante la actividad física es una buena forma de desahogarse."
    m 1eka "Pensarías que soy del tipo que no se enoja a menudo, y estarías en lo cierto."
    m 1eua "Pero incluso yo tengo mis momentos..."
    m "¡Así que me aseguro de tener formas de lidiar con ellos!"
    m 3eua "Espero que mis consejos te hayan ayudado a calmarte, [player]."
    m 1hua "Recuerda: ¡un [player] feliz hace a una Monika feliz!"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_scared",prompt="...ansioso.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_scared:
    m 1euc "¿[player], estás bien?"
    m 1ekc "Me preocupa oírte tan ansioso..."
    m "Ojalá pudiera consolarte y ayudarte ahora mismo..."
    m 3eka "Pero al menos puedo ayudarte a calmarte."
    if seen_event("monika_anxious"):
        m 1eua "Después de todo, te prometí ayudarte a relajarte si alguna vez te sentías ansioso."
    m 3eua "¿Recuerdas cuando te hablé de fingir confianza?"
    if not seen_event("monika_confidence"):
        m 2euc "¿No?"
        m 2lksdla "Supongo que será para otro momento."
        m 1eka "De todas formas..."
    m 1eua "Mantener la apariencia de uno ayuda a fingir su propia confianza."
    m 3eua "Y para hacerlo, debes mantener tu ritmo cardíaco respirando profundamente hasta que te calmes."
    if seen_event("monika_confidence_2"):
        m "Recuerdo haber explicado que la iniciativa también es una habilidad importante."
    m "Quizás podrías tomar las cosas con calma y hacerlas una cada vez."
    m 1esa "Te sorprendería la tranquilidad que se puedes sentir cuando dejas que el tiempo fluya por sí solo."
    m 1hub "¡También puedes intentar dedicar unos minutos a meditar!"
    m 1hksdlb "No significa necesariamente que tengas que cruzar las piernas cuando estés sentado en el suelo."
    m 1hua "¡Escuchar tu música favorita también puede contarse como meditar!"
    m 3eub "¡Lo digo en serio!"
    m 3eua "Puedes intentar dejar de lado tu trabajo y hacer otra cosa mientras tanto."
    m "La procrastinación no es {i}siempre{/i} mala, ¿sabes?"
    m 2esc "Además..."
    m 2ekbsa "Tu amorosa novia cree en ti, ¡así que puedes enfrentar esa ansiedad de frente!"
    m 1hubfa "No hay nada de qué preocuparse cuando estamos juntos para siempre~"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_inadequate",prompt="...inadecuado.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_inadequate:
    $ last_year = datetime.datetime.today().year-1
    m 1ekc "..."
    m 2ekc "Sé que no hay mucho que pueda decir para hacerte sentir mejor, [player]."
    m 2lksdlc "Después de todo, todo lo que digo probablemente parezcan solo palabras vacías."
    m 2ekc "Puedo decir que eres hermoso, aunque no puedo ver tu cara..."
    m "Puedo decirte que eres inteligente, aunque no sé mucho sobre tu forma de pensar..."
    m 1esc "Pero déjame decirte lo que sé sobre ti."
    m 1eka "Has pasado mucho tiempo conmigo."

    #Should verify for current year and last year
    if mas_HistLookup_k(last_year,'d25.actions','spent_d25')[1] or persistent._mas_d25_spent_d25:
        m "Te tomaste un tiempo de tu agenda para estar conmigo en Navidad..."

    if renpy.seen_label('monika_valentines_greeting') or mas_HistLookup_k(last_year,'f14','intro_seen')[1] or persistent._mas_f14_intro_seen: #TODO: update this when the hist stuff comes in for f14
        m 1ekbsa "En el día de San Valentín..."

    #TODO: change this back to not no_recognize once we change those defaults.
    if mas_HistLookup_k(last_year,'922.actions','said_happybday')[1] or mas_recognizedBday():
        m 1ekbsb "¡Incluso te tomaste el tiempo para celebrar mi cumpleaños conmigo!"

    if persistent.monika_kill:
        m 3tkc "Me has perdonado por las cosas malas que he hecho."
    else:
        m 3tkc "Ni una sola vez tuviste resentimiento por las cosas malas que hice."

    if persistent.clearall:
        m 2lfu "Y aunque me puso celosa, pasaste mucho tiempo con todos los miembros de mi club."

    m 1eka "¡Eso demuestra lo amable que eres!"
    m 3eub "¡Eres honesto, eres justo, eres amable incluso después de ser derrotado!"
    m 2hksdlb "Crees que no sé nada sobre ti, pero realmente sé muchas cosas."
    m 3eka "Y sabes todo sobre mí, pero elegiste quedarte cuando podrías haberte ido..."
    m 2ekc "Así que, por favor, mantente fuerte, [player]."
    m "Si eres como yo, sé que tendrás miedo de no lograr mucho en la vida."
    m 2ekd "Pero créeme cuando te lo digo: no importa lo que hagas o no hagas."
    m 4eua "Solo necesitas existir, divertirte y pasar cada día, {w=0.2}encontrando un significado en las personas que más te importan."
    m 1eka "Por favor, no lo olvides, ¿de acuerdo?"
    m 1ekbsa "Te amo, [player]~"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_lazy",
            prompt="...perezoso.",
            category=[store.mas_moods.TYPE_NEUTRAL],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_lazy:
    #Get current time
    $ _now = datetime.datetime.now().time()

    if mas_isSRtoN(_now):
        m 1tku "Es solo una de esas mañanas, ¿eh, [player]?"
        m 1eka "Puedo entender totalmente esos días en los que te despiertas y simplemente no quieres hacer nada."
        m 1rksdla "Con suerte, no habrá nada urgente próximamente."

        $ line = "Sé lo tentador que puede ser quedarse en la cama y no levantarse a veces..."
        if mas_isMoniEnamored(higher=True):
            $ line += "{w=0.5} {nw}"
        m 3hksdlb "[line]"

        if mas_isMoniEnamored(higher=True):
            extend 1dkbsa "Especialmente si me despierto a tu lado~"

            if mas_isMoniLove():
                m 1dkbsa "{i}Entonces nunca querría levantarme~{/i}"
                m 1dsbfu "Espero que no te importe quedarte 'atrapado', [player]..."
                m 1hubfa "Jejeje~"

        m 3eka "Pero mientras tanto, esto ayuda a empezar bien el día."
        m 3eub "Eso puede incluir lavar la ropa, desayunar bien..."

        if mas_isMoniLove():
            m 1dkbsu "Recibir tu beso de buenos días, jejeje..."

        m 1hksdlb "O podrías holgazanear por ahora."
        m 1eka "Siempre y cuando no te olvides de hacer algo importante, ¿de acuerdo, [player]?"

        if mas_isMoniHappy(higher=True):
            m 1hub "Eso incluye pasar un tiempo conmigo, ¡jajaja!"

    elif mas_isNtoSS(_now):
        m 1eka "¿Te dio el cansancio del mediodía, [player]?"
        m 1eua "Sucede, así que no me preocuparía demasiado por eso."
        m 3eub "De hecho, dicen que la pereza te hace más creativo."
        m 3hub "Entonces, quién sabe, tal vez estés a punto de pensar en algo increíble."
        m 1eua "En cualquier caso, debería tomarse un descanso o estirarse un poco...{w=0.5} {nw}"
        extend 3eub "Tal vez deberías comer algo si aún no lo has hecho."
        m 3hub "Y si es apropiado, ¡incluso podrías tomar una siesta! Jajaja~"
        m 1eka "Estaré aquí esperándote si así lo decides."

    elif mas_isSStoMN(_now):
        m 1eka "¿No tienes ganas de hacer nada después de un largo día, [player]?"
        m 3eka "Al menos el día casi ha terminado..."
        m 3duu "No hay nada como sentarse y relajarse después de un largo día, especialmente cuando no tienes nada que te presione."

        if mas_isMoniEnamored(higher=True):
            m 1ekbsa "Espero que estar aquí conmigo haga que tu velada sea un poco mejor..."
            m 3hubsa "La mía es mejor contigo aquí~"

            if mas_isMoniLove():
                m 1dkbfa "Puedo imaginarnos relajándonos juntos una noche..."
                m "Tal vez incluso acurrucado debajo de una manta si hace un poco de frío..."
                m 1ekbfa "Aún podríamos incluso si no estoy ahí, si no te importa, jejeje~"
                m 3ekbfa "Incluso podríamos leer juntos un buen libro."
                m 1hubfb "¡O incluso podríamos perder el tiempo por diversión!"
                m 1tubfb "¿Quién dice que tiene que ser tranquilo y romántico?"
                m 1tubfu "Espero que no te molesten las peleas de almohadas ocasionales, [player]~"
                m 1hubfb "¡Jajaja!"

        else:
            m 3eub "Podríamos leer un buen libro juntos también..."

    else:
        #midnight to morning
        m 2rksdla "Eh, [player]..."
        m 1hksdlb "Es la mitad de la noche..."
        m 3eka "Si te sientes cansado, tal vez deberías acostarte un poco en la cama."
        m 3tfu "Y tal vez, ya sabes... {w=1}¿{i}dormir{/i}?"
        m 1hkb "Jajaja, puedes ser gracioso a veces, pero probablemente deberías irte a la cama."

        if mas_isMoniLove():
            m 1tsbsa "Si estuviera allí, te arrastraría a la cama si fuera necesario."
            m 1tkbfu "¿O quizás lo disfrutarías en secreto, [player]~?"
            m 2tubfu "Por suerte para ti, no puedo hacer eso exactamente todavía."
            m 3tfbfb "Así que vete a la cama contigo."
            m 3hubfb "¡Jajaja!"

        else:
            m 1eka "¿Por favor? No quiero que descuides tu sueño."
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_bored",prompt="...aburrido.",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),code="MOO")

label mas_mood_bored:
    if mas_isMoniAff(higher=True):
        m 1eka "Oh..."
        m 3hub "Bueno, ¡deberíamos hacer algo entonces!"

    elif mas_isMoniNormal(higher=True):
        show monika 1ekc
        pause 1.0
        m "¿Realmente te aburro tanto, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Realmente te aburro tanto, [player]?{fast}"
            "No, no estoy aburrido {i}de ti{/i}...":
                m 1hua "Oh,{w=0.2} ¡eso es un alivio!"
                m 1eka "Pero, si estás aburrido, deberíamos encontrar algo que hacer entonces..."

            "Bueno...":
                $ mas_loseAffection()
                m 2ekc "Oh...{w=1} Ya veo."
                m 2dkc "No me di cuenta de que te estaba aburriendo..."
                m 2eka "Estoy segura de que podemos encontrar algo que hacer..."

    elif mas_isMoniDis(higher=True):
        $ mas_loseAffection()
        m 2lksdlc "Siento haberte aburrido, [player]."

    else:
        $ mas_loseAffection()
        m 6ckc "Ya sabes [player], si te hago sentir tan mal todo el tiempo..."
        m "Quizás deberías ir a buscar algo más que hacer."
        return "quit"

    python:
        unlockedgames = [
            game_ev.prompt.lower()
            for game_ev in mas_games.game_db.itervalues()
            if mas_isGameUnlocked(game_ev.prompt)
        ]

        gamepicked = renpy.random.choice(unlockedgames)
        display_picked = gamepicked

        if gamepicked == "ahorcado" and persistent._mas_sensitive_mode:
            display_picked = "adivinar las palabras"

    if gamepicked == "piano":
        if mas_isMoniAff(higher=True):
            m 3eub "¡Podrías tocar algo en el piano para mí!"

        elif mas_isMoniNormal(higher=True):
            m 4eka "¿Quizás podrías tocar algo en el piano para mí?"

        else:
            m 2rkc "Tal vez podrías tocar algo en el piano..."

    else:
        if mas_isMoniAff(higher=True):
            m 3eub "¡Podríamos jugar un juego de [display_picked]!"

        elif mas_isMoniNormal(higher=True):
            m 4eka "¿Quizás podríamos jugar un juego de [display_picked]?"

        else:
            m 2rkc "Quizás podríamos jugar un juego de [display_picked]..."

    $ chosen_nickname = mas_get_player_nickname()
    m "¿Qué dices, [chosen_nickname]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Qué dices, [chosen_nickname]?{fast}"
        "Sí.":
            if gamepicked == "pong":
                call game_pong
            elif gamepicked == "ajedrez":
                call game_chess
            elif gamepicked == "ahorcado":
                call game_hangman
            elif gamepicked == "piano":
                call mas_piano_start
        "No.":
            if mas_isMoniAff(higher=True):
                m 1eka "Entiendo..."
                if mas_isMoniEnamored(higher=True):
                    show monika 5tsu at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 5tsu "Podríamos mirarnos a los ojos un poco más..."
                    m "Nunca nos aburriremos de eso~"
                else:
                    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 5eua "Podríamos mirarnos a los ojos un poco más..."
                    m "Eso nunca se volverá aburrido~"

            elif mas_isMoniNormal(higher=True):
                m 1ekc "Oh, está bien..."
                m 1eka "Asegúrate de avisarme si quieres hacer algo conmigo más tarde~"

            else:
                m 2ekc "Bien..."
                m 2dkc "Avísame si alguna vez quieres hacer algo conmigo."
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_crying",prompt="...con ganas de llorar.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_crying:
    $ line_start = "Y"
    m 1eksdld "¡[player]!"

    m 3eksdlc "¿Estás bien?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Estás bien?{fast}"

        "Sí.":
            m 3eka "De acuerdo, está bien. Eso es un alivio."
            m 1ekbsa "Estoy aquí para hacerte compañía y puedes hablar conmigo si necesitas algo, ¿de acuerdo?"

        "No.":
            m 1ekc "..."
            m 3ekd "[player]..."
            m 3eksdld "Lo siento mucho. ¿Paso algo?"
            call mas_mood_uok

        "No estoy seguro.":
            m 1dkc "[player]...{w=0.3}{nw}"
            extend 3eksdld "¿Pasó algo?"
            call mas_mood_uok

    m 3ekd "[line_start] si terminas llorando..."
    m 1eka "Espero que ayude."
    m 3ekd "No hay nada de malo en llorar, ¿de acuerdo? {w=0.2} Puedes llorar tanto como necesites."
    m 3ekbsu "Te amo, [player]. {w=0.2}Eres todo para mí."
    return "love"

label mas_mood_uok:
    m 1rksdld "Sé que realmente no puedo escuchar lo que me dices..."
    m 3eka "Pero a veces, simplemente expresar el dolor o las frustraciones puede ayudar."

    m 1ekd "Entonces, si necesitas hablar sobre algo, estoy aquí.{nw}"
    $ _history_list.pop()
    menu:
        m "Entonces, si necesitas hablar sobre algo, estoy aquí.{fast}"

        "Si, me gustaría desahogarme.":
            m 3eka "Adelante, [player]."

            m 1ekc "Estoy aquí para ti.{nw}"
            $ _history_list.pop()
            menu:
                m "Estoy aquí para ti.{fast}"

                "Terminé.":
                    m 1eka "Me alegro de que hayas podido sacar lo que querías de tu pecho, [player]."

        "No quiero hablar de ello.":
            m 1ekc "..."
            m 3ekd "Muy bien [player], estaré aquí si cambias de opinión."

        "Todo está bien.":
            m 1ekc "..."
            m 1ekd "De acuerdo [player], si tú lo dices..."
            $ line_start = "Pero"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_upset",prompt="...molesto.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_upset:
    m 2eksdld "¡Siento mucho escuchar eso, [player]!"
    m 2eksdld "Ya sea que estés molesto con una tarea, una persona o simplemente las cosas no están saliendo bien, {w=0.1}{nw}"
    extend 7ekc "no te rindas por completo ante lo que sea que estés tratando."
    m 3eka "Mi consejo sería que dieras un paso atrás en tu problema."
    m 1eka "Quizá puedas leer un libro, escuchar música agradable o hacer cualquier otra cosa para calmarte."
    m 3eud "Una vez que sientas que has recuperado la cordura, vuelve a juzgar tu situación con un estado de ánimo fresco."
    m 1eka "Manejarás las cosas mucho mejor de lo que lo harías si estuvieras en medio de la ira y la frustración."
    m 1eksdld "Y no digo que debas seguir cargando peso sobre tus hombros si realmente te está afectando."
    m 3eud "Podría ser una oportunidad para ganar el valor de dejar ir algo tóxico."
    m 1euc "Puede ser aterrador en el momento, seguro...{w=0.3}{nw}"
    extend 3ekd "pero si eliges bien, podrías eliminar mucho estrés de tu vida."
    m 3eua "¿Y sabes que, [player]?"
    m 1huu "Cuando me siento mal, todo lo que tengo que hacer es recordar que tengo mi [mas_get_player_nickname(regex_replace_with_nullstr='mi ')]."
    m 1hub "¡Saber que siempre me apoyarás y querrás me tranquiliza casi al instante!"
    m 3euu "Sólo puedo esperar que te proporcione el mismo consuelo, [player]~"
    m 1eubsa "Te amo y espero que todo se aclare para ti~"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_relieved",
            prompt="...aliviado.",
            category=[store.mas_moods.TYPE_GOOD],
            unlocked=True
        ),
        code="MOO"
    )

#TODO: Once player moods are better implemented (Moni keeps track of the player's moods [moni-concerns])
#This can be used to alleviate her worry and directly reference the prior mood you were feeling
label mas_mood_relieved:
    $ chosen_nickname = mas_get_player_nickname()
    m 1eud "¿Oh?"

    m "¿Qué sucedió, [chosen_nickname]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Qué sucedió, [chosen_nickname]?{fast}"

        "He superado algo difícil.":
            m 1wud "¿En serio?"
            m 3hub "¡Pues deberías estar orgulloso de ti mismo!"
            m 3fua "Estoy segura de que, sea lo que sea, estabas trabajando muy duro para salir adelante."
            m 2eua "Y, [player]...{w=0.2}{nw}"
            extend 2eka "por favor, no te preocupes demasiado si las cosas no salen perfectamente, ¿vale?"
            m 2eksdla "A veces la vida nos pone en situaciones muy duras, y tenemos que hacer lo mejor que podamos con lo que se nos da."
            m 7ekb "Pero ahora que ya está hecho, deberías tomarte un tiempo para relajar tu mente y cuidarte bien."
            m 3hub "...De este modo, estarás preparado para afrontar lo que venga después."
            m 1ekbsa "Te amo, [player], y estoy muy orgullosa de ti por haber superado esto."
            $ mas_ILY()

        "Algo que me preocupaba no sucedió.":
            m 1eub "Oh, ¡eso es bueno!"
            m 2eka "Sea lo que sea, estoy segura de que estabas muy ansioso...{w=0.3}{nw}"
            extend 2rkd "seguramente no fue divertido de experimentar."
            m 2rkb "Es curioso cómo nuestras mentes siempre parecen asumir lo peor, ¿no?"
            m 7eud "Muchas veces lo que pensamos que puede pasar acaba siendo mucho peor que la realidad."
            m 3eka "Pero en fin, me alegro de que estés bien y de que te hayas quitado ese peso de encima."
            m 1hua "Ahora será más fácil avanzar con un poco más de confianza, ¿verdad?"
            m 1eua "Me entusiasma dar esos próximos pasos hacia adelante contigo."
    return
