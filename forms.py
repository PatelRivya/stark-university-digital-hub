from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import (
    Student, Enrollment, Event, EventRegistration, 
    Notice, Feedback, Department, Course, Faculty, Facility
)


class StudentRegistrationForm(UserCreationForm):
    """Form for student registration"""
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    gender = forms.ChoiceField(
        choices=[('', 'Select gender')] + Student.GENDER_CHOICES,
        required=False
    )
    phone = forms.CharField(max_length=20, required=False)
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3})
    )
    city = forms.CharField(max_length=100, required=False)
    country = forms.CharField(max_length=100, required=False)
    
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'username',
            'password1', 'password2', 'date_of_birth', 'gender',
            'phone', 'address', 'city', 'country'
        )

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class StudentProfileForm(forms.ModelForm):
    """Form for student profile"""
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Student
        fields = ('date_of_birth', 'gender', 'phone', 'address', 'city', 'country', 'photo')
        widgets = {
            'gender': forms.RadioSelect(),
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class EnrollmentForm(forms.ModelForm):
    """Form for course enrollment"""
    class Meta:
        model = Enrollment
        fields = ('course',)
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
        }


class EventRegistrationForm(forms.ModelForm):
    """Form for event registration"""
    class Meta:
        model = EventRegistration
        fields = ()


class FeedbackForm(forms.ModelForm):
    """Form for feedback submission"""
    class Meta:
        model = Feedback
        fields = ('subject', 'message', 'rating')
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'rating': forms.RadioSelect(choices=Feedback.RATING_CHOICES),
        }


class ContactForm(forms.Form):
    """Form for general contact/feedback"""
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=200, required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class SearchForm(forms.Form):
    """Form for search functionality"""
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search...'
        })
    )


class CourseFilterForm(forms.Form):
    """Form for filtering courses"""
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(is_active=True),
        required=False,
        empty_label="All Departments"
    )
    level = forms.ChoiceField(
        choices=[('', 'All Levels')] + Course.LEVEL_CHOICES,
        required=False
    )


class DepartmentSearchForm(forms.Form):
    """Form for department search"""
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search departments...'})
    )


class FacultyFilterForm(forms.Form):
    """Form for filtering faculty"""
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(is_active=True),
        required=False,
        empty_label="All Departments"
    )
    designation = forms.ChoiceField(
        choices=[('', 'All Designations')] + Faculty.DESIGNATION_CHOICES,
        required=False
    )


class EventFilterForm(forms.Form):
    """Form for filtering events"""
    EVENT_STATUS_CHOICES = [
        ('', 'All Events'),
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('past', 'Past Events'),
    ]
    
    event_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Event.EVENT_TYPE_CHOICES,
        required=False
    )
    status = forms.ChoiceField(
        choices=EVENT_STATUS_CHOICES,
        required=False
    )


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class NoticeFilterForm(forms.Form):
    """Form for filtering notices"""
    notice_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Notice.NOTICE_TYPE_CHOICES,
        required=False
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(is_active=True),
        required=False,
        empty_label="All Departments"
    )
