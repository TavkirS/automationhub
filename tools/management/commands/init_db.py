from django.core.management.base import BaseCommand
from django.db import connection, ProgrammingError, transaction
from tools.models import Category

class Command(BaseCommand):
    help = 'Initialize the database with required data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Initializing database...')
        
        try:
            with transaction.atomic():
                # Create initial categories
                categories = [
                    {
                        'name': 'Web Testing',
                        'slug': 'web-testing',
                        'description': 'Tools for testing web applications'
                    },
                    {
                        'name': 'API Testing',
                        'slug': 'api-testing',
                        'description': 'Tools for testing APIs and web services'
                    },
                    {
                        'name': 'Mobile Testing',
                        'slug': 'mobile-testing',
                        'description': 'Tools for testing mobile applications'
                    },
                    {
                        'name': 'Performance Testing',
                        'slug': 'performance-testing',
                        'description': 'Tools for performance and load testing'
                    }
                ]
                
                for category_data in categories:
                    Category.objects.get_or_create(
                        slug=category_data['slug'],
                        defaults=category_data
                    )
                
                self.stdout.write(self.style.SUCCESS('Database initialized successfully!'))
                
        except ProgrammingError as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            self.stdout.write('Attempting to create tables manually...')
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS tools_category (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(100) NOT NULL,
                            slug VARCHAR(100) NOT NULL UNIQUE,
                            description TEXT
                        );
                    """)
                self.stdout.write(self.style.SUCCESS('Tables created successfully!'))
                # Try creating categories again
                for category_data in categories:
                    Category.objects.get_or_create(
                        slug=category_data['slug'],
                        defaults=category_data
                    )
                self.stdout.write(self.style.SUCCESS('Data initialized successfully!'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create tables: {str(e)}'))
                raise
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Unexpected error: {str(e)}'))
            raise 