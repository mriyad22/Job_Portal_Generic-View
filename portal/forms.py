from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



class RegisterForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = [
            'display_name', 
            'username', 
            'email', 
            'user_type', 
            'password1', 
            'password2' ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})



class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})



class RecProUpdateForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfileModel
        fields = '__all__'
        exclude = ['recruiter']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})




class SeekProUpdateForm(forms.ModelForm):
    class Meta:
        model = SeekerProfileModel
        fields = '__all__'
        exclude = ['seeker']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})



class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPostModel
        fields = '__all__'
        exclude = ['posted_by']

        widgets = {
            'deadline': forms.DateInput(attrs={'type':'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
    


class JobApplyForm(forms.ModelForm):
    class Meta:
        model = JobApplyModel
        fields = ['resume']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})