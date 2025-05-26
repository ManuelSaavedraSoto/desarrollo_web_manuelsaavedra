# pylint: disable=too-few-public-methods
"""Module that uses WTForms for comments."""

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    HiddenField,
    validators,
)


class CommentForm(FlaskForm):
    """Form for comments"""

    name = StringField(
        "Nombre", [validators.InputRequired(), validators.Length(min=3, max=80)]
    )
    text = TextAreaField(
        "Comentario", [validators.InputRequired(), validators.Length(min=5)]
    )
    activity_id = HiddenField()
