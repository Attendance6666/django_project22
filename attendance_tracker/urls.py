from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home, name='home'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
    path('students/', views.students_list, name='students_list'),
    
    
    path('api/students/', views.api_students_list, name='api_students'),
    path('api/attendance/', views.api_attendance, name='api_attendance'),
]