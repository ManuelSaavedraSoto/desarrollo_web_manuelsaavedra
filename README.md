# Tarea 2 - Manuel Saavedra

## Decisiones de Diseño

## Estructura del Proyecto
```
.
├── README.md                    
├── requirements.txt             
└── src                          
    ├── app.py                   
    ├── db                       
    │   ├── connection.py        
    │   ├── __init__.py          
    │   ├── models.py            
    │   └── sql                  
    │       ├── dummy-activities.
    │       ├── region-comuna.sql
    │       └── tarea2.sql       
    ├── static                   
    │   ├── css                  
    │   │   └── style.css        
    │   ├── js                   
    │   │   ├── activity_form.js 
    │   │   ├── activity_list.js 
    │   │   └── common_ui.js     
    │   ├── media                
    │   │   └── placeholder.png  
    │   └── uploads                    
    │       ├── cat_1.jpg        
    │       ├── cat_2.jpg        
    │       ├── cat_3.jpg        
    │       ├── cat_4.jpg        
    │       ├── cat_5.jpg        
    │       ├── cat_6.jpg        
    │       ├── cat_7.jpg        
    │       └── cat_8.jpg        
    ├── templates                
    │   ├── activity_detail.html 
    │   ├── activity_form.html   
    │   ├── activity_list.html   
    │   ├── activity_stats.html  
    │   ├── index.html           
    │   └── layout.html          
    └── utils                    
        ├── __init__.py          
        ├── utils.py             
        └── validation.py                                                                                                   
```

## Decisiones de Diseño

### Linting y Formato

Utiliće PyLint junto a Python Black para forzar y mantener un estilo de código estándar y legible para comodidad
personal y al momento de revisar la tarea.

### Diseño de Interfaz (UI/UX)

Seguí el diseño establecido anteriormente pero agregué más definiciones en el archivo `.css` como se sugirió 
en los comentarios de la revisión de la Tarea 1.

Respecto a notificaciones de usuario lo implemente mediante toasters que son menos molestos que alertas y 
se pueden implementar solamente con JavaScript y CSS sin tener que importar los mensajes flash de Flask.

### Conexión con DB

Para la conexión con la base de datos seguí el esquema que se establecé en las tutoriales de SQLAlchemy y Flask

### App de Flask

Para la app principal decidí separar las funciones auxiliares y de validación en un módulo distinto para mantener
la legibilidad, la única excepción es ```handle_activity_post()``` ya que esta necesita el request y actúa 
más como una extensión de la ruta de POST que derechamente una función auxiliar "aislada".

Por otra parte, implemente rutas "API" para poder tomar ventaja de funciones asincrónicas en el formulario y
listado de actividades, evitando redireccionar de forma innecesaria y mejorar el dinamismo de la página.

### Templates

Principalmente fueron refactorizados para utilizar templating de Jinja2 y reducir el código duplicado.

### Scripting

Se añadieron más scripts tanto para manejo de UI y validación de formularios como para conexiones asíncronas con
la base de datos y poder cargar información que de otra forma tendría que cargarse mediante templates de Jinja2 
y elementos ocultos en HTML o constantemente realizar requests nuevos.

Para legibilidad y no importar scripts innecesarios, se separaron los scripts en tres archivos.

### Base de Datos

Se dejo un archivo que genera datos "dummy" junto a las imágenes necesarias en la carpeta correspondiente para 
poder probar la página de forma adecuada.