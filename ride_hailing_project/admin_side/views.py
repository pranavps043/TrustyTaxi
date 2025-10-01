from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from user_side.models import CustomUser
from .models import Driver, Ride
from .forms import DriverForm
from user_side.models import Ride, Driver, CustomUser
from user_side.models import Feedback

# Helper decorator to allow only admins
def admin_required(view_func):
    decorated_view_func = login_required(
        user_passes_test(lambda u: u.is_authenticated and u.role == 'admin')(view_func)
    )
    return decorated_view_func

def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None and user.role == 'admin':
            login(request, user)
            return redirect('admin_dashboard')
        else:
            context = {'error': 'Invalid credentials or not an admin.'}
            return render(request, 'admin_side/admin_login.html', context)
    return render(request, 'admin_side/admin_login.html')

@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@admin_required
def dashboard(request):
    drivers = Driver.objects.all()
    rides = Ride.objects.all()
    context = {
        'total_drivers': drivers.count(),
        'total_rides': rides.count(),
        'pending_rides': rides.filter(status='pending').count(),
        'approved_drivers': drivers.filter(status='approved').count(),
    }
    return render(request, 'admin_side/dashboard.html', context)


@admin_required
def driver_list(request):
    drivers = Driver.objects.all()
    return render(request, 'admin_side/driver_list.html', {'drivers': drivers})

@admin_required
def driver_form(request, pk=None):
    print("\n=== Driver Form View ===")
    print(f"Method: {request.method}")
    
    if pk:
        driver = get_object_or_404(Driver, pk=pk)
        print(f"Editing existing driver: {driver}")
    else:
        driver = None
        print("Creating new driver")

    if request.method == 'POST':
        print("\nForm data received:", request.POST)
        form = DriverForm(request.POST, instance=driver)
        
        if form.is_valid():
            print("Form is valid. Saving driver...")
            try:
                # Create a new driver instance but don't save it yet
                driver = form.save(commit=False)
                
                # If this is a new driver, set the date_joined
                if not driver.pk:
                    from django.utils import timezone
                    driver.date_joined = timezone.now()
                
                # Save the driver to the database
                driver.save()
                
                # Save any many-to-many relationships if they exist
                form.save_m2m()
                
                print(f"Driver saved successfully with ID: {driver.id}")
                return redirect('driver_list')
                
            except Exception as e:
                import traceback
                print("Error during save:", str(e))
                print("Traceback:")
                traceback.print_exc()
                form.add_error(None, f"Error saving driver: {str(e)}")
        else:
            print("Form validation failed. Errors:", form.errors)
            # Print each field's errors for debugging
            for field in form:
                if field.errors:
                    print(f"Field '{field.name}' errors: {field.errors}")
    else:
        form = DriverForm(instance=driver)
        print("Serving fresh form")

    return render(request, 'admin_side/driver_form.html', {'form': form})

@admin_required
def driver_delete(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    if request.method == 'POST':
        driver.delete()
        return redirect('driver_list')
    return render(request, 'admin_side/driver_delete_confirm.html', {'driver': driver})


# Ride management views
@admin_required
def ride_list(request):
    rides = Ride.objects.all()
    return render(request, 'admin_side/ride_list.html', {'rides': rides})

@admin_required
def ride_assign(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)
    drivers = Driver.objects.filter(status='approved')

    if request.method == 'POST':
        driver_id = request.POST.get('driver')
        driver = get_object_or_404(Driver, id=driver_id)
        ride.driver = driver
        ride.status = 'assigned'
        ride.save()
        return redirect('ride_list')

    return render(request, 'admin_side/ride_assign.html', {'ride': ride, 'drivers': drivers})

# Booking management
@admin_required
def booking_list(request):
    rides = Ride.objects.all()
    return render(request, 'admin_side/booking_list.html', {'rides': rides})

@admin_required
def booking_edit(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)
    if request.method == 'POST':
        ride.pickup = request.POST.get('pickup')
        ride.dropoff = request.POST.get('dropoff')
        ride.ride_type = request.POST.get('ride_type')
        ride.status = request.POST.get('status')
        ride.save()
        return redirect('booking_list')
    return render(request, 'admin_side/booking_edit.html', {'ride': ride})


@admin_required
def feedback_list(request):
    feedbacks = Feedback.objects.select_related('ride', 'user').all()
    return render(request, 'admin_side/feedback_list.html', {'feedbacks': feedbacks})