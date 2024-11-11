from django.contrib import admin
from django.contrib.auth import views as auth_views 
from django.urls import path, include
from django.shortcuts import redirect
from inventory import views

urlpatterns = [
    path('', lambda request: redirect('/home/')),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path("home/", views.HomePage, name = 'home'),
    path("inventory/", include("inventory.urls"), name = 'inventory'),

    path('maximal/', views.Maximalview, name='maximal'),
    path("inventory/add/", views.AddItemInv, name = 'add_item'),
    path("delete/<int:pk>/", views.DeleteItem, name = 'delete_item'),
    path('edit/<int:itemID>/', views.EditItem, name='edit_item'),

    path("analytics/", views.Analytics, name = 'analytics'),
    path('admin/', admin.site.urls),
]

