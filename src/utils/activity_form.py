# pylint: disable=too-few-public-methods
"""WTForms for activities."""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import (
    StringField,
    SelectField,
    TextAreaField,
    EmailField,
    TelField,
    BooleanField,
    DateTimeLocalField,
    validators,
)

FILENAME_REGEXP = r"^([\/].+)+\.(jpg|png|jpeg)$"

RRSS_MAPPING = [
    ("WhatsApp", "whatsapp"),
    ("Telegram", "telegram"),
    ("X", "X"),
    ("Instagram", "instagram"),
    ("Tik-Tok", "tiktok"),
    ("Otro", "otra"),
]

THEME_MAPPING = [
    ("Música", "música"),
    ("Deporte", "deporte"),
    ("Ciencias", "ciencias"),
    ("Religión", "religión"),
    ("Política", "política"),
    ("Tecnología", "tecnología"),
    ("Juegos", "juegos"),
    ("Baile", "baile"),
    ("Comida", "comida"),
    ("Otro", "otro"),
]


class RequiredGroup:
    """Validates that at least one field of the group has data."""

    def __init__(self, field_group, message=None):
        self.field_group = field_group
        if not message:
            message = f"At least one field from {self.field_group} must be provided."
        self.message = message

    def __call__(self, form, field):
        is_valid = bool(field.data)
        for other_field_name in self.field_group:
            other_field = form._fields.get(other_field_name)
            is_valid = is_valid or bool(other_field.data)
        if not is_valid:
            raise validators.ValidationError(self.message)


class RequiredIfThenLength(validators.InputRequired):
    """If the target field has data, validate that this field has data of a given length"""

    def __init__(
        self, other_field_name, *args, min=-1, max=-1, message=None, **kwargs
    ):  # pylint: disable=redefined-builtin
        self.other_field_name = other_field_name
        self.min = min
        self.max = max
        if not message:
            message = f"Field must be between {min} and {max} characters long."
        self.message = message
        super().__init__(*args, **kwargs)
        self.field_flags = {}

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception(  # pylint: disable=broad-exception-raised
                f"no field named {self.other_field_name} in form"
            )
        if bool(other_field.data):
            l = field.data and len(field.data) or 0
            if l < self.min or self.max != -1 and l > self.max:
                raise validators.ValidationError(self.message)


class ActivityForm(FlaskForm):
    """Form for activity submission."""

    region = SelectField(
        "Region",
        [validators.InputRequired(message="Región es requerida")],
        choices=[("", "Seleccione una región.", {"disabled": True, "hidden": True})],
    )
    comuna = SelectField(
        "Comuna",
        [validators.InputRequired(message="Comuna es requerida")],
        choices=[("", "Seleccione una comuna.", {"disabled": True, "hidden": True})],
        render_kw={"disabled": True},
    )
    sector = TextAreaField(
        "Sector", [validators.Length(message="Máximo 100 caracteres", max=100)]
    )
    nombre = StringField(
        "Nombre",
        [
            validators.InputRequired(message="Nombre es requerido."),
            validators.Length(max=200, message="Largo máximo 200 caracteres."),
        ],
    )
    email = EmailField(
        "Email",
        [
            validators.InputRequired(message="Email es requerido."),
            validators.Email(message="No cumple con formato de email."),
        ],
    )
    telefono = TelField(
        "Teléfono",
        [
            validators.DataRequired(message="Teléfono es requerido."),
            validators.Regexp(
                r"\+[0-9]{3}\.[0-9]{8}", message="No cumple con formato de teléfono."
            ),
        ],
        render_kw={"placeholder": "+123.12345678"},
    )
    rrss_0_check = BooleanField(
        "WhatsApp",
        [
            validators.Optional(),
        ],
    )
    rrss_1_check = BooleanField(
        "Telegram",
        [
            validators.Optional(),
        ],
    )
    rrss_2_check = BooleanField(
        "X",
        [
            validators.Optional(),
        ],
    )
    rrss_3_check = BooleanField(
        "Instagram",
        [
            validators.Optional(),
        ],
    )
    rrss_4_check = BooleanField(
        "Tik-Tok",
        [
            validators.Optional(),
        ],
    )
    rrss_5_check = BooleanField(
        "Otro",
        [
            RequiredGroup(
                [
                    "rrss_0_check",
                    "rrss_1_check",
                    "rrss_2_check",
                    "rrss_3_check",
                    "rrss_4_check",
                ],
                "Método de Contacto es obligatorio.",
            ),
        ],
    )
    rrss_0_user = StringField(
        "Usuario de WhatsApp",
        [
            RequiredIfThenLength(
                "rrss_0_check",
                min=4,
                max=50,
                message="Falto agregar contacto de WhatsApp.",
            )
        ],
        render_kw={"disabled": True, "placeholder": "Usuario de WhatsApp"},
    )
    rrss_1_user = StringField(
        "Usuario de Telegram",
        [
            RequiredIfThenLength(
                "rrss_1_check",
                min=4,
                max=50,
                message="Falto agregar contacto de Telegram.",
            )
        ],
        render_kw={"disabled": True, "placeholder": "Usuario de Telegram"},
    )
    rrss_2_user = StringField(
        "Usuario de X",
        [
            RequiredIfThenLength(
                "rrss_2_check", min=4, max=50, message="Falto agregar contacto de X."
            )
        ],
        render_kw={"disabled": True, "placeholder": "Usuario de X"},
    )
    rrss_3_user = StringField(
        "Usuario de Instagram",
        [
            RequiredIfThenLength(
                "rrss_3_check",
                min=4,
                max=50,
                message="Falto agregar contacto de Instagram.",
            )
        ],
        render_kw={"disabled": True, "placeholder": "Usuario de Instagram"},
    )
    rrss_4_user = StringField(
        "Usuario de Tik-Tok",
        [
            RequiredIfThenLength(
                "rrss_4_check",
                min=4,
                max=50,
                message="Falto agregar contacto de Tik-Tok.",
            )
        ],
        render_kw={"disabled": True, "placeholder": "Usuario de Tik-Tok"},
    )
    rrss_5_user = StringField(
        "Otro",
        [
            RequiredIfThenLength(
                "rrss_5_check", min=4, max=50, message="Falto agregar otro contacto."
            )
        ],
        render_kw={"disabled": True, "placeholder": "Otra red social..."},
    )
    date_start = DateTimeLocalField(
        "Día/Hora de Inicio",
        [validators.InputRequired(message="La fecha y hora de inicio son requeridas.")],
    )
    date_end = DateTimeLocalField(
        "Dia/Hora de Término", [validators.Optional()], render_kw={"disabled": True}
    )
    descripcion = TextAreaField(
        "Descripción",
        [
            validators.InputRequired(
                message="La descripción de la actividad es requerida."
            )
        ],
        render_kw={"cols": 50, "rows": 10},
    )
    theme_0 = BooleanField(
        "Música",
        [
            validators.Optional(),
        ],
    )
    theme_1 = BooleanField(
        "Deporte",
        [
            validators.Optional(),
        ],
    )
    theme_2 = BooleanField(
        "Ciencias",
        [
            validators.Optional(),
        ],
    )
    theme_3 = BooleanField(
        "Religión",
        [
            validators.Optional(),
        ],
    )
    theme_4 = BooleanField(
        "Política",
        [
            validators.Optional(),
        ],
    )
    theme_5 = BooleanField(
        "Tecnología",
        [
            validators.Optional(),
        ],
    )
    theme_6 = BooleanField(
        "Juegos",
        [
            validators.Optional(),
        ],
    )
    theme_7 = BooleanField(
        "Baile",
        [
            validators.Optional(),
        ],
    )
    theme_8 = BooleanField(
        "Comida",
        [
            validators.Optional(),
        ],
    )
    theme_9 = BooleanField(
        "Otro",
        [
            RequiredGroup(
                [
                    "theme_0",
                    "theme_1",
                    "theme_2",
                    "theme_3",
                    "theme_4",
                    "theme_5",
                    "theme_6",
                    "theme_7",
                    "theme_8",
                    "theme_9",
                ],
                "Tema es obligatorio.",
            ),
        ],
    )
    theme_9_text = StringField(
        "Otro tema",
        [
            RequiredIfThenLength(
                "theme_9",
                min=3,
                max=15,
                message="Falto descripción de otro tema, o no es de 3 a 15 caracteres.",
            )
        ],
        render_kw={"disabled": True, "placeholder": "Otro tema..."},
    )
    photo_0 = FileField(
        "Foto 1",
        [
            FileRequired(message="La primera foto es obligatoria."),
            FileAllowed(["jpg", "png", "jpeg"], message="El formato es erroneo."),
        ],
    )
    photo_1 = FileField(
        "Foto 2",
        [
            FileAllowed(["jpg", "png", "jpeg"], message="El formato es erroneo."),
        ],
    )
    photo_2 = FileField(
        "Foto 3",
        [
            FileAllowed(["jpg", "png", "jpeg"], message="El formato es erroneo."),
        ],
    )
    photo_3 = FileField(
        "Foto 4",
        [
            FileAllowed(["jpg", "png", "jpeg"], message="El formato es erroneo."),
        ],
    )
    photo_4 = FileField(
        "Foto 5",
        [
            FileAllowed(["jpg", "png", "jpeg"], message="El formato es erroneo."),
        ],
    )
