document.addEventListener('DOMContentLoaded', () => {
    const roleTabs = document.querySelectorAll('.role-tab');
    const roleHiddenInput = document.getElementById('id_role');
    const submitBtn = document.getElementById('submit-btn');
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

    // 2. Role Selector Tabs & Button Text Sync
    if (roleTabs.length && roleHiddenInput && submitBtn) {
        roleTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const selectedRole = tab.getAttribute('data-role');

                // Update hidden form field
                roleHiddenInput.value = selectedRole;

                // Toggle active tab visual style
                roleTabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');

                // Dynamic button label
                const roleLabel = selectedRole === 'student' ? 'Student' : 'Faculty';
                submitBtn.textContent = `Sign In as ${roleLabel}`;
            });
        });
    }
});