from django.db import models

from course.models import BaseClass

# Create your models here.

class Instructors(BaseClass):

    name = models.CharField(max_length=50)

    image = models.ImageField(upload_to='instructor-images/')

    description = models.TextField()

    def __str__(self):

        return self.name
    

    class Meta :

        verbose_name = 'Instructors'

        verbose_name_plural = 'Instructors'


