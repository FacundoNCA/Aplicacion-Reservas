document.getElementById('register-form').addEventListener('submit', function(event) {
    event.preventDefault();

    let email = document.getElementById('email').value;
    let contrasena = document.getElementById('contrasena').value;
    let confirmContrasena = document.getElementById('confirm-contrasena').value;

    if (contrasena !== confirmContrasena) {
        document.getElementById('register-message').innerText = "Las contraseñas no coinciden.";
        return;
    }

    // Si las contraseñas coinciden, enviar el formulario al backend
    fetch('/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            contrasena: contrasena
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en el registro');
        }
        return response.json(); // Parsear la respuesta JSON
    })
    .then(data => {
        // Manejar la respuesta del backend
        console.log('Registro exitoso:', data.message);
        // Redirigir a Reservas.html si todo sale bien
        window.location.href = '/Reservas.html';
    })
    .catch(error => {
        console.error('Error:', error);
        // Manejar errores de registro aquí
        document.getElementById('register-message').innerText = "Error en el registro. Por favor, inténtelo nuevamente.";
    });
});
