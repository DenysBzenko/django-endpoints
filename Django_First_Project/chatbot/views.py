from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from .models import Message
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateformat import DateFormat
import json

def home(request):
    return JsonResponse({"endpoints": ["GET /messages/ - show all message ", "GET /messages/<id>/-  show message only one user for id", "POST /messages/create/ - create message ", "DELETE /messages/delete/<id>/ - delete message for id"]})

def message_list(request):
    messages = Message.objects.all().values('id', 'author', 'content', 'created_at')
    messages_list = list(messages)
    for message in messages_list:
        message['created_at'] = DateFormat(message['created_at']).format('Y-m-d H:i:s')
    return JsonResponse(messages_list, safe=False)

def message_detail(request, id):
    message = get_object_or_404(Message, id=id)
    return JsonResponse({"id": message.id, "author": message.author, "content": message.content, "created_at": DateFormat(message.created_at).format('Y-m-d H:i:s')})

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
        message = get_object_or_404(Message, id=id)
        message.delete()
        return JsonResponse({"success": "Message deleted"})
    else:
        return HttpResponseNotAllowed(['DELETE'])
