document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('registerForm');
    const nameInput = document.getElementById('nome');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('senha');
    const confirmPasswordInput = document.getElementById('confirmarSenha');
    const nameError = document.getElementById('nomeError');
    const emailError = document.getElementById('emailError');
    const passwordError = document.getElementById('senhaError');
    const confirmPasswordError = document.getElementById('confirmarSenhaError');

    const showPopup = (message) => {
        const existingPopup = document.querySelector('.popup');
        if (existingPopup) {
            existingPopup.remove();
        }

        const popup = document.createElement('div');
        popup.className = 'popup error';
        popup.innerHTML = `<span class="popup-message">${message}</span>`;
        
        document.body.appendChild(popup);
        
        setTimeout(() => {
            popup.style.animation = 'fadeOut 0.3s ease-out';
            setTimeout(() => popup.remove(), 300);
        }, 3000);
    };

    const isValidEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    const isValidPassword = (password) => password.length >= 6;
    const passwordsMatch = (pass1, pass2) => pass1 === pass2;

    const showError = (input, errorElement, message) => {
        input.classList.add('error');
        errorElement.textContent = message;
        showPopup(message);
    };

    const clearError = (input, errorElement) => {
        input.classList.remove('error');
        errorElement.textContent = '';
    };

    nameInput.addEventListener('blur', () => {
        if (!nameInput.value.trim()) {
            showError(nameInput, nameError, 'O nome é obrigatório');
        } else {
            clearError(nameInput, nameError);
        }
    });

    emailInput.addEventListener('blur', () => {
        if (!emailInput.value) {
            showError(emailInput, emailError, 'O email é obrigatório');
        } else if (!isValidEmail(emailInput.value)) {
            showError(emailInput, emailError, 'Digite um email válido');
        } else {
            clearError(emailInput, emailError);
        }
    });

    passwordInput.addEventListener('blur', () => {
        if (!passwordInput.value) {
            showError(passwordInput, passwordError, 'A senha é obrigatória');
        } else if (!isValidPassword(passwordInput.value)) {
            showError(passwordInput, passwordError, 'A senha deve ter pelo menos 6 caracteres');
        } else {
            clearError(passwordInput, passwordError);
        }
    });

    confirmPasswordInput.addEventListener('blur', () => {
        if (!confirmPasswordInput.value) {
            showError(confirmPasswordInput, confirmPasswordError, 'A confirmação de senha é obrigatória');
        } else if (!passwordsMatch(passwordInput.value, confirmPasswordInput.value)) {
            showError(confirmPasswordInput, confirmPasswordError, 'As senhas não coincidem');
        } else {
            clearError(confirmPasswordInput, confirmPasswordError);
        }
    });

    [nameInput, emailInput, passwordInput, confirmPasswordInput].forEach(input => {
        input.addEventListener('input', () => clearError(input, input.nextElementSibling));
    });

    registerForm.addEventListener('submit', (e) => {
        let isValid = true;

        if (!nameInput.value.trim()) {
            showError(nameInput, nameError, 'O nome é obrigatório');
            isValid = false;
        }

        if (!emailInput.value) {
            showError(emailInput, emailError, 'O email é obrigatório');
            isValid = false;
        } else if (!isValidEmail(emailInput.value)) {
            showError(emailInput, emailError, 'Digite um email válido');
            isValid = false;
        }

        if (!passwordInput.value) {
            showError(passwordInput, passwordError, 'A senha é obrigatória');
            isValid = false;
        } else if (!isValidPassword(passwordInput.value)) {
            showError(passwordInput, passwordError, 'A senha deve ter pelo menos 6 caracteres');
            isValid = false;
        }

        if (!confirmPasswordInput.value) {
            showError(confirmPasswordInput, confirmPasswordError, 'A confirmação de senha é obrigatória');
            isValid = false;
        } else if (!passwordsMatch(passwordInput.value, confirmPasswordInput.value)) {
            showError(confirmPasswordInput, confirmPasswordError, 'As senhas não coincidem');
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault();
        }
    });

    const divErrors = document.querySelector('.errors');
    const errors = divErrors ? divErrors.querySelectorAll('p') : [];
    let errorMessages = Array.from(errors).map(el => el.textContent).join('<br>'); // Usar <br> para as quebras de linha

    if (errorMessages) {
        showPopup(errorMessages); // Passe o HTML com <br> no popup
    }
});
