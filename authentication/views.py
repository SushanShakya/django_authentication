from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib import auth
from mysite import settings
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from .tokens import token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.

def home(req):
    return render(req, 'authentication/index.html')

def register(req):
    if req.method == "POST":
        # Extract the submitted Data
        name = req.POST['name']
        email = req.POST['email']
        password = req.POST['password']

        # Sanitize the input
        try:
            # 1. User Exists 
            if User.objects.filter(username=email):
                messages.error(req, "We have recognized this email as existent.")
                raise 'e'
            
            # 2. User Name too long
            if len(name) > 30:
                messages.error(req, "Is this your name or name of the whole town !")
                raise 'e'

            # 3. User Name contains special characters
            if not name.isalnum():
                messages.error(req, "Is this your name or name of the whole town !")
                raise 'e'
        except:
            return redirect('home')

        # Register the User in DB
        user = User.objects.create_user(username=email, password=password)
        user.first_name = name
        user.is_active = False
        user.save()

        # Show Registration Message
        messages.success(req, "You're in !")

        # Send Confirmation Mail ( Code for authenticating email ) 
        current_site = get_current_site(req)
        subject = f"Knock Knock {user.first_name} !!!"
        message = render_to_string('email_confirmation.html', {
            'name': user.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token_generator.create_hash(user)
        })

        email = EmailMessage(
            subject,
            message, 
            settings.EMAIL_HOST_USER,
            [user.username]
        )
        email.fail_silently = False
        email.send()

        # from_email = settings.EMAIL_HOST_USER
        # to_emails = [user.username]
        # send_mail(subject, message, from_email, to_emails, fail_silently=True)

        return redirect('login')


    return render(req, 'authentication/register.html')

def login(req):
    if(req.method == "POST"):
        #Extract user input
        email = req.POST['email']
        password = req.POST['password']

        #Check existence in db
        user = authenticate(username=email, password=password)

        if user is not None:
            # Valid User
            auth.login(req, user)
            return render(req, "authentication/index.html", {"uname" : user.first_name })
        else:
            # Invalid User
            messages.error(req, "I don't fuking know you !")
            return redirect('home')


    return render(req, 'authentication/login.html')

def logout(req):
    auth.logout(req)
    messages.success(req, "See ya again !!")
    return redirect('home')

def activate(req, uidb64, token):
    user = None
    try:
        uidb64 = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uidb64)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and token_generator.check(user, token):
        user.is_active = True
        user.save()
        auth.login(req, user)
        messages.success(req, "Activation Success")
        return redirect('home')
    
    return render(req, 'activation_error.html')
