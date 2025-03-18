document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the member dashboard with search section
    if (document.getElementById('search-books-section')) {
        // Setup search form
        document.getElementById('search-btn').addEventListener('click', searchBooks);
        
        // Load search section when the tab is clicked
        document.getElementById('nav-search-books').addEventListener('click', () => {
            // Clear previous search results
            document.getElementById('search-results-list').innerHTML = '';
        });
    }
});

// Update the searchBooks function:
async function searchBooks() {
    const titleSearch = document.getElementById('book-search-title').value.trim();
    const authorSearch = document.getElementById('book-search-author').value.trim();
    const categorySearch = document.getElementById('book-search-category').value.trim();
    const barcodeSearch = document.getElementById('book-search-barcode').value.trim();
    
    // If all fields are empty, load all books
    if (!titleSearch && !authorSearch && !categorySearch && !barcodeSearch) {
        loadBooks();
        return;
    }
    
    try {
        const booksList = document.getElementById('books-list');
        booksList.innerHTML = '<tr><td colspan="6">Searching...</td></tr>';
        
        // Build search query params
        let queryParams = [];
        if (titleSearch) queryParams.push(`title=${encodeURIComponent(titleSearch)}`);
        if (authorSearch) queryParams.push(`author=${encodeURIComponent(authorSearch)}`);
        // CRITICAL FIX: Use subject_category not subject to match backend parameter name
        if (categorySearch) queryParams.push(`subject_category=${encodeURIComponent(categorySearch)}`);
        if (barcodeSearch) queryParams.push(`barcode=${encodeURIComponent(barcodeSearch)}`);
        
        const queryString = queryParams.join('&');
        
        const response = await handleApiResponse(fetch(`/api/search/books?${queryString}`, {
            headers: getAuthHeader()
        }));
        
        if (response.ok) {
            const data = await response.json();
            
            // Handle different response formats
            let books;
            if (Array.isArray(data)) {
                books = data;
            } else if (data && Array.isArray(data.books)) {
                books = data.books;
            } else {
                console.error('Unexpected API response format:', data);
                books = [];
            }
            
            if (books.length === 0) {
                booksList.innerHTML = '<tr><td colspan="6">No books found matching your search criteria.</td></tr>';
            } else {
                displayBooks(books);
            }
        } else {
            booksList.innerHTML = '<tr><td colspan="6">Error searching books. Please try again.</td></tr>';
        }
    } catch (error) {
        console.error('Error searching books:', error);
        document.getElementById('books-list').innerHTML = 
            '<tr><td colspan="6">Error searching books. Please try again.</td></tr>';
    }
}

function displaySearchResults(books) {
    const searchResultsList = document.getElementById('search-results-list');
    
    if (books.length === 0) {
        searchResultsList.innerHTML = '<tr><td colspan="5">No books found matching your search criteria.</td></tr>';
        return;
    }
    
    searchResultsList.innerHTML = '';
    
    books.forEach(book => {
        const availableCopies = book.available_copies || 0;
        const totalCopies = book.total_copies || 0;
        
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${book.title}</td>
            <td>${book.author}</td>
            <td>${book.subject_category}</td>
            <td>${availableCopies}/${totalCopies}</td>
            <td>
                ${availableCopies > 0 
                    ? `<button class="btn-small" onclick="requestBook('${book.barcode}')">Request</button>`
                    : '<span class="unavailable">Unavailable</span>'
                }
                <button class="btn-small" onclick="viewBookDetails('${book.barcode}')">Details</button>
            </td>
        `;
        searchResultsList.appendChild(row);
    });
}

async function viewBookDetails(barcode) {
    try {
        const response = await handleApiResponse(fetch(`/api/books/${barcode}`, {
            headers: getAuthHeader()
        }));
        
        if (response.ok) {
            const book = await response.json();
            
            // Display book details in a simple alert
            const detailsText = `
                Title: ${book.title}
                Author: ${book.author}
                Category: ${book.subject_category}
                Publication Date: ${new Date(book.publication_date).toLocaleDateString()}
                Available Copies: ${book.available_copies || 0}/${book.total_copies || 0}
                Barcode: ${book.barcode}
            `;
            
            alert(detailsText);
        } else {
            alert('Error: Book details not found');
        }
    } catch (error) {
        console.error('Error viewing book details:', error);
        alert('Error loading book details. Please try again.');
    }
}

async function requestBook(barcode) {
    try {
        // Get current user info
        const userResponse = await handleApiResponse(fetch('/dashboard/get-current-user', {
            headers: getAuthHeader()
        }));
        
        if (!userResponse.ok) {
            throw new Error('Failed to load user information');
        }
        
        const userData = await userResponse.json();
        
        // Request (checkout) the book using the user's barcode
        const checkoutResponse = await handleApiResponse(fetch('/api/checkout', {
            method: 'POST',
            headers: getAuthHeader(),
            body: JSON.stringify({
                user_barcode: userData.barcode,
                book_barcode: barcode
            })
        }));
        
        if (checkoutResponse.ok) {
            const data = await checkoutResponse.json();
            alert(`Book checkout successful!\nDue date: ${new Date(data.due_date).toLocaleDateString()}`);
            
            // Refresh search results to update availability
            searchBooks();
        } else {
            const error = await checkoutResponse.json();
            alert(`Error: ${error.error || 'Failed to checkout book'}`);
        }
    } catch (error) {
        console.error('Error requesting book:', error);
        alert('Error requesting book. Please try again.');
    }
}