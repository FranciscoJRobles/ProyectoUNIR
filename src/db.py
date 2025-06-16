import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

load_dotenv()

# Configuración de la base de datos MySQL en Azure
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_PORT=os.getenv("MYSQL_PORT")     
MYSQL_SSL_CA=os.getenv("MYSQL_SSL_CA")


def get_database_uri():
    return (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
        f"?ssl_ca={MYSQL_SSL_CA}" if MYSQL_SSL_CA else
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )


# Instancia global de SQLAlchemy (debe ser importada en los modelos)
db = SQLAlchemy()


# Función para inicializar la base de datos con la app Flask
def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

