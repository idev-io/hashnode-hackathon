from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name="topthings"

urlpatterns = [
    # Authentication
    path('logout/', views.logout_page, name="logout"),
    

    # Frontend
    path('', views.home_page, name="home"),
    path('things/', views.things, name="things"),
    path('things/thing/<slug:slug>/', views.single_thing, name='single-thing'),
    path('things/thing/edit/<slug:slug>/', views.edit_thing, name='edit-thing'),
    path('things/thing/delete/<slug:slug>', views.delete_thing, name='delete-thing'),
    path('about/', views.about, name="about-me"),

    # Dashboard
    path('auth/users/dashboard/', views.dashboard, name="user-dashboard"),
    path('things/create-new-thing/', views.create_thing, name="create-thing"),
    
]

handler404 = 'top_things.views.error_page'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
