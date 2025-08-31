document.addEventListener('DOMContentLoaded', () => {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const agentForm = document.getElementById('agent-form');
    const outputArea = document.getElementById('output-area');
    const submitBtn = document.getElementById('submit-btn');
    const submitSpinner = document.getElementById('submit-spinner');
    const submitText = document.getElementById('submit-text');

    // --- Dark Mode Logic ---
    // Check for saved theme in localStorage and apply it
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme) {
        document.documentElement.setAttribute('data-bs-theme', currentTheme);
        if (currentTheme === 'dark') {
            darkModeToggle.checked = true;
        }
    }

    darkModeToggle.addEventListener('change', () => {
        if (darkModeToggle.checked) {
            document.documentElement.setAttribute('data-bs-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-bs-theme', 'light');
            localStorage.setItem('theme', 'light');
        }
    });

    // --- Form Submission Logic ---
    agentForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Show loading state
        submitText.textContent = 'Processing...';
        submitSpinner.classList.remove('d-none');
        submitBtn.disabled = true;
        outputArea.textContent = 'Waiting for AI response...';

        const formData = new FormData(agentForm);

        try {
            const response = await fetch('/process', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'An unknown error occurred.');
            }

            const result = await response.json();
            outputArea.textContent = result.response;

        } catch (error) {
            outputArea.textContent = `Error: ${error.message}`;
            outputArea.style.color = 'red';
        } finally {
            // Restore button state
            submitText.textContent = 'Run Agent';
            submitSpinner.classList.add('d-none');
            submitBtn.disabled = false;
        }
    });
});