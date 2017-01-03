from django.shortcuts import render
from django.views.generic import View


class IngresarCalles(View):

    def get(self, request):
        return render(request=request,
                      template_name='buscador/forma_buscador.html')
