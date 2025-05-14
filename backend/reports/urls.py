from django.urls import path
from .views import report_dashboard, delivery_report

urlpatterns = [
    path('', report_dashboard, name='report_dashboard'),
    path('report/', delivery_report, name='delivery_report'),  # <-- Новый API
]