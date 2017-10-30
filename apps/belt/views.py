from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
from datetime import datetime, timedelta, time
from django.db.models import Q


def index(request):
    context = { 'user': User.objects.all() }
    return render(request, 'belt/index.html', context)


def regist(request):
    #postData: user's postinfo
    postData = {
        'name' : request.POST['name'],
        'email' : request.POST['email'],
        'password' : request.POST['password'],
        'password_confirm' : request.POST['password_confirm'],
        'birthday': request.POST['birthday'],
    }
    #to chekc errors and user info and use sessions 
    errors = User.objects.basic_validator(postData)
    if len(errors) ==0:

        request.session['id'] = User.objects.filter(email=postData['email'])[0].id
        request.session['name'] = postData['name']
        return redirect('/appointments')
    else: 
        for errors in errors:
            messages.info(request, errors) 
        return redirect ('/')


def login(request):
    print "inside login"
    postData = {
    'email' : request.POST['email'],
    'password' : request.POST['password']
    
    }
    #error handler checks user input
    errors = User.objects.login(postData)
    print errors
    #if theres no errors
    if len(errors) == 0:
        print "success"
        request.session['id'] = User.objects.filter(email=postData['email'])[0].id
        request.session['name'] = User.objects.filter(email=postData['email'])[0].name
        return redirect('/appointments')
    for errors in errors:
        messages.info(request, errors)
    return redirect('/')

def success(request):
    context = {}
    try:
        request.session['id']
    except KeyError:
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    today = datetime.now().date()
    context = {
        'user': user,
        'later_appt' : Appt.objects.filter(user=user).exclude(date=today).order_by('date'),
        'today_appt': Appt.objects.filter(user=user).filter(date=today).order_by('time'),
        'today_date' : datetime.now().date()
        # 'appt' : Appt.objects.filter(user=user)
        
                

    }
    return render(request, 'belt/appt.html', context)


def logout(request):
    #delte id
    del request.session['id']
    del request.session['name']
    return redirect('/')

def add(request):
#check to see validation 

    tasks = request.POST['tasks']
    time = request.POST['time']        
    date = request.POST['date']

    errors_t = Appt.objects.t_validator(request.POST)
    if len(errors_t):
        #always gonna go to this route, rework logic to see if it's an empty list
        for error in errors_t:
            messages.error(request, error)
        return redirect('/appointments')
    else:
        user = User.objects.get(id = request.session['id'])
    #new_q = Quotes.objects.filter(author=author,quotes=quotes)[0]
        Appt.objects.create(tasks=tasks, date=date, time=time, status="pending", user=user) 
    
    return redirect("/appointments")


def delete(request, id):
    Appt.objects.get(id = id).delete()
    return redirect('/appointments')


def update(request, id):
        # if request.method == 'POST':
    #     if len(request.POST['tasks']) < 1:
    #         errors.error(request, "tasks should not be empty!")
    #     if len(request.POST['time']) < str(datetime.now().time()):
    #         messages.error(request, "please enter your future time")
    #     else: 
    #     #if there;s no error then update info 
    appt = Appt.objects.get(id = id)
    appt.tasks = request.POST['task']
    appt.date = request.POST['date']
    appt.time = request.POST['time']
    appt.save()
    return redirect('/appointments')
    

def edit(request, id):
    context = {
        'appt' : Appt.objects.get(id = id),
        'date' : str(Appt.objects.get(id=id).date),
        'time' : str(Appt.objects.get(id=id).time),
    }
    return render (request, 'belt/edit.html', context)