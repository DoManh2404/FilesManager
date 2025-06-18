from asgiref.sync import sync_to_async
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
import os
import unicodedata
from urllib.parse import quote, unquote
from myapp.forms import forms_files


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')


class FileListView(View):
    def get(self, request):
        try:
            media_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_file')
            os.makedirs(media_path, exist_ok=True)

            files_list = os.listdir(media_path)
            file_info = []

            for file in files_list:
                file_path = os.path.join(media_path, file)
                file_size = os.path.getsize(file_path) / (1024 * 1024)
                modified_time = timezone.datetime.fromtimestamp(os.path.getmtime(file_path))
                file_info.append({
                    "name": file,
                    "size": file_size,
                    "modified_time": modified_time
                })

            file_info.sort(key=lambda x: x["modified_time"], reverse=True)

            paginator = Paginator(file_info, 10)
            page = request.GET.get('page')
            try:
                files = paginator.page(page)
            except PageNotAnInteger:
                files = paginator.page(1)
            except EmptyPage:
                files = paginator.page(paginator.num_pages)

            return render(request, 'myapp/file_list.html', {'files': files})
        except Exception as e:
            print(e)
            return HttpResponseBadRequest("Bad Request Message")


class FileUploadView(View):
    def get(self, request):
        form = forms_files.FileFieldForm()
        return render(request, 'myapp/file_upload.html', {'form': form})

    def post(self, request):
        ip = get_client_ip(request)
        print("upload ip:", ip)

        form = forms_files.FileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file_field')
            for f in files:
                self.handle_uploaded_file(f)
            return HttpResponse('File uploaded successfully')
        return HttpResponseBadRequest("Invalid form submission")

    def handle_uploaded_file(self, f):
        try:
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploaded_file')
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, f.name)
            with open(file_path, 'wb+') as dest:
                for chunk in f.chunks():
                    dest.write(chunk)
        except Exception as e:
            print(e)


class FileDownloadView(View):
    def get(self, request, file_name):
        decoded_file_name = unquote(file_name)
        file_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_file',decoded_file_name)

        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/force-download')
                response['Content-Disposition'] = f"attachment; filename*=UTF-8''{quote(decoded_file_name)}"
                return response
        return HttpResponseNotFound("File not found")


@method_decorator(csrf_exempt, name='dispatch')
class FileDeleteView(View):
    def post(self, request):
        file_name = request.POST.get('file_name')
        file_path = os.path.join(settings.MEDIA_ROOT,'uploaded_file', file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            return JsonResponse({'success': True})
        return JsonResponse({'error': f'File {file_name} does not exist.'})


@method_decorator(csrf_exempt, name='dispatch')  # Optional if you use CSRF token properly
class FileSearchView(View):
    async def post(self, request):
        search_name = request.POST.get('file_name').strip()
        search_name_norm = unicodedata.normalize('NFC', search_name).lower()

        def sync_search():
            matched_files = []
            search_dir = os.path.join(settings.MEDIA_ROOT, 'uploaded_file')

            for dirpath, _, filenames in os.walk(search_dir):
                for fname in filenames:
                    fname_norm = unicodedata.normalize('NFC', fname).lower()
                    if search_name_norm in fname_norm:
                        matched_files.append(os.path.join(dirpath, fname))
            return matched_files

        files_list = await sync_to_async(sync_search)()

        file_info = []
        for file_path in files_list:
            try:
                file_stat = await sync_to_async(os.stat)(file_path)
                file_info.append({
                    "name": os.path.basename(file_path),
                    "size": file_stat.st_size / (1024 * 1024),
                    "modified_time": timezone.datetime.fromtimestamp(file_stat.st_mtime),
                })
            except OSError as e:
                print(e)

        file_info.sort(key=lambda x: x["modified_time"], reverse=True)

        paginator = Paginator(file_info, 10)
        page = request.GET.get('page')
        try:
            files = paginator.page(page)
        except PageNotAnInteger:
            files = paginator.page(1)
        except EmptyPage:
            files = paginator.page(paginator.num_pages)

        html = render_to_string('myapp/file_list_body.html', {'files': files})
        return JsonResponse({'html': html})
