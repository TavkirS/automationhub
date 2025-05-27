from django.urls import path
from . import views

app_name = 'tools'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:category_slug>/', views.home, name='home_by_category'),
    path('tool/<slug:tool_slug>/', views.tool_detail, name='tool_detail'),
    path('search/', views.search_tools, name='search_tools'),
    # path('api/search-commands/', views.search_commands_api, name='search_commands_api'),
    # path('api/filter-commands/', views.filter_commands, name='filter_commands'),
]
