const socket = io();

// Escuchar evento 'actualizacion_casillero'
socket.on('actualizacion_historial', function (data) {
    if (data[0] === userCasillero) {
        var tbody = document.getElementById('solicitudesTableBody');

        var row = tbody.insertRow();
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);
        var cell5 = row.insertCell(4);

        cell1.textContent = data[2] || 'N/A';
        cell2.textContent = data[1] || 'N/A';
        cell3.textContent = "#" + (data[3] || '0');
        cell4.textContent = data[4] || 'N/A';
        cell5.textContent = data[5] || 'N/A';

    }
});