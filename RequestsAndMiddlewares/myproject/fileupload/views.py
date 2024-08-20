from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.files.storage import FileSystemStorage

MAX_FILE_SIZE_MB = 1  # Максимальный размер файла в Мб


@require_POST
def upload_file(request):
    file = request.FILES.get('file')

    if not file:
        return JsonResponse({'error': 'No file uploaded.'}, status=400)

    if file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        return JsonResponse({'error': 'File size exceeds 1 MB limit.'}, status=400)

    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    return JsonResponse({'message': 'File uploaded successfully.', 'filename': filename}, status=200)