# University Management System - Django Project

A comprehensive, fully dynamic university management system built with Django that provides complete functionality for managing departments, courses, faculty, students, events, and campus facilities.

## Features

### 🎓 Academic Management
- **Departments**: Organize and display all university departments
- **Courses**: Manage course offerings with enrollment tracking
- **Faculty Management**: Display faculty members with detailed profiles
- **Student Enrollments**: Track student course enrollments with status management
- **Enrollment Tracking**: View enrollment statistics and course availability

### 👥 User Management
- **Student Registration**: Complete student registration system
- **User Authentication**: Login/logout functionality
- **Profile Management**: Student profile creation and updates
- **Password Management**: Secure password change functionality

### 📅 Events & Announcements
- **Event Management**: Create and manage university events
- **Event Registration**: Students can register for events with capacity management
- **Notices/Announcements**: Post urgent and featured announcements
- **Facility Management**: Showcase campus facilities with opening hours

### 🔍 Search & Discovery
- **Global Search**: Search across all content types
- **Advanced Search**: Detailed filtering by department, type, and status
- **Filter System**: Filter courses, events, faculty by multiple criteria
- **Pagination**: Efficient content browsing with pagination

### 📊 Analytics & Dashboard
- **Student Dashboard**: Personalized dashboard with enrolled courses and events
- **Statistics Page**: University-wide statistics and analytics
- **Admin Interface**: Comprehensive Django admin with custom configurations

### 💬 Feedback System
- **Contact Forms**: General contact and feedback submission
- **User Feedback**: Rate and review university services
- **Feedback Management**: Admin tools for managing feedback

## Technology Stack

- **Backend**: Django 6.0.2
- **Database**: SQLite3 (development), can use PostgreSQL for production
- **Frontend**: Bootstrap 5.3.0
- **Icons**: Bootstrap Icons
- **ORM**: Django ORM with migrations

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager
- Virtual environment (recommended)

### Step-by-Step Installation

1. **Navigate to project directory**:
   ```bash
   cd c:\Users\pc\Desktop\NEW PROJECT\university_site
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install django pillow
   ```

4. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (admin)**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   - Main site: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

## Project Structure

```
university_site/
├── manage.py
├── main/
│   ├── models.py         # Database models
│   ├── views.py          # View logic
│   ├── forms.py          # Form definitions
│   ├── admin.py          # Admin configurations
│   ├── urls.py           # URL routing
│   ├── apps.py
│   ├── tests.py
│   └── migrations/
├── university_site/
│   ├── settings.py       # Project settings
│   ├── urls.py           # Main URL config
│   ├── wsgi.py
│   └── asgi.py
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── dashboard.html
│   ├── contact.html
│   ├── auth/
│   ├── departments/
│   ├── courses/
│   ├── faculty/
│   ├── events/
│   ├── notices/
│   └── facilities/
└── static/
    ├── css/
    └── images/
```

## Database Models

### Core Models
- **Department**: University departments
- **Course**: Academic courses with enrollment limits
- **Faculty**: Faculty members with designations
- **Student**: Student profiles with enrollment tracking
- **Enrollment**: Course enrollment records

### Events & Campus Life
- **Event**: University events and seminars
- **EventRegistration**: Event attendance tracking
- **Notice**: Announcements and notices
- **Facility**: Campus facilities and resources

### User Interactions
- **Feedback**: Student feedback and ratings

## Key Views & Features

### Home Page
- Featured events and notices
- University statistics
- Quick access to departments, courses, faculty, facilities
- Upcoming events listing

### Departments
- Browse all departments
- Filter and search functionality
- Department detail pages with courses and faculty
- Contact information

### Courses
- Browse courses by department and level
- Enroll/unenroll functionality
- Capacity and seat availability tracking
- Course detail pages with enrollment information

### Faculty
- Browse all faculty members
- Filter by department and designation
- Individual faculty profiles with contact information
- Research interests and office hours

### Events
- Browse upcoming, ongoing, and past events
- Event registration system with capacity management
- Event detail pages with registration deadlines
- Event type filtering

### Notices
- Featured and urgent announcements
- Filter by type and department
- Search functionality
- Expiry date management

### Student Dashboard
- View enrolled courses
- Registered events
- Complete profile information
- Quick statistics

## Admin Features

- Full CRUD operations for all models
- Bulk actions (mark notices as read, etc.)
- Custom filters and search
- Readonly fields for audit trails
- Organized fieldsets for data entry
- Statistics and summaries

## Forms Available

- Student Registration Form
- Student Profile Form
- Course Enrollment Form
- Event Registration Form
- Feedback Form
- Contact Form
- Search Forms with filters
- User Profile Update Form
- Password Change Form

## URLs/Routes

### Authentication
- `/register/` - Student registration
- `/login/` - User login
- `/logout/` - User logout
- `/complete-profile/` - Complete student profile
- `/update-profile/` - Update user profile
- `/change-password/` - Change password

### Content
- `/` - Home page
- `/dashboard/` - Student dashboard
- `/about/` - About page
- `/statistics/` - Statistics page
- `/contact/` - Contact form

### Departments
- `/departments/` - List all departments
- `/department/<slug>/` - Department detail

### Courses
- `/courses/` - List all courses
- `/course/<slug>/` - Course detail
- `/course/<slug>/enroll/` - Enroll in course

### Faculty
- `/faculty/` - List all faculty
- `/faculty/<slug>/` - Faculty detail

### Events
- `/events/` - List all events
- `/event/<slug>/` - Event detail
- `/event/<slug>/register/` - Register for event

### Notices
- `/notices/` - List all notices
- `/notice/<slug>/` - Notice detail

### Facilities
- `/facilities/` - List all facilities
- `/facility/<id>/` - Facility detail

### Utilities
- `/search/` - Global search
- `/search/advanced/` - Advanced search
- `/feedback/` - Submit feedback
- `/api/dashboard-stats/` - API endpoint for dashboard stats

## Customization

### Adding New Features
1. Create model in `main/models.py`
2. Create form in `main/forms.py`
3. Create view in `main/views.py`
4. Add URL in `main/urls.py`
5. Register in `main/admin.py`
6. Create templates in `templates/`

### Styling
- Bootstrap 5 classes used throughout
- Custom CSS in `base.html`
- Modify color variables in `:root` selector

## Security Features

- CSRF protection on all forms
- Password validation
- User authentication required for sensitive operations
- Admin authentication
- Email field validation
- Input sanitization through Django forms

## API Endpoints

- `/api/dashboard-stats/` - GET request returns user dashboard statistics in JSON format

## Future Enhancements

- Grade management system
- Course scheduling and timetable
- Online attendance tracking
- Assignment and submission system
- Library management
- Hostel management
- Alumni portal
- Mobile app integration
- Email notifications
- Payment gateway integration
- Video streaming for online classes
- Discussion forums

## Support & Documentation

For detailed information on Django models, views, and administration, refer to:
- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)

## License

This project is open source and available for educational purposes.

## Troubleshooting

### Migration Issues
```bash
python manage.py makemigrations
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### Database Reset (Development Only)
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## Contributing

This is a fully functional system ready for deployment. Contributions and improvements are welcome!

---

**Version**: 1.0  
**Last Updated**: 2024  
**Status**: Fully Dynamic & Functional
