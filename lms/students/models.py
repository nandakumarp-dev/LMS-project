from django.db import models

# Create your models here.

from course.models import BaseClass

class QualficationChoices(models.TextChoices):

    MATRICULATION = 'Matriculation','Matriculation'
    POST_MATRICULATION = 'Post Matriculation','Post Matriculation'
    DIPLOMA = 'Diploma','Diploma'
    GRADUATE = 'Graduate','Graduate'
    POST_GRADUATE = 'Post Graduate','Post Graduate'
    PHD = 'PHD','PHD'

class Students(BaseClass):

    profile = models.ForeignKey('authentication.Profile',on_delete=models.CASCADE)

    name = models.CharField(max_length=50)

    image = models.ImageField(upload_to='student-images/')

    qualification = models.CharField(max_length=50,choices=QualficationChoices.choices)

    def __str__(self):

        return self.name
    
    class Meta:

        verbose_name = 'Students'

        verbose_name_plural = 'Students'