from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from api import views
urlpatterns = [
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('login/', obtain_auth_token, name='login'),
    path('register/', obtain_auth_token, name='register')
]