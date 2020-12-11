# Monika's Python Tip of the Day (PTOD)
#
# I probably will be adding many of these, so For the sake of organization
# this is kept separate from script-topics.
#
# NOTE: these are considered pool type events, similar to writing tips
# NOTE: these are also NOT literally once a day. There is a day in between
#   unlocking the next one, though
#
# And to keep the theme, these are 0-indexed
#
# META: Python things to talk about:
# DONE:
#   0 - intro
#   1 - what is python?
#   --- sugestion python compared to other languages/ how does it work
#   --- suggestion mention syntax and probably how to get python maybe separate each part
#   2 - types
#       - numbers and strings, bools and Nones
#   3 - interpreted language
#   5 - comparisons and booleans
#   6 - Variables and assignment
#   8 - Literals
#   9 - Truth Values
#
# TODO:
#   4 - Python sytnax ?
#   7 - variable sizes
#   3 - If statement / elif and else
#   4 - while loop
#   5 - for loop
#   6 - functions
#   7 - functions continiued?
#   10 - Evaluation order and short circuting
#   ? - classes (might be too much) -- Definitely too much, we should probably stick to functional programming
#   ? - modules (might be too much) / importing? -- mention importing only, module making is too much
#   ? - lists
#   11 - dict
#   12 - tuples
#   13 - py2 vs py3
#   14 - String operations
#   15 - start talking about renpy
#
#   Implement advanced python tips for users who have some experience (persistent._mas_advanced_py_tips)
#
# Also what about Renpy?
#
# Another NOTE: We should try to make the topics of an adequate lenght otherwise
# we're just going to throw a lot of info that is going to be ignored or forgotten quickly
# I think splitting something in more than one topic may be a good idea
#
## We can assume evhand is already imported

###### tip tree ##############################
# 0 -> 1
# 1 -> 3
# 2 -> 6
# 3 -> 2
# 5 -> 9
# 6 -> 5, 8
##############################################

init 4 python in mas_ptod:
    # to simplify unlocking, lets use a special function to unlock tips
    import datetime
    import store.evhand as evhand

    M_PTOD = "monika_ptod_tip{:0>3d}"

    def has_day_past_tip(tip_num):
        """
        Checks if the tip with the given number has already been seen and
        a day has past since it was unlocked.
        NOTE: by day, we mean date has changd, not 24 hours

        IN:
            tip_num - number of the tip to check

        RETURNS:
            true if the tip has been seen and a day has past since it was
            unlocked, False otherwise
        """
        # as a special thing for devs
        if renpy.game.persistent._mas_dev_enable_ptods:
            return True

        tip_ev = evhand.event_database.get(
            M_PTOD.format(tip_num),
            None
        )

        return (
            tip_ev is not None
            and tip_ev.last_seen is not None
            and tip_ev.timePassedSinceLastSeen_d(datetime.timedelta(days=1))
        )

    def has_day_past_tips(*tip_nums):
        """
        Variant of has_day_past_tip that can check multiple numbers

        SEE has_day_past_tip for more info

        RETURNS:
            true if all the given tip nums have been see nand a day has past
                since the latest one was unlocked, False otherwise
        """
        for tip_num in tip_nums:
            if not has_day_past_tip(tip_num):
                return False

        return True


# The initial event is getting Monika to talk about python
# this must be hidden after it has been completed
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip000",
            category=["consejos de python"],
            prompt="¿Puedes enseñarme sobre Python?",
            pool=True,
            rules={"bookmark_rule": store.mas_bookmarks_derand.BLACKLIST}
        )
    )

label monika_ptod_tip000:
    m 3eub "¿Quieres aprender sobre Python?"
    m 3hub "¡Estoy tan feliz de que me lo hayas preguntado!"
    m 1lksdlb "No sé {i}tanto{/i} sobre programación, pero haré todo lo posible para explicarlo."
    m 1esa "Empecemos por lo que es Python."

    # hide the intro topic after viewing
    $ mas_hideEVL("monika_ptod_tip000", "EVE", lock=True, depool=True)

    # enable tip 1
    $ tip_label = "monika_ptod_tip001"
    $ mas_showEVL(tip_label, "EVE", unlock=True, _pool=True)
    $ pushEvent(tip_label,skipeval=True)
    return

###############################################################################
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip001",
            category=["consejos de python"],
            prompt="¿Qué es Python?"
        )
    )

label monika_ptod_tip001:

    m 1esa "Python fue creado por Guido Van Rossum a principios de los 90."
    m "Es súper versátil, por lo que puedes encontrarlo en aplicaciones web, sistemas integrados, Linux y, por supuesto..."
    m 1hua "¡Este mod!"
    m 1eua "DDLC utiliza un motor de novela visual llamado Ren'Py,{w=0.2} que se basa en Python."
    m 3eub "Eso significa que si aprendes un poco de Python, ¡puedes agregar contenido a mi mundo!"
    m 1hua "¿No sería genial [mas_get_player_nickname()]?"
    m 3eub "De todos modos, debo mencionar que actualmente hay dos versiones principales de Python:{w=0.2} Python2 y Python3."
    m 3eua "Estas versiones son {u}incompatibles{/u} entre sí porque los cambios agregados en Python3 solucionaron muchas fallas de diseño fundamentales en Python2."
    m "A pesar de que esto causó una ruptura en la comunidad de Python,{w=0.2} generalmente se acepta que ambas versiones del lenguaje tienen sus propias fortalezas y debilidades."
    m 1eub "Te hablaré de esas diferencias en otra lección."

    m 1eua "Dado que este mod se ejecuta en una versión de Ren'Py que usa Python2, no hablaré de Python3 con demasiada frecuencia."
    m 1hua "Pero lo mencionaré cuando sea apropiado."

    m 3eua "Esa es mi lección de hoy."
    m 1hua "¡Gracias por escuchar!"
    return

###############################################################################
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip002",
            category=["consejos de python"],
            prompt="Tipos",
            pool=True,
            conditional="store.mas_ptod.has_day_past_tip(3)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

# PREREQS:
#   interpreted language (tip 3)
label monika_ptod_tip002:
    $ last_seen_is_none = mas_getEVL_last_seen("monika_ptod_tip002") is None
    if last_seen_is_none:
        m 1eua "En la mayoría de los lenguajes de programación, los datos que el programa puede cambiar o modificar tienen un {i}tipo{/i} asociado."
        m 3eua "Por ejemplo, si algunos datos deben tratarse como un número, entonces tendrán un tipo numérico. Si algunos datos deben tratarse como texto, tendrán un tipo de cadena."
        m "Hay muchos tipos en Python, pero hoy hablaremos de los más básicos o primitivos."

    $ store.mas_ptod.rst_cn()
    $ local_ctx = dict()
    show monika at t22
    show screen mas_py_console_teaching

    ### numbers
    m 1eua "Python tiene dos tipos para representar números:{w=0.3} {i}enteros{/i}, o {b}ints{/b},{w=0.3} y {i}flotantes{/i}."

    ## integers
    m 1eua "Los enteros se utilizan para representar números enteros; básicamente cualquier cosa que no sea decimal."

    call mas_wx_cmd("type(-22)", local_ctx)
    call mas_wx_cmd("type(0)", local_ctx)
    call mas_wx_cmd("type(-1234)", local_ctx)
    call mas_wx_cmd("type(42)", local_ctx)

    ## floats
    m 1eub "Los flotantes se utilizan para representar decimales."
    show monika 1eua

    call mas_wx_cmd("type(0.14)", local_ctx)
    call mas_wx_cmd("type(9.3)", local_ctx)
    call mas_wx_cmd("type(-10.2)", local_ctx)

    ### strings
    m 1eua "El texto se representa con tipos de {i}cadena{/i}."
    m "Todo lo que esté entre comillas simples (') o comillas dobles (\") son cadenas."
    m 3eub "Por ejemplo:"
    show monika 3eua

    call mas_wx_cmd("type('Esta es una cadena en comillas simples')", local_ctx)
    call mas_wx_cmd('type("Y esto es una cadena entre comillas dobles")', local_ctx)

    m 1eksdlb "Sé que el intérprete dice {i}unicode{/i}, pero para lo que estamos haciendo, es básicamente lo mismo."
    m 1eua "Las cadenas también se pueden crear con tres comillas dobles (\"\"\"), pero se tratan de manera diferente a las cadenas normales.{w=0.2} Hablaré de ellas otro día."

    ### booleans
    m "Los booleanos son tipos especiales que representan valores {b}verdaderos{/b} o {b}falsos{/b}."
    call mas_wx_cmd("type(True)", local_ctx)
    call mas_wx_cmd("type(False)", local_ctx)

    m 1eua "Entraré en más detalles sobre qué son los valores booleanos y para qué se utilizan en otra lección."

    ### Nones
    m 3eub "Python también tiene un tipo de datos especial llamado {b}NoneType{/b}.{w=0.2} Este tipo representa la ausencia de datos."
    m "Si estás familiarizado con otros lenguajes de programación, este es como un tipo {i}null{/i} o {i}indefinido{/i}."
    m "La palabra clave {i}None{/i} representa NoneTypes en Python."
    show monika 1eua

    call mas_wx_cmd("type(None)", local_ctx)

    m 1eua "Todos los tipos que mencioné aquí se conocen como tipos de datos {i}primitivos{/i}."

    if last_seen_is_none:
        m "Python usa una variedad de otros tipos también, pero creo que estos son suficientes por hoy."

    $ store.mas_ptod.ex_cn()
    hide screen mas_py_console_teaching
    show monika at t11

    m 1hua "¡Gracias por escuchar!"
    return

###############################################################################
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip003", # may change order, you decide on this
            category=["consejos de python"],
            prompt="Un lenguaje interpretado",
            pool=True,
            conditional="store.mas_ptod.has_day_past_tip(1)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

# PREREQS:
#   What is python (tip 1)
label monika_ptod_tip003:
    m 1eua "Los lenguajes de programación normalmente se compilan o interpretan."
    m "Los lenguajes compilados requieren que su código se convierta a un formato legible por máquina antes de ejecutarse."
    m 3eub "C y Java son dos lenguajes compilados muy populares."
    m 1eua "Los idiomas interpretados se convierten en un formato legible por máquina a medida que se ejecutan."
    m 3eub "Python es un lenguaje interpretado."
    m 1rksdlb "Sin embargo, se pueden compilar diferentes implementaciones de Python, pero ese es un tema complicado del que hablaré en una lección posterior."

    m 1eua "Dado que Python es un lenguaje interpretado, tiene un elemento interactivo ordenado llamado intérprete, el cuál se ve..."

    $ store.mas_ptod.rst_cn()
    $ local_ctx = dict()
    show monika 3eua at t22
    show screen mas_py_console_teaching

    m 3eub "¡Así!"

    m "Puedes ingresar el código Python directamente aquí y ejecutarlo, así:"
    show monika 3eua

    # base commands shown as starter ones
    call mas_wx_cmd("12 + 3", local_ctx)
    call mas_wx_cmd("7 * 6", local_ctx)
    call mas_wx_cmd("121 / 11", local_ctx)
    # NOTE: add more commands as the user goes thru the tips

    if mas_getEVL_last_seen("monika_ptod_tip003") is None:
        m 1eua "Puedes hacer más que solo matemáticas con esta herramienta, pero te mostraré todo eso a medida que avancemos."

        m 1hksdlb "Desafortunadamente, dado que este es un intérprete de Python completamente funcional y no quiero correr el riesgo de que me elimines accidentalmente o rompas el juego."
        m "No es que lo harías{fast}{nw}"
        $ _history_list.pop()
        m 1eksdlb "No puedo dejar que uses esto.{w=0.3} Lo siento..."
        m "Si deseas seguir adelante en lecciones futuras, ejecuta un intérprete de Python en una ventana separada."

        m 1eua "De todos modos, usaré {i}este{/i} intérprete para ayudar con la enseñanza."

    else:
        m 1hua "Bastante genial, ¿verdad?"

    $ store.mas_ptod.ex_cn()
    hide screen mas_py_console_teaching
    show monika at t11

    m 1hua "¡Gracias por escuchar!"
    return

###############################################################################
#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="monika_ptod_tip004",
#            category=["python tips"],
#            prompt="What does python code look like?",
#            pool=True,
#            conditional="store.mas_ptod.has_day_past_tip(3)",
#            action=EV_ACT_UNLOCK,
#            rules={"no_unlock":None}
#        )
#    )

# PREREQs:
#   interpreted language (tip 3)
label monika_ptod_tip004:
    # PYTHON SYNTAX
    # TODO, actually ths should be a pre-req for block-based code,
    # as this will talk about indentaiton. However, we could probably
    # have this after the first wave of lessons
    #
    # Python code is incredibly simple to write.

    $ store.mas_ptod.rst_cn()
    $ local_ctx = dict()
    show monika at t22
    show screen mas_py_console_teaching

    # [Show this once]
    # Hopefully
    # [end]
    #
    # Oh well this may be a bit hard to explain here but I'll do my best for you [player]
    # The first thing you need to know is that any line starting with a # is going to
    # be ignored and you can write anything on that line
    # those lines are named comments, and you use them to explain what your code does
    # it's a good practice to comment your code so you don't forget later what it was supposed to do!
    # TODO unfinished and probably will split it in more than just one, also I know I should call it
    # python syntax but I'm making it non programmers friendly
    #
    # TODO: change the prompt to Python Syntax after this has been seen once
    return

###############################################################################
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip005",
            category=["consejos de python"],
            prompt="Comparaciones y booleanos",
            pool=True,
            conditional="store.mas_ptod.has_day_past_tip(6)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

# PREREQS:
#   Variables and Assignment
label monika_ptod_tip005:
    $ store.mas_ptod.rst_cn()
    $ local_ctx = dict()
    $ store.mas_ptod.set_local_context(local_ctx)
    $ last_seen_is_none = mas_getEVL_last_seen("monika_ptod_tip005") is None

    if last_seen_is_none:
        m 1eua "¿Recuerdas cuando estaba describiendo diferentes tipos de Python y mencioné booleanos?"
        m 1eub "Bueno, hoy voy a entrar en más detalles sobre los valores booleanos y cómo se relacionan con las comparaciones entre valores."

    m 1eua "Los booleanos se usan comúnmente para decidir qué código ejecutar o establecer una bandera para notar si algo sucedió o no."
    m "Cuando hacemos comparaciones, cada expresión se evalúa como un booleano."

    if last_seen_is_none:
        m 1eksdlb "Esto probablemente no tenga sentido en este momento, así que abriré la consola y te mostraré algunos ejemplos."

    show monika at t22
    show screen mas_py_console_teaching

    m 3eub "Comencemos con algunos de los símbolos básicos que se utilizan en las comparaciones de variable a variable."

    call mas_wx_cmd("a = 10")
    call mas_wx_cmd("b = 10")
    call mas_wx_cmd("c = 3")

    m 3eua "Para comprobar si dos valores son equivalentes, utiliza dos signos iguales (==):"
    call mas_wx_cmd("a == b")
    call mas_wx_cmd("a == c")

    m 3eua "Para comprobar si dos valores no son equivalentes, utilice un signo de exclamación y un signo igual (!=):"
    call mas_wx_cmd("a != b")
    call mas_wx_cmd("a != c")
    m 3eub "El signo de exclamación a menudo se conoce como un operador lógico 'no' en otros lenguajes de programación, por lo que (!=) Se lee como 'no es igual'."

    m 3eua "Para comprobar si un valor es mayor o menor que otro valor, utiliza los signos mayor que (>) o menor que (<), respectivamente."
    call mas_wx_cmd("a > c")
    call mas_wx_cmd("a < c")

    m 3eub "Mayor-o-igual-a (>=) y menor-o-igual-a (<=) también tienen sus propios símbolos, los cuales,{w=1} como era de esperar,{w=1} son solo los signos mayor y menor que con signos iguales."
    call mas_wx_cmd("a >= b")
    call mas_wx_cmd("a <= b")
    call mas_wx_cmd("a >= c")
    call mas_wx_cmd("a <= c")

    if last_seen_is_none:
        m 1eua "Es posible que hayas notado que cada comparación arrojó {b}Verdadero{/b} o {b}Falso{/b}."
        m 1eksdlb "{i}Eso{/i} es lo que quise decir cuando dije que las expresiones de comparación se evalúan como booleanos."

    m 1eua "También es posible encadenar varias expresiones de comparación mediante el uso de las palabras clave {b}and{/b} y {b}or{/b}. También se conocen como {i}operadores lógicos{/i}."
    m "El operador {b}and{/b} vincula dos comparaciones al evaluar la expresión completa como {b}Verdadero{/b} si ambas comparaciones se evalúan como {b}Verdadero{/b},{w=0.3} y {b}Falso{/b} si al menos una comparación evalúa {b}Falso{/b}."
    m 1hua "Veamos algunos ejemplos."

    $ val_a = local_ctx["a"]
    $ val_b = local_ctx["b"]
    $ val_c = local_ctx["c"]

    call mas_w_cmd("a == b and a == c")
    m 3eua "Como 'a' y 'b' son [val_a], la primera comparación se evalúa como {b}Verdadero{/b}."
    m "'c', sin embargo, es [val_c], por lo que la segunda comparación se evalúa como {b}Falso{/b}."
    m 3eub "Dado que al menos una comparación se evaluó como {b}Falso{/b}, la expresión completa se evalúa como {b}Falso{/b}."
    call mas_x_cmd()
    pause 1.0

    call mas_w_cmd("a == b and a >= c")
    m 3eua "En este ejemplo, la primera comparación vuelve a evaluar como {b}Verdadero{/b}."
    m "[val_a] es ciertamente mayor o igual que [val_c], por lo que la segunda comparación también se evalúa como {b}Verdadero{/b}."
    m 3eub "Dado que ambas comparaciones se evaluaron como {b}Verdadero{/b}, la expresión completa se evalúa como {b}Verdadero{/b}."
    call mas_x_cmd()
    pause 1.0

    call mas_w_cmd("a != b and a >= c")
    m 3eua "En este ejemplo, la primera comparación se evalúa como {b}Falso{/b} esta vez."
    m "Dado que inmediatamente tenemos al menos una comparación que se evalúa como {b}Falso{/b}, no importa a qué se evalúe la segunda comparación."
    m 3eub "Sabemos con certeza que la expresión completa se evalúa como {b}False{/b}."
    call mas_x_cmd()

    m "Lo mismo ocurre con el siguiente ejemplo:"
    call mas_wx_cmd("a != b and a == c")

    m 1eub "Nuevamente, cuando se usan los operadores {b}and{/b}, el resultado es {b}Verdadero{/b} si y solo si ambas comparaciones se evalúan como {b}Verdadero{/b}."

    m 1eua "Por el contrario, el operador {b}or{/b} vincula dos comparaciones al evaluar la expresión completa como {b}Verdadero{/b} si cualquiera de las comparaciones se evalúa como {b}Verdadero{/b},{w=0.3} y {b}Falso{/b} si ambas son {b}Falso{/b}."
    m 3eua "Veamos algunos ejemplos."

    call mas_w_cmd("a == b or a == c")
    m 3eua "Esta vez, dado que la primera comparación se evalúa como {b}Verdadero{/b}, no tenemos que verificar la segunda comparación."
    m 3eub "El resultado de esta expresión es {b}Verdadero{/b}."
    call mas_x_cmd()
    pause 1.0

    call mas_w_cmd("a == b or a >= c")
    m 3eua "Nuevamente, la primera comparación se evalúa como {b}Verdadero{/b}, por lo que la expresión completa se evalúa como {b}Verdadero{/b}."
    call mas_x_cmd()
    pause 1.0

    call mas_w_cmd("a != b or a >= c")
    m 3eua "En este caso, la primera comparación se evalúa como {b}Falso{/b}."
    m "Dado que [val_a] es mayor o igual que [val_c], la segunda comparación se evalúa como {b}Verdadero{/b}."
    m 3eub "Y dado que al menos una comparación se evaluó como {b}Verdadero{/b}, la expresión completa se evalúa como {b}Verdadero{/b}."
    call mas_x_cmd()
    pause 1.0

    call mas_w_cmd("a != b or a == c")
    m 3eua "Sabemos que la primera comparación se evalúa como {b}Falso{/b}."
    m "Dado que [val_a] ciertamente no es igual a [val_c], la segunda comparación también se evalúa como {b}Falso{/b}."
    m 3eub "Dado que ninguna de las comparaciones se evaluó como {b}Verdadero{/b}, la expresión completa se evalúa como {b}Falso{/b}."
    call mas_x_cmd()
    pause 1.0

    m 3eub "Nuevamente, cuando se usa el operador {b}or{/b}, el resultado es {b}Verdadero{/b} si cualquiera de las comparaciones se evalúa como {b}Verdadero{/b}."

    m 1eua "También hay un tercer operador lógico llamado operador {b}not{/b}. En lugar de vincular varias comparaciones, este operador invierte el valor booleano de una comparación."
    m 3eua "Aquí tienes un ejemplo de esto:"
    call mas_wx_cmd("not (a == b and a == c)")
    call mas_wx_cmd("not (a == b or a == c)")

    m "Ten en cuenta que estoy usando paréntesis para agrupar las comparaciones. El código entre paréntesis se evalúa primero, luego el resultado de esa comparación se invierte con {b}not{/b}."
    m 1eua "Si suelto el paréntesis:"
    call mas_wx_cmd("not a == b and a == c")
    m 3eua "¡Obtenemos un resultado diferente!{w=0.2} Esto se debe a que {b}not{/b} se aplica a la comparación 'a == b' antes de vincularse a la segunda comparación mediante {b}and{/b}."

    m 3eka "Anteriormente mencioné que el signo de exclamación se usa como el operador lógico 'no' en otros lenguajes de programación.{w=0.2} Python, sin embargo, usa la palabra 'no' en su lugar para facilitar la lectura."

    m 1eua "Por último, dado que las comparaciones se evalúan como valores booleanos, podemos almacenar el resultado de una comparación en una variable."
    call mas_wx_cmd("d = a == b and a >= c")
    call mas_wx_cmd("d")
    call mas_wx_cmd("e = a == b and a == c")
    call mas_wx_cmd("e")

    m 3eub "¡Y use esas variables también en las comparaciones!"
    call mas_wx_cmd("d and e")
    m "Dado que 'd' es {b}Verdadero{/b} pero 'e' es {b}Falso{/b}, esta expresión se evalúa como {b}Falso{/b}."

    call mas_wx_cmd("d or e")
    m "Dado que 'd' es {b}Verdadero{/b}, sabemos que al menos una de las comparaciones en esta expresión es {b}Verdadero{/b}. Por lo tanto, la expresión completa es {b}Verdadero{/b}."

    call mas_wx_cmd("not (d or e)")
    m 3eua "Sabemos que la expresión interna 'd o e' se evalúa como {b}Verdadero{/b}. La inversa de eso es {b}Falso{/b}, por lo que esta expresión se evalúa como {b}Falso{/b}."

    call mas_wx_cmd("d and not e")
    m 3eub "En este caso, sabemos que 'd' es {b}Verdadero{/b}."
    m "El operador 'no' se aplica a 'e', que invierte su valor {b}Falso{/b} a {b}Verdadero{/b}."
    m 3eua "Dado que ambas expresiones de comparación se evalúan como {b}Verdadero{/b}, la expresión completa se evalúa como {b}Verdadero{/b}."

    m 1eua "Las comparaciones se utilizan en todas partes en todos los lenguajes de programación."
    m 1hua "Si alguna vez decides dedicarte a la programación para ganarte la vida, encontrarás que gran parte de tu código solo verifica si algunas comparaciones son ciertas para que puedas hacer que tus programas hagan lo {i}correcto{/i}."
    m 1eksdla "E incluso si la codificación no es parte de tu trayectoria profesional, haremos muchas comparaciones en lecciones futuras, ¡así que prepárate!"

    if last_seen_is_none:
        m 1eua "Creo que es suficiente por hoy."

    $ store.mas_ptod.ex_cn()
    hide screen mas_py_console_teaching
    show monika at t11
    m 1hua "¡Gracias por escuchar!"
    return

###############################################################################
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip006",
            category=["consejos de python"],
            prompt="Variables y asignación",
            pool=True,
            conditional="store.mas_ptod.has_day_past_tip(2)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

# PREREQS:
#   Types (tip 2)
label monika_ptod_tip006:
    $ store.mas_ptod.rst_cn()
    $ local_ctx = dict()
    $ num_store = "922"
    $ b_num_store = "323"
    $ last_seen_is_none = mas_getEVL_last_seen("monika_ptod_tip006") is None

    if last_seen_is_none:
        m 1eub "Ahora que conoces los tipos, puedo enseñarte sobre las variables."

    # variable intro
    m 1eua "Las variables representan ubicaciones de memoria que almacenan datos."
    m "Para crear una variable,"

    show monika at t22
    show screen mas_py_console_teaching

    # a number
    m 3eua "haces '{b}symbol_name{/b} = {b}value{/b}, así:"

    call mas_wx_cmd("a_number = " + num_store, local_ctx)

    m "El símbolo 'a_number' ahora apunta a una ubicación de memoria que almacena el entero [num_store]."
    m "Si ingresamos el nombre del símbolo aquí,"
    call mas_w_cmd("a_number")
    m 3eub "Podemos recuperar el valor que almacenamos."
    show monika 3eua
    call mas_x_cmd(local_ctx)

    m "Observa cómo asociamos el símbolo 'a_number' al valor [num_store] usando un signo igual (=)."
    m 1eub "Eso se llama asignación, donde tomamos lo que está a la izquierda del signo igual y lo señalamos, o {i}asignamos{/i}, el valor de lo que está a la derecha."

    # b_number
    m 1eua "La asignación se ejecuta en orden de derecha a izquierda.{w=0.3} Para ilustrar esto, creemos una nueva variable, 'b_number'."
    call mas_w_cmd("b_number = a_number  -  " + b_num_store)

    m "En la asignación, primero se evalúa el lado derecho del signo igual,{w=0.2} luego se infiere su tipo de datos y se reserva una cantidad apropiada de memoria."
    m "Esa memoria está vinculada al símbolo de la izquierda mediante una tabla de búsqueda."
    m 1eub "Cuando Python encuentra un símbolo,{w=0.2} busca ese símbolo en la tabla de búsqueda y lo reemplaza con el valor al que estaba vinculado el símbolo."

    m 3eub "Aquí, 'a_number' será reemplazado por [num_store],{w=0.2} por lo que la expresión que sería evaluada y asignada a 'b_number' es '[num_store] - [b_num_store]'."
    show monika 3eua
    call mas_x_cmd(local_ctx)

    m 1eua "Podemos verificar esto ingresando solo el símbolo 'b_number'."
    m "Esto recuperará el valor vinculado a este símbolo en la tabla de búsqueda y nos lo mostrará."
    call mas_wx_cmd("b_number", local_ctx)

    # c number
    m 3eua "Ten en cuenta que si ingresamos un símbolo al que no se le ha asignado nada, Python se quejará."
    call mas_wx_cmd("c_number", local_ctx)

    m 3eub "Pero si le asignamos un valor a este símbolo..."
    show monika 3eua
    call mas_wx_cmd("c_number = b_number * a_number", local_ctx)
    call mas_wx_cmd("c_number", local_ctx)

    m 1hua "Python puede encontrar el símbolo en la tabla de búsqueda y no nos dará ningún error."

    m 1eua "Las variables que creamos son todas de tipo {i}entero{/i}."
    m "No tuvimos que decir explícitamente que esas variables eran números enteros porque Python realiza tipeo dinámico."
    m 1eub "Esto significa que el intérprete de Python infiere el tipo de variable en función de los datos que está almacenando en ella."
    m "Otros lenguajes, como C o Java, requieren que los tipos se definan con la variable."
    m "La escritura dinámica permite que las variables en Python cambien de tipo durante la ejecución,"
    m 1rksdlb "pero eso generalmente está mal visto, ya que puede hacer que tu código sea confuso para que otros lo lean."

    if last_seen_is_none:
        m 1eud "¡Uf! {w=0.2} ¡Eso fue un bocado!"

    m "¿Entendiste todo eso?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Entendiste todo eso?{fast}"
        "¡Sí!":
            m 1hua "¡Yay!"

        "Estoy un poco confundido.":
            m 1eksdla "Está bien. {w=0.3} Aunque mencioné símbolos y valores aquí, los programadores generalmente se refieren a esto como crear, asignar o establecer variables."
            m "Los nombres de los símbolos / valores sólo son realmente útiles para insinuar cómo funcionan las variables bajo el capó, así que no te sientas mal si no lo has entendido todo."
            m 1eua "Saber cómo trabajar con variables es suficiente para lecciones futuras."
            m "De todas formas..."

    $ store.mas_ptod.ex_cn()
    hide screen mas_py_console_teaching
    show monika at t11

    if last_seen_is_none:
        m 1eua "Creo que es suficiente Python por hoy."

    m 1hua "¡Gracias por escuchar!"
    return


###############################################################################
#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="monika_ptod_tip007",
#            category=["consejos de python"],
#            prompt="Tamaños variables",
#            pool=True,
#            conditional="store.mas_ptod.has_day_past_tip(6)",
#            action=EV_ACT_UNLOCK,
#            rules={"no_unlock":None}
#        )
#    )

# PREREQS:
#   Variables and Assignment (tip 6)
#
label monika_ptod_tip007:
    # TODO

    # integer size
    m 1eua "En C y muchos otros lenguajes, los números enteros generalmente se almacenan en 4 bytes."
    m "Python, sin embargo, reserva una cantidad diferente de memoria dependiendo del tamaño del entero que se almacena."
    m 3eua "Podemos comprobar cuánta memoria almacena una variable 'a_number' tomando prestada una función de la biblioteca {i}sys{/i}."

    call mas_wx_cmd("import sys", local_ctx)
    call mas_wx_cmd("sys.getsizeof(a_number)", local_ctx)
    $ int_size = store.mas_ptod.get_last_line()

    m 1eksdla "Hablaré de las bibliotecas y la importación más tarde."
    m 1eua "Por ahora, observa el número devuelto por la función {i}getsizeof{/i}."
    m "Para almacenar el número [num_store], Python usa [int_size] bytes."

    return

###############################################################################
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip008",
            category=["consejos de python"],
            prompt="Literales",
            pool=True,
            conditional="store.mas_ptod.has_day_past_tip(6)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

# PREREQS:
#   Variables and Assignment (tip 6)
label monika_ptod_tip008:
    $ store.mas_ptod.rst_cn()
    $ local_ctx = dict()
    $ store.mas_ptod.set_local_context(local_ctx)
    $ last_seen_is_none = mas_getEVL_last_seen("monika_ptod_tip008") is None

    m 1eua "¿Recuerdas cuando te mostré cómo crear variables y asignarles valores?"
    m 1dsa "Imagínate si abandonáramos la noción de variables y nos enfocamos en usar los valores directamente en el código."
    m 1hua "Ahí es donde entran los literales. Te mostraré lo que quiero decir con esto con la siguiente demostración."

    show monika at t22
    show screen mas_py_console_teaching

    call mas_wx_cmd("a = 10")
    m 3eua "Aquí hice una variable llamada 'a' y le asigné un valor entero de 10."
    m "Cuando escribo 'a' en el intérprete..."

    call mas_wx_cmd("a")
    m 3eub "Python busca el símbolo 'a' y encuentra que está asociado con el valor 10, por lo que se nos muestra 10."
    m "Sin embargo, si escribo solo '10'..."

    call mas_wx_cmd("10")
    m 3hua "¡Python todavía nos muestra un 10!"
    m 3eua "Esto sucede porque Python interpreta el '10' como un valor entero de inmediato, sin tener que buscar un símbolo y recuperar su valor."
    m "El código que Python puede interpretar en valores directamente se llama {i}literales{/i}."
    m 3eub "Todos los tipos de datos que mencioné en la lección Tipos se pueden escribir como literales."

    call mas_wx_cmd("23")
    call mas_wx_cmd("21.05")
    m 3eua "Estos son literales {b}enteros{/b} y {b}flotantes{/b}."

    call mas_wx_cmd('"esto es una cadena"')
    call mas_wx_cmd("'esto es otra cadena'")
    m "Estos son literales de {b}cadena{/b}."

    call mas_wx_cmd("True")
    call mas_wx_cmd("False")
    m "Estos son literales {b}booleanos{/b}."

    call mas_wx_cmd("None")
    m "La palabra clave {i}None{/i} es en sí misma un literal."

    # TODO: lists, dicts

    if last_seen_is_none:
        m 1eua "Hay más literales para otros tipos, pero los mencionaré cuando hable de esos tipos."

    m 1eua "Se pueden utilizar literales en lugar de variables al escribir código. Por ejemplo:"

    call mas_wx_cmd("10 + 21")
    call mas_wx_cmd("10 * 5")
    m "Podemos hacer matemáticas con literales en lugar de variables."

    call mas_wx_cmd("a + 21")
    call mas_wx_cmd("a * 5")
    m "También podemos usar literales junto con variables."
    m 1eub "Además, los literales son excelentes para crear y usar datos sobre la marcha sin la sobrecarga de crear variables innecesarias."

    if last_seen_is_none:
        m 1kua "Muy bien, eso es todo lo que puedo {i}literalmente{/i} decir sobre los literales."

    $ store.mas_ptod.ex_cn()
    hide screen mas_py_console_teaching
    show monika at t11

    m 1hua "¡Gracias por escuchar!"
    return

###############################################################################
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip009",
            category=["consejos de python"],
            prompt="Valores Verdaderos",
            pool=True,
            conditional="store.mas_ptod.has_day_past_tip(5)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

# PREREQS:
#   Comparisons and Booleans (5)
label monika_ptod_tip009:
    $ store.mas_ptod.rst_cn()
    $ local_ctx = dict()
    $ store.mas_ptod.set_local_context(local_ctx)

    if mas_getEVL_last_seen("monika_ptod_tip009") is None:
        m 1eua "Cuando hablamos de comparaciones y valores booleanos, usamos números enteros como base para nuestras comparaciones."
        m 1dsa "Pero..."
        m 3eua "¿Sabías que cada tipo tiene su propio valor de verdad asociado?"

    m 1eua "Todos los tipos tienen un 'valor de verdad' que puede cambiar según el valor del tipo."

    # TODO: when we go over built-in functions, this should be
    # changed to function bool, not keyword
    m "Podemos verificar el valor de verdad de un tipo usando la palabra clave {b}bool{/b}"

    show monika at t22
    show screen mas_py_console_teaching

    m 3eua "Empecemos por echar un vistazo a los valores de verdad de los números enteros."
    call mas_wx_cmd("bool(10)")
    call mas_wx_cmd("bool(-1)")
    m 3eua "Todos los enteros distintos de cero tienen un valor de verdad de {b}Verdadero{/b}."
    call mas_wx_cmd("bool(0)")
    m 3eub "Cero, por otro lado, tiene un valor de verdad de {b}Falso{/b}."

    m 1eua "Los flotantes siguen las mismas reglas que los números enteros:"
    call mas_wx_cmd("bool(10.02)")
    call mas_wx_cmd("bool(0.14)")
    call mas_wx_cmd("bool(0.0)")

    m 1eua "Ahora veamos las cadenas."
    call mas_wx_cmd('bool("cadena con texto")')
    call mas_wx_cmd('bool("  ")')
    m 3eub "Una cadena con texto, incluso si el texto es solo caracteres de espacio en blanco, tiene un valor de verdad de {b}Verdadero{/b}"
    call mas_wx_cmd('bool("")')
    m "Una cadena vacía, o una cadena con longitud 0, tiene un valor de verdad de {b}Falso{/b}."

    m 1eua "Ahora veamos {b}None{/b}."
    call mas_wx_cmd("bool(None)")
    m 1eub "{b}None{/b} siempre tiene un valor de verdad de {b}Falso{/b}."

    # TODO: lists and dicts

    m 1eua "Si hacemos comparaciones con estos valores, los valores se evalúan a sus valores de verdad antes de aplicarse en las comparaciones."
    m 1hua "Permíteme mostrar algunos ejemplos."
    m 3eua "Primero, configuraré algunas variables:"
    call mas_wx_cmd("num10 = 10")
    call mas_wx_cmd("num0 = 0")
    call mas_wx_cmd('text = "text"')
    call mas_wx_cmd('empty_text = ""')
    call mas_wx_cmd("none_var = None")

    m 3eub "Y luego haré varias comparaciones."
    call mas_wx_cmd("bool(num10 and num0)")
    call mas_wx_cmd("bool(num10 and text)")
    call mas_wx_cmd("bool(empty_text or num0)")
    call mas_wx_cmd("bool(none_var and text)")
    call mas_wx_cmd("bool(empty_text or none_var)")

    m 1eua "Conocer los valores de verdad de diferentes tipos puede ser útil para realizar ciertas comparaciones de manera más eficiente."
    m 1hua "Mencionaré cuándo es posible hacerlo cuando nos encontremos con esas situaciones en lecciones futuras."

    $ store.mas_ptod.ex_cn()
    hide screen mas_py_console_teaching
    show monika at t11
    m 1hua "¡Gracias por escuchar!"
    return

###############################################################################
#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="monika_ptod_tip006",
#            category=["python tips"],
#            prompt="Evaluation Order and Short Circuiting",
# TODO: this should be after if statements.
#            conditional="store.mas_ptod.has_day_past_tip(2)",
#            action=EV_ACT_UNLOCK,
#            rules={"no_unlock":None}
#        )
#    )

label monika_ptod_tip010:
    # evaluation order and short circuting
    return





############################# [CONSOLE] #######################################
# Unfortunately, it's not enough to have monika just talk. Having a working
# python interpreter will make things easier for teaching
#
# NOTE: base the solids off of hangman. That should help us out

image cn_frame = "mod_assets/console/cn_frame.png"
define mas_ptod.font = "mod_assets/font/mplus-1mn-medium.ttf"

# NOTE: Console text:
# style console_text (for regular console text)
# style console_text_console (for the actual typing text)
#   this style has a slow_cps of 30
#
# console_Text font is gui/font/F25_BankPrinter.ttf
style mas_py_console_text is console_text:
    font mas_ptod.font
style mas_py_console_text_cn is console_text_console:
    font mas_ptod.font

# images for console stuff
#image mas_py_cn_sym = Text(">>>", style="mas_py_console_text", anchor=(0, 0), xpos=10, ypos=538)
#image mas_py_cn_txt = ParameterizedText(style="mas_py_console_text_cn", anchor=(0, 0), xpos=75, ypos=538)
#image mas_py_cn_hist = ParameterizedText(style="mas_py_console_text", anchor(0, 1.0), xpos=10, ypos=538)

init -1 python in mas_ptod:
    import store.mas_utils as mas_utils

    # symbol that we use
    SYM = ">>> "
    M_SYM = "... "

    # console history is alist
    cn_history = list()

    # history lenghtr limit
    H_SIZE = 20

    # current line
    cn_line = ""

    # current command, may not be what is shown
    cn_cmd = ""

    # block commands
    blk_cmd = list()

    # block commands stack level
    # increment for each stack level, decrement when dropping out of a
    # stack level
    stack_level = 0

    # stack to handle indent levels
    # this means indent levels that the opening : has
    # first stack level should ALWAYS BE 0
    indent_stack = list()

    # version text
    VER_TEXT_1 = "Python {0}"
    VER_TEXT_2 = "{0} in MAS"

    # line length limit
    LINE_MAX = 66

    # STATEs
    # used when the current line is only 1 line
    STATE_SINGLE = 0

    # used when current line is multi line
    STATE_MULTI = 1

    # used when we are doing block statements
    STATE_BLOCK = 2

    # used when doing multi line in block statements
    STATE_BLOCK_MULTI = 3

    # state when inerpreter is off
    STATE_OFF = 4

    # current state
    state = STATE_SINGLE

    # local context
    local_ctx = dict()

    # short variants of the comonly used commands:
    def clr_cn():
        """
        SEE clear_console
        """
        clear_console()


    def ex_cn():
        """
        SEE exit_console
        """
        exit_console()


    def rst_cn():
        """
        SEE restart_console
        """
        restart_console()


    def w_cmd(cmd):
        """
        SEE write_command
        """
        write_command(cmd)


    def x_cmd(context):
        """
        SEE exec_command
        """
        exec_command(context)


    def wx_cmd(cmd, context):
        """
        Does both write_command and exec_command
        """
        w_cmd(cmd)
        x_cmd(context)


    def write_command(cmd):
        """
        Writes a command to the console

        NOTE: Does not EXECUTE
        NOTE: remove previous command
        NOTE: does NOT append to previously written command (unless that cmd
            is in a block and was executed)

        IN:
            cmd - the command to write to the console
        """
        if state == STATE_OFF:
            return

        global cn_line, cn_cmd, state, stack_level

        if state == STATE_MULTI:
            # this is bad! You should execute the previous command first!
            # in this case, we will clear your current command and reset
            # state back to SINGLE
            cn_cmd = ""
            cn_line = ""
            state = STATE_SINGLE

        elif state == STATE_BLOCK_MULTI:
            # this is bad! you should execute the previous command first!
            # we will do the same that as MULTI did, except a different state
            cn_cmd = ""
            cn_line = ""
            state = STATE_BLOCK

        # we dont indent the command
        # we also dont check for indents
        cn_cmd = str(cmd)

        # pick appropriate shell symbol
        if state == STATE_SINGLE:
            # snigle mode
            sym = SYM

        else:
            # block mode
            sym = M_SYM

        # the prefixed command includes the shell symbol
        prefixed_cmd = sym + cn_cmd

        # break the lines accordingly
        cn_lines = _line_break(prefixed_cmd)

        if len(cn_lines) == 1:
            # dont need to split lines
            cn_line = cn_cmd

        else:
            # we need to split lines

            # everything except the last line goes to the history
            _update_console_history_list(cn_lines[:-1])

            # last line becomes the current line
            cn_line = cn_lines[len(cn_lines)-1]

            if state == STATE_SINGLE:
                # single mode
                state = STATE_MULTI

            else:
                # block mode
                state = STATE_BLOCK_MULTI


    def clear_console():
        """
        Cleares console hisotry and current line

        Also resets state to Single
        """
        global cn_history, cn_line, cn_history, state, local_ctx
        cn_line = ""
        cn_cmd = ""
        cn_history = []
        state = STATE_SINGLE
        local_ctx = {}


    def restart_console():
        """
        Cleares console history and current line, also sets up version text
        """
        global state
        import sys
        version = sys.version

        # first closing paren is where we need to split the version text
        split_dex = version.find(")")
        start_lines = [
#            mas_utils.clean_gui_text(VER_TEXT_1.format(version[:split_dex+1])),
#            mas_utils.clean_gui_text(VER_TEXT_2.format(version[split_dex+2:]))
            VER_TEXT_1.format(version[:split_dex+1]),
            VER_TEXT_2.format(version[split_dex+2:])
        ]

        # clear the console and add the 2 new lines
        clear_console()
        _update_console_history_list(start_lines)

        # turn the console on
        state = STATE_SINGLE


    def exit_console():
        """
        Disables the console
        """
        global state
        state = STATE_OFF


    def __exec_cmd(line, context, block=False):
        """
        Tries to eval the line first, then executes.
        Returns the result of the command

        IN:
            line - line to eval / exec
            context - dict that represnts the current context. should be locals
            block - True means we are executing a block command and should
                skip eval

        RETURNS:
            the result of the command, as a string
        """
        if block:
            return __exec_exec(line, context)

        # otherwise try eval first
        return __exec_evalexec(line, context)


    def __exec_exec(line, context):
        """
        Runs exec on the given line
        Returns an empty string or a string with an error if it occured.

        IN:
            line - line to exec
            context - dict that represents the current context

        RETURNS:
            empty string or string with error message
        """
        try:
            exec(line, context)
            return ""

        except Exception as e:
            return _exp_toString(e)


    def __exec_evalexec(line, context):
        """
        Tries to eval the line first, then executes.
        Returns the result of the command

        IN:
            line - line to eval / exec
            context - dict that represents the current context.

        RETURNS:
            the result of the command as a string
        """
        try:
            return str(eval(line, context))

        except:
            # eval fails, try to exec
            return __exec_exec(line, context)


    def exec_command(context):
        """
        Executes the command that is currently in the console.
        This is basically pressing Enter

        IN:
            context - dict that represnts the current context. You should pass
                locals here.
                If None, then we use the local_ctx.
        """
        if state == STATE_OFF:
            return

        if context is None:
            context = local_ctx

        global cn_cmd, cn_line, state, stack_level, blk_cmd

        ################### setup some initial conditions ################

        # block mode just means we are in a block
        block_mode = state == STATE_BLOCK or state == STATE_BLOCK_MULTI

        # empty line signals end of block (usually)
        empty_line = len(cn_cmd.strip()) == 0

        # ends with colon is special case
        time_to_block = cn_cmd.endswith(":")

        # but a bad block can happen (no text except a single colon)
        bad_block = time_to_block and len(cn_cmd.strip()) == 1

        # if this contains a value, then we executee
        full_cmd = None

        ################## pre-execution setup ###########################

        if empty_line:
            # like enter was pressed with no text

            if block_mode:
                # block mode means we clear a stack level
                __popi()

            else:
                # otherwise, add an empty new line to history, and thats it
                # dont need to execute since nothing will happen
                _update_console_history(SYM)
                cn_line = ""
                cn_cmd = ""
                return

        if bad_block:
            # user entered a bad block
            # we will execute it as a command
            full_cmd = cn_cmd
            stack_level = 0
            blk_cmd = list()

        elif time_to_block:
            # we are going to enter a new block mode
            blk_cmd.append(cn_cmd)

            if not block_mode:
                # we didnt start in block mode
                __pushi(0)

            else:
                # block mode
                pre_spaces = _count_sp(cn_cmd)

                if __peeki() != pre_spaces:
                    # if this colon line does NOT match current indentaion
                    # level then we need to push a new stack
                    __pushi(pre_spaces)

        elif block_mode:
            # in block mode already
            blk_cmd.append(cn_cmd)

            if stack_level == 0:
                # we've cleared all stacks, time to execute block commands
                full_cmd = "\n".join(blk_cmd)
                blk_cmd = list()

        else:
            # otherwise, we must be single mode or single multi

            # setup the command to be entered
            full_cmd = cn_cmd

        ########################## execution ##############################

        # execute command, if available
        if full_cmd is not None:
            result = __exec_cmd(full_cmd, context, block_mode)

        else:
            result = ""

        ################### console history update #########################

        if block_mode and empty_line:
            # we MUST be in block mode to reach here
            output = [M_SYM]

        else:
            # otherwise, use the sym we need
            if state == STATE_SINGLE:
                sym = SYM

            elif state == STATE_BLOCK:
                sym = M_SYM

            else:
                # multi dont need symbols
                sym = ""

            output = [sym + cn_line]

        # if we have any results, we need to show them too
        if len(result) > 0:
            output.append(result)

        # update console history and clear current lines / cmd
        cn_line = ""
        cn_cmd = ""
        _update_console_history_list(output)

        ###################### Post-execution updates ####################

        if bad_block:
            # bad block, means we abort lots of things
            state = STATE_SINGLE
            block_mode = False

        elif time_to_block:
            # new block, incrmenet stack levels, change to block states
            state = STATE_BLOCK
            block_mode = True

        ###################### final state updates ######################

        if (state == STATE_MULTI) or (block_mode and stack_level == 0):
            # no more stacks or in multi mode
            state = STATE_SINGLE

        elif state == STATE_BLOCK_MULTI:
            # multi modes end here
            state = STATE_BLOCK


    def get_last_line():
        """
        Retrieves the last line from the console history

        RETURNS:
            last line from console history as a string
        """
        if len(cn_history) > 0:
            return cn_history[len(cn_history)-1]

        return ""


    def set_local_context(context):
        """
        Sets the local context to the given context.

        Stuff in the old context are forgotten.
        """
        global local_ctx
        local_ctx = context


    def __pushi(indent_level):
        """
        Pushes a indent level into the stack

        IN:
            indent_level - indent to push into stack
        """
        global stack_level
        stack_level += 1
        indent_stack.append(indent_level)


    def __popi():
        """
        Pops indent level from stack

        REUTRNS:
            popped indent level
        """
        global stack_level
        stack_level -= 1

        if stack_level < 0:
            stack_level = 0

        if len(indent_stack) > 0:
            indent_stack.pop()


    def __peeki():
        """
        Returns value that would be popped from stack

        RETURNS:
            indent level that would be popped
        """
        return indent_stack[len(indent_stack)-1]


    def _exp_toString(exp):
        """
        Converts the given exception into a string that looks like
        how python interpreter prints out exceptions
        """
        err = repr(exp)
        err_split = err.partition("(")
        return err_split[0] + ": " + str(exp)


    def _indent_line(line):
        """
        Prepends the given line with an appropraite number of spaces, depending
        on the current stack level

        IN:
            line - line to prepend

        RETURNS:
            line prepended with spaces
        """
        return (" " * (stack_level * 4)) + line


    def _count_sp(line):
        """
        Counts number of spaces that prefix this line

        IN:
            line - line to cound spaces

        RETURNS:
            number of spaces at start of line
        """
        return len(line) - len(line.lstrip(" "))


    def _update_console_history(*new_items):
        """
        Updates the console history with the list of new lines to add

        IN:
            new_items - the items to add to the console history
        """
        _update_console_history_list(new_items)


    def _update_console_history_list(new_items):
        """
        Updates console history with list of new lines to add

        IN:
            new_items - list of new itme sto add to console history
        """
        global cn_history

        # make sure to break lines
        for line in new_items:
            broken_lines = _line_break(line)

            # and clean them too
            for b_line in broken_lines:
#                cn_history.append(mas_utils.clean_gui_text(b_line))
                cn_history.append(b_line)

        if len(cn_history) > H_SIZE:
            cn_history = cn_history[-H_SIZE:]


    def _line_break(line):
        """
        Lines cant be too large. This will line break entries.

        IN:
            line - the line to break

        RETURNS:
            list of strings, each item is a line.
        """
        if len(line) <= LINE_MAX:
            return [line]

        # otherwise, its TOO LONG
        broken_lines = list()
        while len(line) > LINE_MAX:
            broken_lines.append(line[:LINE_MAX])
            line = line[LINE_MAX:]

        # add final line
        broken_lines.append(line)
        return broken_lines


screen mas_py_console_teaching():

    frame:
        xanchor 0
        yanchor 0
        xpos 5
        ypos 5
        background "mod_assets/console/cn_frame.png"

        fixed:
            python:
                starting_index = len(store.mas_ptod.cn_history) - 1
                cn_h_y = 413
                cn_l_x = 41

            # console history
            for index in range(starting_index, -1, -1):
                $ cn_line = store.mas_ptod.cn_history[index]
                text "[cn_line]":
                    style "mas_py_console_text"
                    anchor (0, 1.0)
                    xpos 5
                    ypos cn_h_y
                $ cn_h_y -= 20

            # cursor symbol
            if store.mas_ptod.state == store.mas_ptod.STATE_SINGLE:
                text ">>> ":
                    style "mas_py_console_text"
                    anchor (0, 1.0)
                    xpos 5
                    ypos 433

            elif store.mas_ptod.state == store.mas_ptod.STATE_BLOCK:
                text "... ":
                    style "mas_py_console_text"
                    anchor (0, 1.0)
                    xpos 5
                    ypos 433

            else:
                # multi line statement, dont have the sym at all
                $ cn_l_x = 5

            # current line
            if len(store.mas_ptod.cn_line) > 0:
                text "[store.mas_ptod.cn_line]":
                    style "mas_py_console_text_cn"
                    anchor (0, 1.0)
                    xpos cn_l_x
                    ypos 433

# does a write command and waits
label mas_w_cmd(cmd, wait=0.7):
    $ store.mas_ptod.w_cmd(cmd)
    $ renpy.pause(wait, hard=True)
    return

# does an execute and waits
label mas_x_cmd(ctx=None, wait=0.7):
    $ store.mas_ptod.x_cmd(ctx)
    $ renpy.pause(wait, hard=True)
    return

# does both writing and executing, with waits
label mas_wx_cmd(cmd, ctx=None, w_wait=0.7, x_wait=0.7):
    $ store.mas_ptod.w_cmd(cmd)
    $ renpy.pause(w_wait, hard=True)
    $ store.mas_ptod.x_cmd(ctx)
    $ renpy.pause(x_wait, hard=True)
    return

# does both writing and executing, no x wait
label mas_wx_cmd_noxwait(cmd, ctx=None):
    call mas_wx_cmd(cmd, ctx, x_wait=0.0)
    return
