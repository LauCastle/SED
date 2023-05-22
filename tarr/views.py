from django.shortcuts import render, redirect 
from .models import Member
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from tarr.forms import *
from django.contrib.auth.models import User


from sedc import settings




# Create your vi3ews here.
#Inicio de la página
def home(request):
    return render(request, 'home.html')

#registro
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            users = User.onjects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                las_name=form.cleaned_data['last_name']
            )
            users.is_staff = True
            users.is_active = True
            users.is_superuser = True
            users.save()
            messages.success(request, 'Creado satisfactoriamente!')
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    return render(request, 'register.html',{'form':form})

def register_success(request):
    return redirect('/login/')

#pagina cuando se registra
@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def list(request):
    members_list = Member.objects.all()
    paginator = Paginator(members_list, 5)
    page = request.GET.get('page')
    try:
        members = paginator.page(page)
    except PageNotAnInteger:
        members = paginator.page(1)
    except EmptyPage:
        members = paginator.page(paginator.num_pages)
    return render(request, 'list.html', {'members': members})

#usuarios
@login_required
def users(request):
    users_list = User.objects.all()
    paginator = Paginator(users_list, 5)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'users.html', {'users': users})

@login_required
def user_delete(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.warning(request, 'Usiario eliminado !')
    return redirect('/users')

@login_required
def changePassword(request):
    print('changepasword')
    return render(request, 'change_password.html')

@login_required
def update(request, id):
    member = Member.objects.get(id=id)
    member.firstname = request.POST['firstname']
    member.lastname = request.POST['lastname']
    member.mobile_number = request.POST['mobile_number']
    member.description = request.POST['description']
    member.location = request.POST['location']
    member.date = request.POST['date']
    member.save()
    messages.success(request, 'Actualizado satisfactoriamente!')
    return redirect('/list')

@login_required
def delete(request, id):
    member = Member.objects.get(id=id)
    member.delete()
    messages.warning(request, 'Member was deleted successfully!')
    return redirect('/list')

#Eliminar
@login_required
def info(request):
    return render(request, 'info.html')

@login_required
def signout(request):
    logout(request)
    messages.success(request, "saliste exitosamente")
    return redirect('home')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, 'info',{'fname': fname})
        else:
            messages.error(request, "Error")
            return redirect('info')
        
    return render(request, 'login.html')
     
@login_required
def cam(request):
    return render(request, 'cam.html')
