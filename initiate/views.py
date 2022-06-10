from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def createticker(request):
    return render(request, 'createticker.html') 

def active(request):
    return render(request, 'active.html') 

def pending(request):
    return render(request, 'pending.html')   

def history(request):
    return render(request, 'history.html') 

def preview(request):
    return render(request, 'preview.html') 

def schedule(request):
    return render(request, 'schedule.html')  

def login(request):
    return render(request, 'login.html')    
