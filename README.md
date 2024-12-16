# Ejercicio Qanlex scraper web.

Este es un script en Python de un Scraper Web debiendo el mismo conseguir datos de una página web dinámica específica siguiendo criterios de búsqueda concretos.

## Arquitectura.

Script realizado íntegramente en Python, con Selenium, PyMysql, FastAPI, Uvicorn.
> - main.py: Se realizaron dos endpoints sencillos con FastApi a fines de facilitar la prueba y consulta de los datos. El endpoint "/" consulta la base de datos con PyMysql y el endpoint "/begin/{query}" (donde "query" es la palabra clave a consultar en el input, por ejemplo "residuos") el cual iniciará el proceso de scraping en función de la query enviada.
> - driverConfig.py: Configuración del driver de Selenium para la automatización.
> - dbConnection.py: Configuración de la conexión a la base de datos con PyMysql.
> - wsMainProcess.py: Archivo principal del script, aquí comienza el proceso intentando 6 veces si se encuentra con algún error. El mismo cuenta con tiempos aleatorios de espera como estrategia de evasión para el captcha y el llamado a la función reutilizada "getTableData.py".
> - getTableData.py: Función dedicada al raspado de la tabla en cuestión que al mismo tiempo guarda la información en la base de datos.
> - requirements.txt: Listado de depencias necesarias para el correcto funcionamiento del script.

## Funcionamiento.

> - Instalación Python
>  - Inicialización del repositorio git
>  - Entorno virtual de python: python -m venv .venv
> - Activación del entorno: . .venv/Scripts/activate
>  - git clone https://github.com/Hector039/ejercicioWebScraping.git
> - Instalación dependencias: pip freeze > requirements.txt
> - Creación archivo de variables de entorno (proporcionado): .env
> - Creación de base de datos y tabla sencilla Mysql con cliente (por ejemplo Xampp): CREATE TABLE data ( id int PRIMARY KEY AUTO_INCREMENT, expediente varchar(200), jurisdiccion  varchar(200), dependencia varchar(200), situacion varchar(200), caratula varchar(200), ultimaActuacion varchar(200), demandado varchar(200), actor varchar(200));  
> - Inicio: unvicorn main:app (escucha en 127.0.0.1:8000)
> - Endpoint consulta: 127.0.0.1:8000/
> - Endpoint inicio script: 127.0.0.1:8000/begin/residuos

## Consideración importante:

Si bien el script es funcional, el problema crítico para el funcionamiento del mismo es la evasión/resolución del reCaptcha. Se implentaron técnicas de evasión gratuitas como Selenium-Stealth pero que no son del todo garantidas por lo que eventualmente se podría considerar su resolución manual. Por otro lado, no se encontraron herramientas gratuitas en cuanto a la resolución de los mismos, siendo todas ellas de pago.
Para ver la automatización, comentar la línea "options.add_argument('--headless')" en el archivo driverConfig.py.


## Despliegue en la nube con servicios de AWS.

Actualmente este script se encuentra desplegado en la nube, más específicamente en una instancia de EC2 (Amazon linux) la cual, a través de dos funciones Lambda (desencadenadas con el servicio EventBridge), se inicia y detiene en un horario/día/mes/año configurable a requerimiento. En cada inicio esta instancia ejecuta automáticamente el script quedando a la escucha los endpoints antes mencionados para ejecución/consulta a solicitud.
Los datos obtenidos se van guardando en una base de datos RDS Mysql de AWS solamente accesible a través de la instancia y en una tabla como la mencionada anteriormente.
Al inicio de la instancia, esta se conecta con el repositorio en cuestión de GitHub haciendo un pull y actualizando el código automáticamente para el control de versiones y mantenimiento.

## Consideración importante sobre la instancia:

Cabe destacar, que cada vez que la instancia de inicia (solucionable con el servicio de ), esta cambia su IP pública lo cual podría ser beneficioso para la evasión del captcha, pero dificultando las pruebas al requerir el nuevo IP al momento de su encendido para realizar las consultas.