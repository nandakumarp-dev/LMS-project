from django.shortcuts import render,  redirect

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

    def get(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')
        course = Course.objects.get(uuid=uuid)

        
        payment = Payments.objects.get(student__profile=request.user, course=course)

        transaction = Transactions.objects.create(payment=payment)

        client = razorpay.Client(auth=(config('RZP_CLIENT_ID'), config('RZP_CLIENT_SECRET')))
        data = {"amount": payment.amount*100, "currency": "INR", "receipt": "order_rcptid_11"}
        order = client.order.create(data=data)

        rzp_order_id = order.get('id')

        transaction.rzp_order_id = rzp_order_id

        transaction.save()

        data = {'client_id': config('RZP_CLIENT_ID'),'rzp_order_id': rzp_order_id,'amount':payment.amount*100}

        return render(request, 'payments/payments-page.html',context=data)
    


class PaymentVerifyView(View):

    def post(self,request,*args,**kwargs):

        rzp_order_id = request.POST.GET('razorpay_order_id')

        rzp_payment_id = request.POST.get('razorpay_payment_id')

        rzp_payment_signature = request.POST.get('razorpay_signature')


        client = razorpay.Client(auth=(config('RZP_CLIENT_ID'), config('RZP_CLIENT_SECRET')))

        try:

            client.utility.verify_payment_signature({
                                                        'razorpay_order_id': rzp_order_id,
                                                        'razorpay_payment_id': rzp_payment_id,
                                                        'razorpay_signature': rzp_payment_signature
            })

        except:

            pass

        return redirect('home')






        
        

        
        

        return redirect('home')