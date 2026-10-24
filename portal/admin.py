from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register([
    UserModel,
    RecruiterProfileModel,
    SeekerProfileModel,
    JobPostModel,
    JobApplyModel,
    CategoryModel
])