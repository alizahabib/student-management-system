from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.student_login, name='student_login'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),# You’ll define this view later
    path('logout/', views.student_logout, name='student_logout'),
]
