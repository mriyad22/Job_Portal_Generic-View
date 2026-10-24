from django.urls import path
from .views import (
    HomeView, RegisterView, UserLoginView, UserLogoutView, ProfileView, ProfileUpdateView,
    JobListView, JobPostCreateView, JobPostUpdateView, JobPostDeleteView, JobApplyView,
    MyApplicationsView, CandidateListView, PasswordChangeView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register_page'),
    path('login/', UserLoginView.as_view(), name='login_page'),
    path('logout/', UserLogoutView.as_view(), name='logout_page'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile-update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('job-list/', JobListView.as_view(), name='jb_list'),
    path('job-post/', JobPostCreateView.as_view(), name='jb_post'),
    path('job-update/<int:u_id>/', JobPostUpdateView.as_view(), name='jb_update'),
    path('job-delete/<int:d_id>/', JobPostDeleteView.as_view(), name='jb_delete'),
    path('apply/<int:j_id>/', JobApplyView.as_view(), name='apply_job'),
    path('my_applied/', MyApplicationsView.as_view(), name='my_applied'),
    path('candidate/<int:c_id>/', CandidateListView.as_view(), name='candidate'),
    path('passwd-change/', PasswordChangeView.as_view(), name='passwd_change'),
]
