from django.db import models

class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    phone=models.BigIntegerField()
    date_of_birth=models.DateField()
    gender=models.CharField(max_length=10)
    address=models.CharField(max_length=255)
    

    class Meta:
        managed = False
        db_table = 'patients'


class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    first_name=models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'doctors'


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    first_name=models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'admin'

