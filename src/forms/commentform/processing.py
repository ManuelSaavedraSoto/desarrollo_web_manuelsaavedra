"""Module for processing comment forms"""

import datetime
from flask import jsonify
from db import Comentario
from .form import CommentForm


def process_comment(session, form: CommentForm, timestamp: datetime.datetime):
    """Retrieves and sorts"""
    try:
        name = form.name.data
        text = form.text.data
        activity_id = form.activity_id.data

        comment = Comentario(
            actividad_id=activity_id,
            nombre=name,
            texto=text,
            fecha=timestamp,
        )

        session.add(comment)
        session.commit()

        return jsonify({"success": True}), 200
    except ValueError as val_err:
        session.rollback()
        return jsonify({"error": str(val_err)}), 400
    except Exception as err:  # pylint: disable=broad-except
        session.rollback()
        return jsonify({"error": f"Error inesperado: {str(err)}"}), 500
