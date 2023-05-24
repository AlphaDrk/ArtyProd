from django.urls import path
from django.conf.urls.static import static as statistics
from django.conf import settings
from django.contrib.auth import views as auth_views
from .views import (
    ContactUsView,
    HomeView,
    MyPasswordResetView,
    PersHomeView,
    RegisterView,
    clientHomeView,
    contact_user,
    myprofile_view,
    myprojects_view,
    project_request_list,
    project_request_view,
    update_profile,
    update_project,

)
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('PersDash/', PersHomeView.as_view(), name='PersDash'),
    path('clientDash/', clientHomeView.as_view(), name='clientDash'),
    path('login/',auth_views.LoginView.as_view(template_name='registration/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name = 'logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password_reset/', MyPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('contact/', ContactUsView.as_view(), name='contact_us'),
    path('contactUser/', contact_user, name='contact_user'),
    path('myprofile/<int:user_id>/', myprofile_view, name='myprofile'),
    path('update_profile/<int:user_id>/', update_profile, name='update_profile'),
    path('myprojects/', myprojects_view, name='myprojects'),
    path('update_project/<int:project_id>/', update_project, name='update_project'),
    path('project-request/', project_request_view, name='project-request'),
    path('project-rep/', project_request_list, name='project-rep'),
   
]+ statistics(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)