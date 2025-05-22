# pylint: disable=too-few-public-methods
"""Module that uses WTForms for comments."""

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    DateTimeField,
    IntegerField,
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
    activity_id = IntegerField(
        validators=[validators.InputRequired()], render_kw={"hidden": True}
    )
    date = DateTimeField(
        validators=[validators.InputRequired()], render_kw={"hidden": True}
    )
