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


### 1. Desarrollo

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
facilitar la carga de cualquier tipo de encuestas. En este, se presentan las relaciones de las siguientes Entidades:

1. Encuestas (Surveys)
   1. Categoria de Encuesta (QuestionCategory): Por ejemplo para agrupar todas las *Encuestas de Empleabilidad Anuales*.
   2. Periodo (Period): Para identificar las encuestas que pertenecen a un mismo periodo de tiempo.
2. Preguntas (Questions)
   1. Categorias de Pregunta (QuestionCategory): Conjunto de preguntas, de momento solo se encuentra *Datos Personales*.
   2. Preguntas Equivalentes (Equivalent Questions): Revisar punto 4.2
3. Alternativas (OfferedAnswers): Las respuestas disponibles para una pregunta de selección multiple o de alternativas.
4. Respuestas (Answers)
5. Persona (Person): Autor de cada respuesta Individual con su info de contacto.
6. Informes (Dashboards): Conjunto de Gráficos Que pueden pertenecer a una o más encuestas.
7. Consultas/Graficos (Querys): En base a una pregunta seleccionada agrupa todas las respuestas para presentarlas en un gráfico.
8. Facultades (Faculty)
9. Carreras (Careers)
10. Usuarios (Users)
11. Niveles de Acceso (Privileges): Para Regular el acceso a la información dependiendo del Usuario.

*nota: Además de las ya mencionadas también podemos encontrar multiples tablas relacionales*
##### 1.3 Deployment

##### 1.4 Seguridad


### 2 Guía Ininicio Rápida

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

### 3 Aplicaciones / Vistas / Formularios

***Descripción de los controladores de cada Vista***

### 4 Mejoras Próximas

Para continuar ampliando la funcionalidad de esta página, se presentan algunas posibles mejoras al
modelo y la estructura de la página.

#### 4.1 Tablas de datos "Consultas" y "Gráficos"

Con la finalidad de poder realizar gráficos con datos cruzados, se propone la siguiente modificación al
modelo de la base de datos [Nuevo Modelo ER](). *"Un Grafico tiene una o más consultas 
y una consulta pertenece a un grafico"*, donde se entiende por "Consulta" un conjunto de datos que 
contienen una pregunta de la encuesta y sus respectivas respuestas. 

De esta manera se podrán realizar gráficos de Consultas como por ejemplo:

*"Numero Ex alumnos que se encuentren trabajando y hayan cursado un Magister"*

#### 4.2 Implementar Tabla Preguntas Equivalentes

Para poder reutilizar informes anteriores con un grupo de encuestas nuevas. Para esto será necesario crear un formulario 
que permita comparar las preguntas de una encuesta recientemente cargada con las que se 
encuentran ya disponibles en la Base de datos. De esta manera, se tendrá la información necesaria para ofrecerle a 
los administradores replicar algunos de los gráficos de un informe anterior al crear un Nuevo Informe.


### Comentarios
___

Existen múltiples maneras para alimentar la base de datos de una aplicación, en este proyecto se optó por 
trabajar importando tablas de datos en ".csv" pensando en los medios en los que se puede obtener la 
información de SurveyMonkey y en la flexibilidad que otorga no depender de una API en concreto. 
Sin embargo, esa flexibilidad significa también que sea necesario realizar mantención a este sistema 
cada vez que la estructura de las tablas es modificada.

Para prevenir esta arbitrariedad una de las mejores soluciones sería realizar las encuestas dentro de esta 
misma plataforma, centralizando de esta manera la fuente de la información y permitiendo trabajar y controlar 
la información con una menor carga de trabajo.




<p float="left">
  <img src="blob/master/logo-uai.png" alt="drawing" width="300" height="112"/>
  <img src="blob/master/Logo_Alumni.png" alt="drawing" width="367" height="112"/>
</p>



  