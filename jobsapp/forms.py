from django import forms

from jobsapp.models import Job, Applicant , JobModel,CvModel,Education


class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('user', 'created_at',)
        '''labels = {
            "last_date": "Last Date",
            "company_name": "Company Name",
            "company_description": "Company Description"
        }'''

class ApplyJobForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ('job',)

class JobForm(forms.ModelForm):
    class Meta:
        model = JobModel
        exclude = ('user','created_at',)
        fields = (
            'title',
            'description',
            'location',
            'type',
            'category',
            'salary',
            'company_name',
            'company_description',
            'last_date',
            'filled',
        )
        widgets = {
            'title': forms.Textarea(),
            'description': forms.Textarea(),
            'location' : forms.Textarea(),
            'type': forms.Textarea(),
            'category': forms.Textarea(),
            'salary': forms.Textarea(),
            'company_name': forms.Textarea(),
            'company_description': forms.Textarea(),
            'last_date': forms.DateInput(),
        }

class JobUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(JobUpdateForm, self).__init__(*args, **kwargs)

        class Meta:
            model = JobModel
            exclude = ('user', 'created_at', 'filled',)
            # fields = ["title", "description", "location", "type", "category", "salary", "company_name", "company_description", "last_date"]
            fields = ["title", "description"]



class CvForm(forms.ModelForm):
    class Meta:
        model = CvModel
        exclude = ('user',)

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ('user',)