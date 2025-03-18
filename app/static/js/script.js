// Handle registration form submission
document.getElementById('registerForm')?.addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);

    const response = await fetch('/auth/register', {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });

    const result = await response.json();
    if (response.ok) {
        window.location.href = '/login';
    } else {
        document.getElementById('errorMessage').innerText = result.error;
    }
});

// Handle login form submission
document.getElementById('loginForm')?.addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);

    const response = await fetch('/auth/login', {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });

    const result = await response.json();
    if (response.ok) {
        // Store tokens in localStorage
        localStorage.setItem('access_token', result.access_token);
        localStorage.setItem('refresh_token', result.refresh_token);
        localStorage.setItem('role', result.role);

        // Check the role and load the appropriate dashboard
        if (result.role === 'Librarian') {
            loadDashboard('/librarian-dashboard', result.access_token);
        } else if (result.role === 'Member') {
            loadDashboard('/member-dashboard', result.access_token);
        } else {
            alert('Unknown role, please contact support.');
        }
    } else {
        document.getElementById('errorMessage').innerText = result.error;
    }
});

// Function to load dashboard with the token
async function loadDashboard(url, token) {
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const html = await response.text();
            // Replace the current document with the dashboard HTML
            document.open();
            document.write(html);
            document.close();
            
            // Update the URL in the browser bar without triggering a page load
            history.pushState({}, '', url);
        } else {
            alert('Failed to load dashboard: ' + response.statusText);
            window.location.href = '/login';
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
        alert('Error loading dashboard. Please try again.');
    }
}

// // Fetch user data for the dashboard
// document.addEventListener('DOMContentLoaded', async function () {
//     const token = localStorage.getItem('access_token');
//     if (!token) {
//         window.location.href = '/login';
//         return;
//     }

//     const response = await fetch('/user/info', {
//         method: 'GET',
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify(data),
//     });

//     const result = await response.json();
//     if (response.ok) {
//         document.getElementById('userInfo').innerText = `Hello, ${result.name}`;
//     } else {
//         document.getElementById('userInfo').innerText = 'Failed to fetch user data.';
//     }

//     // Handle logout
//     document.getElementById('logoutButton')?.addEventListener('click', function () {
//         localStorage.removeItem('access_token');
//         localStorage.removeItem('refresh_token');
//         window.location.href = '/login';
//     });
// });
