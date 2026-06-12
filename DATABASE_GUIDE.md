# SQLite Database Connection Guide - University Website

## ✅ Database is Fully Connected and Working!

Your Django project is fully connected to SQLite database. Here's the complete data flow:

---

## 1. **Registration Flow → SQLite Database**

### Step 1: User Registers on Website
- User fills registration form at: `http://127.0.0.1:8000/register/`
- User enters: Username, Email, Password, First Name, Last Name

### Step 2: Data Saved to SQLite
The registration form calls the `register_student()` function in [main/views.py](main/views.py):

```python
def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # ← SAVES TO DATABASE
            Student.objects.create(  # ← CREATES STUDENT PROFILE
                user=user,
                roll_number=f"STU{user.id}{timezone.now().strftime('%Y%m%d')}"
            )
```

### Step 3: Data Stored in Two Tables

**Table 1: `auth_user` (Django built-in)**
- username
- email
- password (encrypted)
- first_name
- last_name
- is_staff
- is_superuser
- is_active

**Table 2: `main_student` (Your custom model)**
- user_id (links to auth_user)
- roll_number
- date_of_birth
- gender
- phone
- address
- city
- country
- admission_date
- status
- photo

---

## 2. **Login Flow → SQLite Database**

### Step 1: User Attempts Login
- User enters username & password at: `http://127.0.0.1:8000/login/`

### Step 2: Authentication Check
Django queries SQLite database:
```python
user = authenticate(username=username, password=password)
```
- Looks up username in `auth_user` table
- Compares password hash with stored password

### Step 3: Session Created
- If credentials match → user logged in
- Session stored in `django_session` table

---

## 3. **View Your Data in Admin Panel**

### Access Admin Panel:
1. **URL:** `http://127.0.0.1:8000/admin/`
2. **Username:** `superuser`
3. **Password:** `Admin@123`

### View Registered Users:
1. Click **"Users"** → See all registered users
2. Click on a user → View all their details

### View Student Profiles:
1. Go to **"Main"** section
2. Click **"Students"** → See all student records with roll numbers

### View Other Data:
- **Departments** → All university departments
- **Courses** → All courses offered
- **Faculty** → Faculty members
- **Events** → University events
- **Enrollments** → Student course enrollments

---

## 4. **Database File Location**

Your SQLite database file:
```
📁 university_site/
   📄 db.sqlite3 ← ACTUAL DATABASE FILE
```

This file contains ALL your data (users, students, courses, departments, etc.)

---

## 5. **Database Configuration** (Already Done!)

In [university_site/settings.py](university_site/settings.py):

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

✅ Already configured and ready to use!

---

## 6. **Quick Reference: Key Models**

### User Model (Django Built-in)
- Stores login credentials
- Linked to Student via OneToOneField

### Student Model (Your Custom)
```python
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    photo = models.ImageField(upload_to='students/')
    # ... more fields
```

---

## 7. **How to Run Your Website**

```bash
# Navigate to project directory
cd "c:\Users\pc\Desktop\NEW PROJECT\university_site"

# Start development server
python manage.py runserver

# Server will be at: http://127.0.0.1:8000/
```

---

## 8. **Test the Complete Flow**

### Register a New Student:
1. Go to: `http://127.0.0.1:8000/register/`
2. Fill form and submit
3. Check Admin Panel → Users to see new user created!

### Login with New Account:
1. Go to: `http://127.0.0.1:8000/login/`
2. Enter credentials
3. Access dashboard

### View in Database:
1. Admin Panel → Users → See new registration
2. Admin Panel → Students → See student profile

---

## 9. **Current Users in Database**

| Username | Email | Type |
|----------|-------|------|
| admin | admin@university.edu | Staff/Admin |
| superuser | admin@university.com | Superuser/Admin |

---

## 10. **Important Database Tables**

| Table Name | Purpose |
|-----------|---------|
| `auth_user` | User login credentials |
| `django_session` | User sessions |
| `main_student` | Student profiles |
| `main_department` | University departments |
| `main_course` | Courses |
| `main_faculty` | Faculty members |
| `main_enrollment` | Student course enrollments |
| `main_event` | University events |
| `main_notice` | Notices/Announcements |

---

## ✅ Summary

✅ **SQLite database is connected and working!**
✅ **Registration form saves data to database**
✅ **Login authenticates against database**
✅ **Admin panel shows all database records**
✅ **Ready for production-like testing**

**Next Steps:**
1. Register test students via website
2. View them in Admin Panel
3. Test login/logout
4. Explore all data in Admin Dashboard

---

Generated: June 6, 2026
