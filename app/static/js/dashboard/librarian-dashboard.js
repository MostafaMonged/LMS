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
        // Load books count
        const booksResponse = await handleApiResponse(fetch('/api/books', {
            headers: getAuthHeader()
        }));
        
        if (booksResponse.ok) {
            const booksData = await booksResponse.json();
            console.log("Books data received:", booksData); // Debug log
            
            // Check if booksData is an array
            if (Array.isArray(booksData)) {
                // If it's an array of books
                document.getElementById('total-books').textContent = booksData.length;
                
                // Count available books
                const availableBooks = booksData.reduce((count, book) => {
                    return count + (parseInt(book.available_copies) || 0);
                }, 0);
                
                document.getElementById('available-books').textContent = availableBooks;
            } 
            // If it's a stats object with total_books and available_books properties
            else if (booksData && typeof booksData === 'object' && 'total_books' in booksData && 'available_books' in booksData) {
                document.getElementById('total-books').textContent = booksData.total_books;
                document.getElementById('available-books').textContent = booksData.available_books;
            }
            // If it's an object with a books array
            else if (booksData && typeof booksData === 'object' && Array.isArray(booksData.books)) {
                document.getElementById('total-books').textContent = booksData.books.length;
                
                const availableBooks = booksData.books.reduce((count, book) => {
                    return count + (parseInt(book.available_copies) || 0);
                }, 0);
                
                document.getElementById('available-books').textContent = availableBooks;
            }
            // If we need to count total and available from a different structure
            else if (booksData && typeof booksData === 'object') {
                // Try to find any property that might be a book count
                let totalBooks = 0;
                let availableBooks = 0;
                
                // First try known properties
                if ('count' in booksData) totalBooks = booksData.count;
                if ('total' in booksData) totalBooks = booksData.total;
                if ('available' in booksData) availableBooks = booksData.available;
                
                // If we found values, use them
                if (totalBooks > 0) document.getElementById('total-books').textContent = totalBooks;
                if (availableBooks > 0) document.getElementById('available-books').textContent = availableBooks;
                else document.getElementById('available-books').textContent = "0";
            }
            else {
                // Fallback
                document.getElementById('total-books').textContent = "0";
                document.getElementById('available-books').textContent = "0";
            }
        } else {
            document.getElementById('total-books').textContent = 'Error';
            document.getElementById('available-books').textContent = 'Error';
        }
        
        // Load users count (members only)
        const usersResponse = await handleApiResponse(fetch('/api/users', {
            headers: getAuthHeader()
        }));
        
        if (usersResponse.ok) {
            const usersData = await usersResponse.json();
            console.log("Users data received:", usersData); // Debug log
            
            // Check if usersData is an array
            if (Array.isArray(usersData)) {
                const membersCount = usersData.filter(user => user.role === 'Member').length;
                document.getElementById('total-members').textContent = membersCount;
            } 
            // If it's an object with a count or members_count property
            else if (usersData && typeof usersData === 'object') {
                if ('members_count' in usersData) {
                    document.getElementById('total-members').textContent = usersData.members_count;
                } else if ('count' in usersData) {
                    document.getElementById('total-members').textContent = usersData.count;
                } else {
                    document.getElementById('total-members').textContent = "0";
                }
            } else {
                document.getElementById('total-members').textContent = "0";
            }
        } else {
            document.getElementById('total-members').textContent = 'Error';
        }
        
        // Load overdue books count
        const overdueResponse = await handleApiResponse(fetch('/api/overdue-books', {
            headers: getAuthHeader()
        }));
        
        if (overdueResponse.ok) {
            const overdueData = await overdueResponse.json();
            console.log("Overdue data received:", overdueData); // Debug log
            
            // Check structure of overdueData
            if (overdueData && Array.isArray(overdueData)) {
                document.getElementById('overdue-books').textContent = overdueData.length;
            } else if (overdueData && overdueData.overdue_books && Array.isArray(overdueData.overdue_books)) {
                document.getElementById('overdue-books').textContent = overdueData.overdue_books.length;
            } else if (overdueData && typeof overdueData === 'object') {
                if ('count' in overdueData) {
                    document.getElementById('overdue-books').textContent = overdueData.count;
                } else {
                    document.getElementById('overdue-books').textContent = "0";
                }
            } else {
                document.getElementById('overdue-books').textContent = "0";
            }
        } else {
            document.getElementById('overdue-books').textContent = 'Error';
        }
    } catch (error) {
        console.error('Error loading dashboard stats:', error);
        document.getElementById('total-books').textContent = 'Error';
        document.getElementById('available-books').textContent = 'Error';
        document.getElementById('total-members').textContent = 'Error';
        document.getElementById('overdue-books').textContent = 'Error';
    }
}