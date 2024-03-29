from django.urls import path
from .views import *

urlpatterns = [
    path('create/',CreateEmployee.as_view(), name='create_employee'),
]
