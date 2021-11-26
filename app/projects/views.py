from django.views.generic import ListView

from .models import Project


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/list.html'
    context_object_name = 'projects'
