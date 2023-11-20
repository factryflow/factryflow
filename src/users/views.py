from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def login(request):
    if request.htmx:
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        print(email, password, user)
        if user:
            pass
        else:
            message = "Invalid Login"
        return HttpResponse(message)

    return render(request, "login_register.html")
