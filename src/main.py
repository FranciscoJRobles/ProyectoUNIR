from flask import Flask
from src.routes.task_routes import create_tasks_blueprint

app = Flask(__name__)
app.register_blueprint(create_tasks_blueprint())

if __name__ == '__main__':
    app.run(debug=True)
