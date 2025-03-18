// Check authentication state on page load
document.addEventListener('DOMContentLoaded', function() {
    // Handle page navigation for single-page app experience
    setupInternalNavigation();
    
    // Setup logout button
    document.getElementById('logout-btn')?.addEventListener('click', function() {
        logout();
    });
});

// Make internal navigation work without full page reloads
function setupInternalNavigation() {
    document.addEventListener('click', function(e) {
        // Look for links that should be handled via our authenticated fetch
        if (e.target.tagName === 'A' && e.target.getAttribute('data-internal') === 'true') {
            e.preventDefault();
            const url = e.target.getAttribute('href');
            loadAuthenticatedPage(url);
        }
    });
}

// Function to handle API errors
function handleApiError(error, elementId) {
    console.error(`API Error: ${error}`);
    if (elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `<div class="error-message">An error occurred: ${error.message || 'Unknown error'}</div>`;
        }
    }
}