from django.contrib import admin
from django.contrib.auth import views as auth_views 
from django.urls import path, include
from django.shortcuts import redirect
from inventory import views as user_views

urlpatterns = [
    path('', lambda request: redirect('/home/')),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', user_views.logout_view, name='logout'),

    path("home/", user_views.HomePage, name = 'home'),
    path("inventory/", include("inventory.urls"), name = 'inventory'),
    path('maximal/', user_views.Maximalview, name='maximal'),
    path("inventory/add/", user_views.AddItemInv, name = 'add_item'),
    path("delete/<int:pk>/", user_views.DeleteItem, name = 'delete_item'),
    path('edit/<int:itemID>/', user_views.EditItem, name='edit_item'),

    path("analytics/", user_views.Analytics, name = 'analytics'),
    path('admin/', admin.site.urls),
]

