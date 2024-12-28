from django.urls import path
from administrator import views  # Replace with your app name

urlpatterns = [
    
     path('dashboard/', views.dashboard, name='dashboard'),
     path('doctor_account/',views.doctor_account,name='doctor_account'),
     path('fetch_patients/',views.fetch_patients,name='fetch_patients'),
     path('fetch_doctors/',views.fetch_doctors,name='fetch_doctors'),
     path('delete_patient/<int:patient_id>/',views.delete_patient,name='delete_patient'),
     path('delete_doctor/<int:doctor_id>/',views.delete_doctor,name='delete_doctor'),
     path('view_appointments',views.view_appointments,name='view_appointments'),
     path('overall_stats/',views.overall_stats,name="overall_stats"),
     path('gender_pieChart/',views.gender_pieChart,name='gender_pieChart'),
     path('doctor_specialization/',views.doctor_specialization,name='doctor_specialization'),
     path('monthly_appointment/',views.monthly_appointment,name='monthly_appointment'),
     path('patient_registration_trend/',views.patient_registration_trend,name='patient_registration_trend'),

    # ... other URL patterns
]