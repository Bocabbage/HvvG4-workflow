from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, JsonResponse
from django.core.files import File
import subprocess
import socket
import os
import random
# import glob

# SAVED_FILES_DIR = './files'
STATIC_FILES_DIR = './g4predict/static/files'
SAVED_FILES_DIR = './g4predict/results'
UTILS_DIR = '../../og4_to_vg4/utils'
TRANSFORM_DIR = '../../og4_to_vg4/transformation'
WORKFLOW_DIR = '../../og4_to_vg4'
WORKFLOW_SH = '../../og4_to_vg4/workflow/workflow.sh'


def __render_home_template(request):
    '''render the home-page'''
    files = os.listdir(SAVED_FILES_DIR)
    return render(request, 'g4predict/home.html', {'files': files})


r'''
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
        response = HttpResponse(file.chunks(),
                                content_type='APPLICATION/OCTET-STREAM')
        response['Content-Disposition'] = 'attachment; filename={}'.format(g4FileName)
        response['Content-Length'] = os.path.getsize(file_pathname)

    return response


@require_GET
def result_file_download(request, random_num):
    print("random_num:{}".format(random_num))
    resultFileName = "{}_result.bed".format(random_num)
    resultFilePath = os.path.join(SAVED_FILES_DIR, resultFileName)
    with open(resultFilePath, 'rb') as f:
        file = File(f)
        response = HttpResponse(file.chunks(),
                                content_type='APPLICATION/OCTET-STREAM')
        response['Content-Disposition'] = 'attachment; filename={}'.format(resultFileName)
        response['Content-Length'] = os.path.getsize(resultFilePath)
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
    randomSeed = str(random.randint(0, 5000))
    taskPrefix = atacFile.name.split('.')[0] + randomSeed
    # -------- ComputeCodeHere -------- #
    subprocess.run(["bash",
                    WORKFLOW_SH,
                    # os.path.join(SAVED_FILES_DIR, g4File.name),
                    os.path.join(STATIC_FILES_DIR, g4FileName),
                    os.path.join(SAVED_FILES_DIR, atacFile.name),
                    os.path.join(SAVED_FILES_DIR, bsFile.name),
                    taskPrefix,
                    UTILS_DIR,
                    TRANSFORM_DIR,
                    SAVED_FILES_DIR,
                    WORKFLOW_DIR])
    # --------------------------------- #

    # Noted that the wildcard(*) can't be used directly without shell=True
    subprocess.call('mv {fileDir}/{taskPrefix}_result.bed {fileDir}/{randomNum}_result.bed'.format(
                    fileDir=SAVED_FILES_DIR,
                    taskPrefix=taskPrefix,
                    randomNum=randomSeed),
                    shell=True)
    subprocess.call('rm {fileDir}/{taskPrefix}_*'.format(
                    fileDir=SAVED_FILES_DIR,
                    taskPrefix=taskPrefix),
                    shell=True)

    response_data = {}
    sockObj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockObj.connect(('8.8.8.8', 80))
    host_ip = sockObj.getsockname()[0]
    host_port = request.META['SERVER_PORT']

    response_data['result'] = ("http://{host_ip}:{host_port}/"
                               "g4predict/result_file_download/"
                               "{rand_seed}").format(
        host_ip=host_ip,
        host_port=host_port,
        rand_seed=randomSeed,
    )
    response = JsonResponse(response_data)
    return response
