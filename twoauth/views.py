from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.urls import reverse
from codes.forms import CodeForm
from users.forms import CreateUserForm
from users.models import CustomUser
from .utils import send_sms,token_generator
from django.views import View 
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

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
            login(request,user)
            return redirect('home-view')

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




# def register_view(request):
# 	if request.user.is_authenticated:
# 		return redirect('login-view')
# 	else:
# 		form = CreateUserForm()
# 		if request.method == 'POST':
# 			form = CreateUserForm(request.POST)
# 			if form.is_valid():
# 				form.is_active=False
#                 form.save()
#                 user = form.cleaned_data.get('username')
# 				#messages.success(request, 'Account was created for ' + user)
#                 emailto=form.cleaned_data.get('email')
#                 email_subject="Activate your Email"
#                 email_body='test body'
#                 email=EmailMessage(
#                     email_subject,
#                     email_body,
#                     'noreply@prateek.com',
#                     [emailto]
#                 )

#                 email.send(fail_silently=False)
#                 return redirect('login-view')
			

# 		context = {'form':form}
# 		return render(request, 'register.html', context)  

def register_view(request):
    if request.user.is_authenticated:
        return redirect('login-view')

    else:
        form=CreateUserForm()
        if request.method=="POST":
            form=CreateUserForm(request.POST)
            if form.is_valid():
                user=form.cleaned_data.get("username")
                emailto=form.cleaned_data.get("email")
                password=form.cleaned_data.get("password1")
                phone_number1=form.cleaned_data.get("phone_number")
                user1=CustomUser.objects.create_user(username=user,email=emailto,phone_number=phone_number1)
                user1.set_password(password)
                user1.is_active=False
                user1.save()
                print(user1)
                print("Ho")

                uidb64=urlsafe_base64_encode(force_bytes(user1.id))
                print("Ho")

                domain=get_current_site(request).domain
                print("Ho")

                link=reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user1)})
                print("Ho")

                activate_url='http://'+domain+link
                print("Ho")
                
                email_subject="Activate your email"
                print("Ho")
                email_body="Hi"+user+'Please use the link to verify your account\n'+activate_url
                print("Ho")
                email=EmailMessage(
                    email_subject,
                    email_body,
                    "noreply@prateek.com",
                    [emailto]
                )
                print("Ho")
                email.send(fail_silently=False)
                print("Ho")
                return redirect('login-view')

        context={'form':form}
        return render(request,'register.html',context)        

def logout_view(request):
    logout(request)         
    return redirect('login-view')  


def forget_view(request):
    return render(request,'forget.html', {})  

class VerificationView(View):
    def get(self,request,uidb64,token):
        try:
            id=force_text(urlsafe_base64_decode(uidb64))
            user=CustomUser.objects.get(pk=id)
            if not token_generator.check_token(user,token):
                return redirect('login-view'+'?message='+'User already activated')
        

            if user.is_active:    
                return redirect('login-view')

            user.is_active=True

            user.save()    
            return redirect('login-view')


        except Exception as e:
            pass

        return redirect('login-view')    

        

