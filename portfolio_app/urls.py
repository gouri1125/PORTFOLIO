from django.urls import path
from . import views

app_name = 'portfolio_app'  # ✅ Important for namespacing

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('skills/', views.skills_view, name='skills'),
    path('projects/', views.projects_view, name='projects'),
    path('contact/', views.contact, name='contact'),
    # AUTH
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),

    # path('add-project/', views.add_project, name='add_project'),
]
