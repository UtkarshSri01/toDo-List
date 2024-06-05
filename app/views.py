from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as loginUser,logout
from django.contrib.auth.decorators import login_required
from app.forms import TODOForm
from app.models import TODO

@login_required(login_url='LoginPage')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        #for getting user first name from username
        name = User.objects.get(username=user)
        form = TODOForm()
        todoList = TODO.objects.filter(user=user).order_by('priority')
    
        return render(request, 'index.html', context= {'name':name,'form':form, 'todoList':todoList})

def login(request):
    if request.method=='POST':
        u_name = request.POST.get('username')
        passw = request.POST.get('passw')

        auth_user = authenticate(request,username=u_name,password=passw)
        
        # print(auth_user)
        
        if auth_user is not None:
            loginUser(request,auth_user)
            return redirect('HomePage')
            
        else:
            return redirect('LoginPage')
    
    return render(request, "login.html")

def signUp(request):
    
    if request.method == 'POST':
        name = request.POST.get('name')
        u_name = request.POST.get('username')
        email = request.POST.get('email')
        passw = request.POST.get('passw')
        
        namelst = name.split(' ')
        fname = ''
        lname = ''
        if len(namelst)>1:
            fname = namelst[0]
            lname = namelst[1]
        else:
            fname = namelst[0]
        
        my_user = User.objects.create_user(username=u_name,email=email,password=passw)
        my_user.first_name = fname
        my_user.last_name = lname
        my_user.save()
        return redirect('LoginPage')
    
    
    return render(request, "signup.html")



def signout(request):
    logout(request)
    
    return redirect('LoginPage')

@login_required(login_url='LoginPage')
def add_todo(request):
    
    if request.user.is_authenticated:
        user = request.user
    
        form = TODOForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            todo = form.save(commit=False)
            todo.user = user
            todo.save()

            return redirect('HomePage')
        else:
            return render(request, 'index.html', context={'form': form})
    
    

def del_todo(request, id):
    TODO.objects.get(pk = id).delete()
    return redirect('HomePage')
    
    
def status_todo(request, id, status):
    todo = TODO.objects.get(pk=id)
    todo.status = status
    todo.save()
    return redirect('HomePage')