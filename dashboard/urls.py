from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register_employee, name='register'),
    path('login/',views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_employee, name='add_employee'),
    path('edit/<int:id>/', views.edit_employee, name='edit_employee'),
    path('delete/<int:id>/', views.delete_view, name='delete_employee'),
    path('',views.home, name='home'),
]
