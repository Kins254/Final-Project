from django.db import models

class Patients(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    phone=models.BigIntegerField()
    date_of_birth=models.DateField()
    gender=models.CharField(max_length=10)
    address=models.CharField(max_length=255)
    registration_date = models.DateTimeField(auto_now_add=True)  
    

    class Meta:
        managed = False
        db_table = 'patients'


class Doctors(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)  # Adjusted max_length
    last_name = models.CharField(max_length=50)  # Added field
    specialization = models.CharField(max_length=100)  # Added field
    email = models.EmailField(unique=True, max_length=100)  # Adjusted max_length
    phone = models.CharField(max_length=20)  # Added field
    schedule = models.TextField()  # Added field
    password_hash = models.CharField(max_length=255)  # Unchanged

    class Meta:
        managed = False
        db_table = 'doctors'



class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    first_name=models.CharField(max_length=255)
    username=models.CharField(max_length=255)
    role=models.CharField(max_length=255)
    last_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'admin'


class Appointment(models.Model):  
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    communication_type = models.CharField(max_length=255)
    payment_type = models.CharField(max_length=255, default='unpaid')
    status = models.CharField(max_length=255, default='Pending')
    appointment_type = models.CharField(max_length=255)

    def __str__(self):
        return f"Appointment {self.id} for Patient {self.patient.first_name} {self.patient.last_name}"
    
    class Meta:
        db_table = 'appointments'

class Drug(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)  # Unique name for the drug
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price with two decimals
    description = models.TextField()  # Detailed description of the drug
    image_url = models.URLField(max_length=255)  # URL to the image of the drug
    category = models.CharField(max_length=255)  # Category of the drug (e.g., Antibiotics)
    quantity=models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 'drugs'