"""Utility functions for handling ActivityForms."""

import os
from flask import jsonify
from werkzeug.utils import secure_filename
from db import Actividad, ContactarPor, ActividadTema, Foto
from .form import ActivityForm


def get_inputs(form: ActivityForm):
    """Extracts and sorts inputs from the form."""
    inputs = {
        "region_id": form.region.data,
        "comuna_id": form.comuna.data,
        "sector": form.sector.data,
        "name": form.nombre.data,
        "email": form.email.data,
        "telefono": form.telefono.data,
        "rrss": [
            (form.rrss_0_check.data, form.rrss_0_user.data, "whatsapp"),
            (form.rrss_1_check.data, form.rrss_1_user.data, "telegram"),
            (form.rrss_2_check.data, form.rrss_2_user.data, "X"),
            (form.rrss_3_check.data, form.rrss_3_user.data, "instagram"),
            (form.rrss_4_check.data, form.rrss_4_user.data, "tiktok"),
            (form.rrss_5_check.data, form.rrss_5_user.data, "otra"),
        ],
        "start_time": form.date_start.data,
        "end_time": form.date_end.data,
        "description": form.descripcion.data,
        "themes": [
            (form.theme_0.data, "música"),
            (form.theme_1.data, "deporte"),
            (form.theme_2.data, "ciencias"),
            (form.theme_3.data, "religión"),
            (form.theme_4.data, "política"),
            (form.theme_5.data, "tencología"),
            (form.theme_6.data, "juegos"),
            (form.theme_7.data, "baile"),
            (form.theme_8.data, "comida"),
            (form.theme_9.data, "otro"),
        ],
        "other_theme": form.theme_9_text.data,
        "photos": [
            form.photo_0.data,
            form.photo_1.data,
            form.photo_2.data,
            form.photo_3.data,
            form.photo_4.data,
        ],
    }

    return inputs


def process_activity(session, inputs):
    """Creates an activity object from the validated inputs.

    If end_time is not provided or equals default (start_time + 3 hours),
    it will be stored as None in the database.
    """
    start_time = inputs["start_time"]

    # Calculate default end time (start time + 3 hours)
    default_end = start_time.replace(hour=(start_time.hour + 3) % 24)
    if start_time.hour + 3 >= 24:
        default_end = default_end.replace(day=start_time.day + 1)

    # Check if end time is provided and doesn't match default
    end_time = None
    if inputs.get("end_time"):
        actual_end = inputs["end_time"]
        if actual_end != default_end:
            end_time = actual_end

    activity = Actividad(
        comuna_id=inputs["comuna_id"],
        sector=inputs["sector"],
        nombre=inputs["name"],
        email=inputs["email"],
        celular=inputs["telefono"],
        dia_hora_inicio=start_time,
        dia_hora_termino=end_time,  # Will be None if not provided or matches default
        descripcion=inputs["description"],
    )
    session.add(activity)
    session.flush()

    return activity.id


def process_photos(session, inputs, actividad_id, upload_folder):
    """Process and save activity photos.

    Args:
        session: Database session
        inputs: Dictionary containing validated inputs including photos
        actividad_id: ID of the activity
        upload_folder: Path to upload directory

    Raises:
        ValueError: If there's an error saving the photo files
    """
    for i in range(0, 5):
        photo = inputs["photos"][i]
        if photo:
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


def process_themes(session, inputs, actividad_id):
    """Process and save activity themes.

    Args:
        session: The database session
        themes: List of theme names
        actividad_id: ID of the activity to link themes to
    """
    for check, theme in inputs["themes"]:
        if check:
            tema = ActividadTema(
                tema=theme,
                glosa_otro=None if theme != "otro" else inputs["other_theme"],
                actividad_id=actividad_id,
            )
            session.add(tema)


def process_rrss(session, inputs, actividad_id):
    """Process and save activity contact methods."""
    for check, username, rs in inputs["rrss"]:
        if check:
            contacto = ContactarPor(
                nombre=rs, identificador=username, actividad_id=actividad_id
            )
            session.add(contacto)


def process_activity_form(session, form: ActivityForm, path):
    """Processes the form to add the new activity to the db."""
    try:
        inputs = get_inputs(form)
        activity_id = process_activity(session, inputs)
        process_photos(session, inputs, activity_id, path)
        process_themes(session, inputs, activity_id)
        process_rrss(session, inputs, activity_id)
        session.commit()
        return jsonify({"success": True}), 200
    except ValueError as val_err:
        session.rollback()
        return jsonify({"error": str(val_err)}), 400
    except Exception as err:  # pylint: disable=broad-except
        session.rollback()
        return jsonify({"error": f"Error inesperado: {str(err)}"}), 500
