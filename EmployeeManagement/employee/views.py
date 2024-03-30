from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Employee
from .serializers import EmployeeSerializer, AddressSerializer, WorkExperienceSerializer, QualificationSerializer, ProjectSerializer


# creating a new employee instance
class CreateEmployee(APIView):
    def post(self, request):
        try:
            # Deserialize employee data
            serializer = EmployeeSerializer(data=request.data)
            # Validate employee data
        
            if serializer.is_valid():

                # Check for duplicate email
                if Employee.objects.filter(email=request.data.get('email', '')).exists():
                    return Response({"message": "Employee creation failed due to duplicate email", "success": False}, status=status.HTTP_200_OK)
                
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
                return Response({"message": "Invalid body request", "success": False}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Return error response if any exception occurs
            return Response({"message": "Employee creation failed", "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Retriving employee information
class RetrieveEmployee(APIView):
    def get(self, request, regid=None):
        try:
            if regid:
                # Retrieve employee by regid if provided
                employee = Employee.objects.get(regid=regid)
                serializer = EmployeeSerializer(employee)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # Retrieve all employees
                employees = Employee.objects.all()
                serializer = EmployeeSerializer(employees, many=True)
                return Response({"employees": serializer.data, "message": "employee details found", "success": True,}, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({"message": "Employee not found", "employees": [], "success": False}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": f"Error retrieving employee information: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
# Deleting an employee
class DeleteEmployee(APIView):
    def delete(self, request, regid):
        try:
            # Check if the employee with the given regid exists
            employee = Employee.objects.get(regid=regid)
            # Delete the employee
            employee.delete()
            return Response({"message": "Employee deleted successfully", 'success': True}, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({"message": "Employee not found", "success": False}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "Employee deletion failed", "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

# Updating employee details
class UpdateEmployee(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'regid'

    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({"message": "Employee details updated successfully", "regid": instance.regid, "success": True}, status=status.HTTP_200_OK)
        
        except Employee.DoesNotExist:
            return Response({"message": "Employee not found for this regid", "success": False}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"message": "Employee details updation failed", "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)