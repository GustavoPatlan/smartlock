from info import session, render_template, request, redirect, url_for, TOPIC_COMANDOS, TOPIC_CHEQUEO, json
from config.db import encontrar_locker, asignar_locker, encontrar_locker_abrir, liberar_locker, encontrar_usuario, actualizar_usuario, actualizar_llave_usuario, eliminar_usuario, encontrar_solicitud
from config.functions import action_required, generar_codigo_numeros, validar_correo, generar_codigo, mandar_correo
from mqtt.mqtt import mqtt_client

def  configuracionRutasUser(app):
    @app.route('/home')
    @action_required
    def home():
        usuario = session.get("usuario")
        datos = encontrar_locker_abrir(usuario[0])
        mqtt_client.publish(TOPIC_CHEQUEO, json.dumps(("CHECAR",) + datos), qos=1)
        return render_template('home.html', usuario = usuario)
    
    @app.route('/home/locker', methods=['POST', 'GET'])
    @action_required
    def solicitar_casillero():
        if request.method == 'GET':
            return redirect('/cancel')
        usuario = session.get("usuario")
        data = request.json
        accion = data.get('accion')
        if accion == 'SOLICITAR':
            casillero = encontrar_locker()
            if casillero:
                correo = usuario[0]
                codigo = generar_codigo_numeros(6)
                asignar_locker(codigo, casillero, correo)
                session["usuario"] = [usuario[0], usuario[1], usuario[2], usuario[3], casillero[1], codigo, 
                                    casillero[2], casillero[3],  casillero[4], casillero[5]]
                return {"status": "redirect", "url": url_for('home'), 'mensaje': 'Casillero Asignado Exitosamente', 'accion': '4'}
            else:
                return {"status": "alerta",'mensaje': 'No se asigno el Casillero'}
        else:
            return {"status": "alerta",'mensaje': 'No se asigno el Casillero'}
    
    @app.route('/home/locker/open', methods=['POST', 'GET'])
    @action_required
    def abrir_casillero():
        if request.method == 'GET':
            return redirect('/cancel')
        data = request.json
        accion = data.get('accion')
        if accion == 'ABRIR':
            usuario = session.get("usuario")
            datos = encontrar_locker_abrir(usuario[0])
            mqtt_client.publish(TOPIC_COMANDOS, json.dumps(datos), qos=1)
            return {"status": "alerta"}
    
    @app.route('/home/locker/finish', methods=['POST', 'GET'])
    @action_required
    def finalizar_casillero():
        if request.method == 'GET':
            return redirect('/cancel')
        usuario = session.get("usuario")
        data = request.json
        accion = data.get('accion')
        if accion == 'FINALIZAR':
            usuario = session.get("usuario")
            datos = encontrar_locker_abrir(usuario[0])
            liberar_locker(usuario[0], datos)
            session["usuario"] = [usuario[0], usuario[1], usuario[2], usuario[3], 'SIN ASIGNAR', 'SIN ASIGNAR', 
                                  'SIN ASIGNAR', 'SIN ASIGNAR',  'SIN ASIGNAR', 'SIN ASIGNAR']
            return {"status": "redirect", "url": url_for('home'), 'mensaje': 'Casillero Finalizado', 'accion': '4'}
        else: return {"status": "redirect", "url": url_for('home'), 'mensaje': 'Error de Finalización', 'accion': '3'}
    
    @app.route('/history')
    @action_required
    def history():
        usuario = session.get("usuario")
        correo = usuario[0]
        solicitudes = encontrar_solicitud(correo)
        return render_template('history.html', solicitudes = solicitudes, usuario = usuario[0])
    
    @app.route('/profile')
    @action_required
    def profile():
        usuario = session.get("usuario")
        return render_template('profile.html', usuario = usuario)
    
    @app.route('/profile/code', methods=['POST', 'GET'])
    def profile_code():
        if request.method == 'GET':
            return redirect('/cancel')
        data = request.json
        correo = data.get('correo')
        usuario = session.get("usuario")
        validar = validar_correo(correo)
        if correo == usuario[0]:
            accion = 1
        elif validar is False:
            accion = 0
            return {"status": "error",'mensaje': 'Formato de Correo Electrónico Incorrecto'}
        else:
            resultado = encontrar_usuario(correo)
            if resultado:
                accion = 0
                return {"status": "alerta",'mensaje': 'Usuario ya Registrado'}
            else: accion = 1
        if accion == 1:
            session["code"] = patron = generar_codigo(6)
            mandar_correo(patron, correo)
            return {"status": "openDialog", "mensaje": 'Codigo Enviado'}
        else:
            return {"status": "OK"}
        
    @app.route('/profile/update', methods=['POST', 'GET'])
    def profile_update():
        if request.method == 'GET':
            return redirect('/cancel')
        data = request.json
        correo_nuevo = data.get('correo')
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        codigo = data.get('codigo')
        codigoSesion = session.get("code")
        usuario = session.get("usuario")
        correo = usuario[0]
        if codigo != codigoSesion:
            return {"status": "alerta",'mensaje': 'Codigo Incorrecto'}
        elif codigo == codigoSesion:
            actualizar_usuario(correo_nuevo, nombre, apellido, correo)
            session["usuario"] = [correo_nuevo, nombre, apellido, usuario[3], usuario[4], usuario[5], 
                                    usuario[6], usuario[7],  usuario[8], usuario[9]]
            return {"status": "redirect", "url": url_for('profile'), 'mensaje': 'Datos Actualizados Exitosamente', 'accion': '4'}
        return {"status": "OK"}
    
    @app.route('/profile/pass', methods=['POST', 'GET'])
    def profile_pass():
        if request.method == 'GET':
            return redirect('/cancel')
        data = request.json
        correo = data.get('correo')
        llave = data.get('llave')
        usuario = session.get("usuario")
        if correo == usuario[0]:
            actualizar_llave_usuario(correo, llave)
            session["usuario"] = [usuario[0], usuario[1], usuario[2], llave, usuario[4], usuario[5], 
                                    usuario[6], usuario[7],  usuario[8], usuario[9]]
            return {"status": "closeDialog"}
        return {"status": "OK"}
    
    @app.route('/profile/delete', methods=['POST', 'GET'])
    def profile_delete():
        if request.method == 'GET':
            return redirect('/cancel')
        usuario = session.get("usuario")
        data = request.json
        accion = data.get('accion')
        correo = usuario[0]
        if accion == 'ACEPTAR':
            session.clear()
            eliminar_usuario(correo)
            return {"status": "redirect", "url": url_for('login'), 'mensaje': 'Usuario Eliminado Correctamente', 'accion': '4'}
        return {"status": "OK"}