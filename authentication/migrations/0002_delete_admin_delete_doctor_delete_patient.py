# Generated by Django 5.1.3 on 2024-12-28 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Admin',
        ),
        migrations.DeleteModel(
            name='Doctor',
        ),
        migrations.DeleteModel(
            name='Patient',
        ),
    ]