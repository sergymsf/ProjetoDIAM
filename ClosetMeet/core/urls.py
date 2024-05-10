from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.initial_page, name='initial_page'),
    path('join/', views.join_page, name='join_page'),
    path('login', views.login_handler, name='login_handler'),
    path('logout', views.logout_handler, name='logout_handler'),
    path('signin', views.signin_handler, name='signin_handler'),
    path('personal-page/', views.personal_page, name='personal_page'),
    path('personal-page/edit-profile', views.edit_profile, name='edit_profile'),
    path('personal-page/add-clothing-item', views.add_clothing_item, name='add_clothing_item'),
    ]
