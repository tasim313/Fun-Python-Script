# backend/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt  # Disable CSRF protection for this view (for testing purposes)
def upload_invoice(request):
    if request.method == 'POST':
        try:
            # Process the uploaded file
            file = request.FILES['file']
            # Perform OCR processing (you can use your existing OCR logic here)
            extracted_data = {
                'invoice_number': '12345',
                'date': '2023-10-01',
                'vendor': 'Example Vendor',
                'total_amount': '100.00',
            }
            return JsonResponse(extracted_data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)