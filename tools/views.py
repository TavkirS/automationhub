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
        Q(name__icontains=query)
    ).distinct()
    
    categories = Category.objects.all()
    
    context = {
        'tools': tools,
        'categories': categories,
        'query': query
    }
    return render(request, 'home.html', context)


# from django.shortcuts import render, get_object_or_404
# from django.db.models import Q
# from django.http import JsonResponse
# from .models import Category, Tool, Command

# def home(request, category_slug=None):
#     """
#     View for the homepage displaying all tools or tools filtered by category
#     """
#     categories = Category.objects.all()
#     tools = Tool.objects.all()
    
#     # Filter by category if a category slug is provided
#     selected_category = None
#     if category_slug:
#         selected_category = get_object_or_404(Category, slug=category_slug)
#         tools = tools.filter(category=selected_category)
    
#     context = {
#         'categories': categories,
#         'tools': tools,
#         'selected_category': selected_category
#     }
#     return render(request, 'home.html', context)

# def tool_detail(request, tool_slug):
#     """
#     View for displaying detailed information about a specific tool
#     """
#     tool = get_object_or_404(Tool, slug=tool_slug)
#     examples = tool.examples.all()
#     use_cases = tool.use_cases.all()
    
#     context = {
#         'tool': tool,
#         'examples': examples,
#         'use_cases': use_cases
#     }
#     return render(request, 'tool_detail.html', context)

# def search_tools(request):
#     """
#     View for searching tools
#     """
#     query = request.GET.get('q', '')
#     tools = Tool.objects.filter(
#         Q(name__icontains=query)
#     ).distinct()
    
#     categories = Category.objects.all()
    
#     context = {
#         'tools': tools,
#         'categories': categories,
#         'query': query
#     }
#     return render(request, 'home.html', context)

# def search_commands_api(request):
#     """
#     API endpoint for command auto-suggestions
#     """
#     query = request.GET.get('q', '').strip()
#     tool_slug = request.GET.get('tool_slug', '')
    
#     if not query or len(query) < 2:
#         return JsonResponse({'suggestions': []})
    
#     try:
#         tool = get_object_or_404(Tool, slug=tool_slug)
        
#         # Search commands by title and description
#         commands = Command.objects.filter(
#             tool=tool
#         ).filter(
#             Q(title__icontains=query) | 
#             Q(description__icontains=query)
#         ).distinct()[:10]  # Limit to 10 suggestions
        
#         suggestions = []
#         for command in commands:
#             suggestions.append({
#                 'id': command.id,
#                 'title': command.title,
#                 'description': command.description[:100] + '...' if len(command.description) > 100 else command.description
#             })
        
#         return JsonResponse({'suggestions': suggestions})
        
#     except Exception as e:
#         return JsonResponse({'suggestions': [], 'error': str(e)})

# def filter_commands(request):
#     """
#     Filter commands based on search query and language
#     """
#     if request.method == 'GET':
#         tool_slug = request.GET.get('tool_slug', '')
#         query = request.GET.get('q', '').strip()
#         language = request.GET.get('language', 'python')
        
#         try:
#             tool = get_object_or_404(Tool, slug=tool_slug)
#             commands = tool.commands.all()
            
#             # Filter by search query if provided
#             if query:
#                 commands = commands.filter(
#                     Q(title__icontains=query) | 
#                     Q(description__icontains=query)
#                 )
            
#             # Prepare filtered commands data
#             filtered_commands = []
#             for command in commands:
#                 # Get language examples for this command
#                 language_examples = command.language_examples.filter(language=language)
                
#                 command_data = {
#                     'id': command.id,
#                     'title': command.title,
#                     'description': command.description,
#                     'language_examples': []
#                 }
                
#                 for example in language_examples:
#                     command_data['language_examples'].append({
#                         'language': example.language,
#                         'language_display': example.get_language_display(),
#                         'syntax': example.syntax,
#                         'example': example.example
#                     })
                
#                 filtered_commands.append(command_data)
            
#             return JsonResponse({
#                 'commands': filtered_commands,
#                 'total_count': len(filtered_commands)
#             })
            
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)
    
#     return JsonResponse({'error': 'Invalid request method'}, status=405)