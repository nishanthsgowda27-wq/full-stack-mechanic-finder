from django.urls import path
from . import views

app_name = 'service'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_user, name='register_user'),
    path('register/mechanic/', views.register_mechanic, name='register_mechanic'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/user/', views.dashboard_user, name='dashboard_user'),
    path('dashboard/mechanic/', views.dashboard_mechanic, name='dashboard_mechanic'),
    path('mechanic/<int:id>/', views.mechanic_detail, name='mechanic_detail'),
    path('search/', views.search_mechanic, name='search_mechanic'),
    path('tracking/', views.tracking_map, name='tracking_map'),
    path('book/<int:service_id>/', views.book_service, name='book_service'),
    path('bookings/', views.manage_bookings, name='manage_bookings'),
    path('booking/<int:booking_id>/accept/', views.accept_booking, name='accept_booking'),
    path('booking/<int:booking_id>/reject/', views.reject_booking, name='reject_booking'),
    path('booking/<int:booking_id>/accept/json/', views.accept_booking_ajax, name='accept_booking_ajax'),
    path('booking/<int:booking_id>/reject/json/', views.reject_booking_ajax, name='reject_booking_ajax'),
    # MechanicService CRUD for mechanics
    path('service/add/', views.service_add, name='service_add'),
    path('service/<int:pk>/edit/', views.service_edit, name='service_edit'),
    path('service/<int:pk>/delete/', views.service_delete, name='service_delete'),
]
