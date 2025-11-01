document.addEventListener("DOMContentLoaded", function () {
    const passwordInput = document.querySelector(".password-wrapper input");
    const togglePassword = document.getElementById("toggle-password");

    if (togglePassword && passwordInput) {
        togglePassword.addEventListener("click", function () {
            const isPassword = passwordInput.type === "password";
            passwordInput.type = isPassword ? "text" : "password";
            togglePassword.classList.toggle("fa-eye", !isPassword);
            togglePassword.classList.toggle("fa-eye-slash", isPassword);
        });
    }

    const errorAlert = document.getElementById("error-alert");
    if (errorAlert) {
        setTimeout(() => {
            errorAlert.style.opacity = "0";
            setTimeout(() => errorAlert.remove(), 500);
        }, 3000);
    }
});
