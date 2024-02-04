from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from .models import Message
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateformat import DateFormat
from django.shortcuts import render
from .models import Message
import json

def home(request):
    return render(request, 'home.html')

def message_list(request):
    messages = Message.objects.all()
    return render(request, 'messages_list.html', {'messages': messages})

def message_detail(request, id):
    message = get_object_or_404(Message, id=id)
    return render(request, 'message_detail.html', {'message': message})
@csrf_exempt
def message_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON.")

        if 'author' not in data or 'content' not in data:
            return HttpResponseBadRequest("Missing 'author' or 'content'.")

        message = Message.objects.create(author=data['author'], content=data['content'])
        return JsonResponse({
            "id": message.id,
            "author": message.author,
            "content": message.content,
            "created_at": message.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    else:
        return HttpResponseBadRequest("Only POST requests are allowed.")\


@csrf_exempt
def message_delete(request, id):
    if request.method == 'DELETE':
        try:
            message = Message.objects.get(id=id)
        except Message.DoesNotExist:
            return JsonResponse({'error': 'Message not found.'}, status=404)
        message.delete()
        return JsonResponse({"success": "Message deleted"})
    else:
        return HttpResponseNotAllowed(['DELETE'])
