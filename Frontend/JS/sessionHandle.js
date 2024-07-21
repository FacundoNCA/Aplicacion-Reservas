export function closeSession() {

    Swal.fire({
        title: "¿Quieres cerrar la sesion?",
        text: "En caso de querer reservar tendras que volver a autenticarte",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#93cf46",
        confirmButtonText: "Cerrar sesion",
        cancelButtonText: "Cancelar"

      }).then((result) => {
        if (result.isConfirmed) {
            sessionStorage.removeItem('authToken')
            location.reload()
        }
      });


}

export function deleteAccount() {

  Swal.fire({
      title: "¿Quieres borrar tu cuenta?",
      text: "No podras recuperarla",
      icon: "error",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      cancelButtonColor: "#93cf46",
      confirmButtonText: "Borrar",
      cancelButtonText: "Cancelar"

    }).then((result) => {
      if (result.isConfirmed) {
        const token = sessionStorage.getItem('authToken')


        fetch('http://127.0.0.1:5000/auth/delete', {
          method: 'DELETE',
          headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
          },
        })
        .then(response => response.json())
        .then(data => {
          if (data.succes) {
            Swal.fire({
              icon: "success",
              title: "Cuenta eliminada",
              showConfirmButton: false,
              timer: 1500
            });
            sessionStorage.removeItem('authToken')
            window.history.back()
          } else {
            Swal.fire({
              icon: "error",
              title: "Error al eliminar la cuenta",
              showConfirmButton: false,
              timer: 1500
            });
          }
        })
        .catch(error => {
            console.error('Error:', error);
        
            document.getElementById('register-message').innerText = "Error en el registro. Por favor, inténtelo nuevamente.";
        });
      }
    });


}

export function isAuth(){
    return sessionStorage.getItem('authToken') !== null;
}