from django.core.management import BaseCommand
from django.conf import settings

    


class BasicCommand(BaseCommand):
    
    def show_actions(self, actions: list[str]):
        bar = str('-' * 100)

        print(bar, '\n')

        print('Actions')
        for action in actions:
            print(f' ->  {action}')

        print('\n', bar)

    def get_app_folder(self, options: dict) -> str:
        app_folder = options.get('app_folder')
        return app_folder if app_folder else settings.DEFAULT_APPS_FOLDER
