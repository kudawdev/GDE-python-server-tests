# Laboratorio: Pruebas de concurrencia y paralelismo

Este laboratorio cuenta con pruebas de ejecución de tareas concurrentes y parelelas (Asyncio, Ray y Multiprocessing) utilizando multiples clientes websocket para las pruebas de estrés. Las principales librerias y/o framework 

- **Asyncio**: Es parte de la biblioteca estándar de Python (3.4+) por lo que no requiere instalación adicional (ya incluida en Python) y es útil para programación asíncrona que usa corutinas, es decir, permite que tu código funcione de manera no secuencial, haciendo que sea posible tener varias operaciones sucediendo al mismo tiempo.

- **Ray**: Es un framework de código abierto para la programación distribuida y paralela en Python. Se diseñó para simplificar la creación de aplicaciones y servicios que requieren ejecución de tareas en forma distribuida, como es común en el desarrollo de algoritmos de aprendizaje automático (Machine Learning).

- **Multiprocessing**: Es parte de la biblioteca estándar de Python (2.6+). Fue diseñado para facilitar la ejecución simultánea de tareas y superar las limitaciones impuestas por el Global Interpreter Lock (GIL) en Python, permitiendo la programación multiproceso para optimizar el uso de múltiples CPUs en tareas intensivas. 

# Configuración

### Sección [server]
Esta sección incluye la configuración del servidor.

- `host`: La dirección del host donde el servidor está escuchando. Por ejemplo: 'localhost'
- `port`: El puerto en el que el servidor está escuchando. Por ejemplo: 8765
- `timeout_sec`: El tiempo de espera en segundos para las conexiones del servidor. Por ejemplo: 100

### Sección [client]
Esta sección contiene la configuración del cliente.

- `num_client`: El número de clientes para la prueba de estrés. Por ejemplo: 200
- `tasks`: Los tipos de tareas que los clientes solicitarán, separados por comas. Por ejemplo: 'fib, cpu, io'

### Sección [task_setting]
Esta sección incluye la configuración de las tareas.

- `fibonacci_limit`: El número límite para el cálculo de Fibonacci. Por ejemplo: 5000
- `large_file_name`: El nombre de un gran archivo para las pruebas de entrada/salida. Por ejemplo: 'large_file.txt'

### Sección [other]
Esta sección contiene otras configuraciones.

- `asyn_semaphore`: Número de semáforos asincrónicos. Por ejemplo: 5
- `multiprocessing_processes`: Número de procesos para multiprocesamiento. Por ejemplo: 4

# Pruebas
### Asyncio_semaphore ###
La prueba busca demostrar el uso de Asyncio Semaphore e involucra la interacción entre un servidor basado en WebSockets (`ws_server`) y un cliente WebSocket (`ws_client`). A su vez, se utiliza la API `websockets` de Python y el módulo `asyncio` para manejar procesos asíncronos.

1. **ws_server**: Este script corre un servidor WebSocket que recibe mensajes del cliente. Cuando recibe una mensaje, la pasa a un manejador de tareas (`task_handler`) que espera un cierto número de segundos antes de responder (time sleep).

2. **ws_client**: Este script genera una cantidad específica de "solicitudes" (tareas), cada una de las cuales solicita que el servidor espere un número aleatorio de segundos. Cada una de estas tareas se envía al servidor como una solicitud a través de una conexión WebSocket. 

3. **task_handler**: Este script contiene la lógica para el manejo de las solicitudes. Utiliza un semáforo (`asyncio.Semaphore`) para limitar la cantidad de solicitudes que pueden ser procesadas simultáneamente. Cuando llega una solicitud, la función `handle_request` adquiere este semáforo, espera el número especificado de segundos y luego libera el semáforo.

### Asyncio
Esta prueba busca demostrar el uso de asyncio, además de hacer pruebas de estrés al servidor WebSocket, utilizando `asyncio` y `websockets` en Python para manejar múltiples conexiones y ejecutar tareas de manera asíncrona.

1. **ws_server**: Este script corre un servidor WebSocket que escucha mensajes de los clientes. Cuando se recibe un mensaje, se pasa a un "manejador de tareas" (`task_handler`) para su procesamiento. También maneja desconexiones del cliente y otras excepciones.

2. **ws_client**: Este script genera un específico número de "clientes", cada uno de los cuales envía una secuencia de tareas al servidor. Cada tarea es en realidad un nombre de tarea enviado como una solicitud al servidor a través de una conexión WebSocket.

3. **task_handler**: Este es el "manejador de tareas" que procesa las solicitudes. Según el contenido del mensaje, realiza una tarea "CPU-bound" (suma de una serie de números), una tarea "IO-bound" (lectura y escritura en un archivo grande), o la generación de un número en la secuencia de Fibonacci.

#### Beneficios de esta arquitectura para un servidor web

La arquitectura basada en `asyncio` y `websockets` es muy beneficiosa para un servidor web por varias razones:

- **Escalabilidad**: Permite manejar un gran número de conexiones concurrentes, lo cual es esencial para aplicaciones en tiempo real.

- **Eficiencia**: Al utilizar una arquitectura basada en eventos, solo se utilizan recursos cuando hay trabajo que hacer. Esto es más eficiente que los modelos a base de hilos o procesos, que requieren recursos aún cuando están ociosos.

- **Tolerancia a fallas**: El manejo de excepciones optimizadas por el servidor permite manejar de forma adecuada los errores producidos en tiempo de ejecución, lo cual es esencial para garantizar la continuidad y robustez del servicio.

Esta arquitectura es especialmente beneficiosa al desarrollar aplicaciones que requieran actualizaciones en tiempo real a través de múltiples conexiones.

### Ray
Esta prueba es similar a la prueba de Asyncio, donde se utiliza ahora el framework `ray` para manejar tareas en el servidor.

1. **ws_server**: Este es el servidor WebSocket que se inicializa. Sin embargo, ahora utiliza `ray` para procesar las tareas. Cuando recibe un mensaje de un cliente, la tarea es pasada a `ray`, el cual ejecutará la función `handle_request` de forma **distribuida**.

2. **ws_client**: Esta es una versión muy similar al cliente de la prueba anterior. Cada cliente envía una secuencia de tareas al servidor por medio de una conexión WebSocket.

3. **task_handler**: Aquí es donde se ve la diferencia principal. El manejador ahora utiliza la funcionalidad `ray.remote`, lo que permite que la función `handle_request` corra de manera distribuida.

#### Beneficios de esta arquitectura en un servidor web

La utilización de `ray` en esta arquitectura trae varios beneficios al manejo de tareas en un servidor web, sobre todo cuando estas son intensivas en cómputo o entrada/salida:

- **Desacoplamiento del código**: Ray permite escribir el código de una manera modular y desacoplada, facilitando así la lectura, mantenimiento y testeo del mismo.

- **Computación distribuida de Python**: Ray simplifica la implementación de sistemas de cómputo distribuido, permitiendo que las aplicaciones escalen de manera eficiente en una sola máquina o entre un gran conjunto de máquinas.

- **Manejo eficiente de Recursos**: Ray tiene la capacidad de manejar eficientemente los recursos del sistema y de la red en entornos distribuidos, lo cual es importante para mantener la funcionalidad bajo demanda alta.

En esencia, la principal ventaja de usar Ray en la arquitectura de tu servidor web es que proporciona una forma fácil y flexible de escribir aplicaciones que pueden ejecutarse de manera eficiente a gran escala. Esto es particularmente útil para aplicaciones que necesitan manejar una gran cantidad de tareas en paralelo y que necesiten de ejecución distribuida.

### Asyncio_multiprocessing
Esta prueba es otra variante de las pruebas anteriores, en la que se incorpora el módulo `multiprocessing` de Python para la ejecución paralela de tareas.


1. **ws_server**: Este script inicializa un servidor WebSocket utilizando `asyncio`, pero ahora se utilizan los recursos de `multiprocessing` para ejecutar las tareas. Cuando se recibe un mensaje de un cliente, la tarea se pasa a un proceso separado que es manejado por `multiprocessing`. De este modo, se puede aprovechar todo el potencial de múltiples núcleos de CPU.

2. **ws_client**: Similar a las pruebas anteriores, este script genera una cantidad específica de "clientes", cada uno de los cuales envía una serie de tareas al servidor web.

3. **task_handler**: Este script contiene las funciones que serán llamadas y ejecutadas como un nuevo proceso por `multiprocessing`. Cada función representa una tarea intensiva ya sea en CPU o E/S.

#### Beneficios clave de esta arquitectura para un sistema de servidor

- **Aprovechamiento del paralelismo**: `Multiprocessing` permite que las tareas intensivas de CPU se ejecuten en procesos separados en paralelo, lo que puede resultar en un incremento significativo en el rendimiento general, especialmente en sistemas con múltiples núcleos de CPU.

- **Gestión eficiente de las tareas**: La separación de tareas en múltiples procesos puede ayudar a prevenir los bloqueos y garantizar que una única tarea intensiva no monopolice el tiempo de CPU.

- **Mejor aprovechamiento de los recursos**: Esta arquitectura puede aprovechar todos los núcleos de la CPU, mejorando el uso de los recursos del sistema.

- **Escalabilidad**: En sistemas con un gran número de núcleos de CPU, esta arquitectura es capaz de escalar bien y aumentar el rendimiento al permitir la ejecución simultánea de más tareas.

En esencia, la adopción de una arquitectura que utilice `asyncio` junto con `multiprocessing` para tareas de gestión de tareas y comunicación de red puede resultar en un código más eficiente y escalable, aprovechando al máximo los recursos del sistema.
