from django.shortcuts import render

# Create your views here.
def contactus_view(request):
    return render(request, 'contactus/contactus.html')