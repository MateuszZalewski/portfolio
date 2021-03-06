from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .models import Project


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/list.html'
    context_object_name = 'projects'


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/detail.html'
    extra_context = {'title': 'Project Detail'}
    context_object_name = 'project'


def resume(request):
    return render(request, 'projects/resume.html', context={'title': 'Resume'})
