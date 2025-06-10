from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from django.middleware.csrf import get_token
from django.views import View
from .models import UploadedDocument
import json

@csrf_exempt
@require_http_methods(["POST"])
def signup_view(request):
    try:
        data = json.loads(request.body)
        if User.objects.filter(username=data['username']).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        User.objects.create_user(
            username=data['username'],
            password=data['password'],
            email=data.get('email', ''),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', '')
        )
        return JsonResponse({'message': 'User created successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def upload_document(request):
    user_id = request.POST.get('user_id')
    file = request.FILES.get('file')

    if not user_id or not file:
        return JsonResponse({'error': 'Missing user_id or file'}, status=400)

    try:
        user = User.objects.get(id=user_id)
        document = UploadedDocument.objects.create(
            user=user,
            filename=file.name,
            file=file,
            fraud_score=0.0,  # Replace with real fraud detection logic
            verdict='Pending'
        )
        return JsonResponse({'message': 'File uploaded successfully', 'doc_id': document.id})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def list_documents(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        docs = UploadedDocument.objects.filter(user=user).order_by('-uploaded_at')
        result = [{
            'id': doc.id,
            'filename': doc.filename,
            'uploaded_at': doc.uploaded_at,
            'fraud_score': doc.fraud_score,
            'verdict': doc.verdict,
        } for doc in docs]
        return JsonResponse(result, safe=False)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@csrf_exempt
@require_http_methods(["POST"])
def verify_document(request, doc_id):
    try:
        doc = UploadedDocument.objects.get(id=doc_id)
        doc.verdict = "Verified"
        doc.fraud_score = 0.1  # Simulate verification
        doc.save()
        return JsonResponse({'message': 'Document verified'})
    except UploadedDocument.DoesNotExist:
        return JsonResponse({'error': 'Document not found'}, status=404)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_document(request, doc_id):
    try:
        doc = UploadedDocument.objects.get(id=doc_id)
        doc.delete()
        return JsonResponse({'message': 'Document deleted'})
    except UploadedDocument.DoesNotExist:
        return JsonResponse({'error': 'Document not found'}, status=404)


from django.http import FileResponse, Http404

@csrf_exempt
@require_http_methods(["GET"])
def view_file(request, doc_id):
    try:
        doc = UploadedDocument.objects.get(id=doc_id)
        return FileResponse(doc.file.open(), as_attachment=True, filename=doc.filename)
    except UploadedDocument.DoesNotExist:
        raise Http404("Document not found.")
