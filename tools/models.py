# V1========================

# from django.db import models

# class Category(models.Model):
#     """Model for tool categories"""
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(unique=True)
#     description = models.TextField(blank=True)
    
#     class Meta:
#         verbose_name_plural = "Categories"
#         ordering = ['name']
    
#     def __str__(self):
#         return self.name

# class Tool(models.Model):
#     """Model for automation testing tools"""
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(unique=True)
#     description = models.TextField()
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tools')
#     logo = models.ImageField(upload_to='logos/', blank=True, null=True)
#     website_url = models.URLField(blank=True)
#     github_url = models.URLField(blank=True)
#     installation_steps = models.TextField()
#     common_commands = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         ordering = ['name']
    
#     def __str__(self):
#         return self.name

# class Example(models.Model):
#     """Model for usage examples of tools"""
#     tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='examples')
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     code = models.TextField()
#     explanation = models.TextField(blank=True)
    
#     def __str__(self):
#         return f"{self.tool.name} - {self.title}"

# class UseCase(models.Model):
#     """Model for tool use cases"""
#     tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='use_cases')
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     advantages = models.TextField()
    
#     def __str__(self):
#         return f"{self.tool.name} - {self.title}"


# V2========================


# from django.db import models

# class Category(models.Model):
#     """Model for tool categories"""
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(unique=True)
#     description = models.TextField(blank=True)
    
#     class Meta:
#         verbose_name_plural = "Categories"
#         ordering = ['name']
    
#     def __str__(self):
#         return self.name

# class Tool(models.Model):
#     """Model for automation testing tools"""
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(unique=True)
#     description = models.TextField()
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tools')
#     logo = models.ImageField(upload_to='logos/', blank=True, null=True)
#     website_url = models.URLField(blank=True)
#     github_url = models.URLField(blank=True)
#     installation_steps = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         ordering = ['name']
    
#     def __str__(self):
#         return self.name

# class Command(models.Model):
#     """Model for common commands of tools"""
#     tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='commands')
#     title = models.CharField(max_length=200)
#     syntax = models.TextField()
#     description = models.TextField()
#     example = models.TextField(blank=True)
    
#     def __str__(self):
#         return f"{self.tool.name} - {self.title}"

# class Example(models.Model):
#     """Model for usage examples of tools"""
#     tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='examples')
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     code = models.TextField()
#     explanation = models.TextField(blank=True)
    
#     def __str__(self):
#         return f"{self.tool.name} - {self.title}"

# class UseCase(models.Model):
#     """Model for tool use cases"""
#     tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='use_cases')
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     advantages = models.TextField()
    
#     def __str__(self):
#         return f"{self.tool.name} - {self.title}"

# V3========================

from django.db import models

class Category(models.Model):
    """Model for tool categories"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Tool(models.Model):
    """Model for automation testing tools"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tools')
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    website_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    installation_steps = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

# Define language choices as constants
LANGUAGE_CHOICES = [
    ('python', 'Python'),
    ('java', 'Java'),
    ('javascript', 'JavaScript'),
]

class Command(models.Model):
    """Model for common commands of tools"""
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='commands')
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.tool.name} - {self.title}"

class CommandLanguageExample(models.Model):
    """Model for language-specific syntax and examples for commands"""
    command = models.ForeignKey(Command, on_delete=models.CASCADE, related_name='language_examples')
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    syntax = models.TextField()
    example = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('command', 'language')
        ordering = ['language']
        
    def __str__(self):
        return f"{self.command.title} - {self.get_language_display()}"

class Example(models.Model):
    """Model for usage examples of tools"""
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='examples')
    title = models.CharField(max_length=200)
    description = models.TextField()
    code = models.TextField()
    explanation = models.TextField(blank=True)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='python')
    
    def __str__(self):
        return f"{self.tool.name} - {self.title} ({self.get_language_display()})"

class UseCase(models.Model):
    """Model for tool use cases"""
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='use_cases')
    title = models.CharField(max_length=200)
    description = models.TextField()
    advantages = models.TextField()
    
    def __str__(self):
        return f"{self.tool.name} - {self.title}"
