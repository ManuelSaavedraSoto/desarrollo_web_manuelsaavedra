"""Aplicación Flask para tarea 2 del curso CC5002"""

import os
import re
import json
from datetime import datetime
from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    abort,
)
from werkzeug.utils import secure_filename
from db.db import Session, Region, Comuna, Actividad, Foto, ContactarPor, ActividadTema

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "static", "uploads"
)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.teardown_appcontext
def cleanup():
    """Cleanup function to remove the session after each request."""
    Session.remove()


def allowed_file(filename):
    """Checks if the file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_email(email):
    """Validates the format of an email address."""
    pattern = (
        r"^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9]"
        + r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9]"
        + r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    )
    return bool(re.match(pattern, email))


def validate_phone(phone):
    """Validates the format of a phone number."""
    pattern = r"\+[0-9]{3}\.[0-9]{8}"
    return bool(re.match(pattern, phone))


def validate_datetime(start_time, end_time=None):
    """Validates the format and logic of start and end datetime strings."""
    try:
        # Convert string to datetime object
        start = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
        if end_time:
            if not end_time.strip():  # Allow empty end time
                return True
            end = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
            if end <= start:
                return False

        # Validate that start time is not in the past
        now = datetime.now()
        if start < now:
            return False

        return True
    except (ValueError, AttributeError):
        return False


def validate_themes(themes):
    """Validates the themes selected by the user."""
    valid_themes = {
        "Música",
        "Deporte",
        "Ciencias",
        "Religión",
        "Política",
        "Tecnología",
        "Juegos",
        "Baile",
        "Comida",
        "Otro",
    }
    for theme_value in themes:
        if theme_value not in valid_themes:
            # For "otro" theme type, validate the custom text length
            if not 3 <= len(theme_value) <= 15:
                return False
    return True


def validate_contact_method(method):
    """Validates the contact method selected by the user."""
    method_mapping = {
        "whatsapp": "whatsapp",
        "telegram": "telegram",
        "x": "X",
        "instagram": "instagram",
        "tik-tok": "tiktok",
        "otra": "otra",
    }
    return method.lower() in method_mapping


def get_normalized_contact_method(method):
    """Normalizes the contact method to a standard format."""
    method_mapping = {
        "whatsapp": "whatsapp",
        "telegram": "telegram",
        "x": "X",
        "instagram": "instagram",
        "tik-tok": "tiktok",
        "otra": "otra",
    }
    return method_mapping.get(method.lower(), method.lower())


def validate_comuna(comuna_id, region_id):
    """Validates if the comuna belongs to the specified region."""
    try:
        session = Session()
        comuna = (
            session.query(Comuna).filter_by(id=comuna_id, region_id=region_id).first()
        )
        return comuna is not None
    except (ValueError, TypeError):
        return False


def validate_photo(photo):
    """Validates the uploaded photo file."""
    if not photo or not photo.filename:
        return False
    if not allowed_file(photo.filename):
        return False
    try:
        # Check file size (limit to 5MB)
        photo.seek(0, os.SEEK_END)
        size = photo.tell()
        if size > 5 * 1024 * 1024:  # 5MB
            return False
        photo.seek(0)  # Reset file pointer
        return True
    except (OSError, IOError):
        return False


@app.route("/", methods=["GET"])
def index():
    """Route for the main page."""
    session = Session()
    try:
        actividades = (
            session.query(Actividad)
            .order_by(Actividad.dia_hora_inicio.desc())
            .limit(5)
            .all()
        )
        return render_template("index.html", actividades=actividades)
    finally:
        session.close()


@app.route("/actividades", methods=["GET"])
def activity_list():
    """Route for the activity list page."""
    session = Session()
    try:
        actividades = (
            session.query(Actividad).order_by(Actividad.dia_hora_inicio.desc()).all()
        )
        return render_template("activity_list.html", actividades=actividades)
    finally:
        session.close()


@app.route("/estadisticas", methods=["GET"])
def activity_stats():
    """Route for the activity statistics page."""
    session = Session()
    try:
        # Get all activities
        activities = session.query(Actividad).all()

        # Prepare data for charts
        activities_data = []
        for activity in activities:
            themes = [
                t.glosa_otro if t.tema == "otro" else t.tema.capitalize()
                for t in activity.temas
            ]
            activities_data.append(
                {
                    "start": activity.dia_hora_inicio.strftime("%d-%m-%Y %H:%M"),
                    "themes": themes,
                }
            )

        # Get theme statistics with capitalization
        theme_counts = {}
        for activity in activities:
            for tema in activity.temas:
                if tema.tema == "otro":
                    theme_counts["Otros"] = theme_counts.get("Otros", 0) + 1
                else:
                    capitalized_theme = tema.tema.capitalize()
                    theme_counts[capitalized_theme] = (
                        theme_counts.get(capitalized_theme, 0) + 1
                    )

        # Convert data to JSON for JavaScript
        chart_data = {"activities": activities_data, "theme_counts": theme_counts}

        return render_template("activity_stats.html", chart_data=json.dumps(chart_data))
    finally:
        session.close()


@app.route("/actividades/subir", methods=["GET", "POST"])
def activity_form():
    """Route for the activity upload form."""
    session = Session()
    try:
        if request.method == "GET":
            regiones = session.query(Region).all()
            return render_template("activity_form.html", regiones=regiones)

        # Handle POST request
        try:
            # Validate inputs
            email = request.form.get("email")
            phone = request.form.get("telefono")
            start_time = request.form.get("init-input")
            end_time = request.form.get("end-input")
            comuna_id = request.form.get("comuna")
            region_id = request.form.get("region")

            # Get all theme-related form fields
            theme_inputs = [
                (key, request.form[key])
                for key in request.form
                if key.startswith("theme-")
            ]
            themes = []
            for key, value in theme_inputs:
                if value == "Otro":
                    # Get the "other" theme text from the same index
                    other_theme_value = request.form.get("other-theme")
                    if other_theme_value:
                        themes.append(other_theme_value)
                else:
                    themes.append(value)

            contact_methods = [
                request.form[f"contact-method-{i}"]
                for i in range(len(request.form))
                if f"contact-method-{i}" in request.form
            ]

            # Validate all fields and collect errors
            errors = []

            if not comuna_id or not region_id:
                errors.append("Debe seleccionar una región y comuna")
            elif not validate_comuna(comuna_id, region_id):
                errors.append(
                    "La comuna seleccionada no pertenece a la región indicada"
                )

            if not request.form.get("name"):
                errors.append("El nombre del organizador es obligatorio")

            if not email:
                errors.append("El email es obligatorio")
            elif not validate_email(email):
                errors.append("El formato del email es inválido")

            if not phone:
                errors.append("El teléfono es obligatorio")
            elif not validate_phone(phone):
                errors.append(
                    "El formato del teléfono es inválido (debe ser +XXX.XXXXXXXX)"
                )

            if not start_time:
                errors.append("La fecha y hora de inicio son obligatorias")
            elif not validate_datetime(start_time, end_time):
                if end_time:
                    errors.append(
                        "La fecha/hora de término debe ser posterior a la de inicio"
                    )
                else:
                    errors.append("La fecha/hora de inicio debe ser futura")

            if not themes:
                errors.append("Debe seleccionar al menos un tema")
            elif not validate_themes(themes):
                errors.append(
                    "Los temas seleccionados son inválidos "
                    + "o el tema personalizado debe tener entre 3 y 15 caracteres"
                )

            if not contact_methods:
                errors.append("Debe seleccionar al menos un método de contacto")
            for method in contact_methods:
                if not validate_contact_method(method):
                    errors.append("Método de contacto inválido")

            # Validate first photo is present
            first_photo = request.files.get("foto-input-1")
            if not first_photo or not first_photo.filename:
                errors.append("La primera foto es obligatoria")
            elif not validate_photo(first_photo):
                errors.append(
                    "La primera foto debe ser un archivo de imagen válido (PNG/JPG) menor a 5MB"
                )

            if errors:
                return jsonify({"error": " | ".join(errors)}), 400

            # Create activity record
            actividad = Actividad(
                comuna_id=comuna_id,
                sector=request.form.get("sector"),
                nombre=request.form.get("name"),
                email=email,
                celular=phone,
                dia_hora_inicio=datetime.strptime(start_time, "%Y-%m-%dT%H:%M"),
                dia_hora_termino=(
                    datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
                    if end_time and end_time.strip()
                    else None
                ),
                descripcion=request.form.get("description"),
            )
            session.add(actividad)
            session.flush()

            # Process photos with validation
            photo_count = 0
            for i in range(1, 6):
                photo_key = f"foto-input-{i}"
                if photo_key in request.files:
                    photo = request.files[photo_key]
                    if validate_photo(photo):
                        photo_count += 1
                        ext = os.path.splitext(secure_filename(photo.filename))[
                            1
                        ].lower()
                        new_filename = f"{actividad.id}_{photo_count}{ext}"
                        photo_path = os.path.join("uploads", new_filename)
                        full_path = os.path.join(
                            app.config["UPLOAD_FOLDER"], new_filename
                        )

                        try:
                            photo.save(full_path)
                            foto = Foto(
                                ruta_archivo=photo_path,
                                nombre_archivo=new_filename,
                                actividad_id=actividad.id,
                            )
                            session.add(foto)
                        except IOError:
                            session.rollback()
                            return (
                                jsonify({"error": "Error al guardar archivo de foto"}),
                                400,
                            )

            # Process themes with proper mapping
            theme_mapping = {
                "Música": "música",
                "Deporte": "deporte",
                "Ciencias": "ciencias",
                "Religión": "religión",
                "Política": "política",
                "Tecnología": "tecnología",
                "Juegos": "juegos",
                "Baile": "baile",
                "Comida": "comida",
            }

            for theme_value in themes:
                tema = ActividadTema(
                    tema=theme_mapping.get(theme_value, "otro"),
                    glosa_otro=None if theme_value in theme_mapping else theme_value,
                    actividad_id=actividad.id,
                )
                session.add(tema)

            # Process contact methods with normalization
            i = 0
            while f"contact-method-{i}" in request.form:
                method = request.form[f"contact-method-{i}"]
                identifier = request.form[f"contact-identifier-{i}"]
                contacto = ContactarPor(
                    nombre=get_normalized_contact_method(method),
                    identificador=identifier,
                    actividad_id=actividad.id,
                )
                session.add(contacto)
                i += 1

            session.commit()
            return jsonify({"success": True})
        except (IOError, ValueError, KeyError, AttributeError) as e:
            session.rollback()
            return jsonify({"error": f"Error inesperado: {str(e)}"}), 400
    finally:
        session.close()


@app.route("/actividades/<int:activity_id>", methods=["GET"])
def activity_detail(activity_id):
    """Route for the activity detail page."""
    session = Session()
    try:
        activity = session.query(Actividad).filter_by(id=activity_id).first()
        if not activity:
            abort(404)
        return render_template("activity_detail.html", actividad=activity)
    finally:
        session.close()
