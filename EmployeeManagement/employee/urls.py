from django.urls import path
from .views import *

urlpatterns = [
    path('create/',CreateEmployee.as_view(), name='create_employee'),
    path('retrieve/', RetrieveEmployee.as_view(), name='retrieve_all_employees'),
    path('retrieve/<str:regid>/', RetrieveEmployee.as_view(), name='retrieve_employee_by_regid'),
    path('delete/<str:regid>/', DeleteEmployee.as_view(), name='delete_employee'),
]
