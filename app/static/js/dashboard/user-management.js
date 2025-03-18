document.addEventListener('DOMContentLoaded', function() {
    // Check if the users section exists (we're on the librarian dashboard)
    if (document.getElementById('users-section')) {
        // Load users when the tab is clicked
        document.getElementById('nav-users').addEventListener('click', loadUsers);
        
        // Setup search functionality
        document.getElementById('user-search').addEventListener('input', debounce(searchUsers, 300));
        
        // Setup search by barcode toggle
        document.getElementById('search-by-barcode').addEventListener('change', function() {
            searchUsers();
        });
    }
});

async function loadUsers() {
    try {
        const usersList = document.getElementById('users-list');
        usersList.innerHTML = '<tr><td colspan="5">Loading users...</td></tr>';
        
        const response = await handleApiResponse(fetch('/api/users', {
            headers: getAuthHeader()
        }));
        
        if (response.ok) {
            const data = await response.json();
            
            // Check if data is an array or has a users property that's an array
            let users;
            if (Array.isArray(data)) {
                users = data;
            } else if (data && Array.isArray(data.users)) {
                users = data.users;
            } else {
                // If we can't find an array of users, create an empty array
                console.error('Unexpected API response format:', data);
                users = [];
            }
            
            displayUsers(users);
        } else {
            usersList.innerHTML = '<tr><td colspan="5">Error loading users. Please try again.</td></tr>';
        }
    } catch (error) {
        console.error('Error loading users:', error);
        document.getElementById('users-list').innerHTML = 
            '<tr><td colspan="5">Error loading users. Please try again.</td></tr>';
    }
}

function displayUsers(users) {
    const usersList = document.getElementById('users-list');
    
    // Ensure users is an array
    if (!Array.isArray(users)) {
        console.error('displayUsers received non-array data:', users);
        users = [];
    }
    
    if (users.length === 0) {
        usersList.innerHTML = '<tr><td colspan="5">No users found.</td></tr>';
        return;
    }
    
    usersList.innerHTML = '';
    
    users.forEach(user => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${user.barcode || 'N/A'}</td>
            <td>${user.name || 'N/A'}</td>
            <td>${user.email || 'N/A'}</td>
            <td>${user.role || 'N/A'}</td>
            <td>
                <button class="btn-small" onclick="viewUserDetails('${user.barcode}')">Details</button>
                <button class="btn-small btn-secondary" onclick="deleteUser('${user.barcode}')">Delete</button>
            </td>
        `;
        usersList.appendChild(row);
    });
}

async function searchUsers() {
    const searchInput = document.getElementById('user-search').value.trim();
    const searchByBarcode = document.getElementById('search-by-barcode').checked;
    
    if (searchInput === '') {
        // If search is empty, load all users
        loadUsers();
        return;
    }
    
    try {
        const usersList = document.getElementById('users-list');
        usersList.innerHTML = '<tr><td colspan="5">Searching...</td></tr>';
        
        let url;
        if (searchByBarcode) {
            url = `/api/users/barcode/${searchInput}`;
        } //else {
        //     // This assumes your backend has a search endpoint for users
        //     // You might need to create this endpoint
        //     url = `/api/users?search=${searchInput}`;
        // }
        
        const response = await handleApiResponse(fetch(url, {
            headers: getAuthHeader()
        }));
        
        if (response.ok) {
            if (searchByBarcode) {
                // If searching by barcode, we get a single user
                const user = await response.json();
                displayUsers([user]);
            } else {
                // If searching by name/email, we get an array of users
                const users = await response.json();
                displayUsers(users);
            }
        } else {
            usersList.innerHTML = '<tr><td colspan="5">No users found.</td></tr>';
        }
    } catch (error) {
        console.error('Error searching users:', error);
        document.getElementById('users-list').innerHTML = 
            '<tr><td colspan="5">Error searching users. Please try again.</td></tr>';
    }
}

async function viewUserDetails(barcode) {
    try {
        const response = await handleApiResponse(fetch(`/api/users/barcode/${barcode}`, {
            headers: getAuthHeader()
        }));
        
        if (response.ok) {
            const user = await response.json();
            alert(`User Details:\n\nName: ${user.name}\nEmail: ${user.email}\nRole: ${user.role}\nBarcode: ${user.barcode}\nJoined: ${new Date(user.created_at).toLocaleDateString()}`);
        } else {
            alert('Error: User not found.');
        }
    } catch (error) {
        console.error('Error viewing user details:', error);
        alert('Error loading user details. Please try again.');
    }
}

async function deleteUser(barcode) {
    if (!confirm(`Are you sure you want to delete user with barcode ${barcode}?`)) {
        return;
    }
    
    try {
        const response = await handleApiResponse(fetch(`/api/users`, {
            method: 'DELETE',
            headers: getAuthHeader(),
            body: JSON.stringify({ barcode: barcode })
        }));
        
        if (response.ok) {
            alert('User deleted successfully.');
            loadUsers(); // Reload users list
        } else {
            const data = await response.json();
            alert(`Error: ${data.error || 'Failed to delete user.'}`);
        }
    } catch (error) {
        console.error('Error deleting user:', error);
        alert('Error deleting user. Please try again.');
    }
}

// Utility function to prevent too many requests while typing
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}