from django.shortcuts import render

# Create your views here.



def my_view(request):
    template_name = 'index-6.html'
    return render(request, template_name)