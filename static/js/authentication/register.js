document.addEventListener('DOMContentLoaded', () => {
    const roleCardGroup = document.querySelector('.role-card-group');
    const roleHiddenInput = document.getElementById('id_role');
    // 1. Password Visibility Toggle (works for both Password and Confirm Password)
    document.querySelectorAll('.password-wrapper').forEach(wrapper => {
        const toggleBtn = wrapper.querySelector('.toggle-password');
        const input = wrapper.querySelector('input');
        if (toggleBtn && input) {
            toggleBtn.addEventListener('click', () => {
                const isPassword = input.getAttribute('type') === 'password';
                input.setAttribute('type', isPassword ? 'text' : 'password');
                toggleBtn.textContent = isPassword ? 'HIDE' : 'SHOW';
            });
        }
    });

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