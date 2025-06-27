import os
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from src.routes.task_routes import create_tasks_blueprint
from src.routes.user_story_routes import create_user_stories_blueprint
from src.db import init_db

# Configura la ruta absoluta a la carpeta templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'src','templates')

app = Flask(__name__, template_folder=TEMPLATES_DIR)

# Configuración diferente para desarrollo vs producción
if os.environ.get('FLASK_ENV') == 'production':
    app.debug = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'production-secret-key')
else:
    app.debug = True
    app.config['SECRET_KEY'] = 'dev'  # Necesario para la toolbar
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False  # Opcional, para no interceptar redirecciones
    toolbar = DebugToolbarExtension(app)
init_db(app)
app.register_blueprint(create_tasks_blueprint())
app.register_blueprint(create_user_stories_blueprint())

if __name__ == '__main__':
    with app.app_context():
        from src.models.task import Task
        from src.models.user_story import UserStory
        # Crea las tablas si no existen
        from src.db import db
        db.create_all()
    
    # Configuración diferente para desarrollo vs producción
    if os.environ.get('FLASK_ENV') == 'production':
        app.run(host="0.0.0.0", port=5000, debug=False)
    else:
        app.run(host="0.0.0.0", port=5000, debug=True)
