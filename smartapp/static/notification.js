document.addEventListener("DOMContentLoaded", function () {
    let mensaje = sessionStorage.getItem("notificacion_mensaje");
    let accion = sessionStorage.getItem("notificacion_accion");

    if (mensaje) {
        mostrarNotificacion(mensaje, accion);
        sessionStorage.removeItem("notificacion_mensaje");
        sessionStorage.removeItem("notificacion_accion");
    }
});

function mostrarNotificacion(mensaje, accion) {
    let notificacion = document.getElementById("notificacion");
    let mensajeElemento = document.getElementById("mensaje");
    let icono = document.getElementById("notification_icon");
    let icono_forma = document.getElementById("icon_form");

    mensajeElemento.innerText = mensaje;
    notificacion.style.display = "flex";

    let color;
    switch (accion) {
        case '1':
            color = 'goldenrod';
            icono_forma.setAttribute('name', 'alert-outline');
            break;
        case '2':
            color = 'dodgerblue';
            icono_forma.setAttribute('name', 'notifications-outline');
            break;
        case '3':
            color = 'crimson';
            icono_forma.setAttribute('name', 'flash-outline');
            break;
        case '4':
            color = 'lawngreen';
            icono_forma.setAttribute('name', 'checkmark-outline');
            break;
    }

    icono.style.background = color;

    setTimeout(() => {
        notificacion.style.display = "none";
    }, 4000);
};

function cerrarNotificacion() {
    document.getElementById("notificacion").style.display = "none";
};