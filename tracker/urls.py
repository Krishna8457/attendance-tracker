from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('attendance/<int:course_id>/', views.attendance_sheet, name='attendance_sheet'),
    path('report/<int:course_id>/', views.attendance_report, name='attendance_report'),
    path('chart-data/<int:course_id>/', views.attendance_chart_data, name='attendance_chart_data'),

    # Add this new line for the detailed daily report
    path('report/<int:course_id>/<int:year>/<int:month>/<int:day>/', views.daily_detail_report, name='daily_detail_report'),
]