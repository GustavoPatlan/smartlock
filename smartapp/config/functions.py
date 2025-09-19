from info import session, redirect, app, Message, mail, pytz
from datetime import datetime
import string, random, re

# Decorador para restringir acceso (Usuario)
def action_required(f):
    def wrap(*args, **kwargs):
        if 'usuario' not in session:
            return redirect('/cancel')
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

def mandar_correo_alerta(correo):
    with app.app_context():
        asunto = "Alerta de aperura"
        mensaje = f"Tu casillero esta abierto"
        msg = Message(asunto, sender=app.config["MAIL_USERNAME"], recipients=[correo])
        msg.body = mensaje
        mail.send(msg)

def generar_codigo_numeros(longitud=6):
    numeros = string.digits
    return "".join(random.choice(numeros) for _ in range(longitud))

# Validar Correo
def validar_correo(correo):
    patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(patron, correo) is not None

def generar_codigo(longitud=6):
    caracteres = string.ascii_letters + string.digits
    return "".join(random.choice(caracteres) for _ in range(longitud))

def mandar_correo(patron, correo):
    with app.app_context():
        asunto = "Código de Confirmación"
        mensaje = f"Tu código de confirmación es: {patron}"
        msg = Message(asunto, sender=app.config["MAIL_USERNAME"], recipients=[correo])
        msg.body = mensaje
        mail.send(msg)

def obtenerHorario():
    # Zona horaria de Ciudad de México
    zona = pytz.timezone("America/Mexico_City")
    ahora = datetime.now(zona)

    # Separar hora y fecha
    hora_actual = ahora.time().strftime("%H:%M:%S")
    fecha_actual = ahora.date()
    return [hora_actual, fecha_actual]