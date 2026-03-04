from django import forms
from django.core.validators import FileExtensionValidator
from .models import JobApplication


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            'first_name',
            'last_name', 
            'email',
            'phone',
            'cover_letter',
            'resume',
            'linkedin_profile',
            'portfolio',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Tell us why you\'re interested in this position and why you\'d be a great fit...'
            }),
            'resume': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'linkedin_profile': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/yourprofile'
            }),
            'portfolio': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourportfolio.com'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'First Name *'
        self.fields['last_name'].label = 'Last Name *'
        self.fields['email'].label = 'Email Address *'
        self.fields['phone'].label = 'Phone Number *'
        self.fields['cover_letter'].label = 'Cover Letter *'
        self.fields['resume'].label = 'Resume/CV *'
        self.fields['linkedin_profile'].label = 'LinkedIn Profile (Optional)'
        self.fields['portfolio'].label = 'Portfolio URL (Optional)'
        
        # Add help text
        self.fields['resume'].help_text = 'Upload your resume in PDF, DOC, or DOCX format (Max 5MB)'
        self.fields['linkedin_profile'].help_text = 'Optional: Link to your LinkedIn profile'
        self.fields['portfolio'].help_text = 'Optional: Link to your portfolio website'
    
    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            # Check file size (5MB limit)
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Resume file size must be less than 5MB.')
            
            # Check file extension
            allowed_extensions = ['.pdf', '.doc', '.docx']
            file_extension = resume.name.lower().split('.')[-1]
            if f'.{file_extension}' not in allowed_extensions:
                raise forms.ValidationError(
                    'Resume must be in PDF, DOC, or DOCX format.'
                )
        return resume
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove any non-digit characters for validation
            clean_phone = ''.join(filter(str.isdigit, phone))
            if len(clean_phone) < 10:
                raise forms.ValidationError('Please enter a valid phone number.')
        return phone
    
    def clean_linkedin_profile(self):
        linkedin = self.cleaned_data.get('linkedin_profile')
        if linkedin and not linkedin.startswith('https://'):
            linkedin = 'https://' + linkedin
        return linkedin
    
    def clean_portfolio(self):
        portfolio = self.cleaned_data.get('portfolio')
        if portfolio and not portfolio.startswith('https://'):
            portfolio = 'https://' + portfolio
        return portfolio
