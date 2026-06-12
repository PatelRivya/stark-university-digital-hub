from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Count, Avg
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import transaction
import json
from datetime import timedelta

from .models import (
    Department, Course, Faculty, Student, Enrollment, Event, EventRegistration,
    Notice, Facility, Feedback
)
from .forms import (
    StudentRegistrationForm, StudentProfileForm, EnrollmentForm,
    EventRegistrationForm, FeedbackForm, ContactForm, SearchForm,
    CourseFilterForm, DepartmentSearchForm, FacultyFilterForm,
    EventFilterForm, UserProfileForm, NoticeFilterForm
)


# ============ HOME & DASHBOARD VIEWS ============

def home(request):
    """Home page with featured content"""
    context = {
        'featured_events': Event.objects.filter(is_featured=True, start_date__gte=timezone.now())[:3],
        'featured_notices': Notice.objects.filter(is_featured=True).exclude(expiry_date__lt=timezone.now())[:5],
        'departments_count': Department.objects.filter(is_active=True).count(),
        'courses_count': Course.objects.filter(is_active=True).count(),
        'faculty_count': Faculty.objects.filter(is_active=True).count(),
        'events_upcoming': Event.objects.filter(start_date__gte=timezone.now()).count(),
        'upcoming_events': Event.objects.filter(start_date__gte=timezone.now()).order_by('start_date')[:6],
    }
    return render(request, 'index.html', context)


def dashboard(request):
    """User dashboard"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        student = Student.objects.get(user=request.user)
        context = {
            'student': student,
            'enrollments': student.enrollments.all()[:5],
            'registered_events': EventRegistration.objects.filter(student=student)[:5],
            'enrolled_courses_count': student.enrollments.filter(status='ACTIVE').count(),
            'completed_courses': student.enrollments.filter(status='COMPLETED').count(),
        }
    except Student.DoesNotExist:
        context = {'error': 'Student profile not found'}
    
    return render(request, 'dashboard.html', context)


# ============ AUTHENTICATION VIEWS ============

def generate_student_roll_number(user_id):
    """Generate a unique roll number tied to the saved user id."""
    return f"STU{user_id:06d}{timezone.now().strftime('%y%m%d')}"


def register_student(request):
    """Student registration"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                Student.objects.create(
                    user=user,
                    roll_number=generate_student_roll_number(user.id),
                    date_of_birth=form.cleaned_data.get('date_of_birth'),
                    gender=form.cleaned_data.get('gender') or None,
                    phone=form.cleaned_data.get('phone', ''),
                    address=form.cleaned_data.get('address', ''),
                    city=form.cleaned_data.get('city', ''),
                    country=form.cleaned_data.get('country', ''),
                )
            messages.success(request, 'Registration successful! Your student account has been created.')
            user = authenticate(username=form.cleaned_data['username'],
                              password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form})


@login_required
def complete_profile(request):
    """Complete student profile"""
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found')
        return redirect('home')
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
    else:
        form = StudentProfileForm(instance=student)
    
    return render(request, 'auth/complete_profile.html', {'form': form})


@login_required
def update_profile(request):
    """Update user profile"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'auth/update_profile.html', {'form': form})


# ============ DEPARTMENT VIEWS ============

class DepartmentListView(ListView):
    """List all departments"""
    model = Department
    template_name = 'departments/department_list.html'
    context_object_name = 'departments'
    paginate_by = 12

    def get_queryset(self):
        queryset = Department.objects.filter(is_active=True)
        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(code__icontains=query) |
                Q(description__icontains=query)
            )
        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['form'] = DepartmentSearchForm()
        return context


class DepartmentDetailView(DetailView):
    """Department detail page"""
    model = Department
    template_name = 'departments/department_detail.html'
    context_object_name = 'department'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department = self.get_object()
        context['courses'] = department.courses.filter(is_active=True)
        context['faculty'] = department.faculty_members.filter(is_active=True)
        context['faculty_count'] = context['faculty'].count()
        return context


def department_search(request):
    """Search departments"""
    query = request.GET.get('query', '')
    if query:
        departments = Department.objects.filter(
            Q(name__icontains=query) |
            Q(code__icontains=query) |
            Q(description__icontains=query),
            is_active=True
        )
    else:
        departments = Department.objects.filter(is_active=True)
    
    paginator = Paginator(departments, 12)
    page = request.GET.get('page')
    departments = paginator.get_page(page)
    
    context = {
        'departments': departments,
        'query': query,
        'form': DepartmentSearchForm()
    }
    return render(request, 'departments/department_list.html', context)


# ============ COURSE VIEWS ============

class CourseListView(ListView):
    """List all courses"""
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 12

    def get_queryset(self):
        queryset = Course.objects.filter(is_active=True).select_related('department')
        
        # Filter by department
        dept_id = self.request.GET.get('department')
        if dept_id:
            queryset = queryset.filter(department_id=dept_id)
        
        # Filter by level
        level = self.request.GET.get('level')
        if level:
            queryset = queryset.filter(level=level)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset.order_by('department', 'level', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CourseFilterForm()
        context['search_query'] = self.request.GET.get('search', '')
        return context


class CourseDetailView(DetailView):
    """Course detail page"""
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context['enrolled_students'] = course.enrollments.filter(status='ACTIVE').count()
        context['available_seats'] = course.available_seats
        context['is_enrolled'] = False
        
        if self.request.user.is_authenticated:
            try:
                student = Student.objects.get(user=self.request.user)
                context['is_enrolled'] = course.enrollments.filter(student=student).exists()
            except Student.DoesNotExist:
                pass
        
        return context


@login_required
def enroll_course(request, slug):
    """Enroll in a course"""
    course = get_object_or_404(Course, slug=slug)
    
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, 'Please complete your student profile first')
        return redirect('complete-profile')
    
    # Check if already enrolled
    if Enrollment.objects.filter(student=student, course=course).exists():
        messages.warning(request, 'You are already enrolled in this course')
        return redirect('course-detail', slug=slug)
    
    # Check available seats
    if course.enrolled_students >= course.max_students:
        messages.error(request, 'No seats available in this course')
        return redirect('course-detail', slug=slug)
    
    # Create enrollment
    Enrollment.objects.create(student=student, course=course)
    messages.success(request, f'Successfully enrolled in {course.name}')
    return redirect('course-detail', slug=slug)


@login_required
def unenroll_course(request, enrollment_id):
    """Unenroll from a course"""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    
    try:
        student = Student.objects.get(user=request.user)
        if enrollment.student != student:
            messages.error(request, 'Unauthorized action')
            return redirect('dashboard')
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found')
        return redirect('home')
    
    course_name = enrollment.course.name
    enrollment.delete()
    messages.success(request, f'Unenrolled from {course_name}')
    return redirect('dashboard')


# ============ FACULTY VIEWS ============

class FacultyListView(ListView):
    """List all faculty members"""
    model = Faculty
    template_name = 'faculty/faculty_list.html'
    context_object_name = 'faculty_members'
    paginate_by = 12

    def get_queryset(self):
        queryset = Faculty.objects.filter(is_active=True)
        
        # Filter by department
        dept_id = self.request.GET.get('department')
        if dept_id:
            queryset = queryset.filter(department_id=dept_id)
        
        # Filter by designation
        designation = self.request.GET.get('designation')
        if designation:
            queryset = queryset.filter(designation=designation)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(specialization__icontains=search)
            )
        
        return queryset.order_by('department', 'designation', 'last_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FacultyFilterForm()
        context['search_query'] = self.request.GET.get('search', '')
        return context


class FacultyDetailView(DetailView):
    """Faculty member detail page"""
    model = Faculty
    template_name = 'faculty/faculty_detail.html'
    context_object_name = 'faculty'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faculty = self.get_object()
        # Add additional context if needed
        return context


# ============ EVENT VIEWS ============

class EventListView(ListView):
    """List all events"""
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 12

    def get_queryset(self):
        queryset = Event.objects.all()
        
        # Filter by event type
        event_type = self.request.GET.get('event_type')
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status == 'upcoming':
            queryset = queryset.filter(start_date__gte=timezone.now())
        elif status == 'ongoing':
            now = timezone.now()
            queryset = queryset.filter(start_date__lte=now, end_date__gte=now)
        elif status == 'past':
            queryset = queryset.filter(end_date__lt=timezone.now())
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(location__icontains=search)
            )
        
        return queryset.order_by('-start_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EventFilterForm()
        context['search_query'] = self.request.GET.get('search', '')
        return context


class EventDetailView(DetailView):
    """Event detail page"""
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        context['is_registered'] = False
        context['registration_form'] = EventRegistrationForm()
        
        if self.request.user.is_authenticated:
            try:
                student = Student.objects.get(user=self.request.user)
                context['is_registered'] = EventRegistration.objects.filter(
                    event=event, student=student
                ).exists()
            except Student.DoesNotExist:
                pass
        
        context['remaining_capacity'] = event.capacity - event.registrations_count if event.capacity else None
        return context


@login_required
def register_event(request, slug):
    """Register for an event"""
    event = get_object_or_404(Event, slug=slug)
    
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, 'Please complete your student profile first')
        return redirect('complete-profile')
    
    # Check if registration deadline passed
    if event.registration_deadline and event.registration_deadline < timezone.now():
        messages.error(request, 'Registration deadline has passed')
        return redirect('event-detail', slug=slug)
    
    # Check if already registered
    if EventRegistration.objects.filter(event=event, student=student).exists():
        messages.warning(request, 'You are already registered for this event')
        return redirect('event-detail', slug=slug)
    
    # Check capacity
    if event.capacity and event.registrations_count >= event.capacity:
        messages.error(request, 'Event is full. No more registrations available')
        return redirect('event-detail', slug=slug)
    
    # Create registration
    EventRegistration.objects.create(event=event, student=student)
    messages.success(request, f'Successfully registered for {event.title}')
    return redirect('event-detail', slug=slug)


@login_required
def cancel_event_registration(request, registration_id):
    """Cancel event registration"""
    registration = get_object_or_404(EventRegistration, id=registration_id)
    
    try:
        student = Student.objects.get(user=request.user)
        if registration.student != student:
            messages.error(request, 'Unauthorized action')
            return redirect('dashboard')
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found')
        return redirect('home')
    
    event_title = registration.event.title
    registration.delete()
    messages.success(request, f'Cancelled registration for {event_title}')
    return redirect('dashboard')


# ============ NOTICE VIEWS ============

class NoticeListView(ListView):
    """List all notices"""
    model = Notice
    template_name = 'notices/notice_list.html'
    context_object_name = 'notices'
    paginate_by = 15

    def get_queryset(self):
        queryset = Notice.objects.exclude(
            expiry_date__lt=timezone.now()
        ).filter(is_active=True) if hasattr(Notice, 'is_active') else Notice.objects.exclude(
            expiry_date__lt=timezone.now()
        )
        
        # Filter by type
        notice_type = self.request.GET.get('notice_type')
        if notice_type:
            queryset = queryset.filter(notice_type=notice_type)
        
        # Filter by department
        dept_id = self.request.GET.get('department')
        if dept_id:
            queryset = queryset.filter(department_id=dept_id)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search)
            )
        
        return queryset.order_by('-is_featured', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NoticeFilterForm()
        context['search_query'] = self.request.GET.get('search', '')
        return context


class NoticeDetailView(DetailView):
    """Notice detail page"""
    model = Notice
    template_name = 'notices/notice_detail.html'
    context_object_name = 'notice'
    slug_field = 'slug'


# ============ FACILITY VIEWS ============

class FacilityListView(ListView):
    """List all facilities"""
    model = Facility
    template_name = 'facilities/facility_list.html'
    context_object_name = 'facilities'
    paginate_by = 12

    def get_queryset(self):
        queryset = Facility.objects.filter(is_active=True)
        
        # Filter by type
        facility_type = self.request.GET.get('type')
        if facility_type:
            queryset = queryset.filter(facility_type=facility_type)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(location__icontains=search)
            )
        
        return queryset.order_by('facility_type', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['facility_types'] = dict(Facility.FACILITY_TYPE_CHOICES)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class FacilityDetailView(DetailView):
    """Facility detail page"""
    model = Facility
    template_name = 'facilities/facility_detail.html'
    context_object_name = 'facility'


# ============ FEEDBACK VIEWS ============

class FeedbackCreateView(CreateView):
    """Create feedback"""
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback/feedback_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            try:
                form.instance.student = Student.objects.get(user=self.request.user)
            except Student.DoesNotExist:
                pass
        form.instance.email = form.instance.email or self.request.user.email if self.request.user.is_authenticated else ''
        messages.success(self.request, 'Thank you for your feedback!')
        return super().form_valid(form)


def contact_us(request):
    """Contact form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save feedback
            Feedback.objects.create(
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('home')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})


# ============ SEARCH & FILTER VIEWS ============

def global_search(request):
    """Global search across multiple models"""
    query = request.GET.get('q', '')
    results = {
        'departments': [],
        'courses': [],
        'faculty': [],
        'events': [],
        'notices': [],
    }
    
    if query:
        results['departments'] = Department.objects.filter(
            Q(name__icontains=query) | Q(code__icontains=query),
            is_active=True
        )[:5]
        
        results['courses'] = Course.objects.filter(
            Q(name__icontains=query) | Q(code__icontains=query),
            is_active=True
        )[:5]
        
        results['faculty'] = Faculty.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query),
            is_active=True
        )[:5]
        
        results['events'] = Event.objects.filter(
            Q(title__icontains=query) | Q(location__icontains=query)
        )[:5]
        
        results['notices'] = Notice.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )[:5]
    
    return render(request, 'search_results.html', {'results': results, 'query': query})


def advanced_search(request):
    """Advanced search page"""
    context = {}
    
    if request.method == 'GET' and request.GET:
        search_type = request.GET.get('type', 'all')
        query = request.GET.get('query', '')
        
        if search_type == 'departments' or search_type == 'all':
            context['departments'] = Department.objects.filter(
                Q(name__icontains=query) | Q(code__icontains=query),
                is_active=True
            ) if query else Department.objects.filter(is_active=True)
        
        if search_type == 'courses' or search_type == 'all':
            context['courses'] = Course.objects.filter(
                Q(name__icontains=query) | Q(code__icontains=query),
                is_active=True
            ) if query else Course.objects.filter(is_active=True)
        
        if search_type == 'faculty' or search_type == 'all':
            context['faculty'] = Faculty.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query),
                is_active=True
            ) if query else Faculty.objects.filter(is_active=True)
        
        context['query'] = query
        context['search_type'] = search_type
    
    return render(request, 'advanced_search.html', context)


# ============ STATISTICS & ANALYTICS ============

def statistics(request):
    """Display university statistics"""
    context = {
        'total_departments': Department.objects.filter(is_active=True).count(),
        'total_courses': Course.objects.filter(is_active=True).count(),
        'total_faculty': Faculty.objects.filter(is_active=True).count(),
        'total_students': Student.objects.filter(status='ACTIVE').count(),
        'total_events': Event.objects.count(),
        'upcoming_events': Event.objects.filter(start_date__gte=timezone.now()).count(),
        'courses_by_level': dict(Course.objects.values('level').annotate(count=Count('id')).values_list('level', 'count')),
        'top_courses': Course.objects.annotate(enrollment_count=Count('enrollments')).order_by('-enrollment_count')[:5],
    }
    return render(request, 'statistics.html', context)


def about_us(request):
    """About page"""
    return render(request, 'about.html')


def api_dashboard_stats(request):
    """API endpoint for dashboard statistics"""
    if request.user.is_authenticated:
        try:
            student = Student.objects.get(user=request.user)
            stats = {
                'enrolled_courses': student.enrollments.filter(status='ACTIVE').count(),
                'completed_courses': student.enrollments.filter(status='COMPLETED').count(),
                'registered_events': EventRegistration.objects.filter(student=student, status='REGISTERED').count(),
            }
            return JsonResponse(stats)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student profile not found'}, status=404)
    
    return JsonResponse({'error': 'Unauthorized'}, status=401)

