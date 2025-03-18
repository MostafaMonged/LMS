document.addEventListener('DOMContentLoaded', function() {
    // Check if the transactions section exists (we're on the librarian dashboard)
    if (document.getElementById('transactions-section')) {
        // Load transactions tab functionality
        setupTransactionsTabs();
        
        // Setup issue book form
        document.getElementById('issue-book-form').addEventListener('submit', issueBook);
        
        // Setup return book form
        document.getElementById('return-book-form').addEventListener('submit', returnBook);
        
        // Load overdue books when the tab is clicked
        document.querySelectorAll('.tab-btn').forEach(btn => {
            if (btn.dataset.tab === 'overdue') {
                btn.addEventListener('click', loadOverdueBooks);
            }
        });
    }
});

function setupTransactionsTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabName = this.dataset.tab;
            
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            this.classList.add('active');
            document.getElementById(`${tabName}-tab`).classList.add('active');
        });
    });
}

async function issueBook(e) {
    e.preventDefault();
    
    const userBarcode = document.getElementById('issue-user-barcode').value;
    const bookBarcode = document.getElementById('issue-book-barcode').value;
    
    try {
        const response = await handleApiResponse(fetch('/api/issue', {
            method: 'POST',
            headers: getAuthHeader(),
            body: JSON.stringify({
                user_barcode: userBarcode,
                book_barcode: bookBarcode
            })
        }));
        
        if (response.ok) {
            const data = await response.json();
            alert(`Book issued successfully!\n\nTransaction ID: ${data.transaction_id}\nDue Date: ${data.due_date}`);
            document.getElementById('issue-book-form').reset();
        } else {
            const data = await response.json();
            alert(`Error: ${data.error || 'Failed to issue book.'}`);
        }
    } catch (error) {
        console.error('Error issuing book:', error);
        alert('Error issuing book. Please try again.');
    }
}

async function returnBook(e) {
    e.preventDefault();
    
    const transactionId = document.getElementById('return-transaction-id').value;
    
    try {
        const response = await handleApiResponse(fetch(`/api/return/${transactionId}`, {
            method: 'PUT',
            headers: getAuthHeader()
        }));
        
        if (response.ok) {
            const data = await response.json();
            let message = `Book returned successfully!\n\nTransaction ID: ${data.transaction_id}`;
            
            if (data.fine_amount && data.fine_amount > 0) {
                message += `\nFine Amount: $${data.fine_amount.toFixed(2)}`;
            }
            
            alert(message);
            document.getElementById('return-book-form').reset();
        } else {
            const data = await response.json();
            alert(`Error: ${data.error || 'Failed to return book.'}`);
        }
    } catch (error) {
        console.error('Error returning book:', error);
        alert('Error returning book. Please try again.');
    }
}

async function loadOverdueBooks() {
    try {
        const overdueList = document.getElementById('overdue-list');
        overdueList.innerHTML = '<tr><td colspan="6">Loading overdue books...</td></tr>';
        
        const response = await handleApiResponse(fetch('/api/overdue-books', {
            headers: getAuthHeader()
        }));
        
        if (response.ok) {
            const overdueData = await response.json();
            
            if (overdueData.overdue_books.length === 0) {
                overdueList.innerHTML = '<tr><td colspan="6">No overdue books found.</td></tr>';
                return;
            }
            
            overdueList.innerHTML = '';
            
            overdueData.overdue_books.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.transaction_id}</td>
                    <td>${item.user_name}</td>
                    <td>${item.book_title}</td>
                    <td>${new Date(item.due_date).toLocaleDateString()}</td>
                    <td>${item.days_overdue}</td>
                    <td>$${item.fine_amount.toFixed(2)}</td>
                `;
                overdueList.appendChild(row);
            });
        } else {
            overdueList.innerHTML = '<tr><td colspan="6">Error loading overdue books. Please try again.</td></tr>';
        }
    } catch (error) {
        console.error('Error loading overdue books:', error);
        document.getElementById('overdue-list').innerHTML = 
            '<tr><td colspan="6">Error loading overdue books. Please try again.</td></tr>';
    }
}