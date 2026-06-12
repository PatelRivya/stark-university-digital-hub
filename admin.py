from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Department, Course, Faculty, Student, Enrollment, Event, 
    EventRegistration, Notice, Facility, Feedback
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'head_of_department', 'contact_email', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code', 'description')
    slug_field = 'slug'
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'slug', 'description')
        }),
        ('Contact Information', {
            'fields': ('head_of_department', 'contact_email', 'contact_phone', 'location')
        }),
        ('Additional Information', {
            'fields': ('established_year', 'website', 'image', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department', 'level', 'enrolled_students', 'available_seats', 'is_active')
    list_filter = ('level', 'is_active', 'department', 'created_at')
    search_fields = ('name', 'code', 'description')
    slug_field = 'slug'
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'slug', 'department', 'level', 'description')
        }),
        ('Course Details', {
            'fields': ('duration_months', 'credits', 'fees', 'max_students')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'department', 'designation', 'is_active')
    list_filter = ('designation', 'department', 'is_active', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'specialization')
    slug_field = 'slug'
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'slug', 'email', 'phone')
        }),
        ('Professional Information', {
            'fields': ('department', 'designation', 'specialization', 'qualification', 'experience_years')
        }),
        ('Office Details', {
            'fields': ('office_location', 'office_hours')
        }),
        ('Additional Information', {
            'fields': ('bio', 'photo', 'website', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'user', 'gender', 'status', 'admission_date')
    list_filter = ('status', 'gender', 'admission_date')
    search_fields = ('roll_number', 'user__first_name', 'user__last_name', 'user__email')
    readonly_fields = ('roll_number', 'admission_date', 'created_at', 'updated_at')
    fieldsets = (
        ('User Account', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': ('roll_number', 'date_of_birth', 'gender', 'photo')
        }),
        ('Contact Information', {
            'fields': ('phone', 'address', 'city', 'country')
        }),
        ('Academic Information', {
            'fields': ('admission_date', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'grade', 'enrollment_date')
    list_filter = ('status', 'enrollment_date', 'course__department')
    search_fields = ('student__roll_number', 'course__code', 'course__name')
    readonly_fields = ('enrollment_date',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'start_date', 'is_featured', 'registrations_count')
    list_filter = ('event_type', 'is_featured', 'start_date', 'created_at')
    search_fields = ('title', 'description', 'location')
    slug_field = 'slug'
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'event_type')
        }),
        ('Event Details', {
            'fields': ('start_date', 'end_date', 'location', 'organizer', 'capacity')
        }),
        ('Registration', {
            'fields': ('registration_deadline',)
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Status', {
            'fields': ('is_featured',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'event', 'status', 'registration_date')
    list_filter = ('status', 'registration_date', 'event')
    search_fields = ('student__roll_number', 'event__title')
    readonly_fields = ('registration_date',)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'notice_type', 'is_featured', 'is_urgent', 'created_at', 'is_expired')
    list_filter = ('notice_type', 'is_featured', 'is_urgent', 'created_at')
    search_fields = ('title', 'content')
    slug_field = 'slug'
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'is_expired')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'content', 'notice_type')
        }),
        ('Additional Information', {
            'fields': ('department', 'posted_by', 'image')
        }),
        ('Flags', {
            'fields': ('is_featured', 'is_urgent')
        }),
        ('Expiry', {
            'fields': ('expiry_date', 'is_expired')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'facility_type', 'location', 'capacity', 'is_active')
    list_filter = ('facility_type', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'location')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'facility_type', 'description')
        }),
        ('Location & Capacity', {
            'fields': ('location', 'capacity')
        }),
        ('Operating Hours', {
            'fields': ('opening_time', 'closing_time')
        }),
        ('Contact & Media', {
            'fields': ('contact_email', 'image')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('subject', 'email', 'rating', 'is_read', 'created_at')
    list_filter = ('rating', 'is_read', 'created_at')
    search_fields = ('subject', 'message', 'email')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f'{queryset.count()} feedbacks marked as read')
    mark_as_read.short_description = 'Mark selected as read'

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, f'{queryset.count()} feedbacks marked as unread')
    mark_as_unread.short_description = 'Mark selected as unread'

    fieldsets = (
        ('Feedback Information', {
            'fields': ('student', 'email', 'subject', 'message')
        }),
        ('Rating & Response', {
            'fields': ('rating', 'response', 'is_read')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

