from django.core.management.base import BaseCommand
from urllib.parse import urlparse
import pypandoc
import requests

from projects.models import Project


class Command(BaseCommand):
    help = "Command that fetches README.md for every project with github link"

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

    def _fetch_readme(self, github_link):
        if not github_link:
            return None
        raw_readme_link = self._get_raw_link(github_link=github_link)
        if not raw_readme_link:
            return None
        response = requests.get(raw_readme_link)
        if response.status_code == 200:
            html = self._markdown_to_html5(response.text)
            return html
        return None

    def _get_raw_link(self, github_link):
        parsed = urlparse(github_link)
        try:
            user, repo_name = parsed.path.split('/')[-2:]
        except IndexError:
            return None
        api_link = f'''https://api.github.com/repos/{user}/{repo_name}/contents/README.md'''
        response = requests.get(api_link)
        return response.json().get('download_url', None)

    def _markdown_to_html5(self, text):
        out_format = 'html5'
        out_extensions = ('gfm_auto_identifiers', 'pipe_tables', 'backtick_code_blocks', 'fenced_code_attributes')
        out_extensions = '+'.join(out_extensions)
        out = '+'.join((out_format, out_extensions))
        return pypandoc.convert_text(text, out, format='gfm', extra_args=['--no-highlight'])
