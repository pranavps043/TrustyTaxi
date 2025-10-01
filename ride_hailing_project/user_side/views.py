from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Ride, Feedback
from .forms import SignupForm, LoginForm, RideForm, FeedbackForm
from django.http import HttpResponse
from django.template.loader import render_to_string
import pdfkit  # Or use xhtml2pdf/WeasyPrint as preferred



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'user'
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignupForm()
    return render(request, 'user_side/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'user_side/login.html', {'error': 'Invalid credentials'})
    return render(request, 'user_side/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('user_login')

@login_required
def dashboard(request):
    return render(request, 'user_side/dashboard.html')

@login_required
def book_ride(request):
    if request.method == 'POST':
        form = RideForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.user = request.user
            ride.status = 'pending'
            ride.save()
            return redirect('booking_history')
    else:
        form = RideForm()
    return render(request, 'user_side/ride_booking.html', {'form': form})

@login_required
def booking_history(request):
    rides = Ride.objects.filter(user=request.user).order_by('-booking_time')
    return render(request, 'user_side/booking_history.html', {'rides': rides})

@login_required
def booking_detail(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id, user=request.user)
    return render(request, 'user_side/booking_detail.html', {'ride': ride})

@login_required
def feedback_form(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id, user=request.user)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.ride = ride
            feedback.save()
            return redirect('booking_history')
    else:
        form = FeedbackForm()
    return render(request, 'user_side/feedback_form.html', {'form': form, 'ride': ride})

@login_required
def receipt_pdf(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id, user=request.user)
    html = render_to_string('user_side/receipt_pdf.html', {'ride': ride})
    # Using pdfkit as an example to convert HTML to PDF
    pdf = pdfkit.from_string(html, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ride_receipt_{ride.id}.pdf"'
    return response

