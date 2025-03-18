document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the member dashboard with history section
    if (document.getElementById('history-section')) {
        // Load borrowing history when the tab is clicked
        document.getElementById('nav-history').addEventListener('click', loadBorrowingHistory);
    }
});

async function loadBorrowingHistory() {
    try {
        // Get current user
        const userResponse = await handleApiResponse(fetch('/dashboard/get-current-user', {
            headers: getAuthHeader()
        }));
        
        if (!userResponse.ok) {
            throw new Error('Failed to load user information');
        }
        
        const userData = await userResponse.json();
        
        // Load user's borrowing history
        const historyList = document.getElementById('history-list');
        historyList.innerHTML = '<tr><td colspan="5">Loading borrowing history...</td></tr>';
        
        const historyResponse = await handleApiResponse(fetch(`/api/users/${userData.barcode}/borrowing-history`, {
            headers: getAuthHeader()
        }));
        
        if (historyResponse.ok) {
            const history = await historyResponse.json();
            displayBorrowingHistory(history);
        } else {
            throw new Error('Failed to load borrowing history');
        }
    } catch (error) {
        console.error('Error loading borrowing history:', error);
        document.getElementById('history-list').innerHTML = 
            '<tr><td colspan="5">Error loading your borrowing history. Please try again.</td></tr>';
    }
}

function displayBorrowingHistory(history) {
    const historyList = document.getElementById('history-list');
    
    if (history.length === 0) {
        historyList.innerHTML = '<tr><td colspan="5">You have no borrowing history.</td></tr>';
        return;
    }
    
    historyList.innerHTML = '';
    
    // Sort history by checkout date, most recent first
    history.sort((a, b) => new Date(b.checkout_date) - new Date(a.checkout_date));
    
    history.forEach(item => {
        const checkoutDate = new Date(item.checkout_date).toLocaleDateString();
        const dueDate = new Date(item.due_date).toLocaleDateString();
        const returnDate = item.return_date ? new Date(item.return_date).toLocaleDateString() : 'Not returned';
        
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.book_title}</td>
            <td>${checkoutDate}</td>
            <td>${dueDate}</td>
            <td>${returnDate}</td>
            <td>${item.fine_amount > 0 ? '$' + item.fine_amount.toFixed(2) : 'None'}</td>
        `;
        
        // Add class for items with fines
        if (item.fine_amount > 0) {
            row.classList.add('has-fine');
        }
        
        historyList.appendChild(row);
    });
    
    // Add some CSS to highlight items with fines
    const style = document.createElement('style');
    style.innerHTML = `
        .has-fine {
            background-color: #fff9e6;
        }
        .has-fine td:last-child {
            color: #e67e22;
            font-weight: bold;
        }
    `;
    document.head.appendChild(style);
}