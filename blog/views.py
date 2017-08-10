from django.http import HttpResponse
from django.shortcuts import render
from requests import get, post
from django.core.files.storage import FileSystemStorage

def home(req, text):
    return HttpResponse('Hell0 {}!'.format(text))

def handle_uploaded_file(f):
    with open('name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def contact(request):
    errors = []
    form = {}
    if request.POST:
        form['file'] = request.FILES['file']
        form['email'] = request.POST.get('email')
        form['message'] = request.POST.get('message')
        fs = FileSystemStorage()
        filename = fs.save(form['file'].name, form['file'])
        uploaded_file_url = fs.url(filename)
        if not form['file']:
            errors.append('Enter file')
        if '@' not in form['email']:
            errors.append('Enter e-mail')
        if not form['message']:
            errors.append('Enter message')
        if not errors:
            return render(request, 'hello.html', {'errors': request.FILES, 'form':form})

        
    return render(request, 'contact.html', {'errors': errors, 'form':form})
