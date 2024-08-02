from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .form import LoginForm, FilesForm, CategoryForm
from .models import Files, Category
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Files
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.http import JsonResponse
from django.urls import reverse

def homepage_view(request):
    categories = Category.objects.prefetch_related('sub_files').all()
    if categories is None:
        return render(request, "home.html")
    filterd_data = []
    for index, category in enumerate(categories):
        count = category.sub_files.count()
        if count == 0:
            continue
        firt_image = category.sub_files.filter(file_type="I").first()
        if firt_image is None:
            url = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.hTQHlnEVJc6lMKqO49vcfAAAAA%26pid%3DApi&f=1&ipt=bf69986c2a6966829622e755d592cd66a6ad42887e6df19aebdb9874e27bb2ac&ipo=images"
        else:
            url = firt_image.compressed_file.url
        filterd_data.append({
            "id": index,
            "title": category.title,
            "count": count,
            "url": url
        })
    return render(request, 'home.html', {"categories": filterd_data})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user=user)
                return redirect('adminpage')
            else:
                form.add_error(None, "Invalid username or password!")
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def adminpage_view(request):
    context = Category.objects.prefetch_related('sub_files').all()
    return render(request, 'admin.html', {'context': context})



def add_files(request):
    if request.method == 'POST':
        print(request.POST)
        form = FilesForm(data=request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            files = request.FILES.getlist('file')
            for file in files:
                if form.cleaned_data['file_type'] == 'I':
                    print("working")
                    image = Image.open(file)
                    image_io = BytesIO()
                    image.save(image_io, format='JPEG', quality=10)
                    compressed_image = InMemoryUploadedFile(
                        image_io,
                        'ImageField',
                        f"{file.name.split('.')[0]}_compressed.jpg",
                        'image/jpeg',
                        sys.getsizeof(image_io),
                        None
                    )
                    Files.objects.create(category=category, file=file, compressed_file=compressed_image, file_type=form.cleaned_data['file_type'])
                else:
                    Files.objects.create(category=category, file=file, compressed_file="lol", file_type=form.cleaned_data['file_type'])
            return JsonResponse({'redirect_url': reverse('adminpage')})
        else:
            print("Bad request")
            return JsonResponse({'error': 'Bad request'}, status=400)
    else:
        form = FilesForm()
        params = request.GET.get('type', None)
        if params is None:
            return redirect("adminpage")
    return render(request, 'add-files.html', {'form': form, 'type': params})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        print(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            category = Category.objects.filter(title=title).first()
            if category is None:
                form.save()
                return redirect('adminpage')
            else:
                form.add_error('title', 'Category already exist')
        else:
            print("not valid form")
    else:
        form = CategoryForm()
    
    return render(request, 'add-category.html', {'form': form})



def list_files_view(request, category_name):
    context = Category.objects.prefetch_related('sub_files').filter(title=category_name).first().sub_files.all()
    return render(request, 'list-files.html', {'context': context})


def download_file(request, file_id):
    obj = get_object_or_404(Files, id=file_id)
    file_path = obj.file.path
    file_name = obj.file.name.split('/')[-1]

    try:
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/force-download')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    except FileNotFoundError:
        raise Http404("File does not exist")