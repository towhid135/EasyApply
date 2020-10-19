from django.db import models
from django.utils import timezone

from accounts.models import User

JOB_TYPE = (
    ('1', "Full time"),
    ('2', "Part time"),
    ('3', "Internship"),
)


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField()
    location = models.CharField(max_length=150)
    type = models.CharField(choices=JOB_TYPE, max_length=10)
    category = models.CharField(max_length=100)
    last_date = models.DateTimeField()
    company_name = models.CharField(max_length=100)
    company_description = models.CharField(max_length=300)
    website = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)
    salary = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.title

class JobModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField(default='')
    location = models.CharField(max_length=150,default='')
    type = models.CharField(choices=JOB_TYPE, max_length=10,default='')
    category = models.CharField(max_length=100,default='')
    salary = models.IntegerField(default=0, blank=True)
    company_name = models.CharField(max_length=100,default='')
    company_description = models.CharField(max_length=300,default='')
    last_date = models.DateTimeField(default=None)
    created_at = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)

class CvModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)
    email = models.EmailField(max_length=255)
    dob = models.DateField()
    img = models.ImageField(null=True, blank=True)
    signature = models.ImageField(null=True, blank=True)
    obj = models.TextField()
    work = models.TextField()
    s_skill = models.TextField()
    l_skill = models.TextField()
    t_skill = models.TextField()
    awards = models.TextField()
    interest = models.TextField()
    publication = models.TextField()
    objects = models.Manager()


class Education(models.Model):
    #psc
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    institute1 = models.CharField(max_length=255, default=None, blank=True, null=True)
    board1 = models.CharField(max_length=255, default=None, blank=True, null=True)
    attempted1 = models.CharField(max_length=255, default=None, blank=True, null=True)
    gpa1 = models.CharField(max_length=255, default=None, blank=True, null=True)
    #jsc
    institute2 = models.CharField(max_length=255, default=None, blank=True, null=True)
    board2 = models.CharField(max_length=255, default=None, blank=True, null=True)
    attempted2 = models.CharField(max_length=255, default=None, blank=True, null=True)
    gpa2 = models.CharField(max_length=255, default=None, blank=True, null=True)
    #ssc
    institute3 = models.CharField(max_length=255, default=None, blank=True, null=True)
    board3 = models.CharField(max_length=255, default=None, blank=True, null=True)
    attempted3 = models.CharField(max_length=255, default=None, blank=True, null=True)
    gpa3 = models.CharField(max_length=255, default=None, blank=True, null=True)
    #hsc
    institute4 = models.CharField(max_length=255, default=None, blank=True, null=True)
    board4 = models.CharField(max_length=255, default=None, blank=True, null=True)
    attempted4 = models.CharField(max_length=255, default=None, blank=True, null=True)
    gpa4 = models.CharField(max_length=255, default=None, blank=True, null=True)
    #honors
    institute5 = models.CharField(max_length=255, default=None, blank=True, null=True)
    department5 = models.CharField(max_length=255, default=None, blank=True, null=True)
    passing5 = models.CharField(max_length=255, default=None, blank=True, null=True)
    cgpa5 = models.CharField(max_length=255, default=None, blank=True, null=True)
    #masters
    institute6 = models.CharField(max_length=255, default=None, blank=True, null=True)
    department6 = models.CharField(max_length=255, default=None, blank=True, null=True)
    passing6 = models.CharField(max_length=255, default=None, blank=True, null=True)
    cgpa6 = models.CharField(max_length=255, default=None, blank=True, null=True)
    #PHD
    institute7 = models.CharField(max_length=255, default=None, blank=True, null=True)
    department7 = models.CharField(max_length=255, default=None, blank=True, null=True)
    passing7 = models.CharField(max_length=255, default=None, blank=True, null=True)
    cgpa7 = models.CharField(max_length=255, default=None, blank=True, null=True)




class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(JobModel, on_delete=models.CASCADE, related_name='applicants')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['user', 'job']

    def __str__(self):
        return self.user.get_full_name()
