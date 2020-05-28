from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse
from django.core.files import File
import subprocess
import os
import random
import glob

SAVED_FILES_DIR = './files'
UTILS_DIR = '../../og4_to_vg4/utils'
TRANSFORM_DIR = '../../og4_to_vg4/transformation'
WORKFLOW_DIR = '../../og4_to_vg4'
WORKFLOW_SH = '../../og4_to_vg4/workflow/workflow.sh'


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

@require_POST
def download(request):
    downloadOption = request.POST.getlist("download_option")[0]
    g4FileName = "g4seq_{}.bed".format(downloadOption)
    file_pathname = os.path.join(SAVED_FILES_DIR, g4FileName)
    with open(file_pathname, 'rb') as f:
        file = File(f)
        response = HttpResponse(
                                 file.chunks(),
                                 content_type = 'APPLICATION/OCTET-STREAM'
                               )
        response['Content-Disposition'] = 'attachment; filename={}'.format(g4FileName)
        response['Content-Length'] = os.path.getsize(file_pathname)

    return response

@require_POST
def upload(request):
    option = request.POST.getlist("output_option")[0]
    atacFile = request.FILES.get("atac_filename", None)
    bsFile = request.FILES.get("bs_filename", None)
    g4FileName = "g4seq_{}.bed".format(option)

    # if not g4File or not atacFile:
    #     return __render_home_template(request)
    if not atacFile:
        return __render_home_template(request)
    

    for file in [bsFile, atacFile]:
        pathname = os.path.join(SAVED_FILES_DIR, file.name)
        with open(pathname, 'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)
    # atacPathname = os.path.join(SAVED_FILES_DIR, atacFile.name)
    # with open(atacPathname, 'wb+') as dest:
    #     for chunk in atacFile.chunks():
    #         dest.write(chunk)

    taskPrefix = atacFile.name.split('.')[0] + str(random.randint(0, 5000))
    # -------- ComputeCodeHere -------- #
    subprocess.run([
                     "bash", 
                     WORKFLOW_SH,
                     # os.path.join(SAVED_FILES_DIR, g4File.name),
                     os.path.join(SAVED_FILES_DIR, g4FileName),
                     os.path.join(SAVED_FILES_DIR, atacFile.name),
                     os.path.join(SAVED_FILES_DIR, bsFile.name),
                     taskPrefix,
                     UTILS_DIR,
                     TRANSFORM_DIR,
                     SAVED_FILES_DIR,
                     WORKFLOW_DIR,
                   ])
    # --------------------------------- #
    resultFilePath = os.path.join(SAVED_FILES_DIR, "{}_result.bed".format(taskPrefix))

    with open(resultFilePath, 'rb') as f:
        resultFile = File(f)
        response = HttpResponse(
                                 resultFile.chunks(),
                                 content_type = 'APPLICATION/OCTET-STREAM'
                               )
        response['Content-Disposition'] = 'attachment; filename=result.bed'
        response['Content-Length'] = os.path.getsize(resultFilePath)

    # Noted that the wildcard(*) can't be used directly without shell=True
    subprocess.call('rm {}/{}_*'.format(SAVED_FILES_DIR, taskPrefix), shell=True)

    return response
