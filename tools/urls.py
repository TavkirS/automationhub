from django.urls import path
from . import views

app_name = 'tools'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:category_slug>/', views.home, name='home_by_category'),
    path('tool/<slug:tool_slug>/', views.tool_detail, name='tool_detail'),
    path('search/', views.search_tools, name='search_tools'),
]