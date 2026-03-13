# SibloreEvents - Visual Design Documentation for Affinity/Canva

## Table of Contents
1. [Design System Overview](#design-system-overview)
2. [Color Palette & Visual Identity](#color-palette--visual-identity)
3. [Typography System](#typography-system)
4. [Component Library](#component-library)
5. [Layout Grids & Spacing](#layout-grids--spacing)
6. [Wireframe Templates](#wireframe-templates)
7. [Page Designs & Mockups](#page-designs--mockups)
8. [Mobile Design Specifications](#mobile-design-specifications)
9. [Iconography & Illustrations](#iconography--illustrations)
10. [Image Guidelines & Assets](#image-guidelines--assets)
11. [Animation & Micro-interactions](#animation--micro-interactions)
12. [Design Templates for Affinity/Canva](#design-templates-for-affinitycanva)

---

## Design System Overview

### Design Philosophy
- **Minimalist:** Clean, uncluttered interfaces with purposeful elements
- **Professional:** Business-appropriate aesthetics with modern appeal
- **Accessible:** High contrast, readable typography, WCAG compliant
- **Responsive:** Mobile-first approach with progressive enhancement
- **Consistent:** Unified design language across all touchpoints

### Design Principles
1. **Clarity First:** Information hierarchy and intuitive navigation
2. **Efficiency:** Fast load times and smooth interactions
3. **Trust Building:** Professional appearance and reliable functionality
4. **User-Centric:** Designed for African market context and needs
5. **Scalable:** System that grows with feature additions

### Visual Hierarchy
```
Level 1: Primary Actions (Buttons, Headings)
Level 2: Secondary Information (Subheadings, Links)
Level 3: Supporting Content (Body Text, Metadata)
Level 4: Background Elements (Borders, Dividers)
```

---

## Color Palette & Visual Identity

### Primary Color System

#### Royal Blue (Primary Brand Color)
```
Hex: #2c3e50
RGB: 44, 62, 80
CMYK: 45, 23, 0, 69
Usage: Navigation, headers, primary text, important CTAs
Psychology: Trust, professionalism, stability
```

#### Accent Green (Secondary Brand Color)
```
Hex: #27ae60
RGB: 39, 174, 96
CMYK: 78, 0, 45, 32
Usage: Success states, CTAs, highlights, interactive elements
Psychology: Growth, success, positivity
```

### Extended Color Palette

#### Blue Variations
```
Royal Blue Dark: #1a252f (Hover states, deep accents)
Royal Blue Light: #34495e (Secondary elements)
Royal Blue Ultra Light: #ecf0f1 (Backgrounds)
```

#### Green Variations
```
Accent Green Dark: #229954 (Pressed buttons, active states)
Accent Green Light: #2ecc71 (Success notifications)
Accent Green Ultra Light: #d5f4e6 (Subtle backgrounds)
```

#### Neutral Grays
```
Text Primary: #2c3e50 (Main text content)
Text Secondary: #7f8c8d (Metadata, less important text)
Background Light: #f8f9fa (Page backgrounds, cards)
Background White: #ffffff (Content areas, forms)
Border Light: #e9ecef (Dividers, form borders)
```

#### Semantic Colors
```
Success: #27ae60 (Same as Accent Green)
Warning: #f39c12 (Warnings, pending states)
Danger: #e74c3c (Errors, destructive actions)
Info: #3498db (Information, help text)
```

### Color Usage Guidelines

#### Primary Actions
- **Buttons:** Accent Green (#27ae60)
- **Links:** Accent Green (#27ae60)
- **Active States:** Accent Green Dark (#229954)
- **Hover States:** Accent Green Light (#2ecc71)

#### Secondary Actions
- **Outline Buttons:** Border Accent Green, transparent background
- **Secondary Buttons:** Background Light (#f8f9fa), Border Light (#e9ecef)
- **Cancel Actions:** Text Secondary (#7f8c8d)

#### Background Usage
- **Main Background:** Background White (#ffffff)
- **Section Backgrounds:** Background Light (#f8f9fa)
- **Card Backgrounds:** Background White (#ffffff)
- **Overlay Backgrounds:** Semi-transparent Royal Blue

---

## Typography System

### Font Family
**Primary Font:** Inter
- **Designer:** Rasmus Andersson
- **Style:** Geometric sans-serif
- **Characteristics:** Clean, modern, excellent screen readability
- **Weights:** 300, 400, 500, 600, 700
- **Usage:** All UI elements, body text, headings

### Typography Scale

#### Display Headings
```
Display 1: 3rem (48px) - Hero titles
Display 2: 2.5rem (40px) - Section titles
Display 3: 2rem (32px) - Page titles
Display 4: 1.5rem (24px) - Subsection titles
```

#### Content Headings
```
H1: 1.875rem (30px) - Main page headings
H2: 1.5rem (24px) - Section headings
H3: 1.25rem (20px) - Subsection headings
H4: 1.125rem (18px) - Card titles
H5: 1rem (16px) - Small headings
H6: 0.875rem (14px) - Micro headings
```

#### Body Text
```
Large Body: 1.125rem (18px) - Lead text, descriptions
Body: 1rem (16px) - Main content, paragraphs
Small Body: 0.875rem (14px) - Secondary text
Caption: 0.75rem (12px) - Labels, metadata
```

#### Font Weights
```
Light: 300 - Large headings, decorative text
Regular: 400 - Body text, paragraphs
Medium: 500 - Buttons, labels, emphasis
Semibold: 600 - Headings, important text
Bold: 700 - Strong emphasis, titles
```

#### Line Heights
```
Tight: 1.25 - Large headings
Normal: 1.5 - Body text, most content
Relaxed: 1.6 - Long-form content, readability
```

### Typography Usage Rules

#### Hierarchy Implementation
1. **Use only one H1 per page** for main title
2. **Maintain sequential order** (H1 → H2 → H3)
3. **Don't skip levels** (H1 → H3 without H2)
4. **Use semantic HTML** for accessibility
5. **Maintain contrast ratios** for readability

#### Text Color Application
```
Headings: Text Primary (#2c3e50)
Body Text: Text Primary (#2c3e50)
Secondary Text: Text Secondary (#7f8c8d)
Links: Accent Green (#27ae60)
Disabled Text: Text Secondary with 50% opacity
```

---

## Component Library

### Button Components

#### Primary Button
```
Design Specifications:
- Background: Accent Green (#27ae60)
- Text: White (#ffffff)
- Border: None
- Border Radius: 6px (0.375rem)
- Padding: 12px 16px (0.75rem 1rem)
- Font Size: 14px (0.875rem)
- Font Weight: 500 (Medium)
- Shadow: None (default)
- Hover: Background Accent Green Dark (#229954)
- Active: Background Accent Green Dark + Shadow
- Disabled: 50% opacity, no hover
```

#### Secondary Button
```
Design Specifications:
- Background: Background Light (#f8f9fa)
- Text: Text Primary (#2c3e50)
- Border: Border Light (#e9ecef)
- Border Radius: 6px (0.375rem)
- Padding: 12px 16px (0.75rem 1rem)
- Font Size: 14px (0.875rem)
- Font Weight: 500 (Medium)
- Hover: Background Border Light (#e9ecef)
- Active: Background Border Light + Shadow
```

#### Outline Button
```
Design Specifications:
- Background: Transparent
- Text: Accent Green (#27ae60)
- Border: Accent Green (#27ae60)
- Border Width: 1px
- Border Radius: 6px (0.375rem)
- Padding: 12px 16px (0.75rem 1rem)
- Font Size: 14px (0.875rem)
- Font Weight: 500 (Medium)
- Hover: Background Accent Green with 10% opacity
- Active: Background Accent Green, Text White
```

#### Button Sizes
```
Small: 8px height, 12px padding (0.5rem 0.75rem)
Default: 32px height, 12px padding (0.75rem 1rem)
Large: 40px height, 16px padding (1rem 1.25rem)
Extra Large: 48px height, 20px padding (1.25rem 1.5rem)
```

### Card Components

#### Base Card
```
Design Specifications:
- Background: Background White (#ffffff)
- Border: 1px solid Border Light (#e9ecef)
- Border Radius: 8px (0.5rem)
- Shadow: None (default)
- Padding: 24px (1.5rem)
- Hover: Shadow Small (0 1px 3px rgba(0,0,0,0.12))
- Hover Transform: Translate Y -1px
```

#### Event Card
```
Design Specifications:
- Image Height: 200px
- Image Aspect Ratio: 16:9
- Card Padding: 16px (1rem)
- Title Font Size: 18px (1.125rem)
- Title Font Weight: 600 (Semibold)
- Title Color: Text Primary (#2c3e50)
- Metadata Font Size: 14px (0.875rem)
- Metadata Color: Text Secondary (#7f8c8d)
- Price Badge: Background Accent Green, Text White
- Hover Effect: Image scale 1.05, Card shadow
```

#### Stats Card
```
Design Specifications:
- Background: Background White (#ffffff)
- Border Left: 4px solid Accent Green (#27ae60)
- Border Radius: 8px (0.5rem)
- Padding: 24px (1.5rem)
- Icon Size: 32px (2rem)
- Icon Color: Accent Green (#27ae60)
- Number Font Size: 32px (2rem)
- Number Color: Accent Green (#27ae60)
- Number Font Weight: 700 (Bold)
- Label Font Size: 14px (0.875rem)
- Label Color: Text Secondary (#7f8c8d)
```

### Form Components

#### Input Field
```
Design Specifications:
- Background: Background White (#ffffff)
- Border: 1px solid Border Light (#e9ecef)
- Border Radius: 6px (0.375rem)
- Padding: 12px 16px (0.75rem 1rem)
- Font Size: 14px (0.875rem)
- Font Weight: 400 (Regular)
- Text Color: Text Primary (#2c3e50)
- Placeholder Color: Text Secondary (#7f8c8d)
- Focus Border: Accent Green (#27ae60)
- Focus Shadow: 0 0 0 0.2rem rgba(39, 174, 96, 0.25)
- Error Border: Danger (#e74c3c)
- Error Text: Danger (#e74c3c)
```

#### Select Dropdown
```
Design Specifications:
- Background: Background White (#ffffff)
- Border: 1px solid Border Light (#e9ecef)
- Border Radius: 6px (0.375rem)
- Padding: 12px 16px (0.75rem 1rem)
- Font Size: 14px (0.875rem)
- Arrow Color: Text Secondary (#7f8c8d)
- Hover Border: Accent Green (#27ae60)
- Focus Border: Accent Green (#27ae60)
```

### Alert Components

#### Success Alert
```
Design Specifications:
- Background: Accent Green with 5% opacity (rgba(39, 174, 96, 0.05))
- Border Left: 4px solid Accent Green (#27ae60)
- Border Radius: 8px (0.5rem)
- Padding: 16px 24px (1rem 1.5rem)
- Text Color: Accent Green (#27ae60)
- Icon Color: Accent Green (#27ae60)
- Icon Size: 16px (1rem)
```

#### Warning Alert
```
Design Specifications:
- Background: Warning with 5% opacity (rgba(243, 156, 18, 0.05))
- Border Left: 4px solid Warning (#f39c12)
- Border Radius: 8px (0.5rem)
- Padding: 16px 24px (1rem 1.5rem)
- Text Color: Warning (#f39c12)
- Icon Color: Warning (#f39c12)
- Icon Size: 16px (1rem)
```

---

## Layout Grids & Spacing

### Grid System

#### Bootstrap 5 Grid (12-column system)
```
Container Max Widths:
- XS (None): 100% (576px and below)
- SM: 540px (576px and up)
- MD: 720px (768px and up)
- LG: 960px (992px and up)
- XL: 1140px (1200px and up)
- XXL: 1320px (1400px and up)
```

#### Custom Grid for Affinity/Canva
```
Column Widths (12-column system):
- 1 column: 8.33%
- 2 columns: 16.67%
- 3 columns: 25%
- 4 columns: 33.33%
- 6 columns: 50%
- 8 columns: 66.67%
- 9 columns: 75%
- 12 columns: 100%
```

### Spacing System

#### Base Spacing Unit: 4px
```
Space 1: 4px (0.25rem)
Space 2: 8px (0.5rem)
Space 3: 12px (0.75rem)
Space 4: 16px (1rem)
Space 5: 20px (1.25rem)
Space 6: 24px (1.5rem)
Space 8: 32px (2rem)
Space 10: 40px (2.5rem)
Space 12: 48px (3rem)
Space 16: 64px (4rem)
Space 20: 80px (5rem)
Space 24: 96px (6rem)
```

#### Component Spacing
```
Button Padding: 12px 16px (Space 3 Space 4)
Card Padding: 24px (Space 6)
Form Field Padding: 12px 16px (Space 3 Space 4)
Section Spacing: 48px (Space 12)
Card Gap: 24px (Space 6)
List Item Spacing: 12px (Space 3)
```

### Layout Patterns

#### Container Layout
```
Max Width: 1200px
Centered: Yes
Padding: 16px (Space 4) on mobile, 24px (Space 6) on desktop
```

#### Section Layout
```
Section Padding: 64px 0 (Space 16 vertical)
Container: Max width 1200px, centered
Background: Alternating between white and light gray
```

#### Card Grid Layout
```
Desktop: 4 columns (25% each)
Tablet: 3 columns (33.33% each)
Mobile: 2 columns (50% each)
Small Mobile: 1 column (100%)
Gap: 24px (Space 6)
```

---

## Wireframe Templates

### Page Structure Template

#### Standard Page Layout
```
┌─────────────────────────────────────────────────────────────┐
│ Navigation (64px height)                                │
├─────────────────────────────────────────────────────────────┤
│                                                     │
│  Header Section (optional)                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Page Title (H1)                               │    │
│  │ Subtitle/Breadcrumb                             │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                     │
│  Main Content Area                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Content Blocks/Components                     │    │
│  │                                           │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                     │
│  Footer                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Footer Content                               │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

#### Dashboard Layout
```
┌─────────────────────────────────────────────────────────────┐
│ Navigation (64px height)                                │
├─────────────────────────────────────────────────────────────┤
│                                                     │
│ ┌─────────┐ ┌─────────────────────────────────────────┐ │
│ │ Sidebar │ │ Main Content Area                  │ │
│ │ (240px) │ │                                 │ │
│ │         │ │ ┌─────────────────────────────────┐ │ │
│ │ Nav     │ │ │ Stats Cards (4 columns)       │ │ │
│ │ Items   │ │ └─────────────────────────────────┘ │ │
│ │         │ │                                 │ │
│ │         │ │ ┌─────────────────────────────────┐ │ │
│ │         │ │ │ Recent Activity Table         │ │ │
│ │         │ │ └─────────────────────────────────┘ │ │
│ └─────────┘ └─────────────────────────────────────────┘ │
│                                                     │
│  Footer                                             │
└─────────────────────────────────────────────────────────────┘
```

### Component Wireframes

#### Event Card Wireframe
```
┌─────────────────────────────────┐
│ Image (16:9 aspect ratio)   │
├─────────────────────────────────┤
│ Event Title                 │
│ (H4, 2 lines max)         │
│                           │
│ Metadata                   │
│ • Date & Time             │
│ • Location               │
│ • Price (badge)          │
│                           │
│ [Button] Book Now         │
└─────────────────────────────────┘
```

#### Form Section Wireframe
```
┌─────────────────────────────────┐
│ Section Title               │
├─────────────────────────────────┤
│                           │
│ Label                     │
│ [Input Field]             │
│                           │
│ Label                     │
│ [Input Field]             │
│                           │
│ Label                     │
│ [Dropdown Select]          │
│                           │
│ [Primary Button]           │
└─────────────────────────────────┘
```

---

## Page Designs & Mockups

### Homepage Design

#### Hero Section
```
┌─────────────────────────────────────────────────────────────┐
│ Background: Gradient Royal Blue to Accent Green          │
│                                                     │
│         ┌─────────────────────────────────────┐         │
│         │ Main Heading (Display 2)           │         │
│         │ "Discover Amazing Events"          │         │
│         │                                   │         │
│         │ Subtitle (Lead)                   │         │
│         │ "Your premier platform..."           │         │
│         │                                   │         │
│         │ [Primary Button] Browse Events       │         │
│         │ [Outline Button] Create Event       │         │
│         └─────────────────────────────────────┘         │
│                                                     │
│         Hero Image/Illustration (right side)            │
└─────────────────────────────────────────────────────────────┘
```

#### Features Section
```
┌─────────────────────────────────────────────────────────────┐
│ Section Title: "Why Choose SibloreEvents?"            │
│                                                     │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ Icon    │ │ Icon    │ │ Icon    │ │ Icon    │ │
│ │ (32px)  │ │ (32px)  │ │ (32px)  │ │ (32px)  │ │
│ │         │ │         │ │         │ │         │ │
│ │ Title   │ │ Title   │ │ Title   │ │ Title   │ │
│ │ (H5)    │ │ (H5)    │ │ (H5)    │ │ (H5)    │ │
│ │         │ │         │ │         │ │         │ │
│ │ Description │ │ Description │ │ Description │ │ Description │ │
│ │ (2-3 lines) │ │ (2-3 lines) │ │ (2-3 lines) │ │ (2-3 lines) │ │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
│                                                     │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ Icon    │ │ Icon    │ │ Icon    │ │ Icon    │ │
│ │ (32px)  │ │ (32px)  │ │ (32px)  │ │ (32px)  │ │
│ │ Title   │ │ Title   │ │ Title   │ │ Title   │ │
│ │ Description │ │ Description │ │ Description │ │ Description │ │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Events Listing Page

#### Filter Bar
```
┌─────────────────────────────────────────────────────────────┐
│ Search Input [Search events...]          [Search Button] │
│                                                     │
│ Category Dropdown    Date Range    Price Range    Clear │
│ [All Categories]   [Select Date]   [Min-Max]    [X]  │
└─────────────────────────────────────────────────────────────┘
```

#### Events Grid
```
┌─────────────────────────────────────────────────────────────┐
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ Event   │ │ Event   │ │ Event   │ │ Event   │ │
│ │ Image   │ │ Image   │ │ Image   │ │ Image   │ │
│ ├─────────┤ ├─────────┤ ├─────────┤ ├─────────┤ │
│ │ Title   │ │ Title   │ │ Title   │ │ Title   │ │
│ │ Date    │ │ Date    │ │ Date    │ │ Date    │ │
│ │ Price   │ │ Price   │ │ Price   │ │ Price   │ │
│ │ [Book]  │ │ [Book]  │ │ [Book]  │ │ [Book]  │ │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
│                                                     │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ Event   │ │ Event   │ │ Event   │ │ Event   │ │
│ │ ...     │ │ ...     │ │ ...     │ │ ...     │ │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
│                                                     │
│                [Load More] Pagination                   │
└─────────────────────────────────────────────────────────────┘
```

### Event Detail Page

#### Header Section
```
┌─────────────────────────────────────────────────────────────┐
│ ┌─────────────────┐ ┌─────────────────────────────────┐ │
│ │                 │ │ Event Title                   │ │
│ │ Event Image     │ │ (H1, Bold)                 │ │
│ │ (16:9)         │ │                             │ │
│ │                 │ │ Event Description             │ │
│ │                 │ │ (2-3 paragraphs)            │ │
│ │                 │ │                             │ │
│ │                 │ │ [Primary Button] Book Now     │ │
│ │                 │ │ [Secondary Button] Share      │ │
│ └─────────────────┘ └─────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### Information Tabs
```
┌─────────────────────────────────────────────────────────────┐
│ [Details] [Venue] [Organizer] [Reviews]           │
├─────────────────────────────────────────────────────────────┤
│                                                     │
│ Selected Tab Content                                  │
│                                                     │
│ • Event Details                                      │
│ • Date & Time Information                             │
│ • Ticket Pricing                                    │
│ • Venue Information                                 │
│ • Organizer Profile                                 │
│ • User Reviews                                    │
│                                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Mobile Design Specifications

### Mobile Breakpoints

#### Breakpoint System
```
Small Mobile: 320px - 374px
Mobile: 375px - 413px
Large Mobile: 414px - 767px
Tablet: 768px - 991px
Desktop: 992px and above
```

#### Mobile Layout Adaptations

#### Navigation
```
Mobile Navigation (Hamburger Menu):
┌─────────────────────────────────┐
│ ☰ SibloreEvents        [👤] │
├─────────────────────────────────┤
│                           │
│ Page Content              │
│                           │
│                           │
│                           │
└─────────────────────────────────┘

Slide-out Menu:
┌─────────┐
│ Menu    │
│ Home    │
│ Events  │
│ Merch   │
│ Careers │
│ Profile │
│ Logout  │
└─────────┘
```

#### Event Card Mobile
```
┌─────────────────────────────────┐
│ Image (16:9)               │
├─────────────────────────────────┤
│ Event Title                 │
│ (2 lines max)              │
│                           │
│ • Date & Time             │
│ • Location               │
│ • Price                 │
│                           │
│ [Primary Button]           │
│ Full Width                │
└─────────────────────────────────┘
```

#### Form Mobile
```
┌─────────────────────────────────┐
│ Page Title               │
├─────────────────────────────────┤
│                           │
│ Label                     │
│ [Input Field]             │
│ Full Width                │
│                           │
│ Label                     │
│ [Input Field]             │
│ Full Width                │
│                           │
│ [Primary Button]           │
│ Full Width                │
└─────────────────────────────────┘
```

### Mobile Touch Targets

#### Minimum Touch Target Sizes
```
Buttons: 44px minimum height, 44px minimum width
Links: 44px minimum touch area
Icons: 44px minimum touch area
Form Fields: 44px minimum height
Toggles: 44px minimum touch area
```

#### Mobile Spacing
```
Button Padding: 16px 24px (Space 4 Space 6)
Card Padding: 16px (Space 4)
Section Spacing: 32px (Space 8)
Form Field Padding: 16px (Space 4)
```

---

## Iconography & Illustrations

### Icon System

#### Font Awesome 6.4 Icons
```
Primary Icons:
• fas fa-home (Home)
• fas fa-calendar-alt (Events)
• fas fa-shopping-bag (Merchandise)
• fas fa-briefcase (Careers)
• fas fa-user (Profile)
• fas fa-ticket-alt (Tickets)

Action Icons:
• fas fa-plus (Add/Create)
• fas fa-edit (Edit)
• fas fa-trash (Delete)
• fas fa-search (Search)
• fas fa-filter (Filter)
• fas fa-download (Download)

Status Icons:
• fas fa-check-circle (Success)
• fas fa-exclamation-triangle (Warning)
• fas fa-times-circle (Error)
• fas fa-info-circle (Info)
• fas fa-clock (Pending)
```

#### Icon Usage Guidelines

#### Size Standards
```
Inline Icons: 12px (0.75rem)
Button Icons: 14px (0.875rem)
Card Icons: 24px (1.5rem)
Feature Icons: 32px (2rem)
Hero Icons: 48px (3rem)
```

#### Color Application
```
Primary Actions: Accent Green (#27ae60)
Secondary Actions: Text Primary (#2c3e50)
Status Icons: Corresponding semantic colors
Navigation Icons: Text Primary (#2c3e50)
Disabled Icons: Text Secondary (#7f8c8d)
```

### Illustration Style

#### Custom Illustrations
```
Style: Flat, minimalist, on-brand
Colors: Royal Blue, Accent Green, neutral grays
Usage: Hero sections, empty states, onboarding
Consistency: Same style across all illustrations
```

#### Empty State Illustrations
```
No Events: Calendar with plus icon
No Tickets: Ticket with question mark
No Merchandise: Shopping bag with empty icon
No Results: Search with magnifying glass
Error State: Warning triangle
```

---

## Image Guidelines & Assets

### Image Specifications

#### Event Images
```
Aspect Ratio: 16:9
Minimum Size: 1200x675px
Recommended Size: 1920x1080px
Format: JPG (photos), PNG (graphics)
Compression: Optimized for web (under 200KB)
Color Space: sRGB
```

#### Profile Pictures
```
Aspect Ratio: 1:1 (square)
Minimum Size: 200x200px
Recommended Size: 400x400px
Format: PNG or JPG
Compression: Optimized for web (under 100KB)
Background: Professional, plain background
```

#### Merchandise Images
```
Aspect Ratio: 1:1 (primary), 4:3 (gallery)
Minimum Size: 800x800px (1:1), 800x600px (4:3)
Recommended Size: 1200x1200px (1:1), 1200x900px (4:3)
Format: PNG with transparency
Multiple Views: Front, back, side, detail
Background: White or transparent
```

### Image Treatment

#### Overlay Effects
```
Hero Images: Gradient overlay (Royal Blue to transparent)
Card Images: Subtle shadow on hover
Gallery Images: Border radius 8px
Profile Images: Circular crop with border
Thumbnail Images: Consistent sizing and cropping
```

#### Image Loading
```
Placeholder: Low-quality image placeholder (LQIP)
Lazy Loading: Load images as user scrolls
Progressive Loading: JPEG progressive encoding
Error Fallback: Default placeholder image
Alt Text: Descriptive for accessibility
```

---

## Animation & Micro-interactions

### Animation Principles

#### Timing Standards
```
Fast Transitions: 0.15s (hover states)
Standard Transitions: 0.3s (most interactions)
Slow Transitions: 0.5s (page transitions)
Loading Animations: 1s+ (continuous)
```

#### Easing Functions
```
Ease Out: Natural, smooth deceleration
Ease In Out: Smooth acceleration and deceleration
Linear: Constant speed (loading animations)
Cubic Bezier: Custom easing for specific effects
```

### Interactive Animations

#### Button Interactions
```
Hover:
• Transform: translateY(-1px)
• Shadow: 0 4px 8px rgba(0,0,0,0.15)
• Background: Darken by 10%
• Duration: 0.3s ease

Active:
• Transform: translateY(0px)
• Shadow: 0 2px 4px rgba(0,0,0,0.1)
• Background: Darken by 15%
• Duration: 0.15s ease
```

#### Card Interactions
```
Hover:
• Transform: translateY(-2px)
• Shadow: 0 8px 16px rgba(0,0,0,0.15)
• Image Scale: 1.05
• Duration: 0.3s ease

Focus:
• Outline: 2px solid Accent Green
• Outline Offset: 2px
• Duration: 0.15s ease
```

#### Loading States
```
Spinner Animation:
• Rotation: 360deg continuous
• Duration: 1s linear infinite
• Size: 16px (small), 24px (medium), 32px (large)
• Color: Accent Green

Skeleton Loading:
• Background: Linear gradient shimmer
• Animation: 1.5s ease infinite
• Color: Light gray to white gradient
• Duration: Until content loads
```

### Page Transitions

#### Fade In Animation
```
Initial State:
• Opacity: 0
• Transform: translateY(20px)

Final State:
• Opacity: 1
• Transform: translateY(0)
• Duration: 0.5s ease
```

#### Slide In Animation
```
Initial State:
• Transform: translateX(-100%)
• Opacity: 0

Final State:
• Transform: translateX(0)
• Opacity: 1
• Duration: 0.3s ease
```

---

## Design Templates for Affinity/Canva

### Template Specifications

#### Document Setup
```
Affinity Designer:
• Document Size: 1920x1080px (Desktop)
• Units: Pixels
• DPI: 72
• Color Mode: RGB
• Transparency: Enabled

Canva:
• Custom Size: 1920x1080px
• Units: Pixels
• Background: White
• Guides: 12-column grid
```

#### Grid System Setup
```
12-Column Grid:
• Total Width: 1200px
• Column Width: 80px
• Gutter Width: 20px
• Margins: 60px (sides), 40px (top/bottom)
• Baseline Grid: 4px increments
```

### Template Library

#### Page Templates
```
1. Homepage Template
   - Hero section with gradient background
   - Features grid (4 columns)
   - Stats section
   - Call-to-action section
   - Footer

2. Dashboard Template
   - Sidebar navigation (240px wide)
   - Main content area
   - Stats cards grid
   - Recent activity table
   - Quick actions bar

3. Events Listing Template
   - Filter bar at top
   - Events grid (4 columns)
   - Pagination at bottom
   - Sort options

4. Event Detail Template
   - Hero image with title
   - Tabbed content area
   - Booking sidebar
   - Related events section

5. Form Template
   - Page title and description
   - Multi-column form layout
   - Progress indicator
   - Submit button
```

#### Component Templates
```
1. Button Component Set
   - Primary button (4 sizes)
   - Secondary button (4 sizes)
   - Outline button (4 sizes)
   - Icon buttons
   - Button groups

2. Card Component Set
   - Base card
   - Event card
   - Stats card
   - Profile card
   - Product card

3. Form Component Set
   - Input fields (text, email, password)
   - Select dropdowns
   - Checkboxes and radio buttons
   - Text areas
   - File upload areas

4. Navigation Component Set
   - Primary navigation
   - Mobile navigation
   - Breadcrumbs
   - Pagination
   - Tab navigation
```

### Color Palette Setup

#### Affinity Designer Swatches
```
Create Swatch Palette:
1. Royal Blue (#2c3e50)
2. Royal Blue Dark (#1a252f)
3. Royal Blue Light (#34495e)
4. Accent Green (#27ae60)
5. Accent Green Dark (#229954)
6. Accent Green Light (#2ecc71)
7. Text Primary (#2c3e50)
8. Text Secondary (#7f8c8d)
9. Background Light (#f8f9fa)
10. Background White (#ffffff)
11. Border Light (#e9ecef)
12. Success (#27ae60)
13. Warning (#f39c12)
14. Danger (#e74c3c)
15. Info (#3498db)
```

#### Canva Color Palette
```
Create Custom Palette:
• Primary Colors: Royal Blue, Accent Green
• Secondary Colors: Blue variations, Green variations
• Neutral Colors: Gray scale
• Semantic Colors: Success, Warning, Danger, Info
• Background Colors: White, Light Gray
```

### Typography Setup

#### Affinity Designer Text Styles
```
Create Text Styles:
1. Display 1 (48px, Bold, Inter)
2. Display 2 (40px, Bold, Inter)
3. Display 3 (32px, Semibold, Inter)
4. Display 4 (24px, Semibold, Inter)
5. H1 (30px, Semibold, Inter)
6. H2 (24px, Semibold, Inter)
7. H3 (20px, Semibold, Inter)
8. H4 (18px, Semibold, Inter)
9. H5 (16px, Medium, Inter)
10. H6 (14px, Medium, Inter)
11. Body Large (18px, Regular, Inter)
12. Body (16px, Regular, Inter)
13. Body Small (14px, Regular, Inter)
14. Caption (12px, Regular, Inter)
```

#### Canva Text Styles
```
Save Text Combinations:
• Headings: Inter, Semibold/Bold
• Body Text: Inter, Regular
• Buttons: Inter, Medium
• Labels: Inter, Medium
• Captions: Inter, Regular
```

### Asset Export Specifications

#### Image Export Settings
```
Format: PNG (for graphics), JPG (for photos)
Quality: High (80-90%)
Compression: Optimized for web
Size: Multiple variants (1x, 2x, 3x)
Naming: Descriptive, consistent convention
```

#### Icon Export Settings
```
Format: SVG (for scalability), PNG (for compatibility)
Size: 16px, 24px, 32px, 48px, 64px
Color: Multiple color variants
Background: Transparent
Naming: Consistent naming convention
```

---

## Design Workflow for Affinity/Canva

### Design Process

#### 1. Setup & Planning
```
• Create new document with template
• Set up grid system and guides
• Load color palette and typography
• Create component library
• Plan page structure and layout
```

#### 2. Wireframing
```
• Create low-fidelity wireframes
• Focus on layout and structure
• Use placeholder content
• Establish information hierarchy
• Review and refine layouts
```

#### 3. Visual Design
```
• Apply brand colors and typography
• Create high-fidelity mockups
• Add imagery and icons
• Implement interactive states
• Ensure consistency across pages
```

#### 4. Review & Refinement
```
• Check against design guidelines
• Test responsive layouts
• Validate accessibility standards
• Review brand consistency
• Get feedback and iterate
```

#### 5. Asset Preparation
```
• Export images and icons
• Organize asset library
• Create component variations
• Prepare developer handoff
• Document design decisions
```

### Quality Checklist

#### Design Quality
```
✓ Consistent color usage
✓ Proper typography hierarchy
✓ Adequate contrast ratios
✓ Appropriate spacing
✓ Responsive design considerations
✓ Interactive state definitions
✓ Component reusability
✓ Brand guideline compliance
```

#### Technical Quality
```
✓ Proper file formats
✓ Optimized image sizes
✓ Scalable vector graphics
✓ Organized layer structure
✓ Clear naming conventions
✓ Export specifications
✓ Developer handoff readiness
```

---

## Conclusion

This comprehensive design documentation provides everything needed to create consistent, professional, and user-friendly designs for the SibloreEvents platform using Affinity Designer or Canva. The systematic approach ensures brand consistency, accessibility compliance, and optimal user experience across all touchpoints.

### Key Design Assets
- **Complete color palette** with hex codes and usage guidelines
- **Typography system** with font sizes, weights, and spacing
- **Component library** with detailed specifications
- **Layout grids** for responsive design
- **Wireframe templates** for rapid prototyping
- **Design system** for consistency and scalability

### Implementation Guidelines
- **Step-by-step design process** for efficient workflow
- **Quality checklists** for professional results
- **Export specifications** for developer handoff
- **Responsive considerations** for multi-device support
- **Accessibility standards** for inclusive design

This documentation serves as the definitive guide for all visual design work on the SibloreEvents platform, ensuring consistency and quality across all design deliverables.

---

*Last Updated: March 13, 2026*
*Version: 1.0*
*Document Owner: SibloreEvents Design Team*
