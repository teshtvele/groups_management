from django.core.management.base import BaseCommand
from django.conf import settings
import os
from apps.persons.services import DatabaseInitService


class Command(BaseCommand):
    help = 'Load SQL script to initialize database with functions and triggers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='sqlScript.sql',
            help='Path to SQL script file (default: sqlScript.sql)'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        
        # Если путь относительный, ищем от корня проекта
        if not os.path.isabs(file_path):
            file_path = os.path.join(settings.BASE_DIR, file_path)
        
        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.ERROR(f'SQL script file not found: {file_path}')
            )
            return
        
        self.stdout.write(f'Loading SQL script from: {file_path}')
        
        try:
            DatabaseInitService.load_sql_script_from_file(file_path)
            self.stdout.write(
                self.style.SUCCESS('SQL script loaded successfully!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading SQL script: {e}')
            )
