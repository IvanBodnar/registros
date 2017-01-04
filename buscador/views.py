from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from .forms import CallesForm


class IngresarCalles(View):

    def get(self, request):
        form = CallesForm()
        return render(request=request,
                      template_name='buscador/forma_buscador.html',
                      context={'form': form})

    def post(self, request):
        form = CallesForm(request.POST)
        if form.is_valid():
            calle1 = form.cleaned_data['calle1']
            calle2 = form.cleaned_data['calle2']

            return HttpResponse(calle1 + calle2)
        else:
            return CallesForm()