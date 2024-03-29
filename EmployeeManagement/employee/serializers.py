from rest_framework import serializers
from .models import *



class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class WorkExperienceSerializer(serializers.ModelSerializer):
    companyName = serializers.CharField(source='company_name')
    fromDate = serializers.CharField(source='from_date')
    toDate = serializers.CharField(source='to_date')

    class Meta:
        model = WorkExperience
        fields = ['companyName', 'fromDate', 'toDate', 'address']

class QualificationSerializer(serializers.ModelSerializer):
    qualificationName = serializers.CharField(source='qualification_name')
    fromDate = serializers.CharField(source='from_date')
    toDate = serializers.CharField(source='to_date')
   
    class Meta:
        model = Qualification
        fields = ['qualificationName','fromDate','toDate','percentage']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        
class EmployeeSerializer(serializers.ModelSerializer):
    addressDetails = AddressSerializer(source='address_details', read_only=True)
    workExperience = WorkExperienceSerializer(source='work_experience', many=True, read_only=True)
    qualifications = QualificationSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    phoneNo = serializers.CharField(source='phone_no', allow_null=True, allow_blank=True)
    photo = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = Employee
        fields = ['name','email','age','gender','phoneNo','addressDetails','workExperience','qualifications','projects','photo']

