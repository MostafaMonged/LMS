document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const errorMessage = document.getElementById('error-message');
            
            try {
                const response = await fetch('/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    // Store token in localStorage
                    localStorage.setItem('access_token', data.access_token);
                    localStorage.setItem('refresh_token', data.refresh_token);
                    
                    // Navigate to the appropriate dashboard
                    if (data.role === 'Librarian') {
                        loadAuthenticatedPage('/dashboard/librarian');
                    } else {
                        loadAuthenticatedPage('/dashboard/member');
                    }
                } else {
                    errorMessage.textContent = data.error || 'Login failed';
                }
            } catch (error) {
                console.error('Error:', error);
                errorMessage.textContent = 'An error occurred. Please try again later.';
            }
        });
    }
});