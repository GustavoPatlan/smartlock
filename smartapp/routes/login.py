from info import redirect, session, render_template, request, url_for
from config.functions import validar_correo, generar_codigo, mandar_correo
from config.db import encontrar_usuario, actualizar_llave_usuario, agregar_usuario

def  configuracionRutasLogin(app):
    @app.route('/login')
    def login():
        session.clear()
        return render_template('login.html')
    
    @app.route('/login/in', methods=['POST', 'GET'])
    def login_in():
        if request.method == 'GET':
            return redirect('/cancel')
        data = request.json
        correo = data.get('correo')
        llave = data.get('llave')
        resultado = encontrar_usuario(correo)
        if resultado is None:
            return {"status": "error",'mensaje': 'Usuario Inexistente'}
        elif resultado[3] == llave:
            session["usuario"] = resultado
            return {"status": "redirect", "url": url_for('home'), 'mensaje': 'Inicio de Sesión Exitoso', 'accion': '4'}
        else:
            return {"status": "alerta",'mensaje': 'Contraseña Incorrecta'}
        
    @app.route('/code')
    def code():
        return render_template('code.html')
    
    @app.route('/code/generate', methods=['POST', 'GET'])
    def code_generate():
        if request.method == 'GET':
            return redirect('/cancel')
        data = request.json
        correo = data.get('correo')
        validar = validar_correo(correo)
        if validar is False:
            return {"status": "error",'mensaje': 'Formato de Correo Electrónico Incorrecto'}
        else:
            resultado = encontrar_usuario(correo)
            if resultado is None:
                return {"status": "error",'mensaje': 'Usuario Inexistente'}
            else:
                session["code"] = patron = generar_codigo(6)
                mandar_correo(patron, correo)
                return {"status": "estado",'mensaje': 'Codigo Enviado'}
            
    @app.route('/code/check', methods=['POST', 'GET'])
    def code_check():
        if request.method == 'GET':
            return redirect('/cancel')
        data = request.json
        correo = data.get('correo')
        codigo = data.get('codigo')
        codigoSesion = session.get("code")
        if codigo != codigoSesion:
            return {"status": "alerta",'mensaje': 'Codigo Incorrecto'}
        elif codigo == codigoSesion:
            session["code"] = correo
            return {"status": "estado",'mensaje': 'Ingresa una nueva Contraseña'}
        return {"status": "OK"}
    
    @app.route('/password/new', methods=['POST', 'GET'])
    def password_new():
        if request.method == 'GET':
            return redirect('/cancel')
        data = request.json
        key = data.get('key')
        correo = session.get("code")
        session.clear()
        actualizar_llave_usuario(correo, key)
        return {"status": "redirect", "url": url_for('login'), 'mensaje': 'Contraseña Actualizada', 'accion': '4'}
    
    @app.route('/register')
    def register():
        return render_template('register.html')
    
    @app.route('/register/generate', methods=['POST', 'GET'])
    def register_generate():
        if request.method == 'GET':
            return redirect('/cancel')
        data = request.json
        correo = data.get('correo')
        validar = validar_correo(correo)
        if validar is False:
            return {"status": "error",'mensaje': 'Formato de Correo Electrónico Incorrecto'}
        else:
            resultado = encontrar_usuario(correo)
            if resultado:
                return {"status": "alerta",'mensaje': 'Usuario ya Registrado'}
            else:
                session["code"] = patron = generar_codigo(6)
                mandar_correo(patron, correo)
                return {"status": "estado",'mensaje': 'Codigo Enviado'}
            
    @app.route('/register/add', methods=['POST', 'GET'])
    def register_add():
        if request.method == 'GET':
            return redirect('/cancel')
        data = request.json
        key = data.get('llave')
        correo = data.get('correo')
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        codigo = data.get('codigo')
        codigoSesion = session.get("code")
        if codigo != codigoSesion:
            return {"status": "error",'mensaje': 'Codigo Incorrecto'}
        elif codigo == codigoSesion:
            session.clear()
            agregar_usuario(correo, nombre, apellido, key)
            return {"status": "redirect", "url": url_for('login'), 'mensaje': 'Usuario Registrado Exitosamente', 'accion': '4'}
        return {"status": "OK"}