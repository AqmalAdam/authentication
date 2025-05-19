# core/urls.py  (inside your app folder, same level as views.py)

from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='recipes'),  # you might want to rename 'recipes' to 'home' for clarity
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='login_page'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)