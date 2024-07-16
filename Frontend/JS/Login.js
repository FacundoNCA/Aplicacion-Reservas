document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();


    let email = document.getElementById('email').value;
    let contrasena = document.getElementById('password').value;


    fetch('http://127.0.0.1:5000/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            contraseña: contrasena
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.succes) {
            sessionStorage.setItem('authToken', data.token);;
            // TODO: Cambiar la ruta
            window.location.href = "Reservas.html";
        } else {
            document.getElementById('login-message').innerText = "Email o contraseña incorrecto/s"
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('login-message').innerText = "Error en el inicio de sesión. Por favor, inténtelo nuevamente.";
    });
});
