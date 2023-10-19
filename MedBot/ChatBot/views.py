from django.shortcuts import render, redirect
from .models import Room, Message
from django.http import HttpResponse, JsonResponse
from .chatbotMain import get_output


# Create your views here.

def home(request):
    return render(request, 'chatbotpages/home.html', {'bot_name': 'ChatBot', 'cb_active': 'active', 'pb_active': ""})


def room(request, room):
    username = request.GET.get('username')
    newroom = request.GET.get('newroom')
    room_details = Room.objects.get(name=room)

    return render(request, 'chatbotpages/room.html', {
        'username': username,
        'room': room,
        'room_details': room_details,
        'base_app': '/ChatBot',
        'bot_name': 'ChatBot',
        'cb_active': 'active',
        'pb_active': ""
    })


def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/ChatBot/' + room + '/?username=' + username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()

        message = f"Hey {username}!\n" + "How May I help you?"

        default_message = Message.objects.create(value=message, user="MedBot", room=new_room.id)
        default_message.save()
        return redirect('/ChatBot/' + room + '/?username=' + username)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()

    bot_response, tag = get_output(message)

    bot_message = Message.objects.create(value=bot_response, user='MedBot', room=room_id)
    bot_message.save()

    return HttpResponse("Success!")

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})
