from django.core.management.base import BaseCommand
from django.conf import settings
import os
from apps.persons.services import DatabaseInitService


class Command(BaseCommand):
    help = 'Load and execute SQL script to initialize database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--script-path',
            type=str,
            default='sqlScript.sql',
            help='Path to SQL script file (default: sqlScript.sql)'
        )

    def handle(self, *args, **options):
        script_path = options['script_path']
        
        # Если путь относительный, делаем его относительно корня проекта
        if not os.path.isabs(script_path):
            script_path = os.path.join(settings.BASE_DIR, script_path)
        
        try:
            self.stdout.write(f'Loading SQL script from: {script_path}')
            DatabaseInitService.load_sql_script_from_file(script_path)
            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully loaded SQL script and executed all functions/triggers'
                )
            )
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'SQL script file not found: {script_path}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading SQL script: {e}')
            )
