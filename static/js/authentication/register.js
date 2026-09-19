document.addEventListener('DOMContentLoaded', () => {
    const roleCardGroup = document.querySelector('.role-card-group');
    const roleHiddenInput = document.getElementById('id_role');
    const togglePasswordBtn = document.querySelector('.toggle-password');
    const passwordInput = document.querySelector('input[name="password"]');

    // 1. Password Visibility Toggle
    if (togglePasswordBtn && passwordInput) {
        togglePasswordBtn.addEventListener('click', () => {
            const isPassword = passwordInput.getAttribute('type') === 'password';
            passwordInput.setAttribute('type', isPassword ? 'text' : 'password');
            togglePasswordBtn.textContent = isPassword ? 'HIDE' : 'SHOW';
        });
    }

    // 2. Role Card Selection Handler (Event Delegation)
    if (roleCardGroup && roleHiddenInput) {
        roleCardGroup.addEventListener('click', (e) => {
            const card = e.target.closest('.role-card');
            if (!card) return;

            const selectedRole = card.getAttribute('data-role');

            // Update hidden form field
            roleHiddenInput.value = selectedRole;

            // Update visual active state
            document.querySelectorAll('.role-card').forEach(c => c.classList.remove('active'));
            card.classList.add('active');
        });
    }
});