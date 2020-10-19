from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.views.generic import CreateView, ListView
from accounts.forms import EmployeeProfileUpdateForm
from accounts.models import User
from jobsapp.decorators import user_is_employee
from jobsapp.models import CvModel,Education
from jobsapp.forms import CvForm,EducationForm
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from jobsapp.utils import *
from django.template.loader import get_template


class EditProfileView(UpdateView):
    model = User
    form_class = EmployeeProfileUpdateForm
    context_object_name = 'employee'
    template_name = 'jobs/employee/edit-profile.html'
    success_url = reverse_lazy('accounts:employer-profile-update')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("User doesn't exists")
        # context = self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user
        print(obj)
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj


@login_required
def cvinfo(request):
    return render(request,"info.html")


@login_required
def cv_save(request):
    #print (request.user.id)
    template_name = 'info.html'
    form = CvForm(request.POST,request.FILES)
    if form.is_valid():
        form.instance.user = request.user
        instance = form.save()
        instance.save()
        return render(request, "education.html")
    context = {'form': form,}
    return render(request,template_name, {'form': form})


'''class view_cv(ListView):
    model = CvModel
    model1 = Education
    template_name = 'jobs/viewcv.html'
    context_object_name = 'cv'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id)'''

def view_cv(request):
    cv = CvModel.objects.filter(user_id=request.user.id)
    edu = Education.objects.filter(user_id=request.user.id)
    return render(request,"jobs/viewcv.html",{"cv": cv,"edu":edu})



class PDF(View):
    model = CvModel
    def get(self, request, *args, **kwargs):
        template = get_template('jobs/viewcv.html')
        context_object_name = self.model.objects.filter(user_id=self.request.user.id)

        pdf = render_to_pdf('jobs/viewcv.html', {'cv':context_object_name})
        return HttpResponse(pdf, content_type='application/pdf')

@login_required
def eduinfo(request):
    return render(request,"education.html")
@login_required
def education_save(request):
    #print (request.user.id)
    template_name = 'education.html'
    form = EducationForm(request.POST)
    print ('yes')
    if form.is_valid():
        print ('inside condition')
        form.instance.user = request.user
        instance = form.save()
        instance.save()
        return HttpResponseRedirect(reverse_lazy('jobs:home'))
    #context = {'form': form,}
    return render(request,template_name, {'form': form})
