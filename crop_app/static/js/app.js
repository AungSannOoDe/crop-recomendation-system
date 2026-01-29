
    // 1. Password Visibility Toggle Function
    function initToggle(btnId, inputId) {
        const btn = document.getElementById(btnId);
        const input = document.getElementById(inputId);
        
        btn.addEventListener('click', function() {
            const icon = this.querySelector('i');
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.replace('fa-eye', 'fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.replace('fa-eye-slash', 'fa-eye');
            }
        });
    }

    initToggle('togglePassword', 'passwordInput');
    initToggle('toggleConfirmPassword', 'confirmPasswordInput');

    // 2. Real-time Password Match Check
    const pass = document.getElementById('passwordInput');
    const confirmPass = document.getElementById('confirmPasswordInput');
    const message = document.getElementById('validationMessage');

    function checkMatch() {
        if (confirmPass.value.length > 0) {
            if (pass.value === confirmPass.value) {
                message.textContent = "✓ Passwords match";
                message.className = "mt-1 small text-success";
                confirmPass.classList.remove('is-invalid');
                confirmPass.classList.add('is-valid');
            } else {
                message.textContent = "✗ Passwords do not match";
                message.className = "mt-1 small text-danger";
                confirmPass.classList.remove('is-valid');
                confirmPass.classList.add('is-invalid');
            }
        } else {
            message.textContent = "";
            confirmPass.classList.remove('is-invalid', 'is-valid');
        }
    }

    pass.addEventListener('input', checkMatch);
    confirmPass.addEventListener('input', checkMatch);
