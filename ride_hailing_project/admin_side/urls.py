from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.dashboard, name='admin_dashboard'),

    # Driver URLs
    path('drivers/', views.driver_list, name='driver_list'),
    path('drivers/add/', views.driver_form, name='driver_add'),
    path('drivers/edit/<int:pk>/', views.driver_form, name='driver_edit'),
    path('drivers/delete/<int:pk>/', views.driver_delete, name='driver_delete'),

    # Ride URLs
    path('rides/', views.ride_list, name='ride_list'),
    path('rides/assign/<int:ride_id>/', views.ride_assign, name='ride_assign'),

    # Booking URLs
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/edit/<int:ride_id>/', views.booking_edit, name='booking_edit'),
      path('feedbacks/', views.feedback_list, name='feedback_list'),
]
