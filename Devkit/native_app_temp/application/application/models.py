from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class Project_record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=40)
    selected_frontend = models.CharField(max_length=20)
    selected_backend = models.CharField(max_length=20)
    selected_database = models.CharField(max_length=20)
    yaml_file = models.CharField(max_length=40, null=True, blank=True)
    def save(self, *args, **kwargs):
        super(Project_record, self).save(*args, **kwargs)

    def __str__(self):
        return self.project_name