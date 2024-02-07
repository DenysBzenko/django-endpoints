from django.http import Http404
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from chatbot.data.data import messages
from django.views.decorators.http import require_http_methods


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
@require_http_methods(["POST"])
def message_create(request):
    try:

        data = json.loads(request.body)

        new_id = str(max([int(msg["id"]) for msg in messages['Messages']]) + 1)

        new_message = {
            "id": new_id,
            "author": data.get("author"),
            "content": data.get("content"),
            "created_at": data.get("created_at", "Unknown date")
        }

        messages['Messages'].append(new_message)

        return JsonResponse(new_message, status=201)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    except Exception as e:
        return HttpResponseServerError(str(e))


@csrf_exempt
@require_http_methods(["DELETE"])
def message_delete(request, id):
    global messages
    message_index = next((index for (index, d) in enumerate(messages['Messages']) if d["id"] == str(id)), None)
    if message_index is not None:
        del messages['Messages'][message_index]
        return HttpResponse(status=204)  # No Content
    else:
        return HttpResponseNotFound("Message not found")


def unknown_path(request):
    return HttpResponseNotFound('<h1>Page not found</h1>')
