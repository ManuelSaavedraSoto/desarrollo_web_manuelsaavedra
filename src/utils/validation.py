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


def validate_contact_method(method, identifier=None):
    """Validates the contact method and its identifier if provided.

    Args:
        method: The contact method to validate
        identifier: Optional identifier to validate for the given method

    Returns:
        bool: True if both method and identifier (if provided) are valid, False otherwise
    """
    # Validate method name
    if not method.lower() in {
        "whatsapp",
        "telegram",
        "x",
        "instagram",
        "tik-tok",
        "otra",
    }:
        return False

    # Validate identifier if provided
    if identifier is not None:
        if len(identifier) < 4 or len(identifier) > 50:
            return False

    return True


def get_contact_method_error(method=None, identifier=None):
    """Generates error message for contact method validation failures.

    Args:
        method: The contact method being validated
        identifier: The identifier being validated

    Returns:
        str: An appropriate error message based on the validation failure
    """
    if method and not method.lower() in {
        "whatsapp",
        "telegram",
        "x",
        "instagram",
        "tik-tok",
        "otra",
    }:
        return f"Método de contacto '{method}' no es válido"

    if identifier and (len(identifier) < 4 or len(identifier) > 50):
        return f"El identificador para {method} debe tener entre 4 y 50 caracteres"

    return "Debe seleccionar al menos un método de contacto válido"


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


def validate_selected_region(inputs):
    """Validates if there is a selected region and comuna."""
    return bool(inputs["region_id"] and inputs["comuna_id"])


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


def validate_photos(inputs):
    """Validates the uploaded photos.

    Args:
        inputs: The dictionary containing the uploaded files

    Returns:
        bool: True if all photos are valid, False otherwise
    """
    if not validate_photo(inputs["photo_1"]):
        return False
    for photo in inputs["opt-photos"]:
        if photo and not validate_photo(photo):
            return False
    return True


def validate_inputs(inputs, session):
    """Validates the inputs extracted from the request."""
    validation_rules = {
        "location": {
            "region": {
                "id": "region-select",
                "check": lambda: not validate_selected_region(inputs),
                "message": "Debe seleccionar una región y comuna",
            },
            "comuna": {
                "id": "comuna-select",
                "check": lambda: validate_selected_region(inputs)
                and not validate_comuna(
                    session, inputs["comuna_id"], inputs["region_id"]
                ),
                "message": "La comuna seleccionada no pertenece a la región indicada",
            },
        },
        "contact": {
            "name": {
                "id": "name-input",
                "check": lambda: not inputs["name"],
                "message": "El nombre es obligatorio",
            },
            "email": {
                "id": "email-input",
                "check": lambda: not inputs["email"],
                "message": "El email es obligatorio",
            },
            "email_format": {
                "id": "email-input",
                "check": lambda: inputs["email"]
                and not validate_email(inputs["email"]),
                "message": "El formato del email es inválido",
            },
            "phone": {
                "id": "tel-input",
                "check": lambda: not inputs["phone"],
                "message": "El teléfono es obligatorio",
            },
            "phone_format": {
                "id": "tel-input",
                "check": lambda: inputs["phone"]
                and not validate_phone(inputs["phone"]),
                "message": "El formato del teléfono es inválido (debe ser +XXX.XXXXXXXX)",
            },
        },
        "datetime": {
            "init": {
                "id": "init-datetime",
                "check": lambda: not inputs["start_time"],
                "message": "La fecha y hora de inicio son obligatorias",
            },
            "end": {
                "id": "end-datetime",
                "check": lambda: not validate_datetime(
                    inputs["start_time"], inputs.get("end_time")
                ),
                "message": lambda: (
                    "La fecha/hora de término debe ser posterior a la de inicio"
                    if inputs.get("end_time")
                    else "La fecha/hora de inicio debe ser futura"
                ),
            },
        },
        "themes": {
            "no_selection": {
                "id": "theme-inputs",
                "check": lambda: not inputs["themes"],
                "message": "Debe seleccionar al menos un tema",
            },
            "invalid": {
                "id": "theme-inputs",
                "check": lambda: inputs["themes"]
                and not validate_themes(inputs["themes"]),
                "message": (
                    "Los temas seleccionados son inválidos o "
                    + "el tema personalizado debe tener entre 3 y 15 caracteres"
                ),
            },
        },
        "contact_methods": {
            "no_selection": {
                "id": "contact-methods",
                "check": lambda: not inputs["contact_methods"],
                "message": "Debe seleccionar al menos un método de contacto",
            },
            "invalid": {
                "id": "contact-inputs",
                "check": lambda: inputs["contact_methods"]
                and any(
                    not validate_contact_method(method, identifier)
                    for method, identifier in inputs["contact_methods"].items()
                ),
                "message": get_contact_method_error(
                    inputs["contact_methods"], inputs.get("identifier")
                ),
            },
        },
        "photos": {
            "no_selection": {
                "id": "foto-input-1",
                "check": lambda: not inputs["photo_1"]
                or not inputs["photo_1"].filename,
                "message": "La primera foto es obligatoria",
            },
            "format": {
                "id": "photo-inputs",
                "check": lambda: not validate_photos(inputs),
                "message": (
                    "Fotos deben ser un archivo "
                    + "de imagen válido (PNG/JPG) menor a 5MB"
                ),
            },
        },
    }

    errors = {}
    for category, error_types in validation_rules.items():
        for error_type, rule in error_types.items():
            if rule["check"]():
                message = rule["message"]
                if callable(message):
                    message = message()
                if category not in errors:
                    errors[category] = {}
                errors[category][error_type] = {"msg": message, "id": rule["id"]}
    return errors
