# V1========================

# from django.contrib import admin
# from .models import Category, Tool, Example, UseCase

# class ExampleInline(admin.TabularInline):
#     model = Example
#     extra = 1

# class UseCaseInline(admin.TabularInline):
#     model = UseCase
#     extra = 1

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description')
#     prepopulated_fields = {'slug': ('name',)}
#     search_fields = ('name',)

# @admin.register(Tool)
# class ToolAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category', 'website_url', 'created_at', 'updated_at')
#     list_filter = ('category', 'created_at')
#     search_fields = ('name', 'description')
#     prepopulated_fields = {'slug': ('name',)}
#     inlines = [ExampleInline, UseCaseInline]

# @admin.register(Example)
# class ExampleAdmin(admin.ModelAdmin):
#     list_display = ('title', 'tool')
#     list_filter = ('tool',)
#     search_fields = ('title', 'description', 'code')

# @admin.register(UseCase)
# class UseCaseAdmin(admin.ModelAdmin):
#     list_display = ('title', 'tool')
#     list_filter = ('tool',)
#     search_fields = ('title', 'description', 'advantages')


# V2========================


# from django.contrib import admin
# from .models import Category, Tool, Command, Example, UseCase

# class CommandInline(admin.TabularInline):
#     model = Command
#     extra = 1

# class ExampleInline(admin.TabularInline):
#     model = Example
#     extra = 1

# class UseCaseInline(admin.TabularInline):
#     model = UseCase
#     extra = 1

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description')
#     prepopulated_fields = {'slug': ('name',)}
#     search_fields = ('name',)

# @admin.register(Tool)
# class ToolAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category', 'website_url', 'created_at', 'updated_at')
#     list_filter = ('category', 'created_at')
#     search_fields = ('name', 'description')
#     prepopulated_fields = {'slug': ('name',)}
#     inlines = [CommandInline, ExampleInline, UseCaseInline]

# @admin.register(Command)
# class CommandAdmin(admin.ModelAdmin):
#     list_display = ('title', 'tool')
#     list_filter = ('tool',)
#     search_fields = ('title', 'description', 'syntax', 'example')

# @admin.register(Example)
# class ExampleAdmin(admin.ModelAdmin):
#     list_display = ('title', 'tool')
#     list_filter = ('tool',)
#     search_fields = ('title', 'description', 'code')

# @admin.register(UseCase)
# class UseCaseAdmin(admin.ModelAdmin):
#     list_display = ('title', 'tool')
#     list_filter = ('tool',)
#     search_fields = ('title', 'description', 'advantages')

# V3========================

from django.contrib import admin
from .models import Category, Tool, Command, CommandLanguageExample, Example, UseCase

class CommandLanguageExampleInline(admin.TabularInline):
    model = CommandLanguageExample
    extra = 1
    max_num = 3  # For Python, Java, JavaScript

class CommandInline(admin.TabularInline):
    model = Command
    extra = 1
    show_change_link = True

class ExampleInline(admin.TabularInline):
    model = Example
    extra = 1

class UseCaseInline(admin.TabularInline):
    model = UseCase
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'website_url', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [CommandInline, ExampleInline, UseCaseInline]

@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = ('title', 'tool')
    list_filter = ('tool',)
    search_fields = ('title', 'description')
    inlines = [CommandLanguageExampleInline]

@admin.register(CommandLanguageExample)
class CommandLanguageExampleAdmin(admin.ModelAdmin):
    list_display = ('command', 'language', 'syntax')
    list_filter = ('language', 'command__tool')
    search_fields = ('command__title', 'syntax', 'example')

@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    list_display = ('title', 'tool', 'language')
    list_filter = ('tool', 'language')
    search_fields = ('title', 'description', 'code')

@admin.register(UseCase)
class UseCaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'tool')
    list_filter = ('tool',)
    search_fields = ('title', 'description', 'advantages')
