document.addEventListener("DOMContentLoaded", function () {
    const passwordInput = document.getElementById("id_password");
    const eyeShowIcon = document.getElementById("icon-eye-show");
    const eyeOffIcon = document.getElementById("icon-eye-off");

    // Função para alternar a visibilidade da senha e dos ícones
    function togglePasswordVisibility() {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            eyeShowIcon.style.display = "none";
            eyeOffIcon.style.display = "inline"; // Mostra o ícone de olho cortado
        } else {
            passwordInput.type = "password";
            eyeShowIcon.style.display = "inline"; // Mostra o ícone de olho aberto
            eyeOffIcon.style.display = "none";
        }
    }

    // Adiciona o evento de clique nos ícones
    eyeShowIcon.addEventListener("click", togglePasswordVisibility);
    eyeOffIcon.addEventListener("click", togglePasswordVisibility);
});
