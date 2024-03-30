from django.urls import path
from .views import *

urlpatterns = [
    path('manage/', ManageEmployee.as_view(), name='manage_employee'),
    path('manage/<str:regid>/', ManageEmployee.as_view(), name='manage_employee_detail'),
    path('update/<str:regid>/', UpdateEmployee.as_view(), name='update_employee'),
]
