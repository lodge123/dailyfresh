from  django.urls import path,re_path
from apps.user import views
from apps.user.views import RegisterView,ActiveView,LoginView
app_name = 'apps.user'
urlpatterns=[
    path('register',RegisterView.as_view(),name='register'),
    re_path('active/(?P<token>.*)', ActiveView.as_view(), name='active'),
    path('login',LoginView.as_view(),name='login')
]