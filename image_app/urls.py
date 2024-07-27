from django.urls import path
from . import views
urlpatterns = [
    path("", views.homepage_view, name='homepage'),
    path("images/", views.list_files_view, name='list_files'),
    path("login/", views.login_view, name='login'),
    path("admin/", views.adminpage_view, name='adminpage'),
    path("admin/add-files/", views.add_files, name='add_files'),
    path("admin/add-category/", views.add_category, name='add_category'),
]
