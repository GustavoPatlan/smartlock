from info import mqtt, TOPIC_COMANDOS, TOPIC_PANTALLA, TOPIC_RESPUESTA, TOPIC_CHEQUEO, json, socketio, USER, PASSWORD, url_for
from config.db import encontrar_locker_correo, encontrar_locker_pantalla, agregar_solicitud
from config.functions import mandar_correo_alerta, obtenerHorario

# Cliente MQTT
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(" * Conectado al broker MQTT")
        client.subscribe([(TOPIC_RESPUESTA, 0), (TOPIC_PANTALLA, 0), (TOPIC_COMANDOS, 0), (TOPIC_CHEQUEO, 0)])
    else:
        print(f" * Error de conexión MQTT: {rc}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        # print(data)
        
        # Procesar diferente según el tema
        if msg.topic == TOPIC_RESPUESTA:
            # Lógica para TOPIC_RESPUESTA
            dataCasillero = data['casillero']
            infoLocker = data['locker']
            estadoLocker = data['estado']
            resultado = encontrar_locker_correo(dataCasillero, infoLocker)
            if resultado:
                socketio.emit('actualizacion_casillero', [resultado[0], estadoLocker])
                if estadoLocker == 'ABIERTO':
                    horario = obtenerHorario()
                    agregar_solicitud(resultado[0], horario, dataCasillero, infoLocker)
                    socketio.emit('actualizacion_historial', [resultado[0], str(horario[0]), str(horario[1]), dataCasillero, infoLocker[0], infoLocker[2]+','+infoLocker[3]])
                    mandar_correo_alerta(resultado[0])
        elif msg.topic == TOPIC_PANTALLA:
            # Lógica para TOPIC_PANTALLA
            locker = data['locker']
            resultado = encontrar_locker_pantalla(data['codigo'], locker)
            if resultado:
                datos = [resultado[0], locker[0], locker[1], locker[2], locker[3]]
                client.publish(TOPIC_COMANDOS, json.dumps(datos), qos=1)
        elif msg.topic == TOPIC_CHEQUEO:
            if data[0] == 'RESPUESTA':
                dataCasillero = data[2]
                infoLocker = data[3:]
                resultado = encontrar_locker_correo(dataCasillero, infoLocker)
                socketio.emit('actualizacion_alerta', [resultado[0], data[1]])
    except Exception as e:
        print(f" * Error al procesar mensaje MQTT: {e}")

# Configuración de MQTT
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.tls_set()  # Habilita TLS
mqtt_client.username_pw_set(USER, PASSWORD)