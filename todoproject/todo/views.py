from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Task
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Todo App!")


@csrf_exempt
@require_http_methods(['GET', 'POST'])

def task_list(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        
        tasks_data = [{
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'completed': task.completed,
            'priority': task.priority,
            'created_date': task.created_date,
            'due_date': task.due_date,
        } for task in tasks]
        return JsonResponse(tasks_data, safe=False)


    elif request.method == 'POST':
        try:
            data = json.loads(request.body)

            if not data.get('title'):
                return JsonResponse({'error': 'Title is required'}, status=400)
            
            task = Task.objects.create(
                title=data['title'],
                description=data.get('description', ''),
                priority=data.get('priority', 1),
                due_date=data.get('due_date'),
                completed=data.get('completed', False)
            )

            return JsonResponse({
                'message': 'Task created successfully',
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'priority': task.priority,
                'due_date': task.due_date.isoformat() if task.due_date else None,
                'completed': task.completed,
                'created_date': task.created_date,
                }, status=201)
        

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

@csrf_exempt
@require_http_methods(['GET', 'PUT', 'DELETE'])

def task_detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)
    
    if request.method == "GET":
        return JsonResponse({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'completed': task.completed,
            'created_date': task.created_date.isoformat(),
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'priority': task.get_priority_display()
        })

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            
            # Update task fields if provided in the request
            if 'title' in data:
                task.title = data['title']
            if 'description' in data:
                task.description = data['description']
            if 'completed' in data:
                task.completed = data['completed']
            if 'due_date' in data:
                task.due_date = data['due_date']
            if 'priority' in data:
                task.priority = data['priority']
                
            task.save()

            return JsonResponse({
                'message': 'Task updated successfully',
                'task':{
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'priority': task.priority,
                    'due_date': task.due_date.isoformat() if task.due_date else None,
                    'completed': task.completed,
                }
            })
        
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid JSON format'
            }, status=400)
        
    elif request.method == "DELETE":
        task.delete()
        return JsonResponse({'message': 'Task deleted successfully'}, status=204)

