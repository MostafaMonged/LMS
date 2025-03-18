document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the member dashboard with my books section
    if (document.getElementById('my-books-section')) {
        // Load my books when the tab is clicked
        document.getElementById('nav-my-books').addEventListener('click', loadMyBooks);
    }
});

async function loadMyBooks() {
    try {
        // Get current user
        const userResponse = await handleApiResponse(fetch('/dashboard/get-current-user', {
            headers: getAuthHeader()
        }));
        
        if (!userResponse.ok) {
            throw new Error('Failed to load user information');
        }
        
        const userData = await userResponse.json();
        
        // Load user's current borrowings
        const myBooksList = document.getElementById('my-books-list');
        myBooksList.innerHTML = '<tr><td colspan="5">Loading your books...</td></tr>';
        
        const borrowingsResponse = await handleApiResponse(fetch(`/api/users/${userData.barcode}/borrowings`, {
            headers: getAuthHeader()
        }));
        
        if (borrowingsResponse.ok) {
            const borrowings = await borrowingsResponse.json();
            displayMyBooks(borrowings);
        } else {
            throw new Error('Failed to load borrowings');
        }
    } catch (error) {
        console.error('Error loading my books:', error);
        document.getElementById('my-books-list').innerHTML = 
            '<tr><td colspan="5">Error loading your books. Please try again.</td></tr>';
    }
}

function displayMyBooks(borrowings) {
    const myBooksList = document.getElementById('my-books-list');
    
    if (borrowings.length === 0) {
        myBooksList.innerHTML = '<tr><td colspan="5">You have no books currently checked out.</td></tr>';
        return;
    }
    
    myBooksList.innerHTML = '';
    const now = new Date();
    
    borrowings.forEach(borrowing => {
        const checkoutDate = new Date(borrowing.checkout_date);
        const dueDate = new Date(borrowing.due_date);
        
        // Calculate days left (negative if overdue)
        const daysLeft = Math.ceil((dueDate - now) / (1000 * 60 * 60 * 24));
        
        const row = document.createElement('tr');
        
        // Add a class for overdue books
        if (daysLeft < 0) {
            row.classList.add('overdue');
        }
        
        row.innerHTML = `
            <td>${borrowing.book_title}</td>
            <td>${checkoutDate.toLocaleDateString()}</td>
            <td>${dueDate.toLocaleDateString()}</td>
            <td>${daysLeft < 0 ? 'OVERDUE by ' + Math.abs(daysLeft) + ' days' : daysLeft + ' days'}</td>
            <td>
                <button class="btn-small" onclick="returnBook(${borrowing.transaction_id})">Return</button>
            </td>
        `;
        myBooksList.appendChild(row);
    });
    
    // Add some CSS to highlight overdue books
    const style = document.createElement('style');
    style.innerHTML = `
        .overdue {
            background-color: #ffecec;
            color: #e74c3c;
            font-weight: bold;
        }
    `;
    document.head.appendChild(style);
}

async function returnBook(transactionId) {
    try {
        const response = await handleApiResponse(fetch(`/api/return/${transactionId}`, {
            method: 'PUT',
            headers: getAuthHeader()
        }));
        
        if (response.ok) {
            const data = await response.json();
            
            let message = 'Book returned successfully!';
            if (data.fine_amount && data.fine_amount > 0) {
                message += `\n\nNote: A fine of $${data.fine_amount.toFixed(2)} has been recorded for late return.`;
            }
            
            alert(message);
            
            // Reload my books
            loadMyBooks();
        } else {
            const error = await response.json();
            alert(`Error: ${error.error || 'Failed to return book'}`);
        }
    } catch (error) {
        console.error('Error returning book:', error);
        alert('Error returning book. Please try again.');
    }
}