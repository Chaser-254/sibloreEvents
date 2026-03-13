# SibloreEvents - Brand Assets & Implementation Guide

## Table of Contents
1. [CSS Custom Properties](#css-custom-properties)
2. [Component Library](#component-library)
3. [Template Patterns](#template-patterns)
4. [Icon System](#icon-system)
5. [Animation Guidelines](#animation-guidelines)
6. [Responsive Patterns](#responsive-patterns)
7. [Color System Implementation](#color-system-implementation)
8. [Typography Implementation](#typography-implementation)
9. [Form Patterns](#form-patterns)
10. [Navigation Patterns](#navigation-patterns)

---

## CSS Custom Properties

### Color Variables
```css
:root {
    /* Primary Brand Colors */
    --royal-blue: #2c3e50;
    --royal-blue-dark: #1a252f;
    --royal-blue-light: #34495e;
    
    /* Accent Colors */
    --accent-green: #27ae60;
    --accent-green-dark: #229954;
    --accent-green-light: #2ecc71;
    
    /* Text Colors */
    --text-primary: #2c3e50;
    --text-secondary: #7f8c8d;
    
    /* Background Colors */
    --bg-light: #f8f9fa;
    --bg-white: #ffffff;
    
    /* Border Colors */
    --border-light: #e9ecef;
    
    /* Semantic Colors */
    --success: #27ae60;
    --warning: #f39c12;
    --danger: #e74c3c;
    --info: #3498db;
    
    /* Shadows */
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.12);
    --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
    --shadow-lg: 0 10px 25px rgba(0,0,0,0.1);
}
```

### Typography Variables
```css
:root {
    /* Font Families */
    --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    
    /* Font Sizes */
    --text-xs: 0.75rem;    /* 12px */
    --text-sm: 0.875rem;   /* 14px */
    --text-base: 1rem;     /* 16px */
    --text-lg: 1.125rem;   /* 18px */
    --text-xl: 1.25rem;    /* 20px */
    --text-2xl: 1.5rem;    /* 24px */
    --text-3xl: 1.875rem;  /* 30px */
    --text-4xl: 2.25rem;   /* 36px */
    
    /* Font Weights */
    --font-light: 300;
    --font-normal: 400;
    --font-medium: 500;
    --font-semibold: 600;
    --font-bold: 700;
    
    /* Line Heights */
    --leading-tight: 1.25;
    --leading-normal: 1.5;
    --leading-relaxed: 1.6;
}
```

### Spacing Variables
```css
:root {
    --space-1: 0.25rem;   /* 4px */
    --space-2: 0.5rem;    /* 8px */
    --space-3: 0.75rem;   /* 12px */
    --space-4: 1rem;      /* 16px */
    --space-5: 1.25rem;   /* 20px */
    --space-6: 1.5rem;    /* 24px */
    --space-8: 2rem;      /* 32px */
    --space-10: 2.5rem;   /* 40px */
    --space-12: 3rem;     /* 48px */
    --space-16: 4rem;     /* 64px */
}
```

---

## Component Library

### Button Components

#### Primary Button
```html
<button class="btn btn-primary">
    <i class="fas fa-check me-2"></i>
    Get Started
</button>
```

#### Secondary Button
```html
<button class="btn btn-secondary">
    <i class="fas fa-info-circle me-2"></i>
    Learn More
</button>
```

#### Outline Button
```html
<button class="btn btn-outline-primary">
    <i class="fas fa-download me-2"></i>
    Download
</button>
```

#### Button Sizes
```html
<button class="btn btn-primary btn-sm">Small</button>
<button class="btn btn-primary">Default</button>
<button class="btn btn-primary btn-lg">Large</button>
```

#### Button Groups
```html
<div class="btn-group" role="group">
    <button class="btn btn-outline-primary">Previous</button>
    <button class="btn btn-primary">Next</button>
</div>
```

### Card Components

#### Basic Card
```html
<div class="card">
    <div class="card-header">
        <h5 class="mb-0">
            <i class="fas fa-calendar-alt me-2"></i>
            Event Title
        </h5>
    </div>
    <div class="card-body">
        <p class="card-text">Event description goes here.</p>
        <button class="btn btn-primary btn-sm">View Details</button>
    </div>
</div>
```

#### Event Card
```html
<div class="card event-card">
    <img src="event-image.jpg" class="card-img-top" alt="Event">
    <div class="card-body">
        <h5 class="card-title">Event Name</h5>
        <p class="card-text text-muted">
            <i class="fas fa-calendar me-1"></i> March 15, 2026
            <i class="fas fa-clock ms-3 me-1"></i> 7:00 PM
        </p>
        <div class="d-flex justify-content-between align-items-center">
            <span class="badge bg-success">KES 1,500</span>
            <button class="btn btn-primary btn-sm">Book Now</button>
        </div>
    </div>
</div>
```

#### Stats Card
```html
<div class="stats-card">
    <i class="fas fa-users fa-2x text-primary mb-3"></i>
    <h3 class="text-primary">10,000+</h3>
    <p class="text-muted">Active Users</p>
</div>
```

### Alert Components

#### Success Alert
```html
<div class="alert alert-success" role="alert">
    <i class="fas fa-check-circle me-2"></i>
    Event created successfully!
</div>
```

#### Warning Alert
```html
<div class="alert alert-warning" role="alert">
    <i class="fas fa-exclamation-triangle me-2"></i>
    Limited seats available
</div>
```

#### Error Alert
```html
<div class="alert alert-danger" role="alert">
    <i class="fas fa-exclamation-circle me-2"></i>
    Payment failed. Please try again.
</div>
```

---

## Template Patterns

### Hero Section Pattern
```html
<section class="hero-section bg-primary text-white py-5">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-6">
                <h1 class="display-4 fw-bold mb-4">Discover Amazing Events</h1>
                <p class="lead mb-4">Your premier platform for events and merchandise. Connecting people through unforgettable experiences.</p>
                <div class="d-flex gap-3">
                    <a href="#" class="btn btn-light btn-lg">
                        <i class="fas fa-search me-2"></i>Browse Events
                    </a>
                    <a href="#" class="btn btn-outline-light btn-lg">
                        <i class="fas fa-plus me-2"></i>Create Event
                    </a>
                </div>
            </div>
            <div class="col-lg-6">
                <img src="hero-image.jpg" class="img-fluid rounded" alt="Events">
            </div>
        </div>
    </div>
</section>
```

### Feature Grid Pattern
```html
<section class="py-5">
    <div class="container">
        <div class="row text-center mb-5">
            <div class="col-lg-12">
                <h2 class="display-5 fw-bold">Why Choose SibloreEvents?</h2>
                <p class="lead text-muted">Everything you need to manage and attend events</p>
            </div>
        </div>
        <div class="row g-4">
            <div class="col-md-6 col-lg-3">
                <div class="feature-card h-100">
                    <div class="card-body text-center">
                        <i class="fas fa-ticket-alt fa-3x text-success mb-3"></i>
                        <h5 class="card-title">Easy Booking</h5>
                        <p class="card-text">Book tickets in just a few clicks with our streamlined process.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-6 col-lg-3">
                <div class="feature-card h-100">
                    <div class="card-body text-center">
                        <i class="fas fa-shield-alt fa-3x text-primary mb-3"></i>
                        <h5 class="card-title">Secure Payments</h5>
                        <p class="card-text">Safe and secure payment processing for all transactions.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-6 col-lg-3">
                <div class="feature-card h-100">
                    <div class="card-body text-center">
                        <i class="fas fa-mobile-alt fa-3x text-info mb-3"></i>
                        <h5 class="card-title">Mobile Friendly</h5>
                        <p class="card-text">Access events and manage bookings from any device.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-6 col-lg-3">
                <div class="feature-card h-100">
                    <div class="card-body text-center">
                        <i class="fas fa-headset fa-3x text-warning mb-3"></i>
                        <h5 class="card-title">24/7 Support</h5>
                        <p class="card-text">Round-the-clock customer support for all your needs.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
```

### Dashboard Layout Pattern
```html
<div class="container-fluid">
    <div class="row">
        <!-- Sidebar -->
        <nav class="col-md-3 col-lg-2 d-md-block bg-light sidebar">
            <div class="position-sticky pt-3">
                <ul class="nav flex-column">
                    <li class="nav-item">
                        <a class="nav-link active" href="#">
                            <i class="fas fa-tachometer-alt me-2"></i>
                            Dashboard
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">
                            <i class="fas fa-calendar me-2"></i>
                            My Events
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">
                            <i class="fas fa-ticket-alt me-2"></i>
                            Tickets
                        </a>
                    </li>
                </ul>
            </div>
        </nav>

        <!-- Main Content -->
        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                <h1 class="h2">Dashboard</h1>
                <div class="btn-toolbar mb-2 mb-md-0">
                    <div class="btn-group me-2">
                        <button type="button" class="btn btn-sm btn-outline-secondary">
                            <i class="fas fa-download me-1"></i>Export
                        </button>
                    </div>
                </div>
            </div>

            <!-- Stats Cards -->
            <div class="row g-4 mb-4">
                <div class="col-xl-3 col-md-6">
                    <div class="stat-card">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6 class="text-muted">Total Events</h6>
                                <h3 class="text-primary">24</h3>
                            </div>
                            <i class="fas fa-calendar fa-2x text-primary opacity-25"></i>
                        </div>
                    </div>
                </div>
                <!-- More stat cards... -->
            </div>
        </main>
    </div>
</div>
```

---

## Icon System

### Font Awesome Integration
```html
<!-- Font Awesome 6.4 -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
```

### Icon Usage Guidelines

#### Navigation Icons
```html
<!-- Primary Navigation -->
<i class="fas fa-home me-1"></i>Home
<i class="fas fa-calendar-alt me-1"></i>Events
<i class="fas fa-shopping-bag me-1"></i>Merchandise
<i class="fas fa-briefcase me-1"></i>Careers
```

#### Action Icons
```html
<!-- Actions -->
<i class="fas fa-plus"></i> Add
<i class="fas fa-edit"></i> Edit
<i class="fas fa-trash"></i> Delete
<i class="fas fa-eye"></i> View
<i class="fas fa-download"></i> Download
```

#### Status Icons
```html
<!-- Status Indicators -->
<i class="fas fa-check-circle text-success"></i> Success
<i class="fas fa-exclamation-triangle text-warning"></i> Warning
<i class="fas fa-times-circle text-danger"></i> Error
<i class="fas fa-info-circle text-info"></i> Info
```

#### Social Media Icons
```html
<!-- Footer Social Links -->
<a href="#" class="text-white me-3"><i class="fab fa-whatsapp"></i></a>
<a href="#" class="text-white me-3"><i class="fab fa-instagram"></i></a>
<a href="#" class="text-white me-3"><i class="fab fa-linkedin-in"></i></a>
```

### Icon Sizes
```css
.icon-xs { font-size: 0.75rem; }    /* 12px */
.icon-sm { font-size: 0.875rem; }   /* 14px */
.icon-base { font-size: 1rem; }     /* 16px */
.icon-lg { font-size: 1.25rem; }    /* 20px */
.icon-xl { font-size: 1.5rem; }     /* 24px */
.icon-2xl { font-size: 2rem; }      /* 32px */
.icon-3xl { font-size: 3rem; }      /* 48px */
```

---

## Animation Guidelines

### Transition Standards
```css
/* Standard Transitions */
.transition-all {
    transition: all 0.3s ease;
}

.transition-colors {
    transition: color 0.3s ease, background-color 0.3s ease;
}

.transition-transform {
    transition: transform 0.3s ease;
}
```

### Hover Effects
```css
/* Button Hover */
.btn:hover {
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
}

/* Card Hover */
.card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

/* Link Hover */
a:hover {
    color: var(--accent-green-dark);
}
```

### Loading Animations
```css
/* Spinner Animation */
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.spinner {
    animation: spin 1s linear infinite;
}

/* Pulse Animation */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.pulse {
    animation: pulse 2s infinite;
}
```

### Fade In Animation
```css
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in {
    animation: fadeIn 0.5s ease-in;
}
```

---

## Responsive Patterns

### Breakpoint System
```css
/* Bootstrap 5 Breakpoints */
/* xs: 0px及以上 (默认) */
/* sm: 576px及以上 */
/* md: 768px及以上 */
/* lg: 992px及以上 */
/* xl: 1200px及以上 */
/* xxl: 1400px及以上 */
```

### Mobile Navigation Pattern
```html
<!-- Mobile Menu Toggle -->
<button class="mobile-menu-toggle d-lg-none" onclick="toggleMobileSidebar()">
    <i class="fas fa-bars"></i>
</button>

<!-- Mobile Sidebar -->
<div class="mobile-sidebar" id="mobileSidebar">
    <div class="mobile-sidebar-header">
        <h5 class="fw-bold">SibloreEvents</h5>
        <p class="text-muted">Menu</p>
    </div>
    <div class="mobile-sidebar-body">
        <nav class="mobile-nav">
            <div class="nav-section">
                <div class="nav-section-title">Main</div>
                <a href="#" class="mobile-nav-link">
                    <i class="fas fa-home"></i>
                    <span>Home</span>
                </a>
                <!-- More links... -->
            </div>
        </nav>
    </div>
</div>
```

### Responsive Grid Patterns
```html
<!-- Event Cards Grid -->
<div class="row g-4">
    <div class="col-12 col-sm-6 col-lg-4 col-xl-3">
        <!-- Card -->
    </div>
</div>

<!-- Dashboard Layout -->
<div class="row">
    <div class="col-12 col-lg-8">
        <!-- Main Content -->
    </div>
    <div class="col-12 col-lg-4">
        <!-- Sidebar -->
    </div>
</div>
```

### Responsive Typography
```css
/* Fluid Typography */
@media (max-width: 576px) {
    .display-4 { font-size: 2rem; }
    .display-5 { font-size: 1.75rem; }
    .display-6 { font-size: 1.5rem; }
}

@media (min-width: 1400px) {
    .display-4 { font-size: 3rem; }
    .display-5 { font-size: 2.5rem; }
    .display-6 { font-size: 2rem; }
}
```

---

## Color System Implementation

### Semantic Color Classes
```css
/* Background Colors */
.bg-primary { background-color: var(--royal-blue); }
.bg-success { background-color: var(--accent-green); }
.bg-info { background-color: var(--info); }
.bg-warning { background-color: var(--warning); }
.bg-danger { background-color: var(--danger); }

/* Text Colors */
.text-primary { color: var(--royal-blue); }
.text-success { color: var(--accent-green); }
.text-info { color: var(--info); }
.text-warning { color: var(--warning); }
.text-danger { color: var(--danger); }

/* Border Colors */
.border-primary { border-color: var(--royal-blue); }
.border-success { border-color: var(--accent-green); }
.border-info { border-color: var(--info); }
.border-warning { border-color: var(--warning); }
.border-danger { border-color: var(--danger); }
```

### Gradient Backgrounds
```css
/* Primary Gradient */
.bg-gradient-primary {
    background: linear-gradient(135deg, var(--royal-blue) 0%, var(--accent-green) 100%);
}

/* Hero Gradient */
.bg-gradient-hero {
    background: linear-gradient(135deg, var(--royal-blue) 0%, #1e3a8a 100%);
}

/* Success Gradient */
.bg-gradient-success {
    background: linear-gradient(135deg, var(--accent-green) 0%, var(--accent-green-dark) 100%);
}
```

---

## Typography Implementation

### Text Utilities
```css
/* Font Size Classes */
.text-xs { font-size: var(--text-xs); }
.text-sm { font-size: var(--text-sm); }
.text-base { font-size: var(--text-base); }
.text-lg { font-size: var(--text-lg); }
.text-xl { font-size: var(--text-xl); }
.text-2xl { font-size: var(--text-2xl); }
.text-3xl { font-size: var(--text-3xl); }
.text-4xl { font-size: var(--text-4xl); }

/* Font Weight Classes */
.font-light { font-weight: var(--font-light); }
.font-normal { font-weight: var(--font-normal); }
.font-medium { font-weight: var(--font-medium); }
.font-semibold { font-weight: var(--font-semibold); }
.font-bold { font-weight: var(--font-bold); }

/* Line Height Classes */
.leading-tight { line-height: var(--leading-tight); }
.leading-normal { line-height: var(--leading-normal); }
.leading-relaxed { line-height: var(--leading-relaxed); }
```

### Heading Patterns
```html
<h1 class="display-4 fw-bold">Main Heading</h1>
<h2 class="display-5 fw-semibold">Section Heading</h2>
<h3 class="display-6 fw-medium">Subsection Heading</h3>
<h4 class="h4 fw-semibold">Card Title</h4>
<h5 class="h5 fw-medium">Small Title</h5>
<h6 class="h6 fw-normal">Micro Title</h6>
```

---

## Form Patterns

### Form Layout
```html
<form class="needs-validation" novalidate>
    <div class="row g-3">
        <div class="col-md-6">
            <label for="firstName" class="form-label">First Name</label>
            <input type="text" class="form-control" id="firstName" required>
            <div class="invalid-feedback">
                Please provide a valid first name.
            </div>
        </div>
        <div class="col-md-6">
            <label for="lastName" class="form-label">Last Name</label>
            <input type="text" class="form-control" id="lastName" required>
            <div class="invalid-feedback">
                Please provide a valid last name.
            </div>
        </div>
        <div class="col-12">
            <label for="email" class="form-label">Email</label>
            <input type="email" class="form-control" id="email" required>
            <div class="invalid-feedback">
                Please provide a valid email address.
            </div>
        </div>
        <div class="col-12">
            <button type="submit" class="btn btn-primary">
                <i class="fas fa-check me-2"></i>Submit
            </button>
        </div>
    </div>
</form>
```

### Search Form
```html
<div class="input-group">
    <input type="search" class="form-control" placeholder="Search events...">
    <button class="btn btn-outline-primary" type="button">
        <i class="fas fa-search"></i>
    </button>
</div>
```

### File Upload
```html
<div class="mb-3">
    <label for="formFile" class="form-label">Upload Event Image</label>
    <input class="form-control" type="file" id="formFile" accept="image/*">
    <div class="form-text">Supported formats: JPG, PNG, GIF (Max 5MB)</div>
</div>
```

---

## Navigation Patterns

### Primary Navigation
```html
<nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm sticky-top">
    <div class="container">
        <a class="navbar-brand" href="#">
            <img src="logo.png" alt="SibloreEvents" height="40" width="40">
            <span class="brand-text">SibloreEvents</span>
        </a>
        
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav me-auto">
                <li class="nav-item">
                    <a class="nav-link active" href="#">
                        <i class="fas fa-home me-1"></i>Home
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">
                        <i class="fas fa-calendar-alt me-1"></i>Events
                    </a>
                </li>
            </ul>
            
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link" href="#">
                        <i class="fas fa-sign-in-alt me-1"></i>Login
                    </a>
                </li>
                <li class="nav-item">
                    <a class="btn btn-primary btn-sm ms-2" href="#">
                        <i class="fas fa-user-plus me-1"></i>Sign Up
                    </a>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

### Breadcrumb Navigation
```html
<nav aria-label="breadcrumb">
    <ol class="breadcrumb">
        <li class="breadcrumb-item">
            <a href="#"><i class="fas fa-home me-1"></i>Home</a>
        </li>
        <li class="breadcrumb-item">
            <a href="#">Events</a>
        </li>
        <li class="breadcrumb-item active" aria-current="page">Event Details</li>
    </ol>
</nav>
```

### Pagination
```html
<nav aria-label="Page navigation">
    <ul class="pagination justify-content-center">
        <li class="page-item disabled">
            <a class="page-link" href="#" tabindex="-1">Previous</a>
        </li>
        <li class="page-item active">
            <a class="page-link" href="#">1</a>
        </li>
        <li class="page-item">
            <a class="page-link" href="#">2</a>
        </li>
        <li class="page-item">
            <a class="page-link" href="#">3</a>
        </li>
        <li class="page-item">
            <a class="page-link" href="#">Next</a>
        </li>
    </ul>
</nav>
```

---

## Implementation Checklist

### Before Starting Development
- [ ] Review brand guidelines and color palette
- [ ] Set up CSS custom properties
- [ ] Configure Font Awesome
- [ ] Prepare image assets and optimize
- [ ] Set up responsive breakpoints

### During Development
- [ ] Use semantic HTML5 elements
- [ ] Follow BEM naming conventions for CSS
- [ ] Implement proper ARIA labels
- [ ] Test keyboard navigation
- [ ] Validate HTML and CSS

### Before Launch
- [ ] Cross-browser testing
- [ ] Mobile responsiveness testing
- [ ] Accessibility audit
- [ ] Performance optimization
- [ ] Brand consistency review

---

## Quick Reference

### Common Classes
```css
/* Layout */
.container, .container-fluid
.row, .col-*
.g-4 (gap 4)

/* Typography */
.display-4, .display-5, .display-6
.lead
.fw-bold, .fw-semibold, .fw-medium

/* Colors */
.text-primary, .text-success
.bg-primary, .bg-light
.btn-primary, .btn-secondary

/* Components */
.card, .card-header, .card-body
.alert, .alert-success
.badge, .bg-success

/* Utilities */
.mt-4, .mb-3, .p-3
.d-flex, .justify-content-between
.rounded, .shadow-sm
```

### Brand Colors Quick Reference
- **Primary Blue:** #2c3e50 (text-primary)
- **Accent Green:** #27ae60 (success, btn-primary)
- **Light Gray:** #f8f9fa (bg-light)
- **Border Gray:** #e9ecef (border-light)
- **Text Gray:** #7f8c8d (text-secondary)

---

*This document serves as a practical implementation guide for the SibloreEvents brand. Always refer to the main BRANDING.md document for comprehensive brand guidelines.*
