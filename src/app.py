from flask import Flask, request, jsonify, render_template, abort
from db.db import Session, Region, Comuna, Actividad, Foto, ContactarPor, ActividadTema
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

session = Session()

@app.route('/', methods=['GET'])
def index():
    actividades = session.query(Actividad).order_by(Actividad.dia_hora_inicio.desc()).limit(5).all()
    return render_template('index.html', actividades=actividades)

@app.route('/actividades', methods=['GET'])
def activityList():
    actividades = session.query(Actividad).order_by(Actividad.dia_hora_inicio.desc()).all()
    return render_template('activity_list.html', actividades=actividades)

@app.route('/estadisticas', methods=['GET'])
def activityStats():
    # Get all activities
    activities = session.query(Actividad).all()
    
    # Prepare data for charts
    activities_data = []
    for activity in activities:
        themes = [t.glosa_otro if t.tema == 'otro' else t.tema for t in activity.temas]
        activities_data.append({
            'start': activity.dia_hora_inicio.strftime('%d-%m-%Y %H:%M'),
            'themes': themes
        })
    
    # Get theme statistics
    theme_counts = {}
    for activity in activities:
        for tema in activity.temas:
            if tema.tema == 'otro':
                theme_counts['Otros'] = theme_counts.get('Otros', 0) + 1
            else:
                theme_counts[tema.tema] = theme_counts.get(tema.tema, 0) + 1
    
    # Convert data to JSON for JavaScript
    chart_data = {
        'activities': activities_data,
        'theme_counts': theme_counts
    }
    
    return render_template('activity_stats.html', chart_data=json.dumps(chart_data))

@app.route('/actividades/subir', methods=['GET', 'POST'])
def activityForm():
    regiones = session.query(Region).all()
    if request.method == 'POST':
        try:
            # Create activity record first to get the ID
            actividad = Actividad(
                comuna_id=request.form.get('comuna'),
                sector=request.form.get('sector'),
                nombre=request.form.get('name'),
                email=request.form.get('email'),
                celular=request.form.get('telefono'),
                dia_hora_inicio=request.form.get('init-input'),
                dia_hora_termino=request.form.get('end-input'),
                descripcion=request.form.get('description')
            )
            session.add(actividad)
            session.flush()  # This will assign an ID to actividad

            # Process photos
            photo_count = 0
            for i in range(1, 6):
                photo_key = f'foto-input-{i}'
                if photo_key in request.files:
                    print(f"Processing {photo_key}")
                    # Check if the file is present
                    photo = request.files[photo_key]
                    if photo.filename != '':
                        print(f"File found: {photo.filename}")
                        # Get file extension from original filename
                        ext = os.path.splitext(secure_filename(photo.filename))[1].lower()
                        photo_count += 1
                        
                        # Create new filename with activity_id and photo number
                        new_filename = f'{actividad.id}_{photo_count}{ext}'
                        photo_path = os.path.join('uploads', new_filename)
                        full_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                        
                        # Save the photo
                        photo.save(full_path)
                        
                        foto = Foto(
                            ruta_archivo=photo_path,
                            nombre_archivo=new_filename,
                            actividad_id=actividad.id
                        )
                        session.add(foto)

            # Process other activity data (themes, contact methods, etc.)
            session.commit()
            return jsonify({'message': 'Actividad registrada exitosamente'})
        except Exception as e:
            session.rollback()
            return jsonify({'error': str(e)}), 500
            
    return render_template('activity_form.html', regiones=regiones)

@app.route('/actividades/<int:activity_id>', methods=['GET'])
def activityDetail(activity_id):
    activity = session.query(Actividad).filter_by(id=activity_id).first()
    if not activity:
        abort(404)
    return render_template('activity_detail.html', actividad=activity)