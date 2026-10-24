from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    USER_TYPE = [
        ('Recruiter', 'Recruiter'),
        ('Seeker', 'Seeker')
    ]

    display_name = models.CharField(max_length=255, null=True)
    user_type = models.CharField(max_length=100, choices=USER_TYPE, default="Seeker",null=True)

    def __str__(self):
        return f'{self.username} - {self.user_type}'
    


class RecruiterProfileModel(models.Model):
    company_name = models.CharField(max_length=255, null=True)
    logo = models.ImageField(upload_to='company_logo', null=True)
    address = models.TextField()
    phone = models.CharField(max_length=15, null=True)
    recruiter = models.OneToOneField(
        UserModel, 
        on_delete=models.CASCADE, 
        related_name='recruiter_profile', 
        null=True
        )
    

class SeekerProfileModel(models.Model):
    image = models.ImageField(upload_to='seekerImage', null=True)
    phone = models.CharField(max_length=15, null=True)
    address = models.TextField()
    seeker = models.OneToOneField(
        UserModel, 
        on_delete=models.CASCADE, 
        related_name='seeker_profile', 
        null=True
        )
    
    def __str__(self):
        return f'{self.seeker.display_name}'



class CategoryModel(models.Model):
    category = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'{self.category}'



class JobPostModel(models.Model):
    SHIFT_CHOICH = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Remote', 'Remote')
    ]

    jb_title = models.CharField(max_length=255, null=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name='add_category', null=True)
    jb_description = models.TextField()
    jb_skills = models.TextField()
    shift = models.CharField(max_length=100, choices=SHIFT_CHOICH, default='Full Time', null=True)
    opening = models.PositiveIntegerField(null=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    salary = models.FloatField(null=True)
    deadline = models.DateField(null=True)
    posted_by = models.ForeignKey(
        RecruiterProfileModel,
        on_delete=models.CASCADE, 
        related_name='Rec_job_post',
        null=True
        )
    
    def __str__(self):
        return f'{self.jb_title} - {self.posted_by.company_name}'
    

class JobApplyModel(models.Model):
    resume = models.FileField(upload_to='se_resume')
    apply_at = models.DateField(auto_now_add=True, null=True)

    jb_applyer = models.ForeignKey(
        SeekerProfileModel,
        on_delete=models.CASCADE,
        related_name='seeker_aply_profile',
        null=True
    )

    applied_by = models.ForeignKey(
        JobPostModel,
        on_delete=models.CASCADE,
        related_name='seeker_applied',
        null=True
    )

    def __str__(self):
        return f'{self.jb_applyer.seeker.display_name}'