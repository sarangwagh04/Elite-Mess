from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import MessMenu, PaymentRequest, Attendance, AttendanceSummary
from suggestions.models import Suggestion
from django.contrib.auth.models import User
import pandas as pd
from datetime import datetime

def is_staff_user(user):
    return user.is_staff

@login_required
def student_dashboard(request):
    if request.user.is_staff:
        return redirect('billing:staff_dashboard')
    
    # Get current month/year
    now = datetime.now()
    summary = AttendanceSummary.objects.filter(student=request.user, month=now.month, year=now.year).first()
    
    # Get menu
    menu = MessMenu.objects.all()
    
    # Payments
    last_payment = PaymentRequest.objects.filter(student=request.user).order_by('-created_at').first()
    
    # Feedbacks
    feedbacks = Suggestion.objects.all().order_by('-created_at')
    
    # Attendance for calendar
    attendances = Attendance.objects.filter(student=request.user, date__month=now.month, date__year=now.year, is_present=True)
    present_days = [a.date.day for a in attendances]
    
    return render(request, 'billing/student_dashboard.html', {
        'summary': summary,
        'menu': menu,
        'last_payment': last_payment,
        'feedbacks': feedbacks,
        'present_days': present_days,
        'now': now
    })

@login_required
@user_passes_test(is_staff_user)
def staff_dashboard(request):
    pending_payments = PaymentRequest.objects.filter(status='PENDING').order_by('-created_at')
    feedbacks = Suggestion.objects.all().order_by('-created_at')
    menu = MessMenu.objects.all()
    summaries = AttendanceSummary.objects.all().order_by('-year', '-month')
    
    return render(request, 'billing/staff_dashboard.html', {
        'pending_payments': pending_payments,
        'feedbacks': feedbacks,
        'menu': menu,
        'summaries': summaries
    })

@login_required
def submit_payment(request):
    if request.method == 'POST':
        screenshot = request.FILES.get('screenshot')
        now = datetime.now()
        summary = AttendanceSummary.objects.filter(student=request.user, month=now.month, year=now.year).first()
        
        if screenshot and summary:
            PaymentRequest.objects.create(
                student=request.user,
                summary=summary,
                screenshot=screenshot
            )
            messages.success(request, 'Payment receipt uploaded successfully!')
        else:
            messages.error(request, 'Upload failed. Please ensure you have a bill for this month.')
            
    return redirect('billing:student_dashboard')

@login_required
@user_passes_test(is_staff_user)
def upload_attendance(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        try:
            df = pd.read_excel(excel_file)
            # Expects columns: Username, Day 1, Day 2, ...
            now = datetime.now()
            
            for index, row in df.iterrows():
                username = str(row['Username']).strip()
                user = User.objects.filter(username=username).first()
                if user:
                    # Count 'P' or 1 for presence
                    days_present = 0
                    for col in df.columns:
                        if col.startswith('Day'):
                            if str(row[col]).upper() in ['P', '1', 'PRESENT']:
                                days_present += 1
                                # Log individual attendance
                                day_num = int(col.split(' ')[1])
                                try:
                                    date_obj = datetime(now.year, now.month, day_num)
                                    Attendance.objects.update_or_create(
                                        student=user, date=date_obj,
                                        defaults={'is_present': True}
                                    )
                                except: pass 

                    # Update summary
                    AttendanceSummary.objects.update_or_create(
                        student=user, month=now.month, year=now.year,
                        defaults={'total_present_days': days_present}
                    )
            messages.success(request, 'Attendance processed successfully!')
        except Exception as e:
            messages.error(request, f'Error processing Excel: {str(e)}')
            
    return redirect('billing:staff_dashboard')

@login_required
@user_passes_test(is_staff_user)
def update_menu(request):
    if request.method == 'POST':
        day = request.POST.get('day')
        MessMenu.objects.update_or_create(
            day=day,
            defaults={
                'breakfast': request.POST.get('breakfast'),
                'lunch': request.POST.get('lunch'),
                'dinner': request.POST.get('dinner')
            }
        )
        messages.success(request, f'Menu for {day} updated!')
    return redirect('billing:staff_dashboard')

@login_required
@user_passes_test(is_staff_user)
def approve_payment(request, payment_id):
    payment = get_object_or_404(PaymentRequest, id=payment_id)
    payment.status = 'PAID' if request.POST.get('action') == 'approve' else 'REJECTED'
    payment.save()
    messages.success(request, f'Payment for {payment.student.username} updated.')
    return redirect('billing:staff_dashboard')
