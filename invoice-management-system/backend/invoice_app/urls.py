# backend/urls.py (or invoice_app/urls.py)
from django.urls import path
from .views import upload_invoice  # Import the view function

urlpatterns = [
    path('api/upload-invoice', upload_invoice, name='upload_invoice'),
]