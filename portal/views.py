from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, ListView, UpdateView, DeleteView

from .forms import RegisterForm, LoginForm, RecProUpdateForm, SeekProUpdateForm, JobPostForm, JobApplyForm
from .models import CategoryModel, RecruiterProfileModel, SeekerProfileModel, JobPostModel, JobApplyModel


class FormDataContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = context.get('form')
        return context


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = CategoryModel.objects.all().order_by('category')
        return context


class RegisterView(FormDataContextMixin, FormView):
    template_name = 'auth/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login_page')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your account was created successfully. Please sign in.')
        return super().form_valid(form)


class UserLoginView(FormDataContextMixin, LoginView):
    template_name = 'auth/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, 'You have signed in successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy('home')


class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('login_page')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'


class ProfileUpdateView(FormDataContextMixin, LoginRequiredMixin, FormView):
    template_name = 'profile-update.html'
    success_url = reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        if request.user.user_type == 'Recruiter':
            self.profile_instance = RecruiterProfileModel.objects.filter(recruiter=request.user).first()
        else:
            self.profile_instance = SeekerProfileModel.objects.filter(seeker=request.user).first()
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return RecProUpdateForm if self.request.user.user_type == 'Recruiter' else SeekProUpdateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.profile_instance
        return kwargs

    def form_valid(self, form):
        profile = form.save(commit=False)
        if self.request.user.user_type == 'Recruiter':
            profile.recruiter = self.request.user
        else:
            profile.seeker = self.request.user
        profile.save()
        messages.success(self.request, 'Your profile has been updated.')
        return super().form_valid(form)


class RecruiterRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.user_type == 'Recruiter'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, 'Please sign in as a recruiter to manage job posts.')
        return redirect('jb_list')


class SeekerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.user_type == 'Seeker'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, 'Only job seekers can apply for jobs.')
        return redirect('jb_list')


class JobPostCreateView(FormDataContextMixin, RecruiterRequiredMixin, FormView):
    template_name = 'jobs/jb-post.html'
    form_class = JobPostForm
    success_url = reverse_lazy('jb_list')

    def form_valid(self, form):
        job = form.save(commit=False)
        profile = RecruiterProfileModel.objects.filter(recruiter=self.request.user).first()
        if not profile:
            messages.error(self.request, 'Please complete your recruiter profile before posting a job.')
            return redirect('profile_update')
        job.posted_by = profile
        job.save()
        messages.success(self.request, 'Your job has been published.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'data': context['form'], 'page_title': 'Post a Job', 'submit_label': 'Publish Job'})
        return context


class JobOwnerMixin(RecruiterRequiredMixin):
    def get_queryset(self):
        return JobPostModel.objects.filter(posted_by__recruiter=self.request.user).select_related('posted_by', 'category')


class JobPostUpdateView(FormDataContextMixin, JobOwnerMixin, UpdateView):
    model = JobPostModel
    form_class = JobPostForm
    pk_url_kwarg = 'u_id'
    template_name = 'jobs/jb-post.html'
    success_url = reverse_lazy('jb_list')

    def form_valid(self, form):
        messages.success(self.request, 'The job post has been updated.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'data': context['form'], 'page_title': 'Update Job', 'submit_label': 'Save Changes'})
        return context


class JobPostDeleteView(JobOwnerMixin, DeleteView):
    model = JobPostModel
    pk_url_kwarg = 'd_id'
    template_name = 'delete.html'
    success_url = reverse_lazy('jb_list')
    context_object_name = 'object'

    def form_valid(self, form):
        messages.success(self.request, 'The job post has been deleted.')
        return super().form_valid(form)


class JobListView(ListView):
    model = JobPostModel
    template_name = 'jobs/jb-list.html'
    context_object_name = 'data'
    paginate_by = 9

    def get_queryset(self):
        qs = JobPostModel.objects.select_related('category', 'posted_by', 'posted_by__recruiter').order_by('-created_at', '-id')
        user = self.request.user
        if user.is_authenticated and user.user_type == 'Recruiter':
            profile = RecruiterProfileModel.objects.filter(recruiter=user).first()
            qs = qs.filter(posted_by=profile) if profile else qs.none()
        category_id = self.request.GET.get('cate_id')
        if category_id:
            qs = qs.filter(category_id=category_id)
        keyword = self.request.GET.get('q', '').strip()
        if keyword:
            qs = qs.filter(Q(jb_title__icontains=keyword) | Q(jb_description__icontains=keyword) | Q(jb_skills__icontains=keyword) | Q(posted_by__company_name__icontains=keyword))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['keyword'] = self.request.GET.get('q', '').strip()
        context['selected_category'] = self.request.GET.get('cate_id', '')
        context['categories'] = CategoryModel.objects.all().order_by('category')
        return context


class JobApplyView(FormDataContextMixin, SeekerRequiredMixin, FormView):
    template_name = 'jb-apply.html'
    form_class = JobApplyForm

    def dispatch(self, request, *args, **kwargs):
        self.job = get_object_or_404(JobPostModel, pk=kwargs['j_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        profile = SeekerProfileModel.objects.filter(seeker=self.request.user).first()
        if not profile:
            messages.error(self.request, 'Please complete your seeker profile before applying.')
            return redirect('profile_update')
        application = form.save(commit=False)
        application.jb_applyer = profile
        application.applied_by = self.job
        application.save()
        messages.success(self.request, 'Your application has been submitted.')
        return redirect('my_applied')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'data': context['form'], 'job': self.job})
        return context


class MyApplicationsView(SeekerRequiredMixin, ListView):
    template_name = 'my-applied.html'
    context_object_name = 'data'

    def get_queryset(self):
        profile = SeekerProfileModel.objects.filter(seeker=self.request.user).first()
        if not profile:
            return JobApplyModel.objects.none()
        return JobApplyModel.objects.filter(jb_applyer=profile).select_related(
            'applied_by', 'applied_by__category', 'applied_by__posted_by', 'jb_applyer', 'jb_applyer__seeker'
        ).order_by('-apply_at', '-id')


class CandidateListView(RecruiterRequiredMixin, ListView):
    template_name = 'candidate.html'
    context_object_name = 'data'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_page')
        self.job = get_object_or_404(JobPostModel, pk=kwargs['c_id'], posted_by__recruiter=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return JobApplyModel.objects.filter(applied_by=self.job).select_related(
            'jb_applyer', 'jb_applyer__seeker', 'applied_by'
        ).order_by('-apply_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = self.job
        return context


class PasswordChangeView(FormDataContextMixin, LoginRequiredMixin, FormView):
    template_name = 'auth/password_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, 'Your password has been changed successfully.')
        return super().form_valid(form)
