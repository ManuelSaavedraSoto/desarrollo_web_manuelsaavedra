# Tarea 3 - Manuel Saavedra

## Estructura del Proyecto

Aquí se detalla la estructura de directorios y archivos del proyecto.

Generada mediante el comando `tree` de Bash.
```bash
.
├── README.md
├── requirements.txt
└── src
    ├── app.py
    ├── db
    │   ├── connection.py
    │   ├── __init__.py
    │   ├── models.py
    │   └── sql
    │       ├── dummy-activities.sql
    │       ├── region-comuna.sql
    │       ├── tabla-comentario.sql
    │       └── tarea2.sql
    ├── forms
    │   ├── activityform
    │   │   ├── form.py
    │   │   ├── __init__.py
    │   │   └── processing.py
    │   ├── commentform
    │   │   ├── form.py
    │   │   ├── __init__.py
    │   │   └── processing.py
    │   └── __init__.py
    ├── static
    │   ├── css
    │   │   └── style.css
    │   ├── js
    │   │   ├── activities
    │   │   │   ├── details.js
    │   │   │   ├── list.js
    │   │   │   └── upload_form.js
    │   │   └── code.js
    │   ├── media
    │   │   └── placeholder.png
    │   └── uploads
    │       ├── cat_1.jpg
    │       ├── cat_2.jpg
    │       ├── cat_3.jpg
    │       ├── cat_4.jpg
    │       ├── cat_5.jpg
    │       ├── cat_6.jpg
    │       ├── cat_7.jpg
    │       └── cat_8.jpg
    └── templates
        ├── activities
        │   ├── details.html
        │   ├── list.html
        │   ├── _page.html
        │   ├── stats.html
        │   └── upload_form.html
        ├── errors
        │   ├── 400.html
        │   └── 404.html
        ├── index.html
        └── layout.html
                                                                                           
```

## Decisiones de Diseño

### Reorganización del código

Reorganize el proyecto dado que ha aumentado la cantidad de templates, scripts y código de Python 
para mejorar la estructura de directorios y mantener la legibilidad.

### WTForms & Flask-WTF

Para simplificar y estandarizar el proceso de validación de formularios, reestructure el código para utilizar WTForms.  
De esta forma no me tengo que preocupar de hacer un proceso de validación para cada campo de cada formulario.

### Formulario de Comentario

Siguiendo la misma lógica de simplificar el manejo de formularios, los comentarios no incluyen un campo de fecha-hora  
ya que esta se calcula al momento de subir el comentario a la base de datos. La razón es para evitar spoofing de la  
fecha y garantizar que todas estarán basadas en el mismo punto de referencia, la hora del servidor al momento de  
procesar el formulario.

#### Dummy data

Para probar que funciona el sistema de comentarios se extendió la información dummy para incluir comentarios.

### Gráficos

Para los gráficos utilicé la librería `chart.js` ya que estaba implementada de antes y la he utilizado en proyectos 
anteriores por lo que me resultaba personalmente familiar.

De manera similar, los gráficos ya se generaban con información de la base de datos en la versión anterior, por lo  
que el cambio principal fue separar esa lógica de la ruta `/estadisticas`, moverla a la ruta `/api/actividades/stats`  
y asegurar que el script interactúe con la nueva API de forma correcta.

### Validación en Frontend & Backend

Para mantener una cadena de validación coherente, los formularios no se envían al backend a menos que aprueben la 
validación en frontend.  
Es posible forzar enviar el formulario al backend para visualizar los mensajes de error que este genera llamando 
la función `submitForm()` en la consola del navegador web.

### Manejo de errores 400 y 404

Se agregaron templates básicos para explícitamente manejar errores de tipo 400 y 404 causados por URLs 
maliciosos o erróneos.