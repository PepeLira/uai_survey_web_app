# Survey Web App UAI 



### Proyecto

Esta aplicación surge con la necesidad de poder entregar una plataforma en la que se puedan analizar y observar 
los resultados de las encuestas realizadas por el grupo ***Alumni de la Universidad Adolfo Ibáñez***.

Este proyecto presenta los siguientes objetivos:
-	Facilitar el uso y administración de las Encuestas.
-	Contar con una interacción flexible entre el Usuario y la Base de Datos.
-	Escalabilidad, que le permita añadir funcionalidad y valor a la plataforma.


### Contexto

Cada año ***Alumni UAI*** realiza múltiples encuestas de Empleabilidad a los exalumnos de las diferentes 
unidades académicas de la Universidad Adolfo Ibáñez, cuyos resultados suelen ser de interés para los diferentes 
departamentos de la Universidad e incluso para los alumnos y futuros alumnos de nuestra Universidad.  

Estas encuestas se realizan por medio de la plataforma [SurveyMonkey](https://es.surveymonkey.com/), desde la cual se permite
exportar los resultados en múltiples formatos.


#### 1. Desarrollo

Como solución se presenta una aplicación web, la cual por medio de un sistema de control de usuarios 
permitirá acceder a los resultados más relevantes de cada encuesta. Además, a nivel de administrador, 
permitirá cargar nuevas encuestas, asignar permisos de acceso y otorgará herramientas con las que se puedan visualizar 
los datos por medio de tablas y gráficos (consultas).  

Requerimientos:

- Una versión de Python 3.9.1 o superior.
- Contar con <code>pipenv</code> para administrar espacios virtuales.
- Ademas el sistema de control de versiones <code>git</code>.

##### 1.1 Framework

Este proyecto ha sido desarrollado con el framework [Django 3.1](https://docs.djangoproject.com/en/3.1/), pensando 
en la escalabilidad del proyecto. Django es un framework de python que facilita una modalidad de trabajo rápido y modular,
lo que facilitará la comprensión y el fujo de trabajo de este proyecto.

##### 1.2 Base de Datos

El modelo de la base de datos fue diseñado sobre tres ideas generales: "Control de Usuarios", 
"Administración de Encuestas" y "Carga de Encuestas". Siguiendo el siguiente [Modelo ER](), se presenta un modelo que busca
facilitar la carga de cualquier tipo de encuestas. En 

##### 1.3 Deployment

##### 1.4 Seguridad


#### 2 Guía Ininicio Rápida

Como es habitual en los proyectos de aplicaciones Web, lo primero que se debe hacer es iniciar el ambiente virtual sobre 
el que se está desarrollando. Para esto utilizaremos Pipenv, de no tenerlo instalado siempre se puede instalar con el comando
<code>pip install pipenv</code>.

Primero diríjase al repositorio desde el que se va a trabajar y clone este repositorio con el comando:  

    $ git clone https://github.com/PepeLira/uai_survey_web_app.git
    
Una vez se tenga acceso a los archivos del repositorio, se deben instalar los paquetes del espacio virtual 
contenidos en el archivo <code>Pipfile</code>:

    $ pipenv install
    
Luego iniciamos el espacio virtual:

    $ pipenv shell

Por ultimo para iniciar el servidor local:

    $ Python manage.py runserver 
    
y ingresamos al link que nos entrega la consola 

    $ http://127.0.0.1:8000/


### Alcance y espectativas 
___



<p float="left">
  <img src="blob/master/logo-uai.png" alt="drawing" width="300" height="112"/>
  <img src="blob/master/Logo_Alumni.png" alt="drawing" width="367" height="112"/>
</p>



  