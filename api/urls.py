from django.urls import include, path
from django.conf.urls import url
from rest_framework.authtoken import views
urlpatterns = [
    path('', include('rest_framework')),

]
