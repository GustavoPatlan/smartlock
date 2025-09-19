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

function solicitarCasillero() {
    fetch('/home/locker', {
        method: 'POST',
        body: JSON.stringify({ accion: 'SOLICITAR' }),
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

function abrirCasillero() {
    fetch('/home/locker/open', {
        method: 'POST',
        body: JSON.stringify({ accion: 'ABRIR' }),
        headers: { 'Content-Type': 'application/json' }
    })

        .then(response => response.json())
        .then(data => {
            switch (data.status) {
                case 'alerta':
                    break;
            }
        });
}

let dialogDelete = document.getElementById("deleteAccount");

function openDialogDelete() {
    let sensor = document.getElementById("span_status").innerText.trim().toUpperCase();

    if (sensor === "ABIERTO") {
        mostrarNotificacionRequest('Casillero Abierto', 'goldenrod', 'alert-outline');
    } else {
        dialogDelete.showModal();
    }
}

function closeDialogDelete() {
    dialogDelete.close();
}

function finishLocker() {
    fetch('/home/locker/finish', {
        method: 'POST',
        body: JSON.stringify({ accion: 'FINALIZAR' }),
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

    let sensor = document.getElementById("span_status");

    if (data[0] === userCasillero && data[1] === 'ABIERTO') {
        mostrarNotificacionRequest('Casillero Abierto', 'lawngreen', 'checkmark-outline');

        sensor.style.paddingLeft = '8px';
        sensor.style.paddingRight = '8px';
        sensor.innerText = 'ABIERTO';
        sensor.style.backgroundColor = 'lawngreen'
    }

    if (data[0] === userCasillero && data[1] === 'CERRADO') {
        mostrarNotificacionRequest('Casillero Cerrado', 'crimson', 'flash-outline');
        
        sensor.style.paddingLeft = '8px';
        sensor.style.paddingRight = '8px';
        sensor.innerText = 'CERRADO';
        sensor.style.backgroundColor = 'crimson'
    }
});

// Escuchar evento 'actualizacion_casillero'
socket.on('actualizacion_alerta', function (data) {

    let sensor = document.getElementById("span_status");

    if (data[0] === userCasillero && data[1] === 'ABIERTO') {
        mostrarNotificacionRequest('Casillero Abierto', 'lawngreen', 'checkmark-outline');

        sensor.style.paddingLeft = '8px';
        sensor.style.paddingRight = '8px';
        sensor.innerText = 'ABIERTO';
        sensor.style.backgroundColor = 'lawngreen'
    }

    if (data[0] === userCasillero && data[1] === 'CERRADO') {
        mostrarNotificacionRequest('Casillero Cerrado', 'crimson', 'flash-outline');
        
        sensor.style.paddingLeft = '8px';
        sensor.style.paddingRight = '8px';
        sensor.innerText = 'CERRADO';
        sensor.style.backgroundColor = 'crimson'
    }
});