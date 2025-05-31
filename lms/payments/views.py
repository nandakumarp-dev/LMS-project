from django.shortcuts import render

from django.views import View

from course.models import Course

from .models import Payments

from students.models import Students

# Create your views here.

class EnrollConfirmationView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        course = Course.objects.get(uuid=uuid)

        payment,created = Payments.objects.get_or_create(student=Students.objects.get(profile=request.user),course=course,amount= course.offer_fee if course.offer_fee else course.fee)

        data = {'payment':payment}

        return render(request,'payments/enroll-confirmation.html',context=data)