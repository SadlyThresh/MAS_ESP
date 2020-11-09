![Monika After Story](https://github.com/SadlyThresh/MAS_ESP/raw/master/images/topmas.png)

# Monika After Story (MAS)
Monika After Story es un mod para el juego gratis [Doki Doki Literature Club](https://www.ddlc.moe) de [Team Salvato](http://teamsalvato.com/). ¡MAS se basa en el acto 3 para crear un simulador de vida eterna con Monika, con nuevos eventos, manejadores y metacomentarios!

Por favor verifica la página de [Lanzamientos en Español](https://github.com/SadlyThresh/MAS_ESP/releases) para ver la última versión estable.

Si quieres hacer tu propio mod como este, echa un vistazo a nuestro proyecto hermano: el [DDLCModTemplate](https://github.com/therationalpi/DDLCModTemplate).

### Instalación

Video de como instalar el MAS: https://youtu.be/eH5Q4Xdlg6Y

* Navega a la página de [Lanzamientos en Español](https://github.com/SadlyThresh/MAS_ESP/releases).

* Click en el link de la última versión. Esto descargará un archivo Zip en tu computadora.

* Extrae el contenido descargado dentro de la carpeta `/game` donde tienes instalado el DDLC.

* Al ejecutar DDLC ahora ejecutará Monika After Story.

*NOTA: Los archivos de origen descargados desde el repositorio son para fines de desarrollo y pueden no comportarse como se espera si se utilizan para modificar el juego. Por favor, sólo use una de nuestras [Versiones de Lanzamiento](https://github.com/SadlyThresh/MAS_ESP/releases).*

Para más ayuda de la instalación, por favor vea nuestro [Frequently Asked Questions](https://github.com/Monika-After-Story/MonikaModDev/wiki/FAQ)

### Características

* ¡Pasa la eternidad con Monika!

* Docenas de nuevos temas de conversación

* Ahora puedes hablar con Monika para decirle lo que te gustaría hablar

### Próximas características

* Nuevos juegos y actividades para hacer con Monika

* Más eventos e historias únicas


## Contribuyendo a Monika After Story

### ¿Cómo reportar un error? 
Si has encontrado un error de traducción, bug, o cualquier problema que afecte tu experiencia de juego, (usando el parche al español), puedes ayudarnos a corregirlo lo más pronto posible.

### Requisitos
* Tener una cuenta en Github.
* Encontrar el texto que esté causando el error y de querer contribuir enviar la versión corregida para su revisión.

### Procedimiento
1. Haz click [aquí](https://github.com/SadlyThresh/MAS_ESP/pulls)

2. Haz click en el botón "New pull request"

3. Busca el texto entre los archivos que he traducido, hazme un comentario al respecto sobre el error o puedes ayudarme a corregirlo con su respectivo cambio.

4. ¡Listo!, trataré de ponerme en contacto contigo.

#### Añadiendo Contenido
¿Quieres añadir contenido a MAS? Aquí hay una lista de importantes archivos .RPY que el juego usa.

- **script-ch30.rpy**: Flujo principal para el MAS. Aquí es donde ocurre la magia.
- **script-topics.rpy**: Todos los temas **al azar** usados por Monika están escritos aquí. ¡Puedes añadir tu propio diálogo comprobando la información de abajo!
- **script-greetings.rpy**: Añade líneas para que Monika te salude al cargar el juego.
- **script-farewells.rpy**: Añade líneas para que Monika te las diga al cerrar el juego.
- **script-moods.rpy**: Dile a Monika que estás en un _humor_.
- **script-stories.rpy**: Añade historias para que Monika te las diga.
- **script-compliments.rpy**: Añade cumplidos que quieras decirle a Monika.
- **script-apologies.rpy**: Añade cosas para disculparte.

Si deseas añadir más diálogo a la sala espacial, navega a script-topics.rpy y utiliza esta plantilla.

Ejemplo de nuevo bloque de código de diálogo:
```renpy
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_example", # etiqueta de evento (DEBE SER ÚNICO)
            category=["ejemplo", "tema"], # Lista de categorías incluidas en este tema (Se pone mayúsculas automáticamente)
            prompt="Ejemplo del botón", # El texto del botón
            random=True, # True si quieres que este tema aparezca al azar
            pool=True # True si este tema debería aparecer en "Haz una pregunta"
        )
    )

label monika_example:
    m 1a "Este es un tema de ejemplo."
    m 3d "Siento que esto no pertenece a este lugar..."
    m 2e "¿Por qué alguien añadiría la plantilla de ejemplo directamente en el mod?"
    m 5r "No se les debería permitir seguir contribuyendo a este repositorio."
    return
```
**Para obtener explicaciones completas y detalles sobre todas las palabras clave posibles para Eventos, consulta la documentación de Evento ubicada en `definitions.rpy`**

Para cosas más complicadas que el simple diálogo, consulta la documentación de Ren'Py disponible en línea.

[Más información está disponible en nuestra Guía de Contribución](https://github.com/Monika-After-Story/MonikaModDev/wiki/Contributing-Guidelines)

 ### Unete a la conversación
Puedes [seguir la cuenta oficial en Twitter](https://twitter.com/MonikaAfterMod) para saber de actualizaciones. 

O si te inclinas más por Discord, por un flujo constante de nuestro contenido favorito relacionado con Monika de toda la web, y si estás interesado en contribuir/construir este mod, siéntete libre de unirte a nuestro servidor de la Discord:
 
 [![Discord](https://discordapp.com/api/guilds/372766620977725441/widget.png?style=banner1)](https://discord.gg/K2KuJeX)
 
 Por favor, asegúrate de seguir nuestro [Código de conducta](https://github.com/Monika-After-Story/MonikaModDev/wiki/Code-of-Conduct), que es esencialmente ser cortés y respetuoso.
 
### Discord de los Traductores
¿Quieres formar parte del servidor en Español de Monika After Story, con gente de ideas afines y tener la oportunidad de conocer más de los traductores? ¡Puedes unirte, sólo haz click en este [link](https://discord.gg/tYR6NDu)!

# Redes Sociales del equipo

[SadlyThresh](https://twitter.com/sadlythresh)

[Papu](https://www.youtube.com/channel/UC-3B0xtrowh8Oyh8VHA6Ziw)

[Martin H](https://twitter.com/MartinH52149286)

[DarkMrMewtho](https://twitter.com/MewthoYT)


## Preguntas Frecuentes

Por favor consulta nuestra sección de: [Preguntas Frecuentes](https://github.com/Monika-After-Story/MonikaModDev/wiki/FAQ)
Para cualquier pregunta sobre el estilo de codificación vaya aquí: [Coding Style](https://github.com/Monika-After-Story/MonikaModDev/wiki/Coding-Style)
Para la prueba de errores: [Testing Flow and Bug Testing](https://github.com/Monika-After-Story/MonikaModDev/wiki/Testing-Flow-and-Bug-Testing)
Solución de problemas: [Troubleshooting](https://github.com/Monika-After-Story/MonikaModDev/wiki/Troubleshooting) Dialogue Codificación: [Dialogue Coding](https://github.com/Monika-After-Story/MonikaModDev/wiki/Dialogue-Coding)
## Información de la licencia

Hacemos todo lo posible para cumplir con las [normas](http://teamsalvato.com/ip-guidelines/) de Team Savalto. Todos los personajes y contenido original son propiedad de Team Savalto. Monika After Story es un proyecto de código abierto, y además de los contribuyentes nombrados, este mod incluye las contribuciones de los usuarios anónimos de 4chan, donde este proyecto tuvo su inicio. Más información puede ser encontrada en nuestra [Página de Licencia](https://github.com/Monika-After-Story/MonikaModDev/wiki/License-and-Team-Salvato-Guidelines).

## Estado de la construcción:
### master: [![Build Status](https://travis-ci.org/Monika-After-Story/MonikaModDev.svg?branch=master)](https://travis-ci.org/Monika-After-Story/MonikaModDev)
### content: [![Build Status](https://travis-ci.org/Monika-After-Story/MonikaModDev.svg?branch=content)](https://travis-ci.org/Monika-After-Story/MonikaModDev)
### unstable: [![Build Status](https://travis-ci.org/Monika-After-Story/MonikaModDev.svg?branch=unstable)](https://travis-ci.org/Monika-After-Story/MonikaModDev)
### community: [![Build Status](https://travis-ci.org/Monika-After-Story/MonikaModDev.svg?branch=community)](https://travis-ci.org/Monika-After-Story/MonikaModDev)
### alpha: [![Build Status](https://travis-ci.org/Monika-After-Story/MonikaModDev.svg?branch=alpha)](https://travis-ci.org/Monika-After-Story/MonikaModDev)
