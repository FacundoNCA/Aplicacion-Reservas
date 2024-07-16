document.getElementById('register-form').addEventListener('submit', function(event) {
    event.preventDefault();

    let name = document.getElementById('name').value;
    let lastname = document.getElementById('lastname').value;
    let phone = document.getElementById('phone').value;
    let email = document.getElementById('email').value;
    let contrasena = document.getElementById('contrasena').value;
    let confirmContrasena = document.getElementById('confirm-contrasena').value;

    console.log(email)

    if (contrasena !== confirmContrasena) {
        document.getElementById('register-message').innerText = "Las contraseñas no coinciden.";
        return;
    }

    // Si las contraseñas coinciden, enviar el formulario al backend
    fetch('http://127.0.0.1:5000/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nombre: name,
            apellido: lastname,
            email: email,
            contraseña: contrasena,
            telefono: phone
        })
    })
    .then(response => response.json())
    .then(data => {
        sessionStorage.setItem('authToken', data.token);;
        window.location.href = 'Reservas.html';
    })
    .catch(error => {
        console.error('Error:', error);
    
        document.getElementById('register-message').innerText = "Error en el registro. Por favor, inténtelo nuevamente.";
    });
});
