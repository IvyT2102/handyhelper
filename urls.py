from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard), #/dashboard
    path('logout', views.logout),
    path('new', views.new), #/new
    path('create', views.add_a_job), #/create
    path('<int:job_id>/edit', views.edit),#/1/edit
    path('<int:job_id>/update', views.update),
    path('<int:job_id>', views.job),#/1
    path('<int:job_id>/delete', views.delete),# 1/delete
    path('<int:job_id>/add', views.add_to),
    path('<int:job_id>/remove', views.remove_from),
    ]