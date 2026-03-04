 // 1. Password Visibility Toggles
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

// 2. Real-time Message Helper
function setFieldMessage(elementId, message, isError) {
    const msgDiv = document.getElementById(elementId);
    msgDiv.textContent = message;
    msgDiv.className = isError ? "mt-1 small text-danger" : "mt-1 small text-success";
}

// 3. Real-time Listeners
const usernameInput = document.getElementById('usernameInput');
const emailInput = document.getElementById('emailInput');
const passInput = document.getElementById('passwordInput');
const confirmPassInput = document.getElementById('confirmPasswordInput');

usernameInput.addEventListener('input', () => {
    if (usernameInput.value.trim().length < 3) {
        setFieldMessage('nameError', "✗ Minimum 3 characters", true);
    } else {
        setFieldMessage('nameError', "✓ Username valid", false);
    }
});

emailInput.addEventListener('input', () => {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!regex.test(emailInput.value)) {
        setFieldMessage('emailError', "✗ Invalid email format", true);
    } else {
        setFieldMessage('emailError', "✓ Email format correct", false);
    }
});

function checkPasswords() {
    if (passInput.value.length < 6) {
        setFieldMessage('passwordError', "✗ Min 6 characters", true);
    } else {
        setFieldMessage('passwordError', "✓ Length ok", false);
    }

    if (confirmPassInput.value.length > 0) {
        if (passInput.value === confirmPassInput.value) {
            setFieldMessage('validationMessage', "✓ Passwords match", false);
        } else {
            setFieldMessage('validationMessage', "✗ Passwords do not match", true);
        }
    }
}
passInput.addEventListener('input', checkPasswords);
confirmPassInput.addEventListener('input', checkPasswords);

// 4. Submit Guard
document.getElementById('SignUpform').addEventListener('submit', function(e) {
    const isNameValid = usernameInput.value.trim().length >= 3;
    const isEmailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput.value);
    const isPassValid = passInput.value.length >= 6;
    const isMatchValid = passInput.value === confirmPassInput.value;

    if (!isNameValid || !isEmailValid || !isPassValid || !isMatchValid) {
        e.preventDefault();
        Swal.fire({
            icon: 'error',
            title: 'Check your inputs',
            text: 'Please fix the errors highlighted in red.',
            confirmButtonColor: '#198754'
        });
    }
});

