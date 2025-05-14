"""Utility functions for the project."""

import os
from datetime import datetime
from werkzeug.utils import secure_filename
from db import Actividad, ContactarPor, ActividadTema, Foto
from .validation import validate_photo

# Constants
THEME_MAPPING = {
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


def get_inputs(req):
    """Extracts and validates inputs from the request."""
    inputs = {
        "email": req.form.get("email"),
        "phone": req.form.get("telefono"),
        "start_time": req.form.get("init-input"),
        "end_time": req.form.get("end-input"),
        "comuna_id": req.form.get("comuna"),
        "region_id": req.form.get("region"),
        "name": req.form.get("name"),
        "description": req.form.get("description"),
        "sector": req.form.get("sector"),
        "themes": [],
    }

    theme_inputs = [
        (key, req.form[key]) for key in req.form if key.startswith("theme-")
    ]

    for key, value in theme_inputs:
        if value == "Otro":
            other_theme_value = req.form.get("other-theme")
            if other_theme_value:
                inputs["themes"].append(other_theme_value)
        else:
            inputs["themes"].append(value)

    inputs["contact_methods"] = [
        req.form[f"contact-method-{i}"]
        for i in range(len(req.form))
        if f"contact-method-{i}" in req.form
    ]

    inputs["photo_1"] = req.files.get("foto-input-1")

    return inputs


def create_activity(inputs):
    """Creates an activity object from the validated inputs.

    If end_time is not provided or equals default (start_time + 3 hours),
    it will be stored as None in the database.
    """
    start_time = datetime.strptime(inputs["start_time"], "%Y-%m-%dT%H:%M")

    # Calculate default end time (start time + 3 hours)
    default_end = start_time.replace(hour=(start_time.hour + 3) % 24)
    if start_time.hour + 3 >= 24:
        default_end = default_end.replace(day=start_time.day + 1)

    # Check if end time is provided and doesn't match default
    end_time = None
    if inputs.get("end_time") and inputs["end_time"].strip():
        actual_end = datetime.strptime(inputs["end_time"], "%Y-%m-%dT%H:%M")
        if actual_end != default_end:
            end_time = actual_end

    activity = Actividad(
        comuna_id=inputs["comuna_id"],
        sector=inputs["sector"],
        nombre=inputs["name"],
        email=inputs["email"],
        celular=inputs["phone"],
        dia_hora_inicio=start_time,
        dia_hora_termino=end_time,  # Will be None if not provided or matches default
        descripcion=inputs["description"],
    )
    return activity


def process_photos(session, req, actividad_id, upload_folder):
    """Process and save activity photos.

    Args:
        session: Database session
        req: Flask request object
        actividad_id: ID of the activity
        upload_folder: Path to upload directory

    Raises:
        ValueError: If there's an error saving the photo files
    """
    for i in range(1, 6):
        photo_key = f"foto-input-{i}"
        if photo_key not in req.files:
            continue

        photo = req.files[photo_key]
        if not validate_photo(photo):
            continue

        ext = os.path.splitext(secure_filename(photo.filename))[1].lower()
        new_filename = f"{actividad_id}_{i}{ext}"
        photo_path = os.path.join("uploads", new_filename)
        full_path = os.path.join(upload_folder, new_filename)

        try:
            photo.save(full_path)
            foto = Foto(
                ruta_archivo=photo_path,
                nombre_archivo=new_filename,
                actividad_id=actividad_id,
            )
            session.add(foto)
        except IOError as io_err:
            raise ValueError(
                f"Error al guardar archivo de foto: {str(io_err)}"
            ) from io_err


def process_themes(session, themes, actividad_id):
    """Process and save activity themes.

    Args:
        session: The database session
        themes: List of theme names
        actividad_id: ID of the activity to link themes to
    """
    for theme_value in themes:
        tema = ActividadTema(
            tema=THEME_MAPPING.get(theme_value, "otro"),
            glosa_otro=None if theme_value in THEME_MAPPING else theme_value,
            actividad_id=actividad_id,
        )
        session.add(tema)


def process_contact_methods(session, req, actividad_id):
    """Process and save activity contact methods."""
    i = 0
    while f"contact-method-{i}" in req.form:
        method = req.form[f"contact-method-{i}"]
        identifier = req.form[f"contact-identifier-{i}"]
        contacto = ContactarPor(
            nombre=get_normalized_contact_method(method),
            identificador=identifier,
            actividad_id=actividad_id,
        )
        session.add(contacto)
        i += 1
