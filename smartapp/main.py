from info import app, socketio, redirect, session, BROKER, PORT, threading
from mqtt.mqtt import mqtt_client
from routes.login import configuracionRutasLogin
from routes.user import configuracionRutasUser

configuracionRutasLogin(app)
configuracionRutasUser(app)

@app.route('/')
def index():
    return redirect('/login')    

@app.route('/cancel')
def cancel():
    session.clear()
    return redirect('/login')

# Iniciar MQTT en un hilo separado
def iniciar_mqtt():
    mqtt_client.connect(BROKER, PORT, 60)
    mqtt_client.loop_forever()

if __name__ == '__main__':
    threading.Thread(target=iniciar_mqtt, daemon=True).start()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)