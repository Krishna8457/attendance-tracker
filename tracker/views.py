# --- IMPORTS ---
# You need to add JsonResponse and Count to your imports
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Count, Q
from .models import Student, Course, Attendance
from django.utils import timezone


# --- EXISTING VIEWS (for taking attendance) ---
# Keep these exactly as they are.
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'tracker/course_list.html', {'courses': courses})

def attendance_sheet(request, course_id):
    course = Course.objects.get(id=course_id)
    students = course.students.all()
    date = timezone.now().date()

    if request.method == 'POST':
        for student in students:
            is_present = request.POST.get(f'student_{student.id}') == 'on'
            Attendance.objects.update_or_create(
                student=student,
                course=course,
                date=date,
                defaults={'present': is_present}
            )
        # I'll redirect to the new report page for a better user experience
        return redirect('attendance_report', course_id=course.id)

    # Get a list of IDs for students already marked as present today
    present_student_ids = set(
        Attendance.objects.filter(course=course, date=date, present=True)
        .values_list('student_id', flat=True)
    )

    return render(request, 'tracker/attendance_sheet.html', {
        'course': course,
        'students': students,
        'date': date,
        'present_student_ids': present_student_ids
    })


# --- NEW VIEWS (for the chart report) ---
# Add these new functions below your existing ones.
def attendance_report(request, course_id):
    course = Course.objects.get(id=course_id)
    # This new line gets a unique list of all dates that have attendance records
    dates = Attendance.objects.filter(course=course).values_list('date', flat=True).distinct().order_by('-date')
    
    # We now pass the 'dates' to the template
    return render(request, 'tracker/attendance_report.html', {'course': course, 'dates': dates})

def attendance_chart_data(request, course_id):
    course = Course.objects.get(id=course_id)
    # This query groups attendance by date and counts the present/absent students for each day
    attendance_data = Attendance.objects.filter(course=course) \
        .values('date') \
        .annotate(present_count=Count('pk', filter=Q(present=True)),
                  absent_count=Count('pk', filter=Q(present=False))) \
        .order_by('date')

    # Prepare data for the chart
    labels = [item['date'].strftime('%b %d') for item in attendance_data] # e.g., "Aug 10"
    present_data = [item['present_count'] for item in attendance_data]
    absent_data = [item['absent_count'] for item in attendance_data]

    # Return the data in a format JavaScript can understand
    return JsonResponse({
        'labels': labels,
        'present_data': present_data,
        'absent_data': absent_data,
    })

from datetime import date

# Add this new function to the end of your views.py file
def daily_detail_report(request, course_id, year, month, day):
    course = Course.objects.get(id=course_id)
    report_date = date(year, month, day)

    present_students = Student.objects.filter(
        attendance__course_id=course_id,
        attendance__date=report_date,
        attendance__present=True
    )

    absent_students = Student.objects.filter(
        attendance__course_id=course_id,
        attendance__date=report_date,
        attendance__present=False
    )

    # This view will send all this data to a new template that we will create later
    return render(request, 'tracker/daily_detail_report.html', {
        'course': course,
        'report_date': report_date,
        'present_students': present_students,
        'absent_students': absent_students,
    })