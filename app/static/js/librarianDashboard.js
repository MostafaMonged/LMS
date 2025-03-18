// Function to fetch dashboard data with authorization token
async function getDashboardData(role) {
    const data = await apiRequest(`/${role}-dashboard`);

    if (data.error) {
        if (data.error.includes('JWT')) {
            alert("Session expired or invalid token. Please log in again.");
            logout(); // Log out if token is invalid or expired
        } else {
            console.error('Error fetching dashboard data:', data.error);
        }
        return;
    }

    // // Render dashboard data here (e.g., display total books, stats, etc.)
    // renderDashboardData(data);
}

// // Function to render dashboard data
// function renderDashboardData(data) {
//     // Example: Display dashboard info (customize as needed)
//     document.getElementById('dashboardContent').innerHTML = `
//         <p>Total Books: ${data.totalBooks}</p>
//         <p>Total Users: ${data.totalUsers}</p>
//         <!-- Add more dashboard data here -->
//     `;
// }

// Handle loading all users
async function loadUsers() {
    const data = await apiRequest('/api/users');

    if (data.error) {
        document.getElementById('userList').innerHTML = `<p class="error">${data.error}</p>`;
        return;
    }

    const userListHtml = data.map(user =>
        `<li>ID: ${user.id} | Name: ${user.name} | Email: ${user.email} | Role: ${user.role}</li>`
    ).join('');

    document.getElementById('userList').innerHTML = `<ul>${userListHtml}</ul>`;
}

// Handle loading user details by ID
async function loadUserDetails() {
    const userId = document.getElementById('userId').value.trim();
    if (!userId) {
        alert('Please enter a user ID');
        return;
    }

    const data = await apiRequest(`/api/users/${userId}`);
    if (data.error) {
        document.getElementById('userDetailsInfo').innerHTML = `<p class="error">${data.error}</p>`;
    } else {
        document.getElementById('userDetailsInfo').innerHTML = `
            <p>Name: ${data.name}</p>
            <p>Email: ${data.email}</p>
            <p>Role: ${data.role}</p>
        `;
    }
}

// Handle deleting a user by email
async function deleteUser() {
    const emailToDelete = document.getElementById('userEmailToDelete').value.trim();
    if (!emailToDelete) {
        alert('Please enter a user email');
        return;
    }

    const data = await apiRequest('/api/users', 'DELETE', { email: emailToDelete });
    if (data.error) {
        alert(data.error);
    } else {
        alert('User deleted successfully');
        loadUsers(); // Refresh user list after deletion
    }
}

// Logout function to clear local storage and redirect to login
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('role');
    window.location.replace('/login'); // Prevents back navigation
}


// Utility function for making API requests
async function apiRequest(url, method = 'GET', data = null, isAuthenticated = true) {
    const options = {
        method: method,
        headers: {
            "Content-Type": "application/json",
        },
    };

    // Add Authorization header if required
    if (isAuthenticated) {
        const accessToken = localStorage.getItem('access_token');
        if (accessToken) {
            options.headers['Authorization'] = `Bearer ${accessToken}`;
        }
    }

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, options);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'An unknown error occurred');
        }

        return result;
    } catch (error) {
        console.error('API Request failed:', error);
        return { error: error.message };
    }
}

// Attach event listeners after DOM content is loaded
document.addEventListener('DOMContentLoaded', function () {
    const role = localStorage.getItem('role');
    
    // If the role is not set or invalid, redirect to login
    if (!role) {
        window.location.href = '/login';
    }

    getDashboardData(role); // Fetch dashboard data after login redirect
    document.getElementById('loadUsersButton')?.addEventListener('click', loadUsers);
    document.getElementById('loadUserDetailsButton')?.addEventListener('click', loadUserDetails);
    document.getElementById('deleteUserButton')?.addEventListener('click', deleteUser);
    document.getElementById('logoutButton')?.addEventListener('click', logout);
});
