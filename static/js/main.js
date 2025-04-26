// Main JavaScript file for the Bus Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Initialize popovers
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
    
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
    
    // Toggle sidebar on mobile
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            document.querySelector('.sidebar').classList.toggle('show');
        });
    }
    
    // Close alert messages
    const alertCloseButtons = document.querySelectorAll('.alert .btn-close');
    alertCloseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const alert = this.closest('.alert');
            alert.classList.add('fade');
            setTimeout(() => {
                alert.style.display = 'none';
            }, 150);
        });
    });
    
    // Handle status indicators display
    const statusElements = document.querySelectorAll('[data-status]');
    statusElements.forEach(element => {
        const status = element.dataset.status.toLowerCase().replace(' ', '-');
        const indicator = document.createElement('span');
        indicator.classList.add('status-indicator', `status-${status}`);
        element.prepend(indicator);
    });
    
    // Color-code route elements
    const routeElements = document.querySelectorAll('[data-route-color]');
    routeElements.forEach(element => {
        const color = element.dataset.routeColor;
        const indicator = document.createElement('span');
        indicator.classList.add('route-color-indicator');
        indicator.style.backgroundColor = color;
        element.prepend(indicator);
    });
});

// Helper function to format time
function formatTime(date) {
    if (!date) return 'N/A';
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

// Helper function to format date
function formatDate(date) {
    if (!date) return 'N/A';
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

// Function to simulate real-time updates (for demo purposes)
function simulateRealTimeUpdates() {
    // This would be replaced with actual API calls in a production environment
    console.log('Simulating real-time updates...');
    // Update would happen here via WebSockets or periodic AJAX calls
}
