document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('.login-form');
    const emailInput = document.getElementById('email');
    const senhaInput = document.getElementById('senha');
    const emailError = document.getElementById('emailError');
    const senhaError = document.getElementById('senhaError');

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

    const isValidEmail = (email) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    };

    const isValidPassword = (password) => password.length >= 6;

    const showError = (input, errorElement, message) => {
        input.classList.add('error');
        errorElement.textContent = message;
        showPopup(message);
    };

    const clearError = (input, errorElement) => {
        input.classList.remove('error');
        errorElement.textContent = '';
    };

    emailInput.addEventListener('blur', () => {
        if (!emailInput.value) {
            showError(emailInput, emailError, 'O email é obrigatório');
        } else if (!isValidEmail(emailInput.value)) {
            showError(emailInput, emailError, 'Digite um email válido');
        } else {
            clearError(emailInput, emailError);
        }
    });

    senhaInput.addEventListener('blur', () => {
        if (!senhaInput.value) {
            showError(senhaInput, senhaError, 'A senha é obrigatória');
        } else if (!isValidPassword(senhaInput.value)) {
            showError(senhaInput, senhaError, 'A senha deve ter pelo menos 6 caracteres');
        } else {
            clearError(senhaInput, senhaError);
        }
    });

    emailInput.addEventListener('input', () => clearError(emailInput, emailError));
    senhaInput.addEventListener('input', () => clearError(senhaInput, senhaError));

    loginForm.addEventListener('submit', (e) => {
        let isValid = true;

        if (!emailInput.value) {
            showError(emailInput, emailError, 'O email é obrigatório');
            isValid = false;
        } else if (!isValidEmail(emailInput.value)) {
            showError(emailInput, emailError, 'Digite um email válido');
            isValid = false;
        }

        if (!senhaInput.value) {
            showError(senhaInput, senhaError, 'A senha é obrigatória');
            isValid = false;
        } else if (!isValidPassword(senhaInput.value)) {
            showError(senhaInput, senhaError, 'A senha deve ter pelo menos 6 caracteres');
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault(); // Impede envio se houver erro
        }
    });
});
