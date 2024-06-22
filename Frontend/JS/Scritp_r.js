document.addEventListener("DOMContentLoaded", function() {
    var formulario = document.getElementById("formulario");

    formulario.addEventListener("submit", function(event) {
        event.preventDefault();

        var nombre = document.getElementById("name").value.trim();
        var apellido = document.getElementById("surname").value.trim();
        var email = document.getElementById("email").value.trim();
        var room = document.getElementById("room").value;
        var fechaLlegada = document.getElementById("fecha_llegada").value.trim();
        var fechaSalida = document.getElementById("fecha_salida").value.trim();

        // Validación de campos obligatorios
        if (nombre === "" || apellido === "" || email === "" || room === "" || fechaLlegada === "" || fechaSalida === "") {
            alert("Por favor, completa todos los campos obligatorios.");
            return;
        }

        // Validación de correo electrónico
        var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        if (!emailPattern.test(email)) {
            alert("Por favor, introduce un correo electrónico válido.");
            return;
        }

        // Validación de fechas
        if (new Date(fechaLlegada) >= new Date(fechaSalida)) {
            alert("La fecha de salida debe ser posterior a la fecha de llegada.");
            return;
        }

        // Si todo está validado correctamente, enviar el formulario
        this.submit();
    });
});
