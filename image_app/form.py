from django import forms
from .models import Files, Category

class FilesForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = ['category', 'file_type']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']

class LoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=100)
    password = forms.CharField(label="password", max_length=100)