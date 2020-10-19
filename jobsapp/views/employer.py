from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView,UpdateView,DeleteView
from jobsapp import urls

from jobsapp.decorators import user_is_employer
from jobsapp.forms import CreateJobForm,JobForm, JobUpdateForm
from jobsapp.models import Job, Applicant , JobModel,CvModel,Education
from jobsapp import models

from django.shortcuts import render
from django.views import View



class DashboardView(ListView):
    #model = Job
    model = JobModel
    template_name = 'jobs/employer/dashboard.html'
    context_object_name = 'jobs'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id)


class ApplicantPerJobView(ListView):
    model = Applicant
    template_name = 'jobs/employer/applicants.html'
    context_object_name = 'applicants'
    paginate_by = 1

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return Applicant.objects.filter(job_id=self.kwargs['job_id']).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = JobModel.objects.get(id=self.kwargs['job_id'])
        return context


class JobCreateView(CreateView):
    template_name = 'jobs/create.html'
    form_class = CreateJobForm
    success_url = reverse_lazy('jobs:employer-dashboard')
    extra_context = {
        'title': 'Post New Job'
    }

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('accounts:login')
        if self.request.user.is_authenticated and self.request.user.role != 'employer':
            return reverse_lazy('accounts:login')
        return super().dispatch(self.request, *args, **kwargs)

    '''def form_valid(self, form):
        form.instance.user = self.request.user
        #return super(JobCreateView, self).form_valid(form)
        job = form.save(commit=False)
        job.save()
        return HttpResponseRedirect(reverse_lazy('jobs:employer-dashboard'))'''

    def post(self, request, *args, **kwargs):
        self.object = None
        #form = self.get_form(self.form_class)
        #form = self.form_class
        form = CreateJobForm(request.POST or None)
        if form.is_valid():
            form.instance.user = self.request.user
            instance = form.save()
            instance.save()
            #job = form.save(commit=False)
            #form.save()
            return HttpResponseRedirect(reverse_lazy('jobs:employer-dashboard'))
            #return redirect('accounts:login')
            #return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ApplicantsListView(ListView):
    model = Applicant
    template_name = 'jobs/employer/all-applicants.html'
    context_object_name = 'applicants'

    def get_queryset(self):
        # jobs = Job.objects.filter(user_id=self.request.user.id)
        return self.model.objects.filter(job__user_id=self.request.user.id)

'''class EmployeeDetailsView(ListView):
    model = CvModel
    template_name = 'jobs/viewcv.html'
    context_object_name = 'cv'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)
    def get_queryset(self):
        # jobs = Job.objects.filter(user_id=self.request.user.id)
        return self.model.objects.filter(user_id= self.kwargs['pk'])'''
def EmployeeDetailsView(request,pk):
    cv = CvModel.objects.filter(user_id= pk)
    edu = Education.objects.filter(user_id= pk)
    return render(request,"jobs/viewcv.html",{"cv": cv,"edu":edu})


@login_required(login_url=reverse_lazy('accounts:login'))
def filled(request, job_id=None):
    try:
        job = JobModel.objects.get(user_id=request.user.id, id=job_id)
        job.filled = True
        job.save()
    except IntegrityError as e:
        print(e.message)
        return HttpResponseRedirect(reverse_lazy('jobs:employer-dashboard'))
    return HttpResponseRedirect(reverse_lazy('jobs:employer-dashboard'))


class job_post(View):
    form_class = JobForm
    template_name = 'jobs/job_create.html'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def get(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        context = {'form': form, }
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            form.instance.user = self.request.user
            instance = form.save()
            instance.save()
            return HttpResponseRedirect(reverse_lazy('jobs:employer-dashboard'))

        return render(request, self.template_name, {'form': form})

'''class EditJobView(View):
    model = JobModel
    form_class = JobUpdateForm
    #context_object_name = 'form'
    template_name = 'jobs/employer/edit-profile.html'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def get(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        context = {'form': form, }
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            form.instance.user = self.request.user
            instance = form.save()
            instance.save()
            return HttpResponseRedirect(reverse_lazy('jobs:employer-dashboard'))

        return render(request, self.template_name, {'form': form})'''


class EditJobView(UpdateView):
    model = JobModel
    template_name = 'jobs/employer/edit-profile.html'
    #fields = ['title','description','location','type','category','salary','company_name','company_description']
    #fields = '__all__'
    fields = ['title', 'description','company_description','location','salary','last_date']
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('jobs:employer-dashboard')


class DeleteJobView(DeleteView):
    model = JobModel
    template_name = 'jobs/employer/delete_job.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('jobs:employer-dashboard')


'''class EditJobView(UpdateView):
    model = JobModel
    form_class = JobUpdateForm
    #context_object_name = 'form'
    template_name = 'jobs/employer/edit-profile.html'
    success_url = reverse_lazy('jobs:employer-dashboard')
    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("User doesn't exists")
        #form = JobModel.objects.get(id=self.kwargs['self.request.id'])
        #print (form)
        return render(request, self.template_name, {'form': form})
        #context = self.get_context_data(object=self.object)
        #return self.render_to_response(self.get_context_data())


    def get_object(self, queryset=None):
        obj = self.request.user

        print('entered to get_object')
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj'''

'''@login_required
def job_post(request):
    #print (request.user.id)
    template_name = 'jobs/job_create.html'
    form = JobForm(request.POST or None)
    if form.is_valid():
        form.instance.user = request.user
        instance = form.save()
        instance.save()
        return HttpResponseRedirect(reverse_lazy('jobs:employer-dashboard'))
    context = {
        'form': form,

    }
    return render(request,template_name, {'form': form})
'''