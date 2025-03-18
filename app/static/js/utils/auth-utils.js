// Check if user is logged in
function isLoggedIn() {
    return localStorage.getItem('access_token') !== null;
}

// Get the authorization header for API requests
function getAuthHeader() {
    const token = localStorage.getItem('access_token');
    return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };
}

// Load protected page content with authentication token
async function loadAuthenticatedPage(url) {
    try {
        const token = localStorage.getItem('access_token');
        if (!token) {
            window.location.href = '/login';
            return;
        }

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const html = await response.text();
            document.open();
            document.write(html);
            document.close();
            history.pushState({}, '', url);
        } else if (response.status === 401) {
            // If unauthorized, redirect to login
            localStorage.removeItem('access_token');
            window.location.href = '/login';
        } else {
            alert('Failed to load page: ' + response.statusText);
        }
    } catch (error) {
        console.error('Error loading page:', error);
        alert('Error loading page. Please try again.');
    }
}

// Clear tokens and redirect to login
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('role');
    window.location.href = '/login';
}

// Handle API responses - with basic error handling
async function handleApiResponse(responsePromise) {
    try {
        const response = await responsePromise;
        
        if (response.status === 401) {
            // If unauthorized, redirect to login
            logout();
        }
        
        return response;
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// Set up click handler for internal links
document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', function(e) {
        const anchor = e.target.closest('a[data-internal="true"]');
        if (anchor) {
            e.preventDefault();
            const url = anchor.getAttribute('href');
            loadAuthenticatedPage(url);
        }
    });
});