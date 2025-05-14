"""Validation functions for the project."""

import os
import re
from datetime import datetime, timedelta
from sqlalchemy import text

# Constants
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
VALID_THEMES = {
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


def allowed_file(filename):
    """Checks if the file has an allowed extension.

    Args:
        filename: The name of the file to check

    Returns:
        bool: True if the file extension is allowed, False otherwise
    """
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
    """Validates the format and logic of start and end datetime strings.

    Args:
        start_time: Start datetime in ISO format
        end_time: Optional end datetime in ISO format. If not provided or matches
                 default (start_time + 3 hours), validation passes.

    Returns:
        bool: True if the datetimes are valid, False otherwise
    """
    try:
        start = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
        now = datetime.now()

        # Start time must be in the future
        if start < now:
            return False

        # If no end time provided, validation passes
        if not end_time or not end_time.strip():
            return True

        end = datetime.fromisoformat(end_time.replace("Z", "+00:00"))

        # Calculate default end time (start + 3 hours)
        default_end = start.replace(hour=(start.hour + 3) % 24)
        if start.hour + 3 >= 24:
            default_end = default_end.replace(day=start.day + 1)

        # If end time matches default, it's valid
        if end == default_end:
            return True

        # Otherwise ensure it's at least 1 hour after start
        min_end = start + timedelta(hours=1)
        return end >= min_end

    except (ValueError, AttributeError):
        return False


def validate_themes(themes):
    """Validates the themes selected by the user."""
    custom_themes = [t for t in themes if t not in VALID_THEMES]
    return all(3 <= len(theme) <= 15 for theme in custom_themes)


def validate_contact_method(method):
    """Validates the contact method selected by the user."""
    return method.lower() in {
        "whatsapp",
        "telegram",
        "x",
        "instagram",
        "tik-tok",
        "otra",
    }


def validate_comuna(session, comuna_id, region_id):
    """Validates if the comuna belongs to the specified region."""
    try:
        result = session.execute(
            text(
                "SELECT 1 FROM comuna WHERE id = :comuna_id AND region_id = :region_id LIMIT 1"
            ),
            {"comuna_id": comuna_id, "region_id": region_id},
        ).first()
        return bool(result)
    except (ValueError, TypeError):
        return False


def validate_photo(photo):
    """Validates the uploaded photo file.

    Args:
        photo: The uploaded file object to validate

    Returns:
        bool: True if the photo is valid, False otherwise
    """
    if not photo or not photo.filename:
        return False
    if not allowed_file(photo.filename):
        return False
    try:
        photo.seek(0, os.SEEK_END)
        size = photo.tell()
        if size > MAX_FILE_SIZE:
            return False
        photo.seek(0)
        return True
    except (OSError, IOError):
        return False


def validate_inputs(inputs, session):
    """Validates the inputs extracted from the request."""
    validation_rules = [
        (
            not inputs["comuna_id"] or not inputs["region_id"],
            "Debe seleccionar una región y comuna",
        ),
        (
            not validate_comuna(session, inputs["comuna_id"], inputs["region_id"]),
            "La comuna seleccionada no pertenece a la región indicada",
        ),
        (not inputs["email"], "El email es obligatorio"),
        (not validate_email(inputs["email"]), "El formato del email es inválido"),
        (not inputs["phone"], "El teléfono es obligatorio"),
        (
            not validate_phone(inputs["phone"]),
            "El formato del teléfono es inválido (debe ser +XXX.XXXXXXXX)",
        ),
        (not inputs["start_time"], "La fecha y hora de inicio son obligatorias"),
        (
            not validate_datetime(inputs["start_time"], inputs.get("end_time")),
            (
                "La fecha/hora de término debe ser posterior a la de inicio"
                if inputs.get("end_time")
                else "La fecha/hora de inicio debe ser futura"
            ),
        ),
        (not inputs["themes"], "Debe seleccionar al menos un tema"),
        (
            not validate_themes(inputs["themes"]),
            "Los temas seleccionados son inválidos o"
            + " el tema personalizado debe tener entre 3 y 15 caracteres",
        ),
        (
            not inputs["contact_methods"],
            "Debe seleccionar al menos un método de contacto",
        ),
        (
            any(not validate_contact_method(m) for m in inputs["contact_methods"]),
            "Método de contacto inválido",
        ),
        (
            not inputs["photo_1"] or not inputs["photo_1"].filename,
            "La primera foto es obligatoria",
        ),
        (
            not validate_photo(inputs["photo_1"]),
            "La primera foto debe ser un archivo de imagen válido (PNG/JPG) menor a 5MB",
        ),
    ]

    return [error for condition, error in validation_rules if condition]
