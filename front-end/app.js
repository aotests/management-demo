document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const submitButton = loginForm.querySelector('button');
    const errorMessage = document.getElementById('error-message');

    function validateEmail(email) {
        // Simpler and more reliable regex for email validation
        const re = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
        return re.test(String(email).toLowerCase());
    }

    function updateFormState() {
        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();
        submitButton.disabled = !(email && password);
    }

    emailInput.addEventListener('input', updateFormState);
    passwordInput.addEventListener('input', updateFormState);

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        errorMessage.textContent = ''; // Clear previous errors

        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();

        // Custom validation
        if (!email || !password) {
            errorMessage.textContent = 'Por favor, preencha todos os campos.';
            return;
        }

        if (!validateEmail(email)) {
            errorMessage.textContent = 'Por favor, insira um e-mail válido.';
            return;
        }

        try {
            const response = await fetch('https://management-demo-i6to.onrender.com/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            if (response.ok) {
                const userData = await response.json(); // Extract user data from response
                sessionStorage.setItem('isAuthenticated', 'true');
                sessionStorage.setItem('userData', JSON.stringify(userData)); // Store user data
                window.location.href = 'dashboard.html';
            } else {
                const errorData = await response.json();
                errorMessage.textContent = errorData.detail || 'Ocorreu um erro desconhecido.';
            }
        } catch (error) {
            errorMessage.textContent = 'Falha ao conectar com o servidor.';
        }
    });

    // Initial form state check
    updateFormState();

    const togglePassword = document.querySelector('.toggle-password');
    togglePassword.addEventListener('click', () => {
        // toggle the type attribute
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        // toggle the eye icon
        togglePassword.textContent = type === 'password' ? '👁️' : '🙈';
    });
});