from Fast.sheets.project import DjangoProject
from Fast.sheets.eraser import delete_comments_by_folder
from ..comand import BasicCommand
from pathlib import Path
from django.conf import settings
from directory_tree import display_tree

    


class Command(BasicCommand):
    
    help = "Starting project with fast"

    def add_arguments(self, parser):
        parser.add_argument('--del', '-d', action='store_true')
        parser.add_argument('--worker', '-w', action='store_true')

    def handle(self, *args, **options):
        self.create_project_folders(settings.BASE_DIR, options)
        
        if options['del']:
            delete_comments_by_folder(str(settings.BASE_DIR), settings.PROJECT_NAME)

        project = DjangoProject(str(settings.BASE_DIR), settings.PROJECT_NAME)
        project.insert_important_comments()
        project.adapt_settings()
        project.adapt_urls_py()

        display_tree(str(settings.BASE_DIR))
        self.show_actions([
            'creating folders for project',
            'deleting default django comments',
            'inserting important comments for Fast',
            'changing  settings',
            '   TEMPLATES["DIRS"], LANGUAGE_CODE, TIME_ZONE, STATICFILES_DIRS, STATIC_ROOT, MEDIA_ROOT',
            '   MEDIA_URL, ACCOUNT_SESSION_REMEMBER',
            'adapting archive urls.py',
        ])

    def create_project_folders(self, project_path: Path, options):
        folders = [
            'backend',
            'frontend',
            'frontend/static',
            'frontend/media',
            'frontend/static/styles',
            'frontend/static/styles/min',
            'frontend/static/styles/apps',
            'frontend/static/styles/_compacts',
            'frontend/static/scripts',
            'frontend/static/scripts/min',
            'frontend/static/scripts/apps',
            'frontend/static/scripts/_compacts',
            'frontend/templates',
            'frontend/templates/_compacts',
            'frontend/templates/min',
            'frontend/templates/bases',
            'frontend/templates/pages',
            'test',
            'test/backend',
            'test/frontend',
            'test/e2e',
            'test/dependencies',
        ]
        if options['worker']:
            folders += [
                'worker',
                'worker/api',
                'worker/cache_pages',
                'worker/static_pages_generator',
                'test/worker',
                'test/worker/api',
                'test/worker/cache_pages',
                'test/worker/static_pages_generator',
            ]

        for folder in folders:
            new_path = Path(project_path, folder)
            new_path.mkdir()