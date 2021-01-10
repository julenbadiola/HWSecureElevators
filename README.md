# Secure Elevators
## Introducción
El objetivo de este proyecto es proporcionar de los ascensores un espacio seguro donde se pudiera evitar el contacto con superficies y la ventilación estuviese asegurada, evitando así posibles infecciones por viruses como el SARS-CoV-2. 

Para ello, el programa, escrito en Python3, es ejecutado sobre una serie de raspberry pi (3b); una de ellas adopta el rol de "Cabina", mientras que las demás son "Plantas". 

> A partir de ahora, módulo de cabina se sustituirá por MC y módulo de planta por MP.

> La URL del servidor es: https://secureelevatorsdemo.herokuapp.com

## Descripción componentes hardware

Todas las raspberry utilizan un **SX1278 433MHz LoRa Module** para comunicarse. 

En el caso del **MP**, también tiene conectados:

| Elemento | Puerto de conexión |
| --- | --- |
| LEDs | Enumera todos los archivos nuevos o modificados |
| Sensor de proximidad | Muestra las diferencias de archivo que no han sido preparadas |
| Botones | Muestra las diferencias de archivo que no han sido preparadas |


En el caso del **MC**, también tiene conectados:

| Elemento | Puerto de conexión |
| --- | --- |
| Webcam | USB |
| Micrófono | Integrado en la webcam, de modo que USB |
| Altavoz | Jack 3.5mm o Bluetooth |


## Descripción software

### Descripción de la jerarquía de ficheros
1. **/logic**: Directorio que contiene las clases de la lógica de negocio.
    
    1. **Elevator.py**: Clase singleton que representa la cabina del elevador. En ella ocurren los procesos de llamada, viaje, solicitud de piso...
    1. **ServerCommunication.py**: Clase singleton encargada de la comunicación con el servidor web del proyecto, ubicado en https://secureelevatorsdemo.herokuapp.com
    1. **VoiceAssistant.py**: Clase singleton que representa el asistente de voz. Hace uso de `pico2wave` para transformar texto en voz.
    1. **VoiceRecognition.py**: Fichero que alberga algunas funciones asíncronas (haciendo uso de `asyncio`) que transforman el habla en texto mediante llamadas a la API de Google Speech (lo hace internamente la librería `speech_recognition`).
    1. **CapacityController.py**: Alberga la funcionalidad de detección de personas en base a imágenes input. En nuestro caso, provenienen de la webcam.
    1. **/CapacityTestVideos**: Directorio que contiene dos vídeos para testear el funcionamiento del `CapacityController`. 
1. **/func**: Directorio que contiene algunos métodos y clases genéricas.
    1. **Singleton.py**: Metaclase de la que hacen uso todas las demás clases. Permite el patrón de diseño con ese nombre que permite restringir la creación de objetos pertenecientes a una clase o el valor de un tipo a un único objeto.
    1. **threading.py**: Contiene la clase `Thread_with_trace` y algunas subrutinas para el manejo de hilos. El objetivo es poder parar determinados hilos que se crean durante la ejecución. Además, define la anotación `threading` para definir métodos (dentro de los propios objetos) que son ejecutados en un hilo concurrente.
    1. **numparser.py**: Funciones para detectar el piso al que quiere ir el usuario en base al texto que se ha detectado por su habla. 
    1. **protocol.py**: Asignación de variables y métodos de los que se hará uso para la transferencia de datos.
1. **/lora**: Directorio que contiene lo referente a los módulos de Lora.

1. **/properties**: Directorio que contiene lo referente al manejo de los archivos de configuración.
    1. **elevator.properties**: Archivo de configuración del funcionamiento del elevador creado a partir de los datos obtenidos desde el servidor.
    1. **main.properties**: Archivo de configuración general del proyecto.
    1. **properties.py**: Archivo que alberga la clase `PropertiesManager`, que hereda de Sigleton y que, como su propio nombre indica, es la encargada de manejar los archivos de configuración.
    
1. **client_main.py**: script principal para la ejecución de los módulos de planta.
1. **server_main.py**: script principal para la ejecución del  módulo de cabina.
1. **setupClient.sh**: fichero de instalación de dependencias necesarias para el `client_main.py`
1. **setupServer.sh**: fichero de instalación de dependencias necesarias para el `server_main.py`

### Módulo planta

El objetivo de los módulos de planta es detectar cuando alguien llama al ascensor haciendo uso de un sensor de proximidad.

### Módulo cabina

Este módulo es representado por el fichero `server_main.py`. Es el programa principal, ya que en él es donde ocurren todas las funcionalidades principales del proyecto:

* **Obtención de propiedades**: Las propiedades principales se obtienen del fichero de configuración llamado `main.properties`. En él, se definen algunas constantes de las que hará uso el programa. La clase encargada de obtener dichas propiedades se llama `PropertiesManager`, y está ubicada en el archivo `/properties/properties.py`

* **Obtención de configuración**: Al iniciar el script, se obtiene la configuración del elevador mediante una llamada a la API. Una vez obtenida, se almacena en el fichero `elevator.properties`

* **Funcionalidad del ascensor**: Al iniciar el script, se crea un hilo en el que se espera a recibir datos provenientes de la red lora creada. Estos datos sólo son de un tipo, 

* Funcionalidad del ascensor:




## Instalación y puesta en marcha
### Módulo de cabina

```
chmod +x setupServer.sh
./setupServer.sh
```
##### Ejecución: `python3 server_main.sh`
### Módulo de planta

```
chmod +x setupClient.sh
./setupClient.sh
```
##### Ejecución: `python3 client_main.sh`

## Vídeo demostración

![This is a alt text.](/image/sample.png "This is a sample image.")

## Links y referencias

[Speech recognition using Google Speech API](https://maker.pro/raspberry-pi/projects/speech-recognition-using-google-speech-api-and-python).

[Python Speech Recognition](https://realpython.com/python-speech-recognition/).

[Python RealTime human detection](https://data-flair.training/blogs/python-project-real-time-human-detection-counting/).

Github repo: [PeopleCounter by LukashenkoEvegeniy](https://github.com/LukashenkoEvgeniy/People-Counter/blob/master/PeopleCounterMain.py).


## Problemas generados y soluciones
1. **Se necesita leer y escribir en lora**: Solucion
1. **Problema**: Solucion
1. **VoiceAssistant en español**: Solucion
