document.addEventListener("DOMContentLoaded", function () {
    // Seletores para os campos de senha e ícones de visibilidade
    const password1Input = document.getElementById("id_password1");
    const eyeShowIcon1 = document.getElementById("icon-eye-show-password1");
    const eyeOffIcon1 = document.getElementById("icon-eye-off-password1");

    const password2Input = document.getElementById("id_password2");
    const eyeShowIcon2 = document.getElementById("icon-eye-show-password2");
    const eyeOffIcon2 = document.getElementById("icon-eye-off-password2");

    // Função para alternar a visibilidade do campo password1
    function togglePasswordVisibility1() {
        if (password1Input.type === "password") {
            password1Input.type = "text";
            eyeShowIcon1.style.display = "inline";
            eyeOffIcon1.style.display = "none";
        } else {
            password1Input.type = "password";
            eyeShowIcon1.style.display = "none";
            eyeOffIcon1.style.display = "inline";
        }
    }

    // Função para alternar a visibilidade do campo password2
    function togglePasswordVisibility2() {
        if (password2Input.type === "password") {
            password2Input.type = "text";
            eyeShowIcon2.style.display = "inline";
            eyeOffIcon2.style.display = "none";
        } else {
            password2Input.type = "password";
            eyeShowIcon2.style.display = "none";
            eyeOffIcon2.style.display = "inline";
        }
    }

    // Eventos de clique para alternar visibilidade das senhas
    eyeShowIcon1.addEventListener("click", togglePasswordVisibility1);
    eyeOffIcon1.addEventListener("click", togglePasswordVisibility1);
    eyeShowIcon2.addEventListener("click", togglePasswordVisibility2);
    eyeOffIcon2.addEventListener("click", togglePasswordVisibility2);

    // Configuração inicial dos ícones para o campo password1
    if (password1Input.type === "password") {
        eyeShowIcon1.style.display = "none";
        eyeOffIcon1.style.display = "inline";
    } else {
        eyeShowIcon1.style.display = "inline";
        eyeOffIcon1.style.display = "none";
    }

    // Configuração inicial dos ícones para o campo password2
    if (password2Input.type === "password") {
        eyeShowIcon2.style.display = "none";
        eyeOffIcon2.style.display = "inline";
    } else {
        eyeShowIcon2.style.display = "inline";
        eyeOffIcon2.style.display = "none";
    }
});
