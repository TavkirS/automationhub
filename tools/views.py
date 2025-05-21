from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, Tool

def home(request, category_slug=None):
    """
    View for the homepage displaying all tools or tools filtered by category
    """
    categories = Category.objects.all()
    tools = Tool.objects.all()
    
    # Filter by category if a category slug is provided
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        tools = tools.filter(category=selected_category)
    
    context = {
        'categories': categories,
        'tools': tools,
        'selected_category': selected_category
    }
    return render(request, 'home.html', context)

def tool_detail(request, tool_slug):
    """
    View for displaying detailed information about a specific tool
    """
    tool = get_object_or_404(Tool, slug=tool_slug)
    examples = tool.examples.all()
    use_cases = tool.use_cases.all()
    
    context = {
        'tool': tool,
        'examples': examples,
        'use_cases': use_cases
    }
    return render(request, 'tool_detail.html', context)

def search_tools(request):
    """
    View for searching tools
    """
    query = request.GET.get('q', '')
    tools = Tool.objects.filter(
        Q(name__icontains=query) | 
        Q(description__icontains=query) |
        Q(category__name__icontains=query)
    ).distinct()
    
    categories = Category.objects.all()
    
    context = {
        'tools': tools,
        'categories': categories,
        'query': query
    }
    return render(request, 'home.html', context)