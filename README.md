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

### 1. Desarrollo

Como solución se presenta una aplicación web, la cual por medio de un sistema de control de usuarios 
permitirá acceder a los resultados más relevantes de cada encuesta. Además, a nivel de administrador, 
permitirá cargar nuevas encuestas, asignar permisos de acceso y otorgará herramientas con las que se puedan visualizar 
los datos por medio de tablas y gráficos (consultas).  

##### 1.1 Framework

Este proyecto ha sido desarrollado con el framework [Django 3.1](https://docs.djangoproject.com/en/3.1/), pensando 
en la escalabilidad del proyecto. Django es un framework de python que facilita una modalidad de trabajo rápido y modular,
lo que facilitará la comprensión y el fujo de trabajo de este proyecto.

##### 1.2 Base de Datos

El modelo de la base de datos fue diseñado sobre tres ideas generales: "Control de Usuarios", 
"Administración de Encuestas" y "Carga de Encuestas". Siguiendo el siguiente modelo ER


![Logo_UAI](blob/master/logo-uai.png)



  