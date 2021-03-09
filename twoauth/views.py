from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login
from codes.forms import CodeForm
from users.forms import CreateUserForm
from users.models import CustomUser
from .utils import send_sms

@login_required
def home_view(request):
    return render(request,'main.html', {})

def auth_view(request):
    form=AuthenticationForm()
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)  
        if user is not None:
            request.session['pk']=user.pk
            return redirect('verify-view')

    return render(request,'auth.html', {'form': form})

def verify_view(request):
    form=CodeForm(request.POST or None)
    pk=request.session.get('pk')
    if pk:
        user=CustomUser.objects.get(pk=pk)
        code=user.code  
        code_user=f"{user.username}:{user.code}"
        if not request.POST:
            #send sms
            print(user.phone_number)
            send_sms(code_user,user.phone_number)
            print(code_user)
        if form.is_valid():
            num=form.cleaned_data.get('number')     

            if str(code)==num:
                code.save()
                login(request,user)
                return redirect('home-view')

            else:
                return redirect('login-view')

    return render(request, 'verify.html', {'form': form})  




def register_view(request):
	if request.user.is_authenticated:
		return redirect('login-view')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				#messages.success(request, 'Account was created for ' + user)

				return redirect('login-view')
			

		context = {'form':form}
		return render(request, 'register.html', context)                  