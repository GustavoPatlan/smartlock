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

let dialogUpdate = document.getElementById("updateDialog");
let dialogPass = document.getElementById("updatePass");
let dialogDelete = document.getElementById("deleteAccount");

function openDialogUpdate() {
    let correo = document.getElementById("email").value;
    let nombre = document.getElementById("nombre").value;
    let apellido = document.getElementById("apellido").value;

    if (correo === "" || nombre === "" || apellido === "") {
        mostrarNotificacionRequest('Falta Información', 'goldenrod', 'alert-outline');
    }
    else {
        fetch('/profile/code', {
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
                    case 'openDialog':
                        mostrarNotificacionRequest(data.mensaje, 'dodgerblue', 'notifications-outline');
                        dialogUpdate.showModal();
                        break;
                }
            });
    }
}

function closeDialogUpdate() {
    dialogUpdate.close();
}

function enviarCodigo() {
    let correo = document.getElementById("email").value;
    let nombre = document.getElementById("nombre").value;
    let apellido = document.getElementById("apellido").value;
    let codigo = document.getElementById("codeUpdate").value;

    if (codigo === "") {
        mostrarNotificacionRequest('Codigo Ausente', 'dodgerblue', 'notifications-outline');
    }
    else {
        fetch('/profile/update', {
            method: 'POST',
            body: JSON.stringify({ correo: correo, nombre: nombre, apellido: apellido, codigo: codigo }),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                switch (data.status) {
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

function openDialogPass() {
    dialogPass.showModal();
}

function closeDialogPass() {
    dialogPass.close();
}

function enviarPass() {
    let correo = document.getElementById("email").value;
    let llave = document.getElementById("newPassword").value;

    if (llave === "") {
        mostrarNotificacionRequest('Contraseña Ausente', 'dodgerblue', 'notifications-outline');
    }
    else {
        fetch('/profile/pass', {
            method: 'POST',
            body: JSON.stringify({ correo: correo, llave: llave }),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === "closeDialog") {
                    mostrarNotificacionRequest('Contraseña Actualizada', 'lawngreen', 'checkmark-outline');
                    document.getElementById("newPassword").value = '';
                    dialogPass.close();
                }
            });
    }
}

function openDialogDelete() {
    dialogDelete.showModal();
}

function closeDialogDelete() {
    dialogDelete.close();
}

function eliminarCuenta() {
    fetch('/profile/delete', {
        method: 'POST',
        body: JSON.stringify({ accion: 'ACEPTAR' }),
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

const socket = io();

// Escuchar evento 'actualizacion_casillero'
socket.on('actualizacion_casillero', function (data) {

    if (data[0] === userCasillero && data[1] === 'ABIERTO') {
        mostrarNotificacionRequest('Casillero Abierto', 'lawngreen', 'checkmark-outline');
    }

    if (data[0] === userCasillero && data[1] === 'CERRADO') {
        mostrarNotificacionRequest('Casillero Cerrado', 'crimson', 'flash-outline');
    }
});