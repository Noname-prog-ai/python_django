from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import set_cookie, get_cookie, set_session, get_session

class CustomLogoutView(LogoutView):
    next_page = 'home'

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('setcookie/', set_cookie, name='set_cookie'),
    path('getcookie/', get_cookie, name='get_cookie'),
    path('setsession/', set_session, name='set_session'),
    path('getsession/', get_session, name='get_session'),
]
