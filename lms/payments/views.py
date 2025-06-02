from django.shortcuts import render

from django.views import View

from course.models import Course

from .models import Payments, Transactions 

from students.models import Students

import razorpay

from decouple import config

# Create your views here.


class EnrollConfirmationView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        course = Course.objects.get(uuid=uuid)

        payment,created = Payments.objects.get_or_create(student=Students.objects.get(profile=request.user),course=course,amount= course.offer_fee if course.offer_fee else course.fee)

        data = {'payment':payment}

        return render(request,'payments/enroll-confirmation.html',context=data)
    


class RazorpayView(View):
    
    def get (self, request, *args, **kwargs):

        uuid  = kwargs.get('uuid')

        course = Course.objects.get(uuid=uuid)

        payment = Payments.objects.get(student_profile=request.user, course = course)

        transaction = Transactions.objects.create(payment=payment)

        client = razorpay.Client(auth=(config('RZP_CLIENT_ID'),config('RZP_CLIENT_SECRET')))

        data = { "amount": 500, "currency": "INR", "receipt" : "order_rcptid" }

        order = client.order.create(data=data)

        return render(request,'payments/payments-page.html')