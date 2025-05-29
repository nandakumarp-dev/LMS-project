from django.shortcuts import render

from django.views import View

from course.models import Course

# Create your views here.

class EnrollConfirmationView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        course = Course.objects.get(uuid=uuid)

        data = {'course':course}

        return render(request,'payments/enroll-confirmation.html',context=data)