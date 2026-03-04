# SibloreEvents - Event Ticketing & Merchandise Platform

A comprehensive Django-based platform for selling event tickets, merchandise, and products with role-based access control for buyers, event sellers, and product sellers with affiliate marketing capabilities.

## Features

### User Management
- **Custom User Model** with role-based access (Buyer/Event Seller/Product Seller)
- **User Profiles** with bio, profile pictures, and contact information
- **Authentication System** with registration, login, and logout
- **Dashboard Redirection** based on user type
- **Terms and Conditions** with modal popups for signup and job applications
- **Profile Management** with business name support for sellers

### Event Management
- **Event Creation** for sellers with comprehensive details
- **Event Browsing** with search and category filtering
- **Event Details** with pricing, venue, and availability information
- **Early Bird Pricing** and featured events support
- **VIP Ticket Support** with separate pricing and capacity
- **Ticket Availability Tracking** with sold-out status
- **Auto-Publishing** of events upon creation
- **My Events Page** for sellers to manage all their events
- **Date/Time Pickers** using Flatpickr for event scheduling

### Merchandise System
- **Merchandise Creation** for sellers
- **Product Variants** support (sizes, colors, etc.)
- **Inventory Management** with stock tracking
- **Category-based Browsing** with search functionality

### Product Selling & Affiliate Marketing
- **Product Creation** with comprehensive details (pricing, inventory, shipping)
- **Product Categories** for organized browsing
- **Digital & Physical Products** support
- **Inventory Tracking** with low stock alerts
- **SEO Optimization** with meta titles and descriptions
- **Affiliate Marketing System** with unique tracking codes
- **Commission Management** (5%, 10%, 15%, 20%, 25% rates)
- **Click & Conversion Tracking** for affiliate links
- **Affiliate Dashboard** with performance analytics
- **Product Seller Dashboard** with sales and affiliate metrics
- **Auto-Publishing** of products upon creation

### Ticket Purchasing
- **Ticket Purchase** with quantity selection
- **Payment Simulation** (ready for M-Pesa integration)
- **Ticket History** for buyers
- **Order Tracking** and management
- **Regular & VIP Ticket Options**

### Job Careers System
- **Job Vacancy Creation** for employers
- **Job Browsing** with search and filtering
- **Job Application System** with file uploads
- **Application Success** tracking
- **Terms and Conditions** for job applications

### Seller Dashboards
- **Event Seller Dashboard** with revenue tracking and event statistics
- **Product Seller Dashboard** with product and affiliate metrics
- **Recent Sales** overview
- **Quick Actions** for creating events, products, and merchandise
- **Performance Analytics** for both event and product sellers

### Design & UX
- **Responsive Design** with Bootstrap 5
- **Mobile-Friendly** navigation
- **Clean, Minimalist** interface
- **Interactive Components** with smooth animations
- **Brand Consistency** with signature green color scheme
- **Favicon Integration** using site logo
- **Footer Quick Links** including affiliate marketing

## Technology Stack

- **Backend:** Django 5.0
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Database:** SQLite (development)
- **Forms:** Django Crispy Forms with Bootstrap 5
- **Image Handling:** Pillow
- **Authentication:** Django's built-in auth system
- **Date/Time:** Flatpickr JavaScript library
- **Icons:** Font Awesome 6.4

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd siblore-events
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## User Roles

### Buyers
- Browse events, merchandise, and products
- Purchase tickets and merchandise
- View purchase history
- Leave reviews and feedback
- Manage profile

### Event Sellers
- Create and manage events
- Add and manage merchandise
- Track revenue and sales
- View customer analytics
- Manage inventory
- Access event seller dashboard

### Product Sellers
- Create and manage products
- Enable affiliate marketing
- Track affiliate performance
- Manage commissions and earnings
- Access product seller dashboard
- Create affiliate links with unique codes

## User Flows

1. **Registration → Dashboard** based on account type
2. **Browse Events → Purchase Tickets** 
3. **Browse Merchandise → Place Orders**
4. **Browse Products → Purchase/Affiliate Marketing**
5. **Seller Dashboard → Create/Manage Content**
6. **Profile Management** for all users
7. **Job Applications → Career Opportunities**

## Key Pages

- **Home:** Landing page with platform overview
- **Events:** Browse and filter events
- **Merchandise:** Shop event merchandise
- **Products:** Browse products with affiliate marketing
- **My Tickets:** View purchased tickets
- **My Events:** Seller event management
- **My Products:** Product seller product management
- **Affiliate Dashboard:** Affiliate marketing analytics
- **Dashboards:** Role-based user dashboards
- **Profile:** User profile management
- **Careers:** Job listings and applications

## Configuration

### Environment Variables
The system uses Django's built-in settings. For production, consider:

- `DEBUG=False`
- `ALLOWED_HOSTS` configuration
- Database configuration (PostgreSQL recommended)
- Static files configuration
- Email configuration

### Payment Integration
The system is ready for M-Pesa integration. Current implementation includes:
- Payment simulation for testing
- Ticket status tracking
- Order management
- Ready infrastructure for payment gateway

## Database Models

### Core Models
- **User:** Custom user model with role-based access
- **Event:** Event information with pricing and capacity
- **MerchandiseItem:** Product information with inventory
- **Product:** Product information with affiliate marketing
- **ProductCategory:** Product categorization
- **ProductImage:** Product image gallery
- **AffiliateLink:** Affiliate marketing tracking
- **Ticket:** Ticket purchases with payment status
- **JobVacancy:** Job posting management
- **Review:** User reviews for events and merchandise

## Deployment

For production deployment:

1. **Set up production database** (PostgreSQL recommended)
2. **Configure static files** (AWS S3 or similar)
3. **Set up environment variables**
4. **Configure domain and SSL**
5. **Set up monitoring and logging**

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team

## Future Enhancements

- **M-Pesa Payment Integration**
- **Mobile App Development**
- **Advanced Analytics Dashboard**
- **Email Notifications System**
- **Social Media Integration**
- **Advanced Search and Filtering**
- **Multi-language Support**
- **API Development for Mobile Apps**
- **Advanced Affiliate Marketing Features**
- **Product Recommendation System**

---

**SibloreEvents** - Your premier platform for events, merchandise, and affiliate marketing!
