from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Load initial data (brands, categories, features) and create admin user'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Create a superuser admin account',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('Loading initial data...'))
        
        # Load fixtures
        fixtures = [
            'apps/cars/fixtures/brands.json',
            'apps/cars/fixtures/categories.json',
            'apps/cars/fixtures/features.json',
        ]
        
        for fixture in fixtures:
            try:
                self.stdout.write(f'  Loading {fixture}...')
                call_command('loaddata', fixture, verbosity=0)
                self.stdout.write(self.style.SUCCESS(f'  ✓ {fixture} loaded'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Failed to load {fixture}: {e}'))
        
        # Create superuser if requested
        if options['create_superuser']:
            self.stdout.write('')
            self.stdout.write('Creating superuser...')
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@automaroc.ma',
                    password='admin123'  # Change in production!
                )
                self.stdout.write(self.style.SUCCESS('  ✓ Superuser created:'))
                self.stdout.write('    Username: admin')
                self.stdout.write('    Password: admin123')
                self.stdout.write(self.style.WARNING('    IMPORTANT: Change this password in production!'))
            else:
                self.stdout.write(self.style.WARNING('  Superuser already exists'))
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✓ Initial data loaded successfully!'))
