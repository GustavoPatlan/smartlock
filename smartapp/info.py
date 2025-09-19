# Librerias
from flask import Flask, render_template, session, redirect, request, url_for
from flask_socketio import SocketIO, emit
from flask_mail import Mail, Message
from dotenv import load_dotenv
from pathlib import Path
import paho.mqtt.client as mqtt
import threading, json, os, pytz

# Carga las variables del archivo .env
dotenv_path = Path('secret/.env')
load_dotenv(dotenv_path=dotenv_path)

# Configuración del servidor Backend
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRETKEY")  # Necesario para SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Configuración del correo
app.config["MAIL_SERVER"] = os.getenv("MAILSERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAILPORT"))
app.config["MAIL_USE_TLS"] =True
app.config["MAIL_USE_SSL"] =False
app.config["MAIL_USERNAME"] = os.getenv("MAILUSERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAILPASSWORD")
mail = Mail(app)

# Configuración MQTT
BROKER = os.getenv("BROKER")
PORT = int(os.getenv("PORT"))
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

TOPIC_RESPUESTA = "casillero/respuestas"
TOPIC_PANTALLA = "casillero/pantalla"
TOPIC_COMANDOS = "casillero/comando"
TOPIC_CHEQUEO = "casillero/check"