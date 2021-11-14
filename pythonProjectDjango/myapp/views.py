from django.shortcuts import render, HttpResponse
from datetime import datetime
from myapp.models import Contact
from django.contrib import messages


# Create your views here.

def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def services(request):
    return render(request, 'services.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('textarea')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, data=datetime.today())
        messages.success(request, 'Your msg has been sent!')
        contact.save()

    return render(request, 'contact.html')
