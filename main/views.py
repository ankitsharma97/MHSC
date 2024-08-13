from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import  Patient,  Feedback, Polls,Answer
from django.contrib.auth import update_session_auth_hash
# Create your views here.

def home(request):
    return render(request, 'home.html')


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user:
            auth_login(request, user)
            request.session['name'] = Patient.objects.get(user=user).name
            return redirect('patient')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        phone = request.POST['phone']
        age = request.POST['age']
        if password != password1:
            return render(request, 'signup.html', {'error': 'Password does not match'})
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already exists'})
        user = User.objects.create_user(username=email, email=email, password=password)

        Patient.objects.create(user=user, name=name, phone=phone, age=age)
        return redirect('login')
    return render(request, 'signup.html',)


def logout(request):
    auth_logout(request)
    return redirect('home')


def passchange(request):
    user = request.user
    error = None
    if request.method == "POST":
        password = request.POST.get('password')
        npassword = request.POST.get('npassword')
        if not user.check_password(password):
            error = 'Invalid Password'
        elif password == npassword:
            error = 'New Password is the same as the old password'
        else:
            user.set_password(npassword)
            user.save()
            update_session_auth_hash(request, user)  
            return redirect('login')
    return render(request, 'updatePass.html', {
        'user': user,
        'error': error
    })
    


def patient(request):
    return render(request, 'patient_dash.html')


def editprofile(request):
    user = request.user
    patient = Patient.objects.get(user=user)
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        mobile_number = request.POST.get('mobile_number')
        address = request.POST.get('address')
        pin_code = request.POST.get('pin_code')
        patient.name = name
        patient.phone = phone
        patient.age = age
        patient.mobile_number = mobile_number
        patient.address = address
        patient.pin_code = pin_code
        patient.save()
        return redirect('patient')
    return render(request, 'editprofile.html', {'patient': patient})





def feedback(request):
    name = request.session.get('name')
    if request.method == 'POST':
        name = name
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Feedback.objects.create(name=name, email=email, subject=subject, message=message)
        return redirect('viewfeedback')
    return render(request, 'feedback.html', {'name': name})



def polls(request):
    polls = Polls.objects.all()
    poll_data = []

    if request.method == "POST":
        poll_id = request.POST.get('poll_id')
        selected_option = request.POST.get('option')
        poll = get_object_or_404(Polls, pk=poll_id)

        # Assuming you are using the User model from django.contrib.auth
        if request.user.is_authenticated:
            if not Answer.objects.filter(user=request.user, poll=poll).exists():
                Answer.objects.create(
                    user=request.user,
                    poll=poll,
                    answer=selected_option)
            else:
                answer = Answer.objects.get(user=request.user, poll=poll)
                answer.answer = selected_option
                answer.save()
        else:
            # Handle case where user is not authenticated
            pass

    for poll in polls:
        poll_info = {
            'poll': poll,
            'option1_count': 0,
            'option2_count': 0,
            'option3_count': 0,
            'option4_count': 0,
            'option1_percentage': 0,
            'option2_percentage': 0,
            'option3_percentage': 0,
            'option4_percentage': 0,
        }
        total_answers = Answer.objects.filter(poll=poll).count()

        if total_answers > 0:
            poll_info['option1_count'] = Answer.objects.filter(poll=poll, answer='option1').count()
            poll_info['option2_count'] = Answer.objects.filter(poll=poll, answer='option2').count()
            poll_info['option3_count'] = Answer.objects.filter(poll=poll, answer='option3').count()
            poll_info['option4_count'] = Answer.objects.filter(poll=poll, answer='option4').count()

            poll_info['option1_percentage'] = (poll_info['option1_count'] / total_answers) * 100
            poll_info['option2_percentage'] = (poll_info['option2_count'] / total_answers) * 100
            poll_info['option3_percentage'] = (poll_info['option3_count'] / total_answers) * 100
            poll_info['option4_percentage'] = (poll_info['option4_count'] / total_answers) * 100

        poll_data.append(poll_info)

    return render(request, 'poll.html', {'poll_data': poll_data})




def viewfeedback(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'viewfeedback.html', {'feedbacks': feedbacks})



def about(request):
    return render(request, 'about.html') 


def new(request):
    return render(request, 'new.html')