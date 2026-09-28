from django.db import models
class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    course = models.CharField(max_length=50, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
