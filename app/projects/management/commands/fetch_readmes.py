from django.core.management.base import BaseCommand
import pypandoc
import requests

from projects.models import Project


class Command(BaseCommand):
    help = "Command that fetches README.md for every project with github link"

    def _construct_raw_link(self, github_link):
        github_link = github_link.split(sep='.')[-1]
        raw_readme_link = f'''https://raw.githubusercontent.{github_link}/master/README.md'''
        return raw_readme_link

    def _fetch_readme(self, github_link):
        if not github_link:
            return None
        raw_readme_link = self._construct_raw_link(github_link=github_link)
        response = requests.get(raw_readme_link)
        if response.status_code == 200:
            out_format = 'html5'
            out_extensions = ('gfm_auto_identifiers', 'pipe_tables', 'backtick_code_blocks', 'fenced_code_attributes')
            out_extensions = '+'.join(out_extensions)
            out = '+'.join((out_format, out_extensions))
            return pypandoc.convert_text(response.text, out, format='gfm', extra_args=['--no-highlight'])
        return None

    def handle(self, *args, **options):
        projects = Project.objects.all()
        i = 0
        for project in projects:
            if project.github:
                readme = self._fetch_readme(github_link=project.github)
                if readme:
                    i += 1
                    project.readme = readme
                    project.save()
        self.stdout.write(f'Updated {i} readme fields.')
