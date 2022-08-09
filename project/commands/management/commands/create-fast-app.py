from Fast.sheets.app import DjangoApp
from Fast.sheets.shortcuts import create_archives
from ..comand import BasicCommand
from django.conf import settings
from pathlib import Path
from directory_tree import display_tree


    


class Command(BasicCommand):

    help = 'Command for create fast app'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str)
        parser.add_argument('--use_folders', '-f', action='store_true')
        parser.add_argument('--api_app', '-a', action='store_true')
        parser.add_argument('--api_and_views_app', '-av', action='store_true')
        parser.add_argument('--app_folder', type=str, default=settings.DEFAULT_APPS_FOLDER)
    
    def handle(self, *args, **options):
        # create folder
        app_folder = self.get_app_folder(options)
        new_app_path = Path(settings.BASE_DIR, app_folder, options['app_name'])
        new_app_path.mkdir()
        self.create_app_folders(new_app_path, options)
        self.create_app_archives(new_app_path, options)
        app = DjangoApp(str(settings.BASE_DIR), f'{app_folder}/{options["app_name"]}', options['app_name'], settings.PROJECT_NAME)
        app.create_url_archive()
        app.start_files()
        app.import_for_model()
        app.config_app(app_folder)
        app.register_app(app_folder)
        display_tree(str(new_app_path))
        self.show_actions([
            'create app - https://docs.djangoproject.com/en/4.0/ref/django-admin/#startapp', 
            'register app in settings.INSTALLED_APPS - https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-INSTALLED_APPS',
        ])

    def create_app_folders(self, app_path: Path, options: dict):
        more_folders = self.get_more_folders(options)
        folders = [
            'app',
            'app/migrations',
            'app/tests',
            'actions',
            *more_folders,
        ]
        for folder in folders:
            new_path = Path(app_path, folder)
            new_path.mkdir()

    def create_app_archives(self, app_path: Path, options: dict):
        more_files = self.get_more_files(options)
        create_archives(app_path, [
            '__init__.py',
            'actions/__init__.py',
            'urls.py',
            'app/__init__.py',
            'app/admin.py',
            'app/tests/models_t.py',
            'app/tests/views_t.py',
            'app/migrations/__init__.py',
            'app/tests/__init__.py',
            *more_files,
        ])

    def get_more_folders(self, options: dict) -> list[str]:
        more_folders = []
        if options['use_folders']:
            new_folders = ['app/models']
            if options['api_and_views_app']:
                new_folders.extend(['api', 'views'])
            elif options['api_app']:
                new_folders.append('api')
            else:
                new_folders.append('views')
        return more_folders

    def get_more_files(self, options: dict) -> list[str]:
        more_files = []

        if options['use_folders']:

            new_folders = ['app/models/__init__.py']
            if options['api_and_views_app']:
                new_folders.extend(['api/__init__.py', 'views/__init__.py'])
            elif options['api_app']:
                new_folders.append('api/__init__.py')
            else:
                new_folders.append('views/__init__.py')

        else:

            new_folders = ['app/models.py']
            if options['api_and_views_app']:
                new_folders.extend(['api.py', 'views.py'])
            elif options['api_app']:
                new_folders.append('api.py')
            else:
                new_folders.append('views.py')

        return more_files

        