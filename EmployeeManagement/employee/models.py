from django.db import models

# Create your models here.

class Address(models.Model):
    hno = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

class WorkExperience(models.Model):
    company_name = models.CharField(max_length=100)
    from_date = models.CharField(max_length=50)
    to_date = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    
class Qualification(models.Model):
    qualification_name = models.CharField(max_length=100)
    from_date = models.CharField(max_length=50)
    to_date = models.CharField(max_length=50)
    percentage = models.FloatField()

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    phone_no = models.CharField(max_length=20, blank=True, null=True)
    address_details = models.OneToOneField(Address, on_delete=models.CASCADE)
    work_experience = models.ManyToManyField(WorkExperience, blank=True)
    qualifications = models.ManyToManyField(Qualification, blank=True)
    projects = models.ManyToManyField(Project, blank=True)
    photo = models.ImageField(upload_to='employee_dp/', blank=True, null=True)
    regid = models.CharField(max_length=10, unique=True, editable=False)

    def save(self, *args, **kwargs):
        # Generate regid if it's a new entry
        if not self.pk:
            last_employee = Employee.objects.all().order_by('id').last()
            if last_employee:
                last_regid = last_employee.regid
                # Extract numeric part of regid
                numeric_part = last_regid.split('EMP')[1]
                # Increment the numeric part
                next_id = int(numeric_part) + 1
                # Format the new regid with leading zeros
                self.regid = 'EMP{:03d}'.format(next_id)
            else:
                self.regid = 'EMP001'
        super(Employee, self).save(*args, **kwargs)