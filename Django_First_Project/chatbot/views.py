from django.http import Http404
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from chatbot.data.data import messages
import json

def home(request):
    return render(request, 'home.html')

def message_list(request):
    messages_list = messages['Messages']
    return render(request, 'messages_list.html', {'messages': messages_list})


def message_detail(request, id):

    message = next((item for item in messages['Messages'] if item["id"] == str(id)), None)
    if message is None:
        raise Http404("Message not found")
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
