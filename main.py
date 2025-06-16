from flask import Flask
from src.routes.task_routes import create_tasks_blueprint
from src.routes.user_story_routes import create_user_stories_blueprint
from src.db import init_db

app = Flask(__name__)
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
    app.run(debug=True)
