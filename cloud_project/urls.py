from django.contrib import admin
from django.urls import path
from webapp.itreporting import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('course/', views.course_page, name='course_page'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('module/register/<int:module_id>/', views.register_module, name='register_module'),
    path('module/unregister/<int:module_id>/', views.unregister_module, name='unregister_module'),
    path('my-registrations/', views.my_registrations, name='my_registrations'),
    path('module/<str:module_code>/', views.module_detail, name='module_detail'),
]



