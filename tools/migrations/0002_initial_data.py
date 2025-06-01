from django.db import migrations

def create_initial_data(apps, schema_editor):
    Category = apps.get_model('tools', 'Category')
    Tool = apps.get_model('tools', 'Tool')
    
    # Create initial category if it doesn't exist
    category_slug = 'automation-tools'
    if not Category.objects.filter(slug=category_slug).exists():
        automation_category = Category.objects.create(
            name='Automation Tools',
            slug=category_slug,
            description='Tools for test automation'
        )
        
        # Create initial tool if it doesn't exist
        tool_slug = 'selenium'
        if not Tool.objects.filter(slug=tool_slug).exists():
            Tool.objects.create(
                name='Selenium',
                slug=tool_slug,
                description='Selenium is an open-source tool that automates web browsers.',
                category=automation_category,
                installation_steps='pip install selenium',
            )

def reverse_initial_data(apps, schema_editor):
    Category = apps.get_model('tools', 'Category')
    Category.objects.filter(slug='automation-tools').delete()

class Migration(migrations.Migration):
    dependencies = [
        ('tools', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_data, reverse_initial_data),
    ] 