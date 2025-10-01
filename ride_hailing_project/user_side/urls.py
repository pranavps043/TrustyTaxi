from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('', views.dashboard, name='dashboard'),
    path('book/', views.book_ride, name='book_ride'),
    path('mybookings/', views.booking_history, name='booking_history'),
    path('booking/<int:ride_id>/', views.booking_detail, name='booking_detail'),
    path('feedback/<int:ride_id>/', views.feedback_form, name='feedback_form'),
    path('receipt/<int:ride_id>/', views.receipt_pdf, name='receipt_pdf'),

]
