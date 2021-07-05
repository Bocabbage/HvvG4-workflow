from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
# from django.http import HttpResponse

def __render_home_template(request):
    '''render the home-page'''
    return render(request, 'igvTestDemo/home.html')

@require_GET
def home(request):
    return __render_home_template(request)