from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile
from django.core.mail import send_mail
import random
import string

v_code = '123'

# Create your views here.

def register(request):
    #creating an empty form for user registration
    form = UserCreationForm()

    # after submit button in the HTML page
    if request.method == "POST":
        # filling out the form with the inserted data from HTML page
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # if valid then save to database
            form.save()
            # after a successful registration you can redirect to any page
            return redirect('home')

    context={
        'form' : form
    }

    return render(request, 'UserManagement/register.html', context)



@login_required
def create_profile(request):
    form = ProfileForm()

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)

        if form.is_valid:
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('products_list')

    context = {
        'form' : form
    }
    return render(request, 'UserManagement/create_profile.html', context)



@login_required
def show_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = "Please complete your profile to view"

    context ={
        'profile' : profile
    }
    
    return render(request, 'UserManagement/show_profile.html', context)


def id_generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@login_required
def send_email(request):
    recipient_list = []
    subject = ''
    message = ''
    status = Profile.objects.get(user=request.user).status
    user_message = '' + status

    if request.method == 'POST':

        recipient_list.append( request.POST['recipient'] )
        subject = request.POST['subject']

        code = id_generator()
        v_code = code
        request.session['v_code'] = code

        message += request.POST['body']
        message += '\n Activation code: ' + code


        status = send_mail(
            subject = subject,
            message = message,
            from_email = 'contact.formulabd71@gmail.com',
            recipient_list = recipient_list,
            fail_silently = True
        )

        if status == 1:

            user_message = 'Email sent successfully. Please enter the verification code.'
            context = {
                'message': user_message
            }

            return redirect('verification')
        else:
            user_message = 'Failed! Try again please!'

    context = {
        'message' : user_message
    }
    return render(request, 'UserManagement/send_email.html', context)



@login_required
def verify_email(request):
    message = ''

    if request.method == "POST":
        code = request.POST['code']
        print(code, request.session['v_code'])
        message = 'Not matched!'

        if request.session['v_code'] == code:
            message = "Successful! Your account if activated now!"
            profile = Profile.objects.get(user = request.user)
            profile.status = "True"
            profile.save()
            context = {
                'message': message
            }
            return render(request, 'UserManagement/success.html', context)

    context = {
        'message': message
    }
    return render(request, 'UserManagement/email_verification_code.html', context)


from .forms import DateForm
def time_date(request):
    form = DateForm()
    context = {
        'form' : form
    }

    return render(request, 'UserManagement/time_date.html', context)