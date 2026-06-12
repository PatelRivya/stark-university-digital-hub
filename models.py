from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta


class Department(models.Model):
    """Model for university departments"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    head_of_department = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200, blank=True)
    established_year = models.IntegerField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='departments/', blank=True, null=True)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Departments'

    def __str__(self):
        return f"{self.name} ({self.code})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Course(models.Model):
    """Model for university courses"""
    LEVEL_CHOICES = [
        ('DIPLOMA', 'Diploma'),
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
        ('CERTIFICATE', 'Certificate'),
    ]
    
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    description = models.TextField()
    duration_months = models.IntegerField(validators=[MinValueValidator(1)])
    credits = models.IntegerField(blank=True, null=True)
    fees = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    max_students = models.IntegerField(default=50, validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['department', 'level', 'name']
        unique_together = ['department', 'code']

    def __str__(self):
        return f"{self.code} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def enrolled_students(self):
        return self.enrollments.filter(status='ACTIVE').count()

    @property
    def available_seats(self):
        return max(0, self.max_students - self.enrolled_students)


class Faculty(models.Model):
    """Model for faculty members"""
    DESIGNATION_CHOICES = [
        ('PROFESSOR', 'Professor'),
        ('ASSOCIATE_PROF', 'Associate Professor'),
        ('ASSISTANT_PROF', 'Assistant Professor'),
        ('LECTURER', 'Lecturer'),
        ('INSTRUCTOR', 'Instructor'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    designation = models.CharField(max_length=20, choices=DESIGNATION_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='faculty_members')
    specialization = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    office_location = models.CharField(max_length=100, blank=True)
    office_hours = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='faculty/', blank=True, null=True)
    qualification = models.CharField(max_length=200, blank=True)
    experience_years = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    website = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['department', 'designation', 'last_name']
        verbose_name_plural = 'Faculty'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name}-{self.last_name}")
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    """Model for students"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('GRADUATED', 'Graduated'),
        ('SUSPENDED', 'Suspended'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    admission_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    photo = models.ImageField(upload_to='students/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-admission_date', 'roll_number']

    def __str__(self):
        return f"{self.roll_number} - {self.user.get_full_name()}"


class Enrollment(models.Model):
    """Model for course enrollments"""
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('DROPPED', 'Dropped'),
        ('FAILED', 'Failed'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    grade = models.CharField(max_length=5, blank=True, null=True)
    
    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-enrollment_date']

    def __str__(self):
        return f"{self.student.user.username} - {self.course.code}"


class Event(models.Model):
    """Model for university events"""
    EVENT_TYPE_CHOICES = [
        ('SEMINAR', 'Seminar'),
        ('WORKSHOP', 'Workshop'),
        ('CONFERENCE', 'Conference'),
        ('SPORTS', 'Sports'),
        ('CULTURAL', 'Cultural'),
        ('ACADEMIC', 'Academic'),
        ('OTHER', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    organizer = models.CharField(max_length=150, blank=True)
    capacity = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1)])
    registration_deadline = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = 'Events'

    def __str__(self):
        return f"{self.title} ({self.start_date.strftime('%Y-%m-%d')})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def is_upcoming(self):
        return self.start_date > timezone.now()

    @property
    def is_ongoing(self):
        return self.start_date <= timezone.now() <= self.end_date

    @property
    def is_past(self):
        return self.end_date < timezone.now()

    @property
    def registrations_count(self):
        return self.eventregistration_set.filter(status='REGISTERED').count()


class EventRegistration(models.Model):
    """Model for event registrations"""
    STATUS_CHOICES = [
        ('REGISTERED', 'Registered'),
        ('CANCELLED', 'Cancelled'),
        ('ATTENDED', 'Attended'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REGISTERED')

    class Meta:
        unique_together = ['event', 'student']
        ordering = ['-registration_date']

    def __str__(self):
        return f"{self.student.roll_number} - {self.event.title}"


class Notice(models.Model):
    """Model for university notices/announcements"""
    NOTICE_TYPE_CHOICES = [
        ('ACADEMIC', 'Academic'),
        ('ADMINISTRATIVE', 'Administrative'),
        ('EMERGENCY', 'Emergency'),
        ('GENERAL', 'General'),
        ('PLACEMENT', 'Placement'),
    ]
    
    title = models.CharField(max_length=250)
    content = models.TextField()
    notice_type = models.CharField(max_length=20, choices=NOTICE_TYPE_CHOICES, default='GENERAL')
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='notices/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_urgent = models.BooleanField(default=False)
    expiry_date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']
        verbose_name_plural = 'Notices'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        if self.expiry_date:
            return self.expiry_date < timezone.now()
        return False


class Facility(models.Model):
    """Model for university facilities"""
    FACILITY_TYPE_CHOICES = [
        ('LIBRARY', 'Library'),
        ('LAB', 'Laboratory'),
        ('SPORTS', 'Sports'),
        ('CAFETERIA', 'Cafeteria'),
        ('HOSTEL', 'Hostel'),
        ('PARKING', 'Parking'),
        ('AUDITORIUM', 'Auditorium'),
        ('OTHER', 'Other'),
    ]
    
    name = models.CharField(max_length=150)
    facility_type = models.CharField(max_length=20, choices=FACILITY_TYPE_CHOICES)
    description = models.TextField()
    location = models.CharField(max_length=200)
    capacity = models.IntegerField(blank=True, null=True)
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)
    contact_email = models.EmailField(blank=True)
    image = models.ImageField(upload_to='facilities/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['facility_type', 'name']
        verbose_name_plural = 'Facilities'

    def __str__(self):
        return self.name


class Feedback(models.Model):
    """Model for user feedback"""
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.email}"
