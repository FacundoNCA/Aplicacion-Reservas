import {closeSession, isAuth} from './sessionHandle.js'

function parseDate(date){
    splitDate = date.split("-");
    reversed = splitDate.reverse()

    return reversed.join('/')
}



document.addEventListener("DOMContentLoaded", function() {
    var formulario = document.getElementById("formulario");

    

    if (!isAuth()) {
        Swal.fire("Necesitas autenticarse antes de reservar"

        ).then((res) => {
            window.location.href = "login.html";
        })
    } else {
        const loginButton = document.getElementById('login-btn')
        const logoutButton = document.getElementById('logout-btn')


        loginButton.style.display = 'none';
        logoutButton.style.display = 'block'
        logoutButton.onclick = closeSession;

    }

    formulario.addEventListener("submit", function(event) {
        event.preventDefault();

        const token = sessionStorage.getItem('authToken')

        var room = document.getElementById("room").value;
        var fechaLlegada = document.getElementById("fecha_llegada").value.trim();
        var fechaSalida = document.getElementById("fecha_salida").value.trim();
        // var pay_method = document.getElementById("pay_method").value;

        // Validación de campos obligatorios
        if (room === "" || fechaLlegada === "" || fechaSalida === "") {
            alert("Por favor, completa todos los campos obligatorios.");
            return;
        }

        // Validación de fechas
        if (new Date(fechaLlegada) >= new Date(fechaSalida)) {
            alert("La fecha de salida debe ser posterior a la fecha de llegada.");
            return;
        }

        // console.log(parseDate(fechaSalida))

     

        fetch('http://127.0.0.1:5000/reservas', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                tipo_habitacion: room,
                fecha_llegada: parseDate(fechaLlegada),
                fecha_salida: parseDate(fechaSalida)
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
        })
        .catch(error => {
            console.log(error)
        });
        });
});
