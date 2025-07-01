# Tarea 4 - Manuel Saavedra

## Estructura del Proyecto

Aquí se detalla la estructura de directorios y archivos del proyecto.

Generada mediante el comando `tree -I '.**/|tmp.txt|target|enunciado.pdf'` en Bash.
```bash
.
├── HELP.md
├── mvnw
├── mvnw.cmd
├── pom.xml
├── README.md
└── src
    ├── main
    │   ├── java
    │   │   └── com
    │   │       └── web
    │   │           └── apps
    │   │               └── tarea4
    │   │                   ├── ActivityRepository.java
    │   │                   └── Tarea4Application.java
    │   └── resources
    │       ├── application.properties
    │       ├── static
    │       │   ├── css
    │       │   │   └── style.css
    │       │   └── js
    │       │       └── script.js
    │       ├── templates
    │       │   ├── _eval_tooltip.html
    │       │   └── index.html
    │       └── uploads
    │           ├── cat_1.jpg
    │           ├── cat_2.jpg
    │           ├── cat_3.jpg
    │           ├── cat_4.jpg
    │           ├── cat_5.jpg
    │           ├── cat_6.jpg
    │           ├── cat_7.jpg
    │           └── cat_8.jpg
    └── test
        └── java
            └── com
                └── web
                    └── apps
                        └── tarea4
                            └── Tarea4ApplicationTests.java                                                              
```

## Decisiones de Diseño

- **Separación de responsabilidades:** Se implementó un repositorio (`ActivityRepository`) para encapsular el acceso a la base de datos, mejorando la seguridad y mantenibilidad del código.
- **Validación robusta:** Tanto en el backend como en el frontend se valida que el puntaje ingresado sea un entero entre 1 y 7, mostrando mensajes de error claros al usuario si no se cumple esta condición.
- **Frontend reactivo:** El frontend actualiza la tabla y el puntaje de manera dinámica usando JavaScript y AJAX, sin recargar la página.
- **Uso de fragmentos:** Se utilizan fragmentos de Thymeleaf para mantener separada la definición del tooltip de la página principal.
