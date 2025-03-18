document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in
    if (!isLoggedIn()) {
        window.location.href = '/login';
        return;
    }

    // Setup navigation
    setupNavigation();
    
    // Load user info
    loadUserInfo();
    
    // Load dashboard stats
    loadDashboardStats();
    
    // Setup logout button
    document.getElementById('logout-btn').addEventListener('click', function() {
        logout();
    });
});

// Remove duplicate event listener for logout
// The second DOMContentLoaded event listener is redundant

function setupNavigation() {
    // Get all navigation links
    const navLinks = document.querySelectorAll('.sidebar a');
    
    // Get all dashboard sections
    const sections = document.querySelectorAll('.dashboard-section');
    
    // Add click event to each navigation link
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Check if this is an internal navigation link
            if (this.getAttribute('data-internal') === 'true') {
                // Let the global handler handle it
                return;
            }
            
            e.preventDefault();
            
            // Remove active class from all links and sections
            navLinks.forEach(l => l.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));
            
            // Add active class to clicked link
            this.classList.add('active');
            
            // Get the section id from the link id
            const sectionId = this.id.replace('nav-', '') + '-section';
            
            // Show the corresponding section
            const targetSection = document.getElementById(sectionId);
            if (targetSection) {
                targetSection.classList.add('active');
                
                // Load section specific data if needed
                if (this.id === 'nav-books') {
                    loadBooks();
                } else if (this.id === 'nav-users') {
                    loadUsers();
                } else if (this.id === 'nav-transactions') {
                    // If there's a function to load transactions data
                    if (typeof loadTransactions === 'function') {
                        loadTransactions();
                    }
                }
            }
        });
    });
}

async function loadUserInfo() {
    try {
        const response = await handleApiResponse(fetch('/dashboard/get-current-user', {
            headers: getAuthHeader()
        }));
        
        if (response.ok) {
            const userData = await response.json();
            document.getElementById('user-name').textContent = userData.name;
        }
    } catch (error) {
        console.error('Error loading user info:', error);
    }
}

async function loadDashboardStats() {
    try {
        // Load current user
        const userResponse = await handleApiResponse(fetch('/dashboard/get-current-user', {
            headers: getAuthHeader()
        }));
        
        if (!userResponse.ok) {
            throw new Error('Failed to load user information');
        }
        
        const userData = await userResponse.json();
        
        // Load user's current borrowings
        const borrowingsResponse = await handleApiResponse(fetch(`/api/users/${userData.barcode}/borrowings`, {
            headers: getAuthHeader()
        }));
        
        if (borrowingsResponse.ok) {
            const borrowings = await borrowingsResponse.json();
            
            // Ensure borrowings is an array
            const borrowingsArray = Array.isArray(borrowings) ? borrowings : [];
            
            // Count total borrowed books
            document.getElementById('books-borrowed').textContent = borrowingsArray.length;
            
            // Count books due soon (within next 3 days)
            const now = new Date();
            const threeDaysFromNow = new Date(now);
            threeDaysFromNow.setDate(now.getDate() + 3);
            
            const dueSoonCount = borrowingsArray.filter(book => {
                const dueDate = new Date(book.due_date);
                return dueDate <= threeDaysFromNow && dueDate >= now;
            }).length;
            
            document.getElementById('books-due-soon').textContent = dueSoonCount;
            
            // Count overdue books
            const overdueCount = borrowingsArray.filter(book => {
                return new Date(book.due_date) < now;
            }).length;
            
            document.getElementById('overdue-books').textContent = overdueCount;
        } else {
            throw new Error('Failed to load borrowings');
        }
    } catch (error) {
        console.error('Error loading dashboard stats:', error);
        document.getElementById('books-borrowed').textContent = 'Error';
        document.getElementById('books-due-soon').textContent = 'Error';
        document.getElementById('overdue-books').textContent = 'Error';
    }
}