from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('submit_payment/', views.submit_payment, name='submit_payment'),
    path('update_menu/', views.update_menu, name='update_menu'),
    path('upload_attendance/', views.upload_attendance, name='upload_attendance'),
    path('approve_payment/<int:payment_id>/', views.approve_payment, name='approve_payment'),
]
