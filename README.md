# Secure Elevators
## Introducción
El objetivo de este proyecto es hacer de los elevadores un espacio seguro donde se pueda evitar el contacto con superficies y la ventilación esté asegurada, evitando así posibles infecciones por viruses como el SARS-CoV-2. Para ello, también permite el control de aforo dentro del habitáculo haciendo uso del reconocimiento de imágenes y el control del elevador mediante comandos de voz.

El programa adoptará las funcionalidades que el usuario haya activado en la interfaz web alojada en un dyno de Heroku. Este cliente web y API ha sido desarrollado por Julen Badiola haciendo uso del stack MERN (Mongo, Express, React y NodeJs) como proyecto para la asignatura Desarrollo Avanzado de Software. Por otro lado, el programa recopila información útil sobre el uso del elevador y la envía al servidor central mencionado, donde podrán verse estadísticas de uso. 

![Interfaz web.](/multimedia/animated.gif "Interfaz web.")

> La URL del servidor es: https://secureelevatorsdemo.herokuapp.com

## Descripción general
> Se referenciará al módulo de cabina como MC y al módulo de planta como MP.
### Módulo planta

Este módulo es representado por el fichero `client_main.py`. El objetivo es detectar cuando alguien llama al elevador. Para ello, se hace uso de dos sensores:

1. **Sensor de proximididad**: si la distancia capturada por el sensor es inferior a 2.
1. **Grove Button**: cuando el botón es presionado.


### Módulo cabina

Este módulo es representado por el fichero `server_main.py`. Es el programa principal, ya que en él es donde ocurren todas las funcionalidades principales del proyecto:

* **Obtención de propiedades**: Las propiedades principales se obtienen del fichero de configuración llamado `main.properties`. En él, se definen algunas constantes de las que hará uso el programa. La clase encargada de obtener dichas propiedades se llama `PropertiesManager`, y está ubicada en el archivo `/properties/properties.py`.

* **Obtención de configuración**: Al iniciar el script, se obtiene la configuración del elevador mediante una llamada a la API del servidor. Una vez obtenida, se almacena en el fichero `elevator.properties`.

* **Funcionalidad del elevador**: El elevador está representado por un objeto tipo `Elevator`. En él, se especifica el comportamiento del ascensor como llamadas, viajes, reconocimientos, captura de datos...

* **Recepción de llamadas al ascensor**: Recibe e interpreta los datos enviados desde los MP y acciona el mencionado objeto `Elevator` en función de dichos datos.

* **Reconocimiento de imágenes**: Las imágenes se obtienen en tiempo real desde la webcam. Genera a partir del primer frame obtenido (idealmente el elevador vacío) una imagen que se utilizará para contrastar con las siguientes. Es decir, si el cambio entre el primer frame (elevador vacío) y el frame actual (con 2 personas, por ejemplo) es notable, detectará el número de personas que hay dentro.

* **Reconocimiento de voz**: Hace uso de la API de Google Speech para reconocer el piso al que quiere ir el usuario. La palabra clave es "piso", por lo que cualquier conbinación que contenga dicha palabra accionará el mecanismo de viaje hacia el piso seleccionado:
    * *"Llévame al piso 1"*
    * *"Llévame al primer piso"*
    * *"piso 1"*



## Descripción componentes hardware
Idealmente, se debería implantar una raspberry en la cabina del elevador y que adopte el rol de "módulo de cabina" y, por el otro lado, una raspberry por cada planta y que adopte el rol "módulo de planta".

En el caso del **MP**:

| Elemento | Puerto de conexión | Utilidad |
| --- | --- | --- |
| SX1278 433MHz LoRa Module | Puerto serial | Comunicación entre módulos
| Botón | GPIO 16 | Accionar el mecanismo de llamada al ascensor
| Sensor de proximidad | GPIO 5 | Accionar el mecanismo de llamada al ascensor sin necesidad de contacto con superficies
| LED | GPIO 24 | Proporcionar feedback al usuario cuando acciona la llamada al ascensor (parpadea)



En el caso del **MC**:

| Elemento | Puerto de conexión | Utilidad |
| --- | --- | --- |
| SX1278 433MHz LoRa Module | Puerto serial | Comunicación entre módulos
| Webcam | USB | Control de aforo mediante reconocimiento de imágenes
| Micrófono | Integrado en la webcam, USB | Control del ascensor mediante comandos de voz
| Altavoz | Jack 3.5mm o Bluetooth | El asistente de voz del ascensor proporciona feedback al usuario
| Botón | GPIO 16 | Emular los botones físicos del ascensor para seleccionar un piso

## Descripción de la jerarquía de ficheros (software)
1. **/logic**: Directorio que contiene las clases de la lógica de negocio.
    
    1. **Elevator.py**: Clase singleton que representa la cabina del elevador. En ella ocurren los procesos de llamada, viaje, solicitud de piso...
    1. **ServerCommunication.py**: Clase singleton encargada de la comunicación con el servidor web del proyecto, ubicado en https://secureelevatorsdemo.herokuapp.com
    1. **VoiceAssistant.py**: Clase singleton que representa el asistente de voz. Hace uso de `pico2wave` para transformar texto en voz.
    1. **VoiceRecognition.py**: Fichero que alberga algunas funciones asíncronas (haciendo uso de `asyncio`) que transforman el habla en texto mediante llamadas a la API de Google Speech (lo hace internamente la librería `speech_recognition`).
    1. **CapacityController.py**: Alberga la funcionalidad de detección de personas en base a imágenes input. En nuestro caso, provenienen de la webcam.
    1. **VentilationManager.py**: Alberga la clase singleton responsable de activa la ventilación en caso de que se cumplan ciertas condiciones, como que el tiempo de inactividad del elevador sea superior a 10 segundos.
    
1. **/func**: Directorio que contiene algunos métodos y clases genéricas.
    1. **Singleton.py**: Metaclase de la que hacen uso algunas de las clases. Aplica el patrón de diseño con ese nombre que permite restringir la creación de objetos pertenecientes a una clase o el valor de un tipo a un único objeto.
    1. **threading.py**: Contiene la clase `Thread_with_trace` y algunas subrutinas para el manejo de hilos. El objetivo es poder parar determinados hilos que se crean durante la ejecución. Además, define la anotación `threading` para definir métodos (dentro de los propios objetos) que son ejecutados en un hilo concurrente.
    1. **sensors.py**: Fichero que alberga las clases referentes a los sensores LED, botones y sensor de proximidad en base a ultrasonidos.
    1. **numparser.py**: Funciones para detectar el piso al que quiere ir el usuario en base al texto que se ha detectado por su habla. 
    1. **protocol.py**: Asignación de variables y métodos de los que se hará uso para la transferencia de datos.
1. **/multimedia**: Directorio con imágenes y vídeos para el testeo y documentación.
1. **/lora**: Directorio que contiene lo referente a los módulos de Lora.

1. **/properties**: Directorio que contiene lo referente al manejo de los archivos de configuración.
    1. **properties.py**: Archivo que alberga la clase `PropertiesManager`, que hereda de Sigleton y que, como su propio nombre indica, es la encargada de manejar los archivos de configuración.
    1. **main.properties**: Archivo de configuración general del proyecto. Es estático, nada en él cambia en ejecución.
    1. **elevator.properties**: Al contrario que el anterior, este cambia a partir de los datos obtenidos desde el servidor. Define los pisos y funcionalidades que el usuario ha activado desde la interfaz web.
    
1. **client_main.py**: script principal para la ejecución de los módulos de planta.
1. **server_main.py**: script principal para la ejecución del  módulo de cabina.
1. **setupClient.sh**: fichero de instalación de dependencias necesarias para el `client_main.py`
1. **setupServer.sh**: fichero de instalación de dependencias necesarias para el `server_main.py`


## Comunicación entre módulos (lora)
#### Llamadas al elevador
Para llamar al elevador desde el MP, se envía mediante lora la siguiente información:
```
data = {
    prot.ELEVATOR_CALL: properties.THIS_FLOOR,
}
```
El MC comprueba los datos provenientes del módulo de lora, y si existe una petición `ELEVATOR_CALL`, activa la llamada en el objeto local tipo `Elevator`.

#### Llegadas del elevador
Cada vez que el elevador llega a un piso, el MC envía por lora la siguiente información:
```
data = {
    prot.ELEVATOR_ARRIVE: floorArrived,
}
```
El objetivo de este intercambio de información es que el MP, al recibirlo, desactive el parpadeo del LED (que se ha activado al realizar la llamada al ascensor) si el elevador a llegado a la planta que representa.

## Instalación y puesta en marcha
### Módulo de cabina

```
chmod +x setupServer.sh
./setupServer.sh
```
##### Ejecución: `python3 server_main.py`
### Módulo de planta

```
chmod +x setupClient.sh
./setupClient.sh
```
##### Ejecución: `python3 client_main.py`

## Vídeo demostración
**Como nosotros disponemos de 2 raspberrys, una toma el rol de cabina y la otra de planta.** 

[![Demo video](https://img.youtube.com/vi/lIBlGJ64l38/0.jpg)](https://www.youtube.com/watch?v=lIBlGJ64l38)

## Links y referencias

[Speech recognition using Google Speech API](https://maker.pro/raspberry-pi/projects/speech-recognition-using-google-speech-api-and-python).

[Python Speech Recognition](https://realpython.com/python-speech-recognition/).

[Python RealTime human detection](https://data-flair.training/blogs/python-project-real-time-human-detection-counting/).

Github repo: [PeopleCounter by LukashenkoEvegeniy](https://github.com/LukashenkoEvgeniy/People-Counter/blob/master/PeopleCounterMain.py).


## Problemas generados y soluciones adoptadas
1. **raspberry muerta**
1. **sd muerta**

