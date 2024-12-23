from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'app2'
urlpatterns = [
    path('messages/', views.message_list, name='message_list'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', LogoutView.as_view(next_page='app2:login'), name='logout'),
   
]
