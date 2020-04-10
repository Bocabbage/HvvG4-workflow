from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse
from django.core.files import File
import subprocess
import os

SAVED_FILES_DIR = './files/'

def __render_home_template(request):
    '''render the home-page'''
    files = os.listdir(SAVED_FILES_DIR)
    return render(request, 'g4predict/home.html', {'files': files})

''' 
    The decorator [require_GET] is to require that a view
    only accepts the GET method.
'''
@require_GET
def home(request):
    if not os.path.exists(SAVED_FILES_DIR):
        os.makedirs(SAVED_FILES_DIR)

    return __render_home_template(request)

@require_GET
def download(request, filename):
    file_pathname = os.path.join(SAVED_FILES_DIR, filename)
    with open(file_pathname, 'rb') as f:
        file = File(f)
        response = HttpResponse(
                                 file.chunks(),
                                 content_type = 'APPLICATION/OCTET-STREAM'
                               )
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        response['Content-Length'] = os.path.getsize(file_pathname)

    return response

@require_POST
def upload(request):
    g4File = request.FILES.get("g4-filename", None)
    atacFile = request.FILES.get("atac-filename", None)
    if not g4File or not atacFile:
        return __render_home_template(request)

    for file in [g4File, atacFile]:
        pathname = os.path.join(SAVED_FILES_DIR, file.name)
        with open(pathname, 'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)

    # -------- ComputeCodeHere -------- #
    subprocess.run([
                     "bash", 
                     "/mnt/c/Programming/G4/G4_predict_project/og4_to_vg4/workflow/workflow.sh",
                     os.path.join(SAVED_FILES_DIR, g4File.name),
                     os.path.join(SAVED_FILES_DIR, atacFile.name),
                   ])
    # --------------------------------- #

    # __render_home_template(request)

    with open('/mnt/c/Programming/G4/G4_predict_project/webapp/G4site/files/result.bed', 'rb') as f:
        resultFile = File(f)
        response = HttpResponse(
                                 resultFile.chunks(),
                                 content_type = 'APPLICATION/OCTET-STREAM'
                               )
        response['Content-Disposition'] = 'attachment; filename=result.bed'
        response['Content-Length'] = os.path.getsize('./files/result.bed')

    return response
