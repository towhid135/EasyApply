from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from .views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = "jobs"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search', SearchView.as_view(), name='searh'),
    path('employer/dashboard/', include([
        path('', DashboardView.as_view(), name='employer-dashboard'),
        path('all-applicants', ApplicantsListView.as_view(), name='employer-all-applicants'),
        path('applicants/<int:job_id>', ApplicantPerJobView.as_view(), name='employer-dashboard-applicants'),
        path('mark-filled/<int:job_id>', filled, name='job-mark-filled'),
    ])),
    path('apply-job/<int:job_id>', ApplyJobView.as_view(), name='apply-job'),
    path('jobs', JobListView.as_view(), name='jobs'),
    path('jobs/<int:id>', JobDetailsView.as_view(), name='jobs-detail'),

    path('cvinfo', employee.cvinfo, name='cvinfo'),
    path('cv_save', employee.cv_save, name='cv_save'),

    path('eduinfo', employee.eduinfo, name='eduinfo'),
    path('education/save', employee.education_save, name='edu_save'),

    path('employee/cv/view/pdf', PDF.as_view(), name='pdf'),
    #path('employer/jobs/create', JobCreateView.as_view(), name='employer-jobs-create'),
    #path('employer/jobs/create', employer.job_post, name='employer-jobs-create'),
    path('employer/jobs/create', job_post.as_view(), name='employer-jobs-create'),
    #path('employee/cvinfo', cvinfo.as_view(), name='cvinfo'),
    #path('employee/cv/view', view_cv.as_view(), name='employee-view-cv'),
    path('employee/cv/view', employee.view_cv, name='employee-view-cv'),
    path('job/details/update/<int:pk>', EditJobView.as_view(), name='job-details-update'),
    path('job/details/delete/<int:pk>', DeleteJobView.as_view(), name='job-details-delete'),
    #path('job/employee/details/<int:pk>', EmployeeDetailsView.as_view(), name='employee-details'),
    path('job/employee/details/<int:pk>', employer.EmployeeDetailsView, name='employee-details'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
