document.addEventListener("DOMContentLoaded", function () {
    const passwordInput = document.getElementById("id_password");
    const eyeShowIcon = document.getElementById("icon-eye-show");
    const eyeOffIcon = document.getElementById("icon-eye-off");

    // Função para alternar a visibilidade da senha
    function togglePasswordVisibility() {
        if (passwordInput.type === "password") {
            passwordInput.type = "text"; // Mostra a senha
            eyeShowIcon.style.display = "inline"; // Mostra o ícone de "mostrar senha"
            eyeOffIcon.style.display = "none"; // Esconde o ícone de "esconder senha"
        } else {
            passwordInput.type = "password"; // Oculta a senha
            eyeShowIcon.style.display = "none"; // Esconde o ícone de "mostrar senha"
            eyeOffIcon.style.display = "inline"; // Mostra o ícone de "esconder senha"
        }
    }

    // Adiciona eventos de clique aos ícones
    eyeShowIcon.addEventListener("click", togglePasswordVisibility);
    eyeOffIcon.addEventListener("click", togglePasswordVisibility);

    // Configura o estado inicial dos ícones
    if (passwordInput.type === "password") {
        eyeShowIcon.style.display = "none"; // Esconde "mostrar senha"
        eyeOffIcon.style.display = "inline"; // Mostra "esconder senha"
    } else {
        eyeShowIcon.style.display = "inline"; // Mostra "mostrar senha"
        eyeOffIcon.style.display = "none"; // Esconde "esconder senha"
    }
});
