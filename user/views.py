from django.shortcuts import render


def inicio(request):
    return render(request, template_name='user/inicio.html')
