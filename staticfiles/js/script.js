// Custom JavaScript for SibloreEvents

document.addEventListener('DOMContentLoaded', function() {
    // Initialize progress bar
    initializeProgressBar();
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Smooth scroll for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Dynamic loading indicator
    const loadingIndicators = document.querySelectorAll('.loading-indicator');
    loadingIndicators.forEach(function(indicator) {
        indicator.innerHTML = '<div class="spinner"></div> Loading...';
    });

    // Simple Side Menu Toggle
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Toggle the collapse
            if (navbarCollapse.classList.contains('show')) {
                navbarCollapse.classList.remove('show');
            } else {
                navbarCollapse.classList.add('show');
            }
        });

        // Close menu when clicking on backdrop
        navbarCollapse.addEventListener('click', function(e) {
            if (e.target === navbarCollapse) {
                navbarCollapse.classList.remove('show');
            }
        });

        // Close menu when clicking on close button (×)
        const navbarNav = document.querySelector('.navbar-nav');
        if (navbarNav) {
            navbarNav.addEventListener('click', function(e) {
                // Check if click is on the close button area
                if (e.target === navbarNav && e.offsetX >= navbarNav.offsetWidth - 60) {
                    navbarCollapse.classList.remove('show');
                }
            });
        }

        // Close menu when clicking on links
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
        navLinks.forEach(function(link) {
            link.addEventListener('click', function() {
                navbarCollapse.classList.remove('show');
            });
        });

        // Close menu on escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && navbarCollapse.classList.contains('show')) {
                navbarCollapse.classList.remove('show');
            }
        });
    }

    // Search functionality (if search form exists)
    const searchForm = document.querySelector('#search-form');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[type="search"]');
        const searchResults = document.querySelector('#search-results');
        
        if (searchInput && searchResults) {
            let searchTimeout;
            
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                const query = this.value.trim();
                
                if (query.length < 2) {
                    searchResults.style.display = 'none';
                    return;
                }
                
                searchTimeout = setTimeout(function() {
                    // Here you would typically make an AJAX call to search
                    // For now, we'll just show a loading state
                    searchResults.innerHTML = '<div class="p-3 text-center"><div class="spinner"></div> Searching...</div>';
                    searchResults.style.display = 'block';
                    
                    // Simulate search delay
                    setTimeout(function() {
                        searchResults.innerHTML = '<div class="p-3 text-muted">No results found</div>';
                    }, 1000);
                }, 300);
            });
        }
    }

    // Image preview for file uploads
    const fileInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.createElement('img');
                    preview.src = e.target.result;
                    preview.className = 'img-thumbnail mt-2';
                    preview.style.maxWidth = '200px';
                    
                    // Remove any existing preview
                    const existingPreview = input.parentNode.querySelector('.img-thumbnail');
                    if (existingPreview) {
                        existingPreview.remove();
                    }
                    
                    input.parentNode.appendChild(preview);
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // Quantity selector for merchandise
    const quantitySelectors = document.querySelectorAll('.quantity-selector');
    quantitySelectors.forEach(function(selector) {
        const minusBtn = selector.querySelector('.minus-btn');
        const plusBtn = selector.querySelector('.plus-btn');
        const input = selector.querySelector('input[type="number"]');
        
        if (minusBtn && plusBtn && input) {
            minusBtn.addEventListener('click', function() {
                const currentValue = parseInt(input.value) || 0;
                const minValue = parseInt(input.min) || 1;
                if (currentValue > minValue) {
                    input.value = currentValue - 1;
                }
            });
            
            plusBtn.addEventListener('click', function() {
                const currentValue = parseInt(input.value) || 0;
                const maxValue = parseInt(input.max) || 99;
                if (currentValue < maxValue) {
                    input.value = currentValue + 1;
                }
            });
        }
    });

    // Back to top button
    const backToTopBtn = document.createElement('button');
    backToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTopBtn.className = 'btn btn-primary back-to-top';
    backToTopBtn.style.cssText = 'position: fixed; bottom: 20px; right: 20px; display: none; z-index: 1000; border-radius: 50%; width: 50px; height: 50px;';
    document.body.appendChild(backToTopBtn);
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.style.display = 'block';
        } else {
            backToTopBtn.style.display = 'none';
        }
    });
    
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
});

// Progress Bar Functions
function initializeProgressBar() {
    const progressBar = document.getElementById('progressBar');
    const mainContent = document.getElementById('mainContent');
    
    // Ensure loading screen is visible and content is hidden on page load
    if (progressBar && !progressBar.classList.contains('loading')) {
        progressBar.classList.add('loading');
    }
    if (mainContent) {
        mainContent.style.opacity = '0';
        mainContent.style.visibility = 'hidden';
    }
    
    // Show loading screen on initial page load for 3 seconds
    setTimeout(function() {
        hideProgressBar();
        showMainContent();
    }, 3000);
    
    // Show progress bar on ALL navigation (comprehensive coverage)
    setupNavigationHandlers();
    
    // Show progress bar on form submission
    setupFormHandlers();
}

function setupNavigationHandlers() {
    // Handle all anchor tags
    const links = document.querySelectorAll('a[href]');
    links.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Apply to all internal links (excluding external, anchors, mailto, tel, javascript)
            if (href && 
                !href.startsWith('#') && 
                !href.startsWith('http://') && 
                !href.startsWith('https://') && 
                !href.startsWith('mailto:') && 
                !href.startsWith('tel:') && 
                !href.startsWith('javascript:')) {
                
                e.preventDefault(); // Prevent immediate navigation
                
                // Hide main content and show loading page
                hideMainContent();
                showProgressBar(3000);
                
                // Navigate after 3 seconds
                setTimeout(function() {
                    window.location.href = href;
                }, 3000);
            }
        });
    });
    
    // Handle any dynamically added links
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) { // Element node
                        const newLinks = node.querySelectorAll ? node.querySelectorAll('a[href]') : [];
                        newLinks.forEach(function(link) {
                            // Re-attach event listeners to new links
                            link.addEventListener('click', arguments.callee);
                        });
                    }
                });
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

function setupFormHandlers() {
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            showProgressBar(2000); // Show for 2 seconds on form submission
        });
    });
}

function hideMainContent() {
    const mainContent = document.getElementById('mainContent');
    if (mainContent) {
        mainContent.style.opacity = '0';
        mainContent.style.visibility = 'hidden';
    }
}

function showMainContent() {
    const mainContent = document.getElementById('mainContent');
    if (mainContent) {
        mainContent.style.opacity = '1';
        mainContent.style.visibility = 'visible';
    }
}

function showProgressBar(duration = 2000) {
    const progressBar = document.getElementById('progressBar');
    if (progressBar) {
        // Force immediate visibility
        progressBar.style.display = 'flex';
        progressBar.style.opacity = '1';
        progressBar.style.visibility = 'visible';
        progressBar.classList.add('loading');
        
        // Auto-hide after specified duration
        setTimeout(function() {
            hideProgressBar();
        }, 2000);
    }
}

function hideProgressBar() {
    const progressBar = document.getElementById('progressBar');
    if (progressBar) {
        progressBar.classList.remove('loading');
        setTimeout(function() {
            progressBar.style.opacity = '0';
            progressBar.style.visibility = 'hidden';
        }, 300);
    }
}

function showMainContent() {
    const mainContent = document.getElementById('mainContent');
    if (mainContent) {
        mainContent.style.opacity = '1';
        mainContent.style.visibility = 'visible';
    }
}

function hideMainContent() {
    const mainContent = document.getElementById('mainContent');
    if (mainContent) {
        mainContent.style.opacity = '0';
        mainContent.style.visibility = 'hidden';
    }
}

// Utility functions
function showLoading(element) {
    element.disabled = true;
    element.innerHTML = '<div class="spinner"></div> Loading...';
}

function hideLoading(element, originalText) {
    element.disabled = false;
    element.innerHTML = originalText;
}

function formatCurrency(amount, currency = 'KSh') {
    return `${currency} ${parseFloat(amount).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')}`;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    document.body.appendChild(container);
    return container;
}

// Page loading animation
function showPageLoader() {
    const loader = document.createElement('div');
    loader.className = 'page-loading';
    loader.innerHTML = `
        <div class="spinner-container">
            <div class="spinner"></div>
            <p>Loading...</p>
        </div>
    `;
    document.body.appendChild(loader);
}

function hidePageLoader() {
    const loader = document.querySelector('.page-loading');
    if (loader) {
        loader.remove();
    }
}

// Show page loader on navigation
document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('a[href]');
    links.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Show loader for internal links (excluding anchors and external links)
            if (href && !href.startsWith('#') && !href.startsWith('http') && !href.startsWith('mailto') && !href.startsWith('tel')) {
                showPageLoader();
            }
        });
    });
});
