from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Employee
from .serializers import EmployeeSerializer, AddressSerializer, WorkExperienceSerializer, QualificationSerializer, ProjectSerializer

class CreateEmployee(APIView):
    def post(self, request):
        try:
            # Deserialize employee data
            serializer = EmployeeSerializer(data=request.data)
            # Validate employee data
        
            if serializer.is_valid():

                # Check for duplicate email
                if Employee.objects.filter(email=request.data.get('email', '')).exists():
                    return Response({"message": "Employee already exists"}, status=status.HTTP_200_OK)
                
                # Handle photo field
                photo_data = request.data.get('photo')
                if photo_data:
                    # Pass the photo data to the serializer for processing
                    serializer.validated_data['photo'] = photo_data
                else:
                    # If no photo data is provided, set photo field to None
                    serializer.validated_data['photo'] = None

                # Deserialize and validate address data
                address_serializer = AddressSerializer(data=request.data.get('addressDetails', {}))
                address_serializer.is_valid(raise_exception=True)
                address_instance = address_serializer.save()

                # Deserialize and validate work experience data
                work_experience_serializer = WorkExperienceSerializer(data=request.data.get('workExperience', []), many=True)
                work_experience_serializer.is_valid(raise_exception=True)
                work_experience_instances = work_experience_serializer.save()

                # Deserialize and validate qualifications data
                qualifications_serializer = QualificationSerializer(data=request.data.get('qualifications', []), many=True)
                qualifications_serializer.is_valid(raise_exception=True)
                qualifications_instances = qualifications_serializer.save()

                # Deserialize and validate projects data
                projects_serializer = ProjectSerializer(data=request.data.get('projects', []), many=True)
                projects_serializer.is_valid(raise_exception=True)
                projects_instances = projects_serializer.save()

                # Create employee instance with related data
                employee_instance = serializer.save(
                    address_details=address_instance,
                    work_experience=work_experience_instances,
                    qualifications=qualifications_instances,
                    projects=projects_instances
                )
                
                # Return success response
                return Response({"message": "Employee created successfully", "regid": employee_instance.regid, "success": True}, status=status.HTTP_201_CREATED)
            else:
                # Return response with validation errors
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Return error response if any exception occurs
            return Response({"message": f"Employee creation failed due to exception: {str(e)}", "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
