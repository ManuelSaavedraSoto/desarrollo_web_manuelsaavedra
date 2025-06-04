# Tarea 3 - Manuel Saavedra

## Estructura del Proyecto
```
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
    │   │   ├── activity_detail.js
    │   │   ├── activity_form.js
    │   │   ├── activity_list.js
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
        ├── activity_detail.html
        ├── activity_form.html
        ├── activity_list.html
        ├── activity_page.html
        ├── activity_stats.html
        ├── index.html
        └── layout.html                                                                                                  
```

## Decisiones de Diseño

### WTForms & Flask-WTF

Para simplificar y estandarizar el proceso de validación de formularios, reestructure el código para utilizar WTForms.  
De esta forma no me tengo que preocupar de hacer un proceso de validación para cada campo de cada formulario.

### Formulario de Comentario

Siguiendo la misma lógica de simplificar el manejo de formularios, los comentarios no incluyen un campo de fecha-hora  
ya que esta se calcula al momento de subir el comentario a la base de datos. La razón es para evitar spoofing de la  
fecha y garantizar que todas estarán basadas en el mismo marco de referencia, la hora del servidor al momento de  
procesar el formulario.