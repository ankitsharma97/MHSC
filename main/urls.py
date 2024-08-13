from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('passchange/', views.passchange, name='passchange'),
    path('patient/', views.patient, name='patient'),
    path('feedback/', views.feedback, name='feedback'),
    path('viewfeedback/', views.viewfeedback, name='viewfeedback'),
    path('polls/', views.polls, name='polls'),
    path('about/', views.about, name='about'),
    # path('contact/', views.contact, name='contact'),
    path('new/', views.new, name='new'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)