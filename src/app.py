"""Aplicación Flask para tarea 2 del curso CC5002"""

import os
from flask import Flask, request, jsonify, render_template, abort, url_for
from db import db_init, Session, Region, Actividad
from utils import (
    get_inputs,
    create_activity,
    process_photos,
    process_themes,
    process_contact_methods,
    validate_inputs,
)

db_init()  # Initialize the database

app = Flask(__name__)

# Constants
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "static", "uploads"
)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.teardown_appcontext
def cleanup(exception=None):  # pylint: disable=unused-argument
    """Cleanup function to remove the session after each request."""
    Session.remove()


@app.route("/", methods=["GET"])
def index():
    """Route for the main page."""
    session = Session()
    try:
        # Get the last 5 activities by ID (most recent first)
        actividades = (
            session.query(Actividad).order_by(Actividad.id.desc()).limit(5).all()
        )
        return render_template("index.html", actividades=actividades)
    finally:
        session.close()


@app.route("/actividades", methods=["GET"])
def activity_list():
    """Route for the activity list page."""
    return render_template("activity_list.html")


@app.route("/actividades/subir", methods=["GET", "POST"])
def activity_form():
    """Route for the activity upload form."""
    session = Session()
    try:
        if request.method == "GET":
            regiones = session.query(Region).all()
            return render_template("activity_form.html", regiones=regiones)

        # Handle POST request
        return handle_activity_post(session, request)
    finally:
        session.close()


@app.route("/actividades/<int:activity_id>", methods=["GET"])
def activity_detail(activity_id):
    """Route for the activity detail page."""
    session = Session()
    try:
        # Sanitize activity_id
        if not isinstance(activity_id, int) or activity_id <= 0:
            abort(404)
        activity = session.query(Actividad).filter_by(id=activity_id).first()
        if not activity:
            abort(404)
        return render_template(
            "activity_detail.html",
            actividad=activity,
            def_src=url_for("static", filename="media/placeholder.png"),
        )
    finally:
        session.close()


@app.route("/estadisticas", methods=["GET"])
def activity_stats():
    """Route for the activity statistics page."""
    return render_template("activity_stats.html")


@app.route("/api/regiones", methods=["GET"])
def get_regiones():
    """API endpoint for fetching regiones and their comunas"""
    session = Session()
    try:
        regiones = session.query(Region).all()
        regiones_data = [
            {
                "id": region.id,
                "nombre": region.nombre,
                "comunas": [
                    {"id": comuna.id, "nombre": comuna.nombre}
                    for comuna in region.comunas
                ],
            }
            for region in regiones
        ]
        return jsonify(regiones_data)
    finally:
        session.close()

@app.route("/api/actividades")
def get_activities():
    """API endpoint for activities"""
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

        return jsonify(chart_data)
    finally:
        session.close()

@app.route("/api/actividades/paginated", methods=["POST"])
def get_paginated_activities():
    """API endpoint for paginated activities."""
    session = Session()
    try:
        page = request.form.get("page", 1, type=int)
        per_page = 5

        total_activities = session.query(Actividad).count()
        total_pages = (total_activities + per_page - 1) // per_page
        page = max(1, min(page, total_pages))

        activities = (
            session.query(Actividad)
            .order_by(Actividad.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        html = render_template("activity_page.html", actividades=activities)

        data = {
            "currentPage": page,
            "totalPages": total_pages,
            "html": html, 
        }

        return data
    finally:
        session.close()


def handle_activity_post(session, req):
    """Handles the POST request for activity creation."""
    try:
        inputs = get_inputs(req)
        errors = validate_inputs(inputs, session)

        if errors:
            return jsonify(errors), 400

        actividad = create_activity(inputs)
        session.add(actividad)
        session.flush()

        # Process all activity data
        process_photos(session, req, actividad.id, app.config["UPLOAD_FOLDER"])
        process_themes(session, inputs["themes"], actividad.id)
        process_contact_methods(session, req, actividad.id)

        session.commit()
        return jsonify({"success": True}), 200

    except ValueError as val_err:
        session.rollback()
        return jsonify({"error": str(val_err)}), 400
    except Exception as err:  # pylint: disable=broad-except
        session.rollback()
        return jsonify({"error": f"Error inesperado: {str(err)}"}), 500
