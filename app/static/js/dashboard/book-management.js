document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the librarian dashboard with books section
    if (document.getElementById('books-section')) {
        // Setup add book button
        document.getElementById('add-book-btn').addEventListener('click', showAddBookForm);
        
        // Setup search buttons
        document.getElementById('book-search-btn')?.addEventListener('click', searchBooks);
        document.getElementById('book-search-clear')?.addEventListener('click', function() {
            // Clear all search fields
            document.getElementById('book-search-title').value = '';
            document.getElementById('book-search-author').value = '';
            document.getElementById('book-search-category').value = '';
            document.getElementById('book-search-barcode').value = '';
            
            // Load all books
            loadBooks();
        });
        
        // Load books when the tab is clicked
        document.getElementById('nav-books').addEventListener('click', loadBooks);
    }
});

// Show form to add a new book
function showAddBookForm() {
    // In a real app, you'd show a modal or form
    // For now, we'll use prompts
    
    const title = prompt('Enter book title:');
    if (!title) return; // Cancel if no title
    
    const author = prompt('Enter author:');
    if (!author) return;
    
    const category = prompt('Enter subject category:');
    if (!category) return;
    
    const pubDate = prompt('Enter publication date (YYYY-MM-DD):');
    if (!pubDate) return;
    
    addBook(title, author, category, pubDate);
}

// Add a new book to the database
async function addBook(title, author, subject_category, publication_date) {
    try {
        const response = await handleApiResponse(fetch('/api/books', {
            method: 'POST',
            headers: getAuthHeader(),
            body: JSON.stringify({
                title,
                author,
                subject_category,
                publication_date
            })
        }));
        
        if (response.ok) {
            alert('Book added successfully.');
            loadBooks(); // Reload books list
        } else {
            const errorData = await response.json().catch(() => ({}));
            alert(`Error: ${errorData.error || 'Failed to add book.'}`);
        }
    } catch (error) {
        console.error('Error adding book:', error);
        alert('Error adding book. Please try again.');
    }
}

// Load all books from the database
async function loadBooks() {
    try {
        const booksList = document.getElementById('books-list');
        booksList.innerHTML = '<tr><td colspan="6">Loading books...</td></tr>';
        
        const response = await handleApiResponse(fetch('/api/books', {
            headers: getAuthHeader()
        }));
        
        if (response.ok) {
            const data = await response.json();
            
            // Check if data is an array or has a books property that's an array
            let books;
            if (Array.isArray(data)) {
                books = data;
            } else if (data && Array.isArray(data.books)) {
                books = data.books;
            } else {
                // If we can't find an array of books, create an empty array
                console.error('Unexpected API response format:', data);
                books = [];
            }
            
            displayBooks(books);
        } else {
            booksList.innerHTML = '<tr><td colspan="6">Error loading books. Please try again.</td></tr>';
        }
    } catch (error) {
        console.error('Error loading books:', error);
        document.getElementById('books-list').innerHTML = 
            '<tr><td colspan="6">Error loading books. Please try again.</td></tr>';
    }
}

// Display books in the table
function displayBooks(books) {
    const booksList = document.getElementById('books-list');
    
    // Ensure books is an array
    if (!Array.isArray(books)) {
        console.error('displayBooks received non-array data:', books);
        books = [];
    }
    
    if (books.length === 0) {
        booksList.innerHTML = '<tr><td colspan="6">No books found.</td></tr>';
        return;
    }
    
    booksList.innerHTML = '';
    
    books.forEach(book => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${book.barcode || 'N/A'}</td>
            <td>${book.title || 'N/A'}</td>
            <td>${book.author || 'N/A'}</td>
            <td>${book.subject_category || 'N/A'}</td>
            <td>${book.available_copies || 0}/${book.total_copies || 0}</td>
            <td>
                <button class="btn-small" onclick="editBook('${book.barcode}')">Edit</button>
                <button class="btn-small" onclick="viewCopies('${book.barcode}')">View Copies</button>
                <button class="btn-small" onclick="addCopy('${book.barcode}')">Add Copy</button>
                <button class="btn-small btn-secondary" onclick="deleteBook('${book.barcode}')">Delete</button>
            </td>
        `;
        booksList.appendChild(row);
    });
}

// View copies of a specific book
async function viewCopies(barcode) {
    try {
        // Use the correct API endpoint for fetching book copies
        // UPDATED: Changed from /api/books/${barcode}/copies to /api/book_copies/${barcode}
        const response = await handleApiResponse(fetch(`/api/book_copies/${barcode}`, {
            headers: getAuthHeader()
        }));
        
        if (response.ok) {
            const data = await response.json();
            
            // Ensure we have an array of copies
            const copies = Array.isArray(data) ? data : 
                        (Array.isArray(data.book_copies) ? data.book_copies : []);
            
            if (copies.length === 0) {
                alert(`No copies found for book with barcode: ${barcode}`);
                return;
            }
            
            // Format copies information for display
            let copiesInfo = `Copies of Book (barcode: ${barcode}):\n\n`;
            
            copies.forEach((copy, index) => {
                copiesInfo += `Copy ${index+1}:\n`;
                copiesInfo += `ID: ${copy.id || 'N/A'}\n`;
                copiesInfo += `Location: ${copy.rack_location || 'Not specified'}\n`;
                copiesInfo += `Status: ${copy.is_available ? 'Available' : 'Checked Out'}\n\n`;
            });
            
            alert(copiesInfo);
        } else {
            alert(`Error: Failed to load book copies. Status: ${response.status}`);
        }
    } catch (error) {
        console.error('Error viewing book copies:', error);
        alert('Error loading book copies. Please try again.');
    }
}

// Add a new copy of a book
async function addCopy(barcode) {
    try {
        const location = prompt('Enter rack location for this copy:') || '';
        
        // UPDATED: Changed from /api/books/${barcode}/copies to /api/book_copies/${barcode}
        const response = await handleApiResponse(fetch(`/api/book_copies/${barcode}`, {
            method: 'POST',
            headers: getAuthHeader(),
            body: JSON.stringify({
                rack_location: location
            })
        }));
        
        if (response.ok) {
            alert('Book copy added successfully.');
            loadBooks(); // Reload books list
        } else {
            const errorData = await response.json().catch(() => ({}));
            alert(`Error: ${errorData.error || 'Failed to add book copy.'}`);
        }
    } catch (error) {
        console.error('Error adding book copy:', error);
        alert('Error adding book copy. Please try again.');
    }
}

// Edit book details
async function editBook(barcode) {
    try {
        const response = await handleApiResponse(fetch(`/api/books/${barcode}`, {
            headers: getAuthHeader()
        }));
        
        if (response.ok) {
            const book = await response.json();
            
            // Get updated values for all fields
            const title = prompt('Edit Title:', book.title) || book.title;
            const author = prompt('Edit Author:', book.author) || book.author;
            const subject_category = prompt('Edit Category:', book.subject_category) || book.subject_category;
            
            // Format the publication date for the prompt
            let pubDate = book.publication_date;
            if (pubDate) {
                // If it's a full ISO date, trim to just YYYY-MM-DD
                if (pubDate.includes('T')) {
                    pubDate = pubDate.split('T')[0];
                }
            }
            
            const publication_date = prompt('Edit Publication Date (YYYY-MM-DD):', pubDate) || book.publication_date;
            
            // Only proceed if at least one field was changed
            if (title === book.title && 
                author === book.author && 
                subject_category === book.subject_category &&
                publication_date === book.publication_date) {
                alert('No changes made to the book.');
                return;
            }
            
            const updatedBook = {
                title,
                author,
                subject_category,
                publication_date
            };
            
            const updateResponse = await handleApiResponse(fetch(`/api/books/${barcode}`, {
                method: 'PUT',
                headers: getAuthHeader(),
                body: JSON.stringify(updatedBook)
            }));
            
            if (updateResponse.ok) {
                alert('Book updated successfully.');
                loadBooks(); // Reload books list
            } else {
                const errorData = await updateResponse.json().catch(() => ({}));
                alert(`Error: ${errorData.error || 'Failed to update book.'}`);
            }
        } else {
            alert('Error: Book not found.');
        }
    } catch (error) {
        console.error('Error editing book:', error);
        alert('Error editing book. Please try again.');
    }
}

// Delete a book
async function deleteBook(barcode) {
    try {
        if (!confirm(`Are you sure you want to delete the book with barcode ${barcode}?`)) {
            return;
        }
        
        const response = await handleApiResponse(fetch(`/api/books/${barcode}`, {
            method: 'DELETE',
            headers: getAuthHeader()
        }));
        
        if (response.ok) {
            alert('Book deleted successfully.');
            loadBooks(); // Reload books list
        } else {
            const errorData = await response.json().catch(() => ({}));
            alert(`Error: ${errorData.error || 'Failed to delete book.'}`);
        }
    } catch (error) {
        console.error('Error deleting book:', error);
        alert('Error deleting book. Please try again.');
    }
}

// Fixed searchBooks function using URLSearchParams
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
        
        // Create URLSearchParams object for proper URL parameter encoding
        const params = new URLSearchParams();
        if (titleSearch) params.append('title', titleSearch);
        if (authorSearch) params.append('author', authorSearch);
        if (categorySearch) params.append('subject_category', categorySearch);
        if (barcodeSearch) params.append('barcode', barcodeSearch);
        
        // Convert to string and log for debugging
        const queryString = params.toString();
        console.log(`Searching with: /api/search/books?${queryString}`);
        
        const response = await handleApiResponse(fetch(`/api/search/books?${queryString}`, {
            headers: getAuthHeader()
        }));
        
        if (response.ok) {
            const data = await response.json();
            console.log("Search results:", data);
            
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
            console.error("Search failed with status:", response.status);
            booksList.innerHTML = '<tr><td colspan="6">Error searching books. Please try again.</td></tr>';
        }
    } catch (error) {
        console.error('Error searching books:', error);
        document.getElementById('books-list').innerHTML = 
            '<tr><td colspan="6">Error searching books. Please try again.</td></tr>';
    }
}