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

export function isAuth(){
    return sessionStorage.getItem('authToken') !== null;
}