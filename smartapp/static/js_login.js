let notificacion = document.getElementById("notificacion");
let mensaje = document.getElementById("mensaje");
let icono = document.getElementById("notification_icon");
let icono_forma = document.getElementById("icon_form");

function mostrarNotificacionRequest(texto, color, iconoNombre) {
    mensaje.innerText = texto;
    icono.style.background = color;
    icono_forma.setAttribute('name', iconoNombre);
    notificacion.style.display = "flex";

    setTimeout(() => {
        notificacion.style.display = "none";
    }, 4000);
}

function usuario() {
    let correo = document.getElementById("email").value;
    let llave = document.getElementById("key").value;

    if (correo === '') {
        mostrarNotificacionRequest('Correo Ausente', 'dodgerblue', 'notifications-outline');
    } else if (llave === '') {
        mostrarNotificacionRequest('Contraseña Ausente', 'dodgerblue', 'notifications-outline');
    } else {
        fetch('/login/in', {
            method: 'POST',
            body: JSON.stringify({ correo: correo, llave: llave }),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                switch (data.status) {
                    case 'error':
                        mostrarNotificacionRequest(data.mensaje, 'crimson', 'flash-outline');
                        break;
                    case 'alerta':
                        mostrarNotificacionRequest(data.mensaje, 'goldenrod', 'alert-outline');
                        break;
                    case 'redirect':
                        sessionStorage.setItem("notificacion_mensaje", data.mensaje);
                        sessionStorage.setItem("notificacion_accion", data.accion);
                        window.location.href = data.url;
                        break;
                }
            });
    }
}

function usuarioRegistro() {
    let correo = document.getElementById("email");
    let llave = document.getElementById("key");
    let nombre = document.getElementById("nombre");
    let apellido = document.getElementById("apellido");

    if (correo.value === '' || llave.value === '' || nombre.value === '' || apellido.value === '') {
        mostrarNotificacionRequest('Datos Faltantes', 'dodgerblue', 'notifications-outline');
    } else {
        fetch('/register/generate', {
            method: 'POST',
            body: JSON.stringify({ correo: correo.value }),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                switch (data.status) {
                    case 'error':
                        mostrarNotificacionRequest(data.mensaje, 'crimson', 'flash-outline');
                        break;
                    case 'alerta':
                        mostrarNotificacionRequest(data.mensaje, 'goldenrod', 'alert-outline');
                        break;
                    case 'estado':
                        mostrarNotificacionRequest(data.mensaje, 'dodgerblue', 'notifications-outline');
                        let button = document.getElementById("button_again");

                        document.getElementById("code_input").style.display = "flex";
                        document.getElementById("tittle_code_input").style.display = "block";

                        correo.disabled = true;
                        nombre.disabled = true;
                        apellido.disabled = true;
                        llave.disabled = true;
                        button.innerText = "Reenviar";
                        button.style.textDecoration = "line-through";
                        button.style.pointerEvents = "none";
                        button.disabled = true;

                        setTimeout(() => {
                            button.style.textDecoration = "none";
                            button.style.pointerEvents = "auto";
                            button.disabled = false;
                        }, 6000);
                        break;
                }
            });
    }
}

function usuarioAgregar() {
    let correo = document.getElementById("email").value;
    let llave = document.getElementById("key").value;
    let nombre = document.getElementById("nombre").value;
    let apellido = document.getElementById("apellido").value;
    let codigo = document.getElementById("code").value;

    if (codigo === '') {
        mostrarNotificacionRequest('Codigo Ausente', 'dodgerblue', 'notifications-outline');
    } else {
        fetch('/register/add', {
            method: 'POST',
            body: JSON.stringify({ correo: correo, llave: llave, nombre: nombre, apellido: apellido, codigo: codigo }),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                switch (data.status) {
                    case 'error':
                        mostrarNotificacionRequest(data.mensaje, 'crimson', 'alert-outline');
                        break;
                    case 'redirect':
                        sessionStorage.setItem("notificacion_mensaje", data.mensaje);
                        sessionStorage.setItem("notificacion_accion", data.accion);
                        window.location.href = data.url;
                        break;
                }
            });
    }
}

function enviarCodigo() {
    let correo = document.getElementById("email").value;

    if (correo === '') {
        mostrarNotificacionRequest('Correo Ausente', 'dodgerblue', 'notifications-outline');
    }
    else {
        fetch('/code/generate', {
            method: 'POST',
            body: JSON.stringify({ correo: correo }),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                switch (data.status) {
                    case 'error':
                        mostrarNotificacionRequest(data.mensaje, 'crimson', 'flash-outline');
                        break;
                    case 'alerta':
                        mostrarNotificacionRequest(data.mensaje, 'goldenrod', 'alert-outline');
                        break;
                    case 'estado':
                        mostrarNotificacionRequest(data.mensaje, 'dodgerblue', 'notifications-outline');
                        let button = document.getElementById("button_again");

                        document.getElementById("code_input").style.display = "flex";
                        document.getElementById("tittle_code_input").style.display = "block";

                        correo.disabled = true;
                        button.innerText = "Reenviar";
                        button.style.textDecoration = "line-through";
                        button.style.pointerEvents = "none";
                        button.disabled = true;

                        setTimeout(() => {
                            button.style.textDecoration = "none";
                            button.style.pointerEvents = "auto";
                            button.disabled = false;
                        }, 6000);
                        break;
                }
            });
    }
}

function verificarCodigo() {
    let correo = document.getElementById("email").value;
    let codigo = document.getElementById("code").value;

    if (codigo === '') {
        mostrarNotificacionRequest('Codigo Ausente', 'dodgerblue', 'notifications-outline');
    }
    else {
        fetch('/code/check', {
            method: 'POST',
            body: JSON.stringify({ correo: correo, codigo: codigo }),
            headers: { 'Content-Type': 'application/json' }
        })

            .then(response => response.json())
            .then(data => {
                switch (data.status) {
                    case 'alerta':
                        mostrarNotificacionRequest(data.mensaje, 'goldenrod', 'alert-outline');
                        break;
                    case 'estado':
                        mostrarNotificacionRequest(data.mensaje, 'dodgerblue', 'notifications-outline');
                        document.getElementById("panel_code").style.display = "none";
                        document.getElementById("panel_pass").style.display = "flex";
                        break;
                }
            });
    }
}

function actualizarLlave() {
    let key = document.getElementById("key").value;

    if (key === '') {
        mostrarNotificacionRequest('Contraseña Ausente', 'dodgerblue', 'notifications-outline');
    }
    else {
        fetch('/password/new', {
            method: 'POST',
            body: JSON.stringify({ key: key }),
            headers: { 'Content-Type': 'application/json' }
        })

            .then(response => response.json())
            .then(data => {
                if (data.status === "redirect") {
                    sessionStorage.setItem("notificacion_mensaje", data.mensaje);
                    sessionStorage.setItem("notificacion_accion", data.accion);
                    window.location.href = data.url;
                }
            });
    }
}

function togglePassword() {
    let passwordInput = document.getElementById("key");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
};
