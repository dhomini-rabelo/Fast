from asyncore import read
from pathlib import Path
from ..comand import BasicCommand
from django.conf import settings
import requests
import io

    

class Command(BasicCommand):

    help = 'Compact html file losing extends django command'

    def add_arguments(self, parser):
        parser.add_argument('html_path', type=str)

    def handle(self, *args, **options):
        self.base_path = f'{settings.BASE_DIR}/frontend/templates'
        argument_path = options["html_path"].replace(".", "/")
        path = f'{self.base_path}/{argument_path}.html'

        initial_read = self.get_reading_list(path)
        self.family = self.get_family(initial_read, path)

        if len(self.family) == 1:
            reading = initial_read

        for index_, html_file_path in enumerate(self.family[:-1]):
            son_html_file_path = self.family[index_+1]
            if index_ == 0:
                new_reading_update = self.replace_django_blocks_for_code(html_file_path, son_html_file_path)
            else:
                new_reading_update = self.replace_django_blocks_for_code(reading, son_html_file_path)
            reading = new_reading_update[:]

        reading = self.get_includes_of_html(reading)
        
        compact_path = f'{self.base_path}/_compacts/{argument_path}.html'
        with io.open(compact_path, 'w') as file:
            file.writelines(reading)

        self.show_actions([
            f'create compact page in {compact_path}'
        ])


    def get_reading_list(self, path):
        with io.open(path, 'r') as file:
            reading_list = file.readlines()
        return reading_list

    def get_family(self, reading_list: list[str], initial_path):
        family = [initial_path]
        check = self.get_extends_html(reading_list)
        
        if check is None:
            return family
        
        while check is not None:
            family.append(check)
            new_reading = self.get_reading_list(check)
            check = self.get_extends_html(new_reading)

        return family        

    def get_extends_html(self, reading_list: list[str]) -> str | None:
        first_line = reading_list[0].strip()
        if first_line.startswith(r'{% extends'):
            html_base_archive_path = first_line.split("'")[1]
            extends_html_path = f'{self.base_path}/{html_base_archive_path}'
            return extends_html_path

    

            


